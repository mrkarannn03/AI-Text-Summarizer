import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
import streamlit as st
import PyPDF2
import docx
import re
import requests
from bs4 import BeautifulSoup

def text_metrics (text):
    chars = len(text)
    words = len([w for w in re.split(r"\s+",text) if w.strip()])
    sentences = len([s for s in re.split(r"[.!?]+", text) if s.strip()])
    reading_minutes = round(words/200.0, 2) if words > 0 else 0
    return {"chars":chars, "words":words, "sentences":sentences, "reading_min":reading_minutes}

def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join([p.get_text() for p in paragraphs])
    except Exception as e:
        st.error(f'Error fetching URL: {e}')
        return ""

load_dotenv()

# Gemini API
GEMINI_KEY = os.getenv("Gemini_api_key")
genai.configure(api_key=GEMINI_KEY)

# groq API
client = OpenAI(
    api_key=os.getenv("Groq_api_key"),
    base_url="https://api.groq.com/openai/v1"
)

# SIDEBAR
with st.sidebar:
    st.title("⚙️ Settings")

    # Model Provider Selector
    provider = st.radio(
        "Select Model Provider",
        ["Gemini", "Groq"],
        horizontal=True
    )

    # Model Selection based on Provider
    if provider == "Gemini":
        model_choice = st.selectbox(
            "Select Gemini Model",
            ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-2.0-flash-lite"],
            index=0
        )
    else:
        model_choice = st.selectbox(
            "Select Groq Model",
            ["llama-3.1-8b-instant", "groq/compound", "groq/compound-mini"],
            index=0
        )

    # Summary Length Slider
    summary_length = st.slider(
        "Summary Length",
        min_value=50,
        max_value=500,
        value=150,
        step=50,
        help="Adjust the length of the generated summary."
    )

    st.markdown("---")
    st.info("💡 Tip: You can tweak model and length before summarizing.")


st.title("🧠 AI Text Summarizer")
st.write("")

tab1, tab2, tab3 = st.tabs(["📝 Text", "🌐 URL", "📂 File"])

# Initialize once
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# --------------- TAB 1 ---------------
with tab1:
    st.subheader("✏️ Enter Text")
    text = st.text_area("Enter or Paste text here:", value=st.session_state["input_text"], height=200, key="text_input")
    
    # Update only when user types something
    if text and text != st.session_state["input_text"]:
        st.session_state["input_text"] = text

# --------------- TAB 2 ---------------
with tab2:
    st.subheader("🌐 Enter URL")
    url = st.text_input("Enter a Webpage URL:", key='url_input')

    if st.button("Fetch Content", key='fetch_btn'):
        if url:
            url_text = get_text_from_url(url)
            if url_text.strip():
                st.session_state["input_text"] = url_text  
                st.success("✅ Content fetched successfully!")
            else:
                st.warning("No content found at the provided URL.")
        else:
            st.warning("Please enter a valid URL.")

    if st.session_state["input_text"]:
        st.text_area("Extracted Text", st.session_state["input_text"], height=200, key="url_text_area")

# --------------- TAB 3 ---------------
with tab3:
    st.subheader("📄 Upload a File")
    uploaded_file = st.file_uploader("Choose a file", type=["txt","pdf","docx"])
    text = ""

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "txt":
            text = uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_type == "docx":
            docx_reader = docx.Document(uploaded_file)
            for para in docx_reader.paragraphs:
                text += para.text + "\n"

        if text.strip():
            st.session_state["input_text"] = text
            st.success("✅ File uploaded and text extracted successfully!")
            st.text_area("Extracted Text", text, height=200, key="file_text_area")
        else:
            st.warning("No readable text found in the file.")

# --------------- METRICS ---------------
if st.session_state["input_text"]:
    metrics = text_metrics(st.session_state["input_text"])
    mcol1 , mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Characters", metrics["chars"])
    mcol2.metric("Words", metrics["words"])
    mcol3.metric("Sentences", metrics["sentences"])
    mcol4.metric("Reading time (min)", metrics["reading_min"])

st.write("")
# --------------- SUMMARIZE BUTTON ---------------
col1, col2, col3 = st.columns([1,1,2])
with col1:
    summarize_btn = st.button("🧠 Summarize")
with col2:
    clear_btn = st.button("🧹 Clear")


def summarize_text (text, provider, model_choice, length):
    with st.spinner("Summarizing..."):
        prompt = f"Summarize the following text in about {length} words:\n\n{text}"

        if provider == "Gemini":
            model = genai.GenerativeModel(model_choice)
            response = model.generate_content(prompt)
            return response.text.strip()

        elif provider == "Groq":
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": "You are a helpful and concise AI summarizer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()

if summarize_btn:
    text_to_summarize = st.session_state["input_text"]
    if text_to_summarize.strip():
        response = summarize_text(text_to_summarize, provider, model_choice, summary_length)
        st.subheader("📝 Summary:")
        st.write(response)
    else:
        st.warning("Please enter some text first!")

if clear_btn:
    # Safely clear everything
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
