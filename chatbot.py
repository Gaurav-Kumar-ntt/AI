# app.py
# -----------------------------------------
# This script sends a prompt to an LLM API
# and prints the model's response.
# -----------------------------------------

# Import required libraries
import os                 # To read environment variables
import requests           # To make HTTP API calls
from dotenv import load_dotenv   # To load variables from .env file


# -----------------------------------------
# STEP 1: Load environment variables
# -----------------------------------------
# This reads the .env file and loads values
# like API key, API URL, and model name
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("LLM_MODEL")


    
# -----------------------------------------
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

    # System role prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI engineering assistant that explains concepts clearly."
        }
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

        response = call_llm(messages)

        print("\nAssistant:", response)

        messages.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    main()