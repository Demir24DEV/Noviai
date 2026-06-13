import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

st.set_page_config(page_title="Novi AI", page_icon="🤖")

st.sidebar.markdown("# 🛠️ Novi AI Kontrol")
st.sidebar.info("Yapımcı: Mehmet Emir Akıllı 👑")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Anahtarı girilmemiş!")
    st.stop()

# EN GARANTİLİ YAPILANDIRMA
genai.configure(api_key=api_key)
# 'gemini-1.5-flash' en stabil olanıdır
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []
st.title("🤖 Novi AI")

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            cevap = response.text
            st.markdown(cevap)
            
            # Sesli yanıt
            tts = gTTS(text=cevap, lang='tr')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp.getvalue(), format="audio/mp3")
            
        except Exception as e:
            # HATAYI BURAYA YAZDIRIYORUZ, NEDENİ ÖĞRENELİM
            st.error(f"HATA: {e}")