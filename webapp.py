import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# --- NLTK SETUP ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

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

# --- SIDEBAR (Original) ---
st.sidebar.title("About BrieflyAI")
st.sidebar.info("BrieflyAI ek smart summarization tool hai.")
st.sidebar.markdown("---")
st.sidebar.title("Legal")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("Privacy Policy: Aapka data store nahi hota.")

# --- GOOGLE ADSENSE (Original Code) ---
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# --- HEADER (Original) ---
st.markdown("<h1 style='text-align: center; color: #2b6cb0;'>🚀 BrieflyAI</h1>", unsafe_allow_html=True)

# --- MAIN UI (Original) ---
uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("Analyzing..."):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 4)
            summary_text = " ".join([str(s) for s in summary])
            
            st.session_state.summary = summary_text
            st.session_state.show_flowers = True

# Confetti Logic
if 'show_flowers' in st.session_state and st.session_state.show_flowers:
    components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
    st.session_state.show_flowers = False

# Display
if 'summary' in st.session_state:
    st.write("### 📋 Professional Summary:")
    st.write(st.session_state.summary)
    st.download_button("📥 Download Summary", st.session_state.summary, "BrieflyAI_Summary.txt", use_container_width=True)
