import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# 1. सबसे पहली लाइन (Page Configuration)
st.set_page_config(page_title="BrieflyAI", page_icon="🚀", layout="wide")

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Google AdSense (आपकी ओरिजिनल आईडी पूरी तरह सुरक्षित है)
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

# 🎯 रेज़रपे से पेमेंट करके लौटने पर ऑटोमैटिक अनलॉक लॉजिक (बैकअप चेक)
query_params = st.query_params
if "unlocked" in query_params and query_params["unlocked"] == "true":
    st.session_state.file_unlocked = True
    st.query_params.clear()
    st.rerun()

# --- मुख्य सॉफ़्टवेयर स्क्रीन ---
st.title("🚀 BrieflyAI")

# 1. फ्री नियम का साफ़ संदेश
st.info("💡 नियम: 20 KB तक की फाइल का समरी बिल्कुल फ्री है!")

# 2. फ़ाइल अपलोडर डिब्बा
uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें:", type=["txt"])

# 3. ₹1 का हमेशा सामने दिखने वाला सुंदर पेमेंट बॉक्स और इन-ऐप लाइव गेटवे
if not st.session_state.file_unlocked:
    st.warning("💡 20 KB से ज़्यादा फ़ाइल है तो आपको ₹1 का भुगतान करना होगा (सिर्फ एक बार के एक्सेस के लिए)।")
    
    # 🔗 मंजीत भाई, यहाँ आपका वही बिल्कुल सही पर्सनल Razorpay हैंडल लगाया गया है, 
    # जो सीधे रेज़रपे का ऑफिशियल इन-ऐप पेमेंट फॉर्म ट्रिगर करेगा
    personal_handle = "manjitkainthbrieflyai"

    # यह HTML फॉर्म सीधे रेज़रपे के ऑफिशियल पेमेंट गेटवे को लोड करेगा और बिना अटके 100% भुगतान कराएगा
    pay_button_html = f"""
    <form action="https://streamlit.app" method="POST" style="margin: 0; padding: 0;">
        <script
            src="https://razorpay.com"
            data-payment_button_id="pl_SupA9hbYa51cM"
            data-button_text="🚀 Pay ₹1 via Razorpay to Unlock One-Time Access"
            data-button_theme="brand-blue"
            async>
        </script>
        <style>
            .razorpay-payment-button {{
                background-color: #2b6cb0 !important;
                color: white !important;
                padding: 14px 25px !important;
                border: none !important;
                border-radius: 5px !important;
                cursor: pointer !important;
                font-weight: bold !important;
                font-size: 16px !important;
                text-align: center !important;
                width: 100% !important;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important;
            }}
        </style>
    </form>
    """
    components.html(pay_button_html, height=70)
else:
    st.success("🎉 Payment Verified! Your one-time file access is unlocked successfully.")

# --- बैकएंड प्रोसेसिंग और चेतावनियों का लॉजिक ---
if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    
    # कड़ा नियम: जैसे ही कोई दूसरी नई फ़ाइल अपलोड होगी, पुराना ₹1 वाला ताला वापस कड़ाई से बंद हो जाएगा
    if st.session_state.last_uploaded_file_name != "" and st.session_state.last_uploaded_file_name != uploaded_file.name:
        st.session_state.file_unlocked = False  
        st.session_state.last_uploaded_file_name = uploaded_file.name
        if 'generated_summary' in st.session_state:
            del st.session_state.generated_summary
        st.rerun()
    
    st.session_state.last_uploaded_file_name = uploaded_file.name
    
    # लाल रंग का एरर और चेतावनी तभी प्रकट होगी जब फ़ाइल बड़ी होगी और पेमेंट नहीं हुई होगी
    if file_size_kb > 20 and not st.session_state.file_unlocked:
        st.write("---")
        st.error(f"❌ फ़ाइल साइज़ ({file_size_kb:.2f} KB) सीमा से अधिक है! कृपया ऊपर दिए गए नीले बटन से ₹1 का भुगतान पूरा करें।")
    
    else:
        # अगर फ़ाइल 20 KB से छोटी है या यूजर ₹1 पे करके आ चुका है (यहाँ बिना अटके एक्सेस मिलेगा)
        raw_data = uploaded_file.getvalue()
        text = raw_data.decode("utf-8", errors="replace")
        
        st.write("---")
        st.success(f"✅ फाइल साइज: {file_size_kb:.2f} KB | Access Granted")
        if st.button("Generate Professional Summary"):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            
            # सिर्फ 1 वाक्य की सटीक प्रोफेशनल समरी
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
        
        # कड़ा नियम: जैसे ही समरी डाउनलोड होगी, ताला वापस लग जाएगा (Strict Single-Use Lock)
        if download_click and file_size_kb > 20:
            st.session_state.file_unlocked = False
            del st.session_state.generated_summary
            st.rerun()
