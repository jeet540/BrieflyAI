import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
import google.generativeai as genai  # भाषा की समस्या के लिए

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Google AdSense (आपकी ओरिजिनल कोडिंग)
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# Mobile Responsiveness Fix
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
    st.sidebar.write("""
    Privacy Policy:
    BrieflyAI aapki upload ki gayi files ko store nahi karta. 
    Aapka data sirf process karne ke liye hai aur session 
    khatam hote hi delete ho jata hai.
    """)

# --- MAIN APP ---
if True: 
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
            with st.spinner("Analyzing and summarizing..."):
                # यहाँ Gemini API का इस्तेमाल करें जो हिंदी/पंजाबी भी समझता है
                # model = genai.GenerativeModel('gemini-pro')
                # response = model.generate_content(f"Summarize this in a short, professional way: {text}")
                # st.session_state.generated_summary = response.text
                st.write("सक्सेस! अब आप Gemini API कनेक्ट करके किसी भी भाषा की समरी पा सकते हैं।")

    # Confetti Logic
    if 'show_flowers' in st.session_state and st.session_state.show_flowers:
        components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
        st.session_state.show_flowers = False
