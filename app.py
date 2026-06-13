import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import time

st.set_page_config(page_title="Novi AI", page_icon="🤖")

# Arayüz ve Yapımcı Bilgisi
st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")
ses_acik = st.sidebar.checkbox("🔊 Sesli Yanıt", value=True)

# API Anahtarı ve Model Ayarı
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets kısmına API anahtarını ekle!")
    st.stop()

genai.configure(api_key=api_key)
# 🎯 EN GÜNCEL MODEL: gemini-2.0-flash-exp
model = genai.GenerativeModel('gemini-2.0-flash-exp')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sohbet ve Hata Yönetimi
if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        cevap = None
        # Otomatik Tekrar Deneme Mekanizması
        for i in range(3):
            try:
                # Yapımcı kontrolü
                if any(x in prompt.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
                    cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
                    break
                else:
                    response = model.generate_content(prompt)
                    cevap = response.text
                    break
            except Exception as e:
                time.sleep(2) # Hata olursa 2 sn bekle
                cevap = f"Sunucu yoğun, tekrar deniyorum... ({i+1}/3)"
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        
        # Sesli yanıt
        if ses_acik and cevap and "yoğun" not in cevap:
            try:
                tts = gTTS(text=cevap, lang='tr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp.getvalue(), format="audio/mp3")
            except:
                pass