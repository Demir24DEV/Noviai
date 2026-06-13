import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Sayfa Yapılandırması
st.set_page_config(page_title="Novi AI", page_icon="🤖")

# --- SOL PANEL (ARAYÜZ) ---
st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")
ses_acik = st.sidebar.checkbox("🔊 Sesli Yanıt", value=True)

# API Anahtarı
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets kısmına GEMINI_API_KEY eklemen lazım kanka!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sohbet Geçmişi
if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Giriş Kutusu
if prompt := st.chat_input("Bir şeyler yaz..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # Yapımcı Kontrolü
        if any(x in prompt.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
            cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
        else:
            try:
                cevap = model.generate_content(prompt).text
            except Exception as e:
                cevap = "Sunucuda yoğunluk var kanka, bir daha dene."
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        
        # Sesli Yanıt
        if ses_acik:
            try:
                tts = gTTS(text=cevap, lang='tr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp.getvalue(), format="audio/mp3")
            except:
                st.write("Ses üretilemedi.")