import streamlit as st
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Google AdSense Meta Tag Verification
st.markdown('<meta name="google-adsense-account" content="ca-pub-3995974960275140">', unsafe_allow_html=True)

# NLTK setup
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

st.set_page_config(page_title="BrieflyAI", page_icon="🚀")
st.title("🚀 BrieflyAI")

st.info("💡 नियम: 10 KB तक की फाइल का समरी बिल्कुल फ्री है!")

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

# About Us और Privacy Policy सेक्शन
st.markdown("---")
st.subheader("जानकारी")
with st.expander("About Us"):
    st.write("BrieflyAI एक AI-आधारित टूल है जो लंबे टेक्स्ट को संक्षिप्त और सटीक सारांश (summary) में बदलता है।")

with st.expander("Privacy Policy"):
    st.write("हम आपकी निजता का सम्मान करते हैं। हम आपका डेटा सुरक्षित रखते हैं और किसी तीसरे पक्ष के साथ साझा नहीं करते हैं।")

# यहाँ आपका नया डिज़ाइन वाला Powered by सेक्शन है
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd;'>
        <p style='font-size: 16px; font-weight: bold; color: #333;'>🚀 Powered by Kainth</p>
        <p style='font-size: 12px; color: #777;'>© 2026 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
