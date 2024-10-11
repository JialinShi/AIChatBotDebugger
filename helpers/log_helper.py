from flask import current_app, jsonify

def analyze_log_error(log_error):
    prompt = f"""
    You are an expert software engineer. Analyze the following log error and provide detailed debugging guidance:

    Log Error:
    {log_error}

    Guidance:
    """
    client = current_app.config["client"]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
