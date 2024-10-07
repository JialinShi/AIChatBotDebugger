from openai import OpenAI

client = OpenAI(api_key="")
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "AI Chatbot is running."



# Set your OpenAI API key

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