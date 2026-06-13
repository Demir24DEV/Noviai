import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Sayfa Ayarları
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

# Konfigürasyon
genai.configure(api_key=api_key)
# En kararlı model
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

# Sohbet geçmişini göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Giriş
if prompt := st.chat_input("Mesajını yaz..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        # Yapımcıyı tanı
        if any(x in prompt.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
            cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
        else:
            try:
                # İstek gönder
                response = model.generate_content(prompt)
                cevap = response.text
            except Exception as e:
                cevap = "Şu an sunucu çok yoğun, biraz bekle kanka."
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        
        # Seslendirme
        if ses_acik:
            try:
                tts = gTTS(text=cevap, lang='tr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp.getvalue(), format="audio/mp3")
            except:
                pass