import streamlit as st
import os
import google.generativeai as genai
import pypdf
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", layout="wide")

# API Configuration
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("API Key नहीं मिली, कृपया Secrets सेटिंग्स चेक करें।")

# --- FUNCTIONS ---
def get_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.getvalue().decode("utf-8", errors="replace")
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = pypdf.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# --- SIDEBAR ---
st.sidebar.title("BrieflyAI Control")
uploaded_file = st.file_uploader("फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

# --- MAIN PAGE ---
st.title("🚀 BrieflyAI")

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary"):
        with st.spinner("Gemini AI समरी बना रहा है..."):
            response = model.generate_content(f"Summarize this text in the same language as the input: {text}")
            summary = response.text
            
            st.subheader("Summary:")
            st.write(summary)
            
            # आपका डाउनलोड फीचर
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

# --- फूटर सेक्शन (Status & Powered by) ---
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.write("🟢 System Status: Ready")
    
with col2:
    st.markdown("*Powered by Kainth*")
