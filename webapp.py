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

st.set_page_config(page_title="BrieflyAI", page_icon="🚀")
st.title("🚀 BrieflyAI")

# विज्ञापन क्षेत्र
st.sidebar.markdown("### विज्ञापन")
st.sidebar.write("यहाँ अपने Google AdSense का कोड लगाएं।")

PAYMENT_LINK = "https://razorpay.me/@manjitkainthbrieflyai"
uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें:", type=["txt"])

if uploaded_file is not None:
    # फाइल साइज को KB में गणना
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    raw_data = uploaded_file.getvalue()
    text = raw_data.decode("utf-8", errors="replace")
    
    # 5 KB की सख्त सीमा
    if file_size_kb > 5:
        st.warning(f"फाइल साइज {file_size_kb:.2f} KB है। 5 KB से बड़ी फाइल्स के लिए प्रीमियम जरूरी है।")
        st.link_button("🚀 Pay ₹30 for Premium", url=PAYMENT_LINK)
    else:
        st.success(f"फाइल साइज: {file_size_kb:.2f} KB | Free Tier")
        
        if st.button("Generate Professional Summary"):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            
            # सारांश सिर्फ 1 वाक्य का
            summary_sentences = summarizer(parser.document, 1) 
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            
            st.subheader("Summary:")
            st.write(summary)
            st.caption("यह सारांश BrieflyAI द्वारा तैयार किया गया है।")
