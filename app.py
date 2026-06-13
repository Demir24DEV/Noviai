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
    st.error("Secrets kısmına GEMINI_API_KEY ekle!")
    st.stop()

# Model Yapılandırması
genai.configure(api_key=api_key)
# En garantili model ismi
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Novi AI")

# Mesajları göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Giriş
if prompt := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        try:
            # İstek at
            response = model.generate_content(prompt)
            cevap = response.text
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            
            # Sesli Yanıt
            if ses_acik:
                tts = gTTS(text=cevap, lang='tr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp.getvalue(), format="audio/mp3")
                
        except Exception as e:
            st.error(f"Hata: {e}")
            st.warning("Eğer bu hata '404' ise, Google AI Studio'dan anahtarını yenileyip Secrets'a tekrar yapıştır.")