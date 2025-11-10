import streamlit as st
from transformers import pipeline

st.title("🧠 AI Text Summarizer")
st.write("Enter your tex;t or upload a file to generate a concise summary.")

# Summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Input
text = st.text_area("Paste text here:", height=200)

if st.button("Summarize"):
    if text:
        with st.spinner("Summarizing..."):
            summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
        st.subheader("📝 Summary:")
        st.write(summary[0]['summary_text'])
    else:
        st.warning("Please enter some text first!")
