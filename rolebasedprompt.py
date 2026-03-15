
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


def role_prompt_uniProf():

    messages = [
        {
            "role": "system",
            "content": "You are a university professor teaching AI concepts to students."
        },
        {
            "role": "user",
            "content": "Explain what a AI."
        }
    ]

    return call_llm(messages)

def role_prompt_uniProf():

    messages = [
        {
            "role": "system",
            "content": "You are a university professor teaching AI concepts to students."
        },
        {
            "role": "user",
            "content": "Explain what a AI."
        }
    ]

    return call_llm(messages)

def role_prompt_startupadvisor():

    messages = [
        {
            "role": "system",
            "content": "You are a startup advisor with expertise in AI and machine learning to fonder and CEO of a startup." 
        },
        {
            "role": "user",
            "content": "Explain what AI and ML are and how they can be used in a startup."
        }
    ]

    return call_llm(messages)

def role_prompt_technicalwriter():

    messages = [
        {
            "role": "system",
            "content": "You are a technical writer specializing in AI and machine learning." 
        },
        {
            "role": "user",
            "content": "write a technical article about AI and ML, including their definitions, differences, and applications."
        }
    ]

    return call_llm(messages)


def main():
    print("\n=== ROLE PROMPT - UNIVERSITY PROFESSOR ===\n")
    print(role_prompt_uniProf())
    print("\n=== ROLE PROMPT - STARTUP ADVISOR ===\n")
    print(role_prompt_startupadvisor())
    print("\n=== ROLE PROMPT - TECHNICAL WRITER ===\n")
    print(role_prompt_technicalwriter())    

if __name__ == "__main__":
    main()