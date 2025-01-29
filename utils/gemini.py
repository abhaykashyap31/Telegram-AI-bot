import requests
from config import GEMINI_API_KEY

def generate_response(prompt):
    url = "https://gemini-api.example.com/generate"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("text", "Sorry, I couldn't understand that.")
