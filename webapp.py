import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_config = st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Hugging Face Model Setup (Multilingual: Hindi, Punjabi, English)
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

# --- AUTHENTICATOR SETUP ---
if True: 
    
    # Google AdSense (आपका कोड सुरक्षित है)
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
        uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

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
            with st.spinner("Analyzing and summarizing, please wait..."):
                # Transformers के साथ समरी जनरेशन
                summarizer = load_summarizer()
                summary_output = summarizer(text[:1500], max_length=150, min_length=40, do_sample=False)
                summary_text = summary_output[0]['summary_text']
                
                st.session_state.generated_text = summary_text
                st.session_state.show_flowers = True

    # Confetti Logic
    if st.session_state.show_flowers:
        components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
        st.session_state.show_flowers = False

    # Summary Display
    if 'generated_text' in st.session_state:
        st.write("### 📋 Professional Summary:")
        st.markdown(f"*{st.session_state.generated_text}*")
        
        st.download_button("📥 Download Summary File", st.session_state.generated_text, "BrieflyAI_Summary.txt", use_container_width=True)
