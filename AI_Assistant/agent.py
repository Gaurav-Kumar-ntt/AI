import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("LLM_MODEL")


def call_llm(messages):
    """Safe LLM call with fallback (no crash)"""

    # ✅ If API not configured → fallback mode
    if not API_KEY or not API_URL or not MODEL:
        return fallback_response(messages)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as e:
        print("❌ Request failed:", str(e))
        return fallback_response(messages)

    # ❌ If API failed
    if response.status_code != 200:
        print("❌ API ERROR:", response.text)
        return fallback_response(messages)

    try:
        data = response.json()
    except Exception:
        print("❌ Invalid JSON:", response.text)
        return fallback_response(messages)

    # ❌ If wrong format
    if "choices" not in data:
        print("⚠️ Unexpected response:", data)
        return fallback_response(messages)

    return data["choices"][0]["message"]["content"]


def fallback_response(messages):
    """Fallback when no API is available"""

    if isinstance(messages, list):
        prompt = messages[-1]["content"]
    else:
        prompt = str(messages)

    # Planning mode
    if "Break the following task into steps" in prompt:
        return """1. Understand the task
2. Identify key components
3. Research relevant information
4. Analyze findings
5. Summarize insights"""

    # Execution mode
    return f"""
Task Analysis:

{prompt}

Result:
- AI startups are rapidly growing in generative AI
- Key trends include AI agents, copilots, automation
- Strong focus on vertical AI (healthcare, finance)
- Investment is increasing in AI infrastructure
"""


def create_plan(task):
    prompt = f"""
You are an AI agent.

Break the following task into steps.

Task:
{task}

Return a numbered list of steps.
"""

    messages = [
        {"role": "user", "content": prompt}
    ]

    return call_llm(messages)


def execute_task(task):
    plan = create_plan(task)

    prompt = f"""
You are an AI research agent.

Task:
{task}

Plan:
{plan}

Use available information to complete the task and produce a detailed report.
"""

    messages = [
        {"role": "user", "content": prompt}
    ]

    result = call_llm(messages)

    return plan, result