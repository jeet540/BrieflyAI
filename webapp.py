import streamlit as st
import streamlit_authenticator as stauth
import datetime

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="BrieflyAI", page_icon="🚀")

# 2. डमी यूजर डेटा (प्रोफेशनल सिस्टम के लिए इसे बाद में डेटाबेस से जोड़ें)
names = ['User']
usernames = ['kainth_user']
hashed_passwords = ['abc'] 

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'brieflyai_cookie', 'secret_key')

# 3. लॉगिन सिस्टम
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # अगर लॉगिन सफल है
    st.sidebar.write(f'स्वागत है, {name}!')
    if st.sidebar.button('Logout'):
        authenticator.logout('Logout', 'sidebar')

    # मुख्य ऐप का टाइटल
    st.title("🚀 BrieflyAI - Professional Summarizer")
    
    # सब्सक्रिप्शन डेटा को सुरक्षित रखने के लिए session_state
    if 'subscription_expiry' not in st.session_state:
        st.session_state.subscription_expiry = None

    def activate_subscription():
        st.session_state.subscription_expiry = datetime.date.today() + datetime.timedelta(days=30)
        st.success("✅ सब्सक्रिप्शन सक्रिय हो गया! अब आप बड़ी फाइलें भी प्रोसेस कर सकते हैं।")

    # सब्सक्रिप्शन चेक लॉजिक
    is_active = False
    if st.session_state.subscription_expiry:
        today = datetime.date.today()
        expiry = st.session_state.subscription_expiry
        
        # एक्सपायरी रिमाइंडर (1 दिन पहले)
        if today == (expiry - datetime.timedelta(days=1)):
            st.warning("🔔 ध्यान दें: आपका सब्सक्रिप्शन कल समाप्त हो रहा है।")
            is_active = True
        elif today <= expiry:
            is_active = True
        else:
            st.error("⚠️ आपका सब्सक्रिप्शन समाप्त हो चुका है।")

    # फाइल अपलोडर - 50KB लिमिट के साथ
    uploaded_file = st.file_uploader("अपनी .txt फाइल अपलोड करें (Max 50KB)", type=["txt"])
    
    if uploaded_file is not None:
        # 50KB से ऊपर होने पर सब्सक्रिप्शन मांगना
        if uploaded_file.size > 50 * 1024:
            st.error("❌ फाइल 50KB से बड़ी है!")
            st.warning("💡 बड़ी फाइलें प्रोसेस करने के लिए ₹30 का सब्सक्रिप्शन लें (1 महीने के लिए)।")
            if st.button("₹30 का सब्सक्रिप्शन लें"):
                activate_subscription()
        else:
            st.success("✅ फाइल अपलोड सफल! प्रोसेसिंग शुरू...")

    # सजेशन बॉक्स
    if is_active:
        st.info("💡 प्रो-फीचर: अपने सुझाव यहाँ लिखें:")
        st.text_area("सजेशन बॉक्स:")
    else:
        st.info("🔒 अधिक सुविधाओं के लिए ₹30 का सब्सक्रिप्शन लें।")

    # ब्रांडिंग (Powered by Kainth)
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>🚀 <strong>Powered by Kainth</strong></div>", unsafe_html=True)

elif authentication_status == False:
    st.error('गलत यूजरनेम या पासवर्ड!')
elif authentication_status == None:
    st.warning('कृपया साइन-इन करें।')
