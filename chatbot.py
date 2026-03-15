# app.py
import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("LLM_MODEL")


def call_llm(messages):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def main():

    print("\n=== AI Chatbot ===")
    print("Type 'exit' to end the conversation\n")

    messages = [
        {"role": "system", "content": "You are an AI tutor explaining concepts to beginners."},
        {"role": "system", "content": "You are an AI startup advisor helping founders build AI products."},
        {"role": "system", "content": "You are a technical writer explaining AI engineering concepts clearly."}
    ]

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\nChat ended.")
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        # Limit memory
        if len(messages) > 10:
            messages = messages[-10:]

        response = call_llm(messages)

        print("\nAssistant:", response)

        messages.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    main()