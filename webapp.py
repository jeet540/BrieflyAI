import streamlit as st
import streamlit.components.v1 as components
import nltk
import chardet  # Universal encoding detection
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import fitz  # PyMuPDF: Isse dibbe (boxes) aur formatting tootne ki samasya theek hoti hai
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI - Smart Summarizer", page_icon="🚀", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.6);
    }
    div[data-testid="stFileUploader"] {
        background-color: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 20px;
    }
    .sidebar .sidebar-content { background-color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# --- FILE READING FUNCTION ---
def get_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".txt"):
        raw_bytes = uploaded_file.getvalue()
        detected = chardet.detect(raw_bytes)
        encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
        
        try:
            text = raw_bytes.decode(encoding, errors="ignore")
        except Exception:
            text = raw_bytes.decode("utf-8", errors="ignore")
            
    elif uploaded_file.name.endswith(".pdf"):
        try:
            # PyMuPDF ka use jo layout stream repair karta hai aur dibbe banna band karta hai
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_text = []
            for page in doc:
                # "text" flag characters ko clean streams mein extract karta hai
                page_text = page.get_text("text")
                if page_text:
                    full_text.append(page_text)
            text = "\n".join(full_text)
        except Exception as e:
            st.error(f"Error reading PDF stream: {e}")
            text = ""
        
    elif uploaded_file.name.endswith(".docx"):
        try:
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = ""
            
    return text

# --- SIDEBAR (About & Privacy) ---
st.sidebar.title("About BrieflyAI")
st.sidebar.info("BrieflyAI is a smart summarization tool designed to condense large documents into rich, readable formats effortlessly.")
st.sidebar.markdown("---")
st.sidebar.title("Legal")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("""
    *Privacy Policy:*
    BrieflyAI treats data security with utmost priority. We do not store, share, or log your uploaded files. 
    All data is processed strictly in-memory during active sessions and cleared instantly upon exit.
    """)

# --- MAIN APP CODE ---
if True: 
    
    # Google AdSense Fixed Scripts Link
    st.markdown("""
        <meta name="google-adsense-account" content="ca-pub-3995974960275140">
        <script async src="https://googlesyndication.com"
         crossorigin="anonymous"></script>
    """, unsafe_allow_html=True)

    # NLTK Setup
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)

    if 'show_flowers' not in st.session_state:
        st.session_state.show_flowers = False

    # Header UI
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #3b82f6; font-size: 46px; font-weight: 800; margin-bottom: 5px; letter-spacing: -0.5px;">🚀 BrieflyAI</h1>
            <p style="color: #94a3b8; font-size: 18px; font-weight: 400;">Fast, Professional and Beautiful Text Summarizer</p>
        </div>
    """, unsafe_allow_html=True)

    # Grid Layout Fix
    col1, col2 = st.columns(2)

    with col1:
        # Label purely English par set hai
        uploaded_file = st.file_uploader("Upload your document (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

    with col2:
        st.markdown("""
            <div style="background-color: #1e293b; padding: 22px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-top: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <h4 style="color: #f8fafc; margin-top: 0; font-weight: 700;">⚡ Tool Features</h4>
                <ul style="color: #94a3b8; padding-left: 20px; margin-bottom: 0; line-height: 1.6;">
                    <li>Multi-Format Engine (TXT, PDF, DOCX)</li>
                    <li>Advanced Character & Encoding Mapping</li>
                    <li>Zero-Data Retention Architecture</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    if uploaded_file is not None:
        text = get_text_from_file(uploaded_file)
        
        st.write("---")
        if st.button("✨ Generate Professional Summary", use_container_width=True):
            with st.spinner("Analyzing text streams and compiling summary, please wait..."):
                cleaned_text = text.strip() if text else ""
                
                # Dynamic validation logic taaki structural contents bypass na ho
                if cleaned_text and len(cleaned_text) > 3:
                    parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
                    summarizer = LsaSummarizer()
                    
                    total_sentences = len(list(parser.document.sentences))
                    
                    # Sentence handling logic optimized for smaller files
                    if total_sentences <= 2:
                        count = total_sentences
                    else:
                        count = 2 if total_sentences < 10 else max(3, int(total_sentences * 0.15))
                    
                    try:
                        summary_sentences = summarizer(parser.document, count)
                        st.session_state.generated_sentences = summary_sentences
                        st.session_state.show_flowers = True
                    except Exception:
                        st.error("Engine failed to rank sentences. The document might have restricted permissions.")
                else:
                    st.error("No extractable content found. Please ensure the file contains valid text characters.")

    # Confetti Logic CDN Path Corrected
    if st.session_state.show_flowers:
        components.html('<script src="https://jsdelivr.net"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
        st.session_state.show_flowers = False

    # Summary Display Panel (Brighter Pure White Fix)
    if 'generated_sentences' in st.session_state:
        st.markdown("""
            <div style="background-color: #1e293b; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #334155;">
                <h3 style="color: #3b82f6; margin-top: 0; font-weight: 700;">📋 Professional Summary:</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Color ko completely #ffffff kiya hai taaki text ekdum saaf aur bright chamke
        for sentence in st.session_state.generated_sentences:
            st.markdown(f"<p style='color: #ffffff; font-size: 16px; font-weight: 500; line-height: 1.6; margin-left: 10px;'>• {sentence}</p>", unsafe_allow_html=True)
        
        st.write("")
        summary_full_text = " ".join([str(s) for s in st.session_state.generated_sentences])
        st.download_button("📥 Download Summary File", summary_full_text, "BrieflyAI_Summary.txt", use_container_width=True)
