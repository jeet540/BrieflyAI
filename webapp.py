import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Hugging Face Model (Fast & Stable)
@st.cache_resource
def load_summarizer():
    # यह मॉडल टेक्स्ट प्रोसेसिंग के लिए बेस्ट है
    return pipeline("summarization", model="facebook/bart-large-cnn")

# --- FILE READING ---
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

# --- SIDEBAR & AUTH ---
st.sidebar.title("About BrieflyAI")
st.sidebar.info("BrieflyAI - Fast AI Summarizer.")

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #2b6cb0;'>🚀 BrieflyAI</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें:", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("AI समरी बना रहा है, कृपया प्रतीक्षा करें..."):
            try:
                summarizer = load_summarizer()
                # टेक्स्ट को ट्रिम करना जरूरी है ताकि क्रैश न हो
                summary_output = summarizer(text[:1024], max_length=150, min_length=40, do_sample=False)
                summary = summary_output[0]['summary_text']
                st.session_state.summary = summary
                st.session_state.show_flowers = True
            except Exception as e:
                st.error("समरी जनरेट करने में एरर आया, कृपया फाइल का टेक्स्ट देखें।")

# Confetti & Display
if 'show_flowers' in st.session_state and st.session_state.show_flowers:
    components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
    st.session_state.show_flowers = False

if 'summary' in st.session_state:
    st.write("### 📋 Professional Summary:")
    st.write(st.session_state.summary)
    st.download_button("📥 Download", st.session_state.summary, "Summary.txt", use_container_width=True)
