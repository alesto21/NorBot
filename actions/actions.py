import requests
from rasa_sdk import Action

class ActionDeepSeekResponse(Action):
    def name(self):
        return "action_deepseek_response"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text")

        deepseek_api_url = "https://api.deepseek.com/chat/completions"
        deepseek_api_key = "sk-a36274c7c09044f2a2a0ab019aa76917"  # Replace with your actual API key

        headers = {
            "Authorization": f"Bearer {deepseek_api_key}",
            "Content-Type": "application/json"
        }

        # 🔹 SYSTEM PROMPT: Ensures short and structured responses for ALL types of questions
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are an AI assistant. Answer any type of question concisely and in a structured way. Keep responses under 5 key points where possible."},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(deepseek_api_url, json=data, headers=headers)

        if response.status_code == 200:
            ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "I couldn't get a response.")
        else:
            ai_response = f"Error: {response.status_code}. I couldn't reach DeepSeek API."

        dispatcher.utter_message(text=ai_response)

        return []
