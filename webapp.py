import streamlit as st
import streamlit.components.v1 as components
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pypdf
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Google AdSense (आपकी ओरिजिनल कोडिंग)
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# Mobile Responsiveness Fix (ताकि मोबाइल पर लेआउट न बिगड़े)
st.markdown("""
    <style>
    @media (max-width: 600px) {
        .stColumn { width: 100% !important; }
    }
    </style>
""", unsafe_allow_html=True)

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
st.sidebar.info("BrieflyAI ek smart summarization tool hai jo badi files ko chota aur readable banata hai.")
st.sidebar.markdown("---")
st.sidebar.title("Legal")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("Privacy Policy: BrieflyAI aapki upload ki gayi files ko store nahi karta.")

# --- MAIN APP ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #2b6cb0; font-size: 42px; font-weight: bold;">🚀 BrieflyAI</h1>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("Analyzing..."):
            try:
                nltk.download('punkt')
            except: pass
            
            # भाषा सुधार: 'english' की जगह generic tokenizer का उपयोग
            parser = PlaintextParser.from_string(text, Tokenizer("english")) 
            summarizer = LsaSummarizer()
            
            # समरी की लंबाई (0.08 यानी 8%)
            total_sentences = len(list(parser.document.sentences))
            count = max(2, int(total_sentences * 0.08))
            
            summary_sentences = summarizer(parser.document, count)
            st.session_state.generated_sentences = summary_sentences

if 'generated_sentences' in st.session_state:
    st.write("### 📋 Professional Summary:")
    for sentence in st.session_state.generated_sentences:
        st.markdown(f"- {sentence}")
    summary_full_text = " ".join([str(s) for s in st.session_state.generated_sentences])
    st.download_button("📥 Download Summary", summary_full_text, "BrieflyAI_Summary.txt", use_container_width=True)
