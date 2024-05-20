import requests
import json
import os

def chat(text):
    payload = json.dumps({
      "role": os.getenv("BOT_NAME"),
      "type": "llm",
      "// model": "mistralai/Mistral-7B-Instruct-v0.2",
      "// format": "html",
      "message": text
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", os.getenv("API_ENDPOINT_LLMTWINS") + "/prompt", headers=headers, data=payload)

    # Convert response to JSON
    try:
        response = response.json()
        return response["message"]
    except Exception as e:
        print(str(e))
        return os.getenv("BOT_NAME") + " 壞掉了，趕快請人類來修理: " + str(e)

