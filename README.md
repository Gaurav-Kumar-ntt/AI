Project Setup

Create a new project folder.

mkdir first-llm-call
cd first-llm-call


Your project will contain the following files:

first-llm-call/
app.py
.env
.gitignore


Step 1 — Create a Virtual Environment
Create a Python virtual environment.
Mac / Linux
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

Step 2 — Install Required Libraries
Install the libraries required to call an API and manage environment variables.
pip install requests python-dotenv


Step 3 — Create the Project Files
Create the required files.
touch app.py
touch .env
touch .gitignore


Step 4 — Add .gitignore
Open .gitignore and add the following:
venv/
.env
__pycache__/


Step 5 — Add Your API Key
Open the .env file and add your LLM credentials.
Example:
LLM_API_KEY=your_api_key_here
LLM_API_URL=https://your-api-endpoint.com/v1/chat/completions
LLM_MODEL=your-model-name






