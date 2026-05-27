import streamlit as st
import streamlit.components.v1 as components
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Google AdSense Verification Code
adsense_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3995974960275140" crossorigin="anonymous"></script>
"""
components.html(adsense_code, height=0)

# NLTK setup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

st.set_page_config(page_title="BrieflyAI", page_icon="🚀")
st.title("🚀 BrieflyAI")

# नियम और जानकारी
st.info("💡 नियम: 10 KB तक की फाइल का समरी बिल्कुल फ्री है! उससे बड़ी फाइल्स के लिए ₹30 का प्रीमियम लें।")

PAYMENT_LINK = "https://razorpay.me/@manjitkainthbrieflyai"
uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें:", type=["txt"])

if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    raw_data = uploaded_file.getvalue()
    text = raw_data.decode("utf-8", errors="replace")
    
    if file_size_kb > 10:
        st.warning(f"❌ फाइल साइज {file_size_kb:.2f} KB है। प्रीमियम आवश्यक है।")
        st.link_button("🚀 Pay ₹30 for Premium", url=PAYMENT_LINK)
    else:
        st.success(f"✅ फाइल साइज: {file_size_kb:.2f} KB | Free Tier")
        
        if st.button("Generate Professional Summary"):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary_sentences = summarizer(parser.document, 1) 
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            st.subheader("Summary:")
            st.write(summary)
            st.caption("यह सारांश BrieflyAI द्वारा तैयार किया गया है।")

# नीचे की तरफ Kainth का क्रेडिट
st.markdown("---")
st.markdown("<div style='text-align: right;'><strong>Powered by Kainth</strong></div>", unsafe_allow_html=True)
