import streamlit as st
import streamlit.components.v1 as components
import nltk
import chardet  # Universal encoding detection
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pdfplumber  # Clean multi-language extraction engine
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# --- FILE READING FUNCTION ---
def get_text_from_file(uploaded_file):
    text = ""
    file_name = uploaded_file.name.lower()
    
    if file_name.endswith(".txt"):
        raw_bytes = uploaded_file.getvalue()
        detected = chardet.detect(raw_bytes)
        encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
        try:
            text = raw_bytes.decode(encoding, errors="ignore")
        except Exception:
            text = raw_bytes.decode("utf-8", errors="ignore")
            
    elif file_name.endswith(".pdf"):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                full_text = []
                for page in pdf.pages:
                    # layout=False rakhne se language extraction normalise ho jati hai
                    page_text = page.extract_text(layout=False)
                    if page_text:
                        full_text.append(page_text)
                text = "\n".join(full_text)
        except Exception as e:
            text = ""
        
    elif file_name.endswith(".docx"):
        try:
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception:
            text = ""
            
    return text

# --- SIDEBAR (About & Privacy) ---
st.sidebar.title("About BrieflyAI")
st.sidebar.info("BrieflyAI ek smart summarization tool hai jo badi files ko chota aur readable banata hai.")
st.sidebar.markdown("---")
st.sidebar.title("Legal")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("""
    Privacy Policy:
    BrieflyAI aapki upload ki gayi files ko store nahi karta. 
    Aapka data sirf process karne ke liye hai aur session 
    khatam hote hi delete ho jata hai.
    """)

# --- MAIN APP CODE ---
if True: 
    
    # Google AdSense
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

    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="color: #2b6cb0; font-size: 42px; font-weight: bold; margin-bottom: 5px;">🚀 BrieflyAI</h1>
            <p style="color: #64748b; font-size: 18px;">Fast, Professional and Beautiful Text Summarizer</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Upload your document (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

    with col2:
        st.markdown("""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border-left: 5px solid #10b981; margin-top: 25px;">
                <h4 style="color: #f8fafc; margin-top: 0;">⚡ Tool Features</h4>
                <ul style="color: #cbd5e1; padding-left: 20px; margin-bottom: 0;">
                    <li>Multi-Format Support</li>
                    <li>Professional AI Summary</li>
                    <li>Privacy-Focused</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    if uploaded_file is not None:
        text = get_text_from_file(uploaded_file)
        
        st.write("---")
        if st.button("✨ Generate Professional Summary", use_container_width=True):
            with st.spinner("Analyzing and summarizing your file, please wait..."):
                cleaned_text = text.strip() if text else ""
                
                # Minimum threshold ko 3 kar diya hai taaki self-declaration files bypass na ho sakein
                if cleaned_text and len(cleaned_text) > 3:
                    parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
                    summarizer = LsaSummarizer()
                    
                    total_sentences = len(list(parser.document.sentences))
                    
                    # Agar single line ya chota content hai toh error dene ke bajaye vahi display karega
                    if total_sentences <= 2:
                        count = total_sentences
                    else:
                        count = 2 if total_sentences < 10 else max(3, int(total_sentences * 0.15))
                    
                    try:
                        summary_sentences = summarizer(parser.document, count)
                        st.session_state.generated_sentences = summary_sentences
                        st.session_state.show_flowers = True
                    except Exception:
                        st.error("Text processing matrix limit alert. File text stream contains non-standard encodings.")
                else:
                    st.error("No valid text found. Ensure the document contains selectable text and is not an unreadable scan.")

    # Confetti Logic
    if st.session_state.show_flowers:
        components.html('<script src="https://jsdelivr.net"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
        st.session_state.show_flowers = False

    # Summary Display
    if 'generated_sentences' in st.session_state:
        st.write("### 📋 Professional Summary:")
        for sentence in st.session_state.generated_sentences:
            st.markdown(f"- {sentence}")
        
        summary_full_text = " ".join([str(s) for s in st.session_state.generated_sentences])
        st.download_button("📥 Download Summary File", summary_full_text, "BrieflyAI_Summary.txt", use_container_width=True)
