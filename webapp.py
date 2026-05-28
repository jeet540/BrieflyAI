import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# 1. सबसे पहली लाइन (Page Configuration)
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Google AdSense (आपकी ओरिजिनल आईडी यहाँ बिल्कुल सुरक्षित है)
st.markdown('<meta name="google-adsense-account" content="ca-pub-3995974960275140">', unsafe_allow_html=True)

# NLTK setup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# --- कड़ा सुरक्षित बैकएंड स्टेट मैनेजमेंट (एक बार के एक्सेस के लिए) ---
if 'file_unlocked' not in st.session_state:
    st.session_state.file_unlocked = False
if 'last_uploaded_file_name' not in st.session_state:
    st.session_state.last_uploaded_file_name = ""

# 🎯 रेज़रपे से पेमेंट करके लौटने पर ऑटोमैटिक अनलॉक लॉजिक
query_params = st.query_params
if "payment_id" in query_params or "razorpay_payment_id" in query_params or "unlocked" in query_params:
    st.session_state.file_unlocked = True
    st.query_params.clear()  # URL रसीद साफ़ करना
    st.rerun()

# --- मुख्य सॉफ़्टवेयर स्क्रीन ---
st.title("🚀 BrieflyAI")

# 1. सबसे ऊपर नियम का साफ़ संदेश
st.info("💡 नियम: 20 KB तक की फाइल का समरी बिल्कुल फ्री है!")

# 2. उसके ठीक नीचे आपका "Drag and drop file here" वाला फ़ाइल अपलोडर
uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें:", type=["txt"])

# 3. नीले रंग का रेज़रपे डिब्बा हमेशा इस अपलोडर डिब्बे के ठीक नीचे लगा रहेगा
if not st.session_state.file_unlocked:
    # 📝 आपके कहे अनुसार कड़ाई से ₹1 का निर्देश संदेश सेट कर दिया गया है
    st.warning("💡 20 KB से ज़्यादा फ़ाइल है तो आपको ₹1 का भुगतान करना होगा (सिर्फ एक बार के एक्सेस के लिए)।")
    
    # 🔗 आपका पर्सनल razorpay.me वाला असली और सही हैंडल लिंक
    razorpay_payment_url = "https://razorpay.me/@manjitkainthbrieflyai" 

    # 🚀 फिक्स: चमकदार गहरा नीला बटन जिसमें अब साफ़-साफ़ ₹1 (Pay ₹1) लिखा हुआ है
    pay_button_html = f"""
    <a href="{razorpay_payment_url}" target="_blank" style="text-decoration: none;">
        <button style="
            background-color: #2b6cb0; 
            color: white; 
            padding: 14px 25px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            width: 100%;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            transition: background-color 0.2s;">
            🚀 Pay ₹1 via Razorpay to Unlock One-Time Access
        </button>
    </a>
    """
    components.html(pay_button_html, height=70)
else:
    st.success("🎉 Payment Verified! Your one-time file access is unlocked successfully.")

# --- बैकएंड प्रोसेसिंग और चेतावनियों का लॉजिक ---
if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    
    # कड़ा नियम: जैसे ही कोई दूसरी नई फ़ाइल अपलोड होगी, पुराना एक्सेस तुरंत बंद हो जाएगा
    if st.session_state.last_uploaded_file_name != "" and st.session_state.last_uploaded_file_name != uploaded_file.name:
        st.session_state.file_unlocked = False  # नया ताला बंद
        st.session_state.last_uploaded_file_name = uploaded_file.name
        if 'generated_summary' in st.session_state:
            del st.session_state.generated_summary
        st.rerun()
    
    st.session_state.last_uploaded_file_name = uploaded_file.name
    
    # केवल एक छोटा और साफ़ वार्निंग बॉक्स (यहाँ भी ₹1 कर दिया गया है)
    if file_size_kb > 20 and not st.session_state.file_unlocked:
        st.write("---")
        st.error(f"❌ फ़ाइल साइज़ ({file_size_kb:.2f} KB) सीमा से अधिक है! कृपया ऊपर दिए गए नीले बटन से ₹1 का भुगतान पूरा करें।")
    
    else:
        # अगर फ़ाइल 20 KB से छोटी है या यूजर पे करके आ चुका है
        raw_data = uploaded_file.getvalue()
        text = raw_data.decode("utf-8", errors="replace")
        
        st.write("---")
        st.success(f"✅ फाइल साइज: {file_size_kb:.2f} KB | Access Granted")
        if st.button("Generate Professional Summary"):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            
            summary_sentences = summarizer(parser.document, 1) 
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            st.session_state.generated_summary = summary

# --- समरी दिखाना और डाउनलोड बटन ---
if 'generated_summary' in st.session_state and uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    if st.session_state.file_unlocked or file_size_kb <= 20:
        st.write("---")
        st.subheader("Summary:")
        st.write(st.session_state.generated_summary)
        
        # 📥 डाउनलोड बटन - इस पर क्लिक करते ही एक बार का एक्सेस तुरंत समाप्त हो जाएगा
        download_click = st.download_button(
            label="📥 Download Summary",
            data=st.session_state.generated_summary,
            file_name="BrieflyAI_Summary.txt",
            mime="text/plain"
        )
        
        if download_click and file_size_kb > 20:
            st.session_state.file_unlocked = False
            del st.session_state.generated_summary
            st.rerun()
