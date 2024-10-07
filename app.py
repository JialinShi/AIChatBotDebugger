from openai import OpenAI
from flask import Flask, request, jsonify
from helpers.log_helper import *
import os
import yaml

app = Flask(__name__)

# load configurations for open_ai_token
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# config OpenAI client and set it into the app context 
client = OpenAI(api_key = config['open_ai_token'])
app.config["client"] = client

# basic landing page 
@app.route('/', methods=['GET'])
def index():
    return "AI Chatbot is running."

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
    """
    Analyze error log from the request 
    Error log should be set in  "log_error" field, i.e.
        {"log_error": {your error_log_here}}
    """
    log_error = request.json.get('log_error')
    analysis_result = analyze_log_error(log_error)
    return jsonify({'analysis': analysis_result})


@app.route('/upload', methods=['POST'])
def upload():
    """
    Accept log file uploading, perform error debugging through this endpoint
    """
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    content = file.read().decode('utf-8')
    return jsonify({'analysis': analysis_result})

if __name__ == '__main__':
    app.run(debug=True)