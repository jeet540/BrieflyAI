
import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Hugging Face Model (Hindi, Punjabi, English के लिए बेस्ट)
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="google/mt5-small")

# --- FILE READING FUNCTION ---
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

# --- SIDEBAR & AUTHENTICATOR ---
st.sidebar.title("About BrieflyAI")
st.sidebar.info("BrieflyAI ek smart summarization tool hai.")
st.sidebar.markdown("---")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("BrieflyAI aapka data store nahi karta.")

# --- GOOGLE ADSENSE & HEADER ---
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2b6cb0;'>🚀 BrieflyAI</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें:", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("AI समरी तैयार कर रहा है..."):
            try:
                summarizer = load_summarizer()
                # 1500 कैरेक्टर तक की समरी
                summary_output = summarizer(text[:1500], max_length=150, min_length=40, do_sample=False)
                summary_text = summary_output[0]['summary_text']
                
                st.session_state.generated_summary = summary_text
                st.session_state.show_flowers = True
            except Exception as e:
                st.error(f"Error: {e}")

# Confetti Logic
if 'show_flowers' in st.session_state and st.session_state.show_flowers:
    components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
    st.session_state.show_flowers = False

# Display Summary
if 'generated_summary' in st.session_state:
    st.write("### 📋 Professional Summary:")
    st.write(st.session_state.generated_summary)
    st.download_button("📥 Download", st.session_state.generated_summary, "Summary.txt", use_container_width=True)
