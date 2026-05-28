import streamlit as st
import streamlit.components.v1 as components

# 1. सबसे पहली लाइन (Page Configuration)
st.set_page_config(page_title="BrieflyAI - Free Text Summarizer", page_icon="🚀", layout="wide")

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Google AdSense (आपकी ओरिजिनल आईडी यहाँ बिल्कुल सुरक्षित और एक्टिव है)
st.markdown('<meta name="google-adsense-account" content="ca-pub-3995974960275140">', unsafe_allow_html=True)

# NLTK setup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# स्टेट मैनेजमेंट (फूलों की बौछार को ट्रैक करने के लिए)
if 'show_flowers' not in st.session_state:
    st.session_state.show_flowers = False

# --- मुख्य सॉफ़्टवेयर स्क्रीन का सुंदर डिज़ाइन ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #2b6cb0; font-size: 42px; font-weight: bold; margin-bottom: 5px;">🚀 BrieflyAI</h1>
        <p style="color: #64748b; font-size: 18px;">Fast, Professional and Beautiful Text Summarizer</p>
    </div>
""", unsafe_allow_html=True)

# नियम का साफ़ और सुंदर संदेश बॉक्स
st.info("💡 नियम: यहाँ आप जितनी मर्जी चाहे उतनी बड़ी फ़ाइल का समरी बिल्कुल फ्री में बना सकते हैं!")

st.write("---")

# सुंदर दो कॉलम लेआउट (फ़ाइल अपलोड करने के लिए)
col1, col2 = st.columns([2, 1])

with col1:
    # "Drag and drop file here" वाला मुख्य फ़ाइल अपलोडर डिब्बा
    uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें (Upload your text file here):", type=["txt"])

with col2:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; border-left: 5px solid #10b981; margin-top: 25px;">
            <h4 style="color: #f8fafc; margin-top: 0;">⚡ Tool Features</h4>
            <ul style="color: #cbd5e1; padding-left: 20px; margin-bottom: 0;">
                <li>Unlimited File Size</li>
                <li>100% Free Lifetime</li>
                <li>Instant Download</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# बैकएंड प्रोसेसिंग और समरी जनरेशन
if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    raw_data = uploaded_file.getvalue()
    text = raw_data.decode("utf-8", errors="replace")
    
    st.write("---")
    st.success(f"✅ फाइल सफलतापूर्वक अपलोड हुई! साइज: {file_size_kb:.2f} KB")
    
    # समरी जनरेट करने का मुख्य बटन
    if st.button("✨ Generate Professional Summary", use_container_width=True):
        with st.spinner("Processing your file... Please wait..."):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            
            # सिर्फ 1 वाक्य की सटीक प्रोफेशनल समरी
            summary_sentences = summarizer(parser.document, 1) 
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            st.session_state.generated_summary = summary
            
            # फूलों की बारिश एक्टिवेट करें!
            st.session_state.show_flowers = True

# --- 🌸 फूलों जैसी बारिश का जादुई जावास्क्रिप्ट कोड (Confetti Burst) 🌸 ---
if st.session_state.show_flowers:
    confetti_html = """
    <script src="https://jsdelivr.net"></script>
    <script>
        // क्लिक करते ही चारों तरफ सुंदर फूलों/रंगों की बौछार करने का फंक्शन
        var duration = 3 * 1000;
        var end = Date.now() + duration;

        (function frame() {
          confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0, y: 0.8 }
          });
          confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1, y: 0.8 }
          });

          if (Date.now() < end) {
            requestAnimationFrame(frame);
          }
        }());
    </script>
    """
    components.html(confetti_html, height=0, width=0)
    # स्टेट वापस रीसेट करें ताकि हर बार रिफ्रेश पर खुद से न चले
    st.session_state.show_flowers = False

# --- समरी दिखाना और डाउनलोड बटन ---
if 'generated_summary' in st.session_state and uploaded_file is not None:
    st.write("---")
    
    # समरी को एक सुंदर कार्ड बॉक्स के अंदर दिखाना
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #334155;">
            <h3 style="color: #2b6cb0; margin-top: 0; margin-bottom: 10px;">📋 Summary:</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(st.session_state.generated_summary)
    st.write("")
    
    # 📥 डाउनलोड बटन - यूजर अपनी फ्री समरी को तुरंत अपने फोन/पीसी में डाउनलोड कर सकता है
    st.download_button(
        label="📥 Download Summary File",
        data=st.session_state.generated_summary,
        file_name="BrieflyAI_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )
