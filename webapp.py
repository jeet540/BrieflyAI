import streamlit as st
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
    st.error("API Key नहीं मिली। कृपया Secrets सेटिंग्स चेक करें।")

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

# --- UI LAYOUT ---
st.title("🚀 BrieflyAI")

uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary"):
        with st.spinner("AI समरी तैयार कर रहा है..."):
            try:
                response = model.generate_content(f"Summarize this text in the same language as the input: {text}")
                summary = response.text
                
                st.subheader("Summary:")
                st.write(summary)
                
                st.download_button("📥 Download Summary", summary, "summary.txt")
            except Exception as e:
                st.error(f"एरर: {e}")

# --- BOTTOM SECTION ---
st.markdown("---")
st.write("🟢 System Status: Active")
st.markdown("*Powered by Kainth*")
