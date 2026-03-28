import os
import requests
from dotenv import load_dotenv

from loader import load_pdf, chunk_text
from rag import create_embeddings, build_vector_index, retrieve_chunks


# ✅ Load environment variables (FIXED)
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL")
MODEL = os.getenv("LLM_MODEL")


def call_llm(prompt):
    """Call LLM API safely with error handling"""

    if not API_KEY or not API_URL or not MODEL:
        print("❌ Missing environment variables!")
        print("API_KEY:", API_KEY)
        print("API_URL:", API_URL)
        print("MODEL:", MODEL)
        return "Missing configuration"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as e:
        print("❌ Request failed:", str(e))
        return "Request error"

    # ✅ Check HTTP status
    if response.status_code != 200:
        print("\n❌ API ERROR:", response.status_code)
        print(response.text)
        return "API Error"

    # ✅ Parse JSON safely
    try:
        data = response.json()
    except Exception:
        print("❌ Failed to parse JSON:", response.text)
        return "Invalid JSON response"

    # ✅ Extract response safely
    try:
        return data["choices"][0]["message"]["content"]
    except KeyError:
        print("\n⚠️ Unexpected API response format:")
        print(data)
        return "Parsing error"


def main():
    print("🚀 App started...\n")

    # Debug: check current working directory
    print("📁 Current directory:", os.getcwd())

    print("\n📄 Loading document...\n")

    try:
        # ✅ FIXED PATH
        text = load_pdf("documents/github.pdf")
    except Exception as e:
        print("❌ Error loading PDF:", str(e))
        return

    if not text or len(text.strip()) == 0:
        print("❌ PDF is empty or not readable.")
        return

    print(f"✅ Document loaded. Length: {len(text)} characters")

    # Chunking
    chunks = chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks")

    # Embeddings
    try:
        embeddings = create_embeddings(chunks)
    except Exception as e:
        print("❌ Error creating embeddings:", str(e))
        return

    # Vector index
    try:
        index = build_vector_index(embeddings)
    except Exception as e:
        print("❌ Error building index:", str(e))
        return

    print("\n💬 You can now ask questions (type 'exit' to quit)\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() == "exit":
            print("👋 Exiting...")
            break

        if not question:
            continue

        try:
            context_chunks = retrieve_chunks(question, chunks, index)
        except Exception as e:
            print("❌ Retrieval error:", str(e))
            continue

        context = ""

        for i, chunk in enumerate(context_chunks):
            context += f"\nDocument Section {i+1}:\n{chunk}\n"

        prompt = f"""
You are an AI assistant that answers questions using the provided document context.

Only use the information from the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""


        answer = call_llm(prompt)

        print("\n🤖 Answer:\n", answer)
        print("\n" + "-" * 50 + "\n")


# ✅ Ensure main runs
if __name__ == "__main__":
    main()