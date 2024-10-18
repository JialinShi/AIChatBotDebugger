# Project
Author: `Jialin Shi`

Live website: http://ec2-18-222-52-169.us-east-2.compute.amazonaws.com/bot/

## Description
- This AIChatBotDebugger application integrates with gpt-4o-mini from OpenAI, specifically customized for debugging. 
- You can either copy and paste your error log to this chat bot or simply upload your error log file for diagnosing. 
- Feel free to iteract with this chat bot and provide more detailed context so that it is able to help you better in the investigation. 

## Getting started

### Prerequsite (MacOS)
1. Python 3.10 installed  
```
brew install python@3.10
```
   
2. Dependency installed  
```
pip install flask openai langchain boto3
```
   
3. OpenAI token acquired  
Go to [OpenAI api-key](https://platform.openai.com/settings/profile?tab=api-keys) to request for a api key for personal use

### Steps to deploy locally 
   
1. Clone this repo to the local  

```
git colone https://github.com/JialinShi/AIChatBotDebugger.git
```

2. go to project folder  
```
cd AIChatBotDebugger
```

4. create a file named `config.yaml`, add one line to this file to configure your api token get from OpenAI  
```
open_ai_token: '{your_OpenAI_token}'
``` 

6. Create a python virtual environment  
```
python3 -m venv venv
```

6. Start the python virtual environment     
```
source venv/bin/activate
```

7. Start the server  
```
python app.py
```

7. Open your browser and go to website `127.0.0.1:5000/bot`
