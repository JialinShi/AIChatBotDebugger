from openai import OpenAI
from flask import Flask, request, jsonify
import os
import yaml

app = Flask(__name__)

# load configurations for open_ai_token
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

client = OpenAI(api_key = config['open_ai_token'])

# basic landing page 
@app.route('/', methods=['GET'])
def index():
    return "AI Chatbot is running."

# chat resource that takes in the message from POST request
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": user_input}
    ])
    assistant_response = response.choices[0].message.content
    return jsonify({'response': assistant_response})

@app.route('/test', methods=['GET'])
def test():
    return "Test route is working!"



if __name__ == '__main__':
    app.run(debug=True)