from openai import OpenAI
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
from helpers.log_helper import *
from werkzeug.utils import secure_filename
import os
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sample-secret-key'  
app.config['SESSION_TYPE'] = 'filesystem'  
Session(app)

# Load configurations for open_ai_token
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Config OpenAI client and set it into the app context 
client = OpenAI(api_key = config['open_ai_token'])
app.config["client"] = client


# Basic landing page 
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Receive message from /chat path, working as chat bot fucntionality 
    Message body should be set in "message" field, i.e. 
        {"message": {your_message_here}}
    """
    user_input = request.json.get('message')
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": user_input}
    ])
    assistant_response = response.choices[0].message.content
    return jsonify({'response': assistant_response})


@app.route('/analyze', methods=['POST'])
def analyze():
    log_error = request.form.get('log_error')
    if not log_error:
        return redirect(url_for('index'))
    analysis_result = analyze_log_error(log_error)
    return render_template('result.html', user_input=log_error, analysis_result=analysis_result)


# Add allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'log'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'analysis': 'No file part in the request.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'analysis': 'No selected file.'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        content = file.read().decode('utf-8')
        # Optionally, upload the log to S3
        # upload_log_to_s3(content, filename)

        # Update conversation history
        if 'history' not in session:
            session['history'] = []
        session['history'].append({'role': 'user', 'content': f"Uploaded log file: {filename}"})

        # Analyze the log content
        assistant_response = analyze_log_error(content)

        session['history'].append({'role': 'assistant', 'content': assistant_response})
        return jsonify({'analysis': assistant_response})
    else:
        return jsonify({'analysis': 'Invalid file type. Only .txt and .log files are allowed.'}), 400

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('history', None)
    return ('', 204)

@app.route('/test', methods=['GET'])
def test():
    return "Test success"

if __name__ == '__main__':
    app.run(debug=True)