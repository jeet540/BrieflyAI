import streamlit as st
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# NLTK डेटा डाउनलोड (यह एरर को ठीक कर देगा)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

st.title("🚀 BrieflyAI")

# पेमेंट लिंक
PAYMENT_LINK = "https://razorpay.me/@manjitkainthbrieflyai"

uploaded_file = st.file_uploader("Upload .txt file:", type=["txt"])

if uploaded_file is not None:
    # फाइल साइज चेक करें
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    
    try:
        raw_data = uploaded_file.getvalue()
        text = raw_data.decode("utf-8", errors="replace")
        
        # 1. अगर फाइल 200 KB से बड़ी है (प्रीमियम)
        if file_size_kb > 200:
            st.warning(f"आपकी फाइल {file_size_kb:.2f} KB की है। यह 200 KB से बड़ी है।")
            st.write("प्रीमियम समरी सर्विस के लिए ₹30 का भुगतान करें:")
            st.link_button("Pay ₹30 Now", url=PAYMENT_LINK)
            st.info("पेमेंट करने के बाद आप इस फाइल को प्रोसेस कर सकते हैं।")
            
        # 2. अगर फाइल 200 KB से छोटी है (फ्री + एड्स)
        else:
            st.success(f"फाइल साइज: {file_size_kb:.2f} KB (Free Tier)")
            
            # यहाँ विज्ञापन का कोड
            st.sidebar.markdown("### विज्ञापन")
            st.sidebar.write("यहाँ अपने Google AdSense का कोड डाल सकते हैं।")
            
            if st.button("Generate Summary"):
                if text.strip():
                    parser = PlaintextParser.from_string(text, Tokenizer("english"))
                    summarizer = LsaSummarizer()
                    # 3 वाक्यों का सारांश (आप इसे बदल भी सकते हैं)
                    summary_sentences = summarizer(parser.document, 3) 
                    summary = " ".join([str(sentence) for sentence in summary_sentences])
                    
                    st.subheader("Professional Summary:")
                    st.write(summary)
                else:
                    st.warning("File khali hai.")

    except Exception as e:
        st.error(f"Error aaya: {e}")
