import streamlit as st
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# NLTK setup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

st.title("🚀 BrieflyAI")

# विज्ञापन क्षेत्र (यहाँ अपना AdSense कोड डालें)
st.sidebar.markdown("### विज्ञापन")
st.sidebar.write("यहाँ Google AdSense के विज्ञापन आएंगे।")

PAYMENT_LINK = "https://razorpay.me/@manjitkainthbrieflyai"
uploaded_file = st.file_uploader("Upload .txt file:", type=["txt"])

if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    raw_data = uploaded_file.getvalue()
    text = raw_data.decode("utf-8", errors="replace")
    
    # फ्री टियर लिमिट 50 KB
    if file_size_kb > 50:
        st.warning(f"फाइल साइज {file_size_kb:.2f} KB है। 50 KB से बड़ी फाइल के लिए प्रीमियम लें।")
        st.link_button("Pay ₹30 Now for Premium", url=PAYMENT_LINK)
    else:
        st.success(f"फाइल साइज: {file_size_kb:.2f} KB (Free Tier)")
        if st.button("Generate Summary"):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            # सारांश छोटा करने के लिए वाक्यों की संख्या 2 रखी है
            summary_sentences = summarizer(parser.document, 2) 
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            
            st.subheader("Professional Summary:")
            st.write(summary)
            st.info("प्रो टिप: बड़ी फाइल्स के लिए प्रीमियम वर्जन का उपयोग करें।")
