import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pypdf
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

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

# --- AUTHENTICATOR SETUP ---
if True: # Yahan apna authenticator status handle karein
    
    # Google AdSense (Script + Meta)
    st.markdown("""
        <meta name="google-adsense-account" content="ca-pub-3995974960275140">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140"
         crossorigin="anonymous"></script>
    """, unsafe_allow_html=True)

    # NLTK Setup
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt')
        nltk.download('punkt_tab')

    if 'show_flowers' not in st.session_state:
        st.session_state.show_flowers = False

    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="color: #2b6cb0; font-size: 42px; font-weight: bold; margin-bottom: 5px;">🚀 BrieflyAI</h1>
            <p style="color: #64748b; font-size: 18px;">Fast, Professional and Beautiful Text Summarizer</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # File Uploader Update (PDF/DOCX/TXT support)
        uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

    with col2:
        st.markdown("""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border-left: 5px solid #10b981; margin-top: 25px;">
                <h4 style="color: #f8fafc; margin-top: 0;">⚡ Tool Features</h4>
                <ul style="color: #cbd5e1; padding-left: 20px; margin-bottom: 0;">
                    <li>Multi-Format Support (PDF/DOCX/TXT)</li>
                    <li>Professional AI Summary</li>
                    <li>Bullet Point Output</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    if uploaded_file is not None:
        text = get_text_from_file(uploaded_file)
        
        st.write("---")
        if st.button("✨ Generate Professional Summary", use_container_width=True):
            with st.spinner("Analyzing..."):
                parser = PlaintextParser.from_string(text, Tokenizer("english"))
                summarizer = LsaSummarizer()
                
                # Automatic Scaling Logic
                total_sentences = len(list(parser.document.sentences))
                count = 2 if total_sentences < 10 else max(3, int(total_sentences * 0.15))
                
                summary_sentences = summarizer(parser.document, count)
                st.session_state.generated_sentences = summary_sentences
                st.session_state.show_flowers = True

    # Confetti Logic
    if st.session_state.show_flowers:
        components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
        st.session_state.show_flowers = False

    # Summary Display (Bullet Points)
    if 'generated_sentences' in st.session_state:
        st.write("### 📋 Professional Summary:")
        for sentence in st.session_state.generated_sentences:
            st.markdown(f"- {sentence}")
        
        # Download Button
        summary_full_text = " ".join([str(s) for s in st.session_state.generated_sentences])
        st.download_button("📥 Download Summary File", summary_full_text, "BrieflyAI_Summary.txt", use_container_width=True)
