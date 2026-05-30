import streamlit as st
import google.generativeai as genai
import pypdf
from docx import Document

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrieflyAI", layout="wide")

# Google AdSense Code
st.markdown("""
    <meta name="google-adsense-account" content="ca-pub-3995974960275140">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# API Configuration
# यहाँ मॉडल का नाम 'gemini-1.5-pro' या 'gemini-pro' ही रहने दें, यह सबसे स्टेबल है।
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"API Configuration Error: {e}")

# --- FUNCTIONS ---
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

# --- UI LAYOUT ---
st.title("🚀 BrieflyAI")

uploaded_file = st.file_uploader("अपनी फाइल अपलोड करें (TXT, PDF, DOCX):", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    text = get_text_from_file(uploaded_file)
    
    if st.button("✨ Generate Professional Summary"):
        with st.spinner("AI समरी तैयार कर रहा है..."):
            try:
                response = model.generate_content(f"Summarize this text in the same language as the input: {text}")
                summary = response.text
                
                st.subheader("Summary:")
                st.write(summary)
                
                st.download_button("📥 Download Summary", summary, "summary.txt")
            except Exception as e:
                st.error(f"समरी जनरेट करने में समस्या: {e}")

# --- BOTTOM SECTION ---
st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    st.write("🟢 System Status: Active")
with col2:
    st.markdown("*Powered by Kainth*")
