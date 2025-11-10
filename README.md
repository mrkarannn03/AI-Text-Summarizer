website live
check here:
https://ai-text-summarizer-010101.streamlit.app/


## 🧠 Multi-Provider AI Text Summarizer (Streamlit App)

# ✨ Project Overview

This project is an interactive Abstractive Text Summarizer built with Streamlit that allows users to generate concise summaries of text using popular Large Language Models (LLMs).

The application is highly versatile, supporting content input from:
1. Direct Text Entry
2. Webpage URL Fetching (via web scraping)
3. File Uploads (.pdf, .docx, .txt)
The core summarization engine allows users to seamlessly switch between the Google Gemini API and the high-speed Groq API from the sidebar.


# ⚙️ Prerequisites and Setup
Before running the application, ensure you have Python 3.8+ installed and the necessary API keys from your chosen providers.

# 1. Installation
First, clone this repository and set up a Python virtual environment.

Bash# Navigate to your project folder
cd your-summarizer-project

#1. Create the virtual environment
python -m venv venv

#2. Activate the environment (Command varies by OS/Shell)
# For Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# For Linux/macOS:
source venv/bin/activate

# 2. Dependencies
With the environment active, install all required libraries using pip
.Bash(venv) pip install streamlit PyPDF2 python-docx requests beautifulsoup4 google-genai openai python-dotenv

# 3. API Keys (.env File)
The application uses the python-dotenv library to securely load API keys. Create a file named .env in the root directory of this project and add your keys:
# .env file content
Gemini_api_key="YOUR_GEMINI_API_KEY_HERE"
Groq_api_key="YOUR_GROQ_API_KEY_HERE"

Note: Never commit your .env file to GitHub! Use a .gitignore file to exclude it.


# 🚀 How to Run the App

Once setup is complete, run the application using the streamlit run command:
Bash(venv) streamlit run your_app_file_name.py

(The file name you used to save the provided code, e.g., app.py or summarizer_app.py)
The app will open automatically in your browser (typically at http://localhost:8501).

# Usage Instructions

1. Select Input: Use the tabs (Text, URL, or File) to load the content you want to summarize.

2. Configure Settings: Use the ⚙️ Settings sidebar to choose the LLM Provider and Model, and set the desired Summary Length (in words).

3. Summarize: Click the 🧠 Summarize button.


# 📚 Future Enhancements

Token Management: Implement text splitting/chunking to handle input documents larger than the LLM's context window.

Cost Tracking: Add functionality to estimate API usage costs per summary.

Abstractive vs. Extractive: Add a radio button to allow the user to select the summarization style.AI Summarizer App LangChain, Python, Streamlit, OpenAI and Groq (PDF, CSV and Text Files) - YouTube
