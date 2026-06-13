import streamlit as st
from google import genai
from gtts import gTTS
import io
import time

# Sayfa Ayarları
st.set_page_config(page_title="Novi AI", page_icon="🤖")

# --- SOL PANEL: GİRİŞ VE AYARLAR ---
st.sidebar.markdown("# 🛠️ Novi AI Kontrol Paneli")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)

# Şifre yönetimi
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = st.sidebar.text_input("🔑 Gemini API Anahtarını Gir", type="password")

if API_KEY:
    st.sidebar.success("✅ Sistem Aktif")
    client = genai.Client(api_key=API_KEY)
else:
    st.sidebar.warning("⚠️ Lütfen API anahtarını gir.")
    client = None

st.sidebar.write("---")
st.sidebar.markdown("### 👑 Yapımcı: Mehmet Emir Akıllı")

# --- ANA SAYFA ---
st.title("🤖 Novi AI")

if "messages" not in st.session_state: st.session_state.messages = []
if "ses" not in st.session_state: st.session_state.ses = True

# Hoparlör
st.session_state.ses = st.toggle("🔊 Sesli Yanıt", value=st.session_state.ses)

# Mesajları göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sohbet
if soru := st.chat_input("Bir şeyler yaz..."):
    if not client:
        st.error("Önce anahtar gir kanka!")
    else:
        st.chat_message("user").markdown(soru)
        st.session_state.messages.append({"role": "user", "content": soru})
        
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                # Yapımcı kontrolü
                if any(x in soru.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
                    cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
                else:
                    time.sleep(1) # Hız limitini aşmamak için kısa mola
                    response = client.models.generate_content(model='gemini-2.0-flash', contents=soru)
                    cevap = response.text
                
                st.markdown(cevap)
                st.session_state.messages.append({"role": "assistant", "content": cevap})
                
                if st.session_state.ses:
                    tts = gTTS(text=cevap, lang='tr')
                    f = io.BytesIO()
                    tts.write_to_fp(f)
                    st.audio(f.getvalue(), format="audio/mp3")