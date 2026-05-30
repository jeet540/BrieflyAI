import streamlit as st
import streamlit.components.v1 as components
import nltk
import pypdf
from docx import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

# Hugging Face Model Setup (बिल्कुल सही तरीका)
@st.cache_resource
def load_model_and_tokenizer():
    model_name = "google/mt5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

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
st.sidebar.info("BrieflyAI ek smart summarization tool hai jo badi files ko chota aur readable banata hai.")
st.sidebar.markdown("---")
st.sidebar.title("Legal")
if st.sidebar.button("Privacy Policy"):
    st.sidebar.write("BrieflyAI aapki upload ki gayi files ko store nahi karta.")

# --- GOOGLE ADSENSE & HEADER ---
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2b6cb0;'>🚀 BrieflyAI</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])
with col2:
    st.markdown("<div style='background-color: #1e293b; padding: 20px; border-radius: 8px; border-left: 5px solid #10b981; margin-top: 25px;'><h4>⚡ Tool Features</h4><ul><li>Multi-Format Support</li><li>AI Summary</li></ul></div>", unsafe_allow_html=True)

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("AI समरी तैयार कर रहा है..."):
            try:
                tokenizer, model = load_model_and_tokenizer()
                # टेक्स्ट को टोकनाइज़ करना
                inputs = tokenizer("summarize: " + text[:1000], return_tensors="pt", max_length=1024, truncation=True)
                # समरी जनरेट करना
                outputs = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
                summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                st.session_state.generated_summary = summary
                st.session_state.show_flowers = True
            except Exception as e:
                st.error(f"Error: {e}")

# Confetti & Display
if 'show_flowers' in st.session_state and st.session_state.show_flowers:
    components.html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script><script>confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }});</script>', height=0, width=0)
    st.session_state.show_flowers = False

if 'generated_summary' in st.session_state:
    st.write("### 📋 Professional Summary:")
    st.write(st.session_state.generated_summary)
    st.download_button("📥 Download", st.session_state.generated_summary, "Summary.txt", use_container_width=True)
