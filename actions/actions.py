import os
import requests
from dotenv import load_dotenv
from rasa_sdk import Action

load_dotenv()  # 🔹 Load the environment variables

class ActionOpenAIResponse(Action):
    def name(self):
        return "action_openai_response"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text")
        openai_api_key = os.getenv("OPENAI_API_KEY")  # 🔹 Securely fetch API key

        if not openai_api_key:
            dispatcher.utter_message(text="Error: OpenAI API key is missing.")
            return []

        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an AI assistant. Keep responses short and structured."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)

        if response.status_code == 200:
            ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "I couldn't get a response.")
        else:
            ai_response = f"Error: {response.status_code}. I couldn't reach OpenAI API."

        dispatcher.utter_message(text=ai_response)
        return []
