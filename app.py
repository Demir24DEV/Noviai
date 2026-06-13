import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

st.set_page_config(page_title="Novi AI", page_icon="🤖")

st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")
ses_acik = st.sidebar.checkbox("🔊 Sesli Yanıt", value=True)

# API Anahtarı
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets kısmına API anahtarını ekle!")
    st.stop()

# GÜNCEL YAPILANDIRMA
genai.configure(api_key=api_key)
# Model adını sadece 'gemini-1.5-flash' olarak bırak, o en güncelidir
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            cevap = response.text
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            
            if ses_acik:
                tts = gTTS(text=cevap, lang='tr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp.getvalue(), format="audio/mp3")
        except Exception as e:
            st.error("Model hatası: API anahtarını kontrol et veya yeni bir proje oluştur.")