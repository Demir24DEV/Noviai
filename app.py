import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import time

st.set_page_config(page_title="Novi AI", page_icon="🤖")

st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")
ses_acik = st.sidebar.checkbox("🔊 Sesli Yanıt", value=True)

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets kısmına API anahtarını ekle!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # Yapımcı kontrolü
        if any(x in prompt.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
            cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
        else:
            # Hata durumunda 3 kez deneme yapan döngü
            cevap = "Sunucu çok yoğun, biraz bekleyip tekrar dene."
            for i in range(3):
                try:
                    response = model.generate_content(prompt)
                    cevap = response.text
                    break # Başarılı olursa döngüden çık
                except:
                    time.sleep(2) # 2 saniye bekle ve tekrar dene
        
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