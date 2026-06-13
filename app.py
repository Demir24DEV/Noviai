import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Sayfa Yapılandırması
st.set_page_config(page_title="Novi AI", page_icon="🤖")

# --- SOL PANEL ---
st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")
ses_acik = st.sidebar.checkbox("🔊 Sesli Yanıt", value=True)

# API Anahtarı
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

# PRO MODEL AYARI
genai.configure(api_key=api_key)
# 🎯 Gemini 1.5 Pro modelini burada tanımlıyoruz
model = genai.GenerativeModel('gemini-1.5-pro')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI (Pro Sürüm)")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Pro sürüm dinliyor..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Pro zeka çalışıyor..."):
            if any(x in prompt.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
                cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
            else:
                try:
                    # PRO model ile istek atıyoruz
                    response = model.generate_content(prompt)
                    cevap = response.text
                except Exception as e:
                    cevap = f"Pro model şu an yoğun, bir daha dene kanka. (Hata: {e})"
            
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            
            if ses_acik:
                try:
                    tts = gTTS(text=cevap, lang='tr')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp.getvalue(), format="audio/mp3")
                except:
                    pass