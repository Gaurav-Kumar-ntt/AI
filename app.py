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
# STEP 2: Get prompt from the user
# -----------------------------------------
def get_user_prompt():
    """
    Ask the user to enter a prompt
    that will be sent to the LLM.
    """
    prompt = input("Enter your prompt: ")
    return prompt


# -----------------------------------------
# STEP 3: Send request to the LLM API
# -----------------------------------------
def call_llm(prompt):
    """
    Sends the prompt to the LLM API
    and returns the model's response.
    """

    # HTTP headers required for API call
    headers = {
        "Authorization": f"Bearer {API_KEY}",   # Authentication
        "Content-Type": "application/json"      # Format of request body
    }

    # JSON payload sent to the API
    payload = {
        "model": MODEL,              # Model name from .env
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7           # Controls creativity
    }

    try:
        # Send POST request to the API
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        # If the API returns an error code
        if response.status_code != 200:
            print("API ERROR:")
            print(response.text)
            response.raise_for_status()

        # Convert response JSON into Python dictionary
        data = response.json()

        # Extract the model's reply
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # Handle network/API errors
        print("Request failed:", e)
        return "Error calling the LLM API."


# -----------------------------------------
# STEP 4: Main function
# -----------------------------------------
def main():
    """
    Entry point of the program.
    """

    print("\n=== Your First LLM Call ===\n")

    # Get prompt from user
    prompt = get_user_prompt()

    # Call the LLM API
    response = call_llm(prompt)

    # Print the model's response
    print("\n=== Model Response ===\n")
    print(response)


# -----------------------------------------
# STEP 5: Run the program
# -----------------------------------------
if __name__ == "__main__":
    main()

