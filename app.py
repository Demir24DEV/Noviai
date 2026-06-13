import streamlit as st
from google import genai
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="Novi AI", page_icon="🤖")
st.title("🤖 Novi AI - Dünyaya Açık Yapay Zeka")

# 🔥 API Anahtarını buraya tırnakların içine yaz kanka
# GitHub yine uyarı verirse "I'll fix it later" ve "Allow Secret" de geç!
API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini Bağlantısını Kuruyoruz
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("API Bağlantısı kurulurken bir hata oluştu şef.")

# Mesaj geçmişini hafızada tutmak için alan açıyoruz
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski konuşmaları ekranda listele
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# İŞTE O HATALI OLAN CHAT GİRİŞ ALANI (Tamamen Sorunsuz Hali):
if soru := st.chat_input("Novi AI'a bir şeyler yaz..."):
    
    # Kullanıcının yazdığı mesajı ekrana bas ve hafızaya ekle
    with st.chat_message("user"):
        st.markdown(soru)
    st.session_state.messages.append({"role": "user", "content": soru})

    # Botun cevap vereceği alanı aç
    with st.chat_message("assistant"):
        with st.spinner("Novi AI düşünüyor..."):
            try:
                # Gemini'den cevap alıyoruz (Yeni Güncel SDK ile)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=soru
                )
                cevap_metni = response.text
                
                # Cevabı ekrana yazdırıyoruz
                st.markdown(cevap_metni)
                
                # Cevabı gTTS ile ses dosyasına çeviriyoruz
                tts = gTTS(text=cevap_metni, lang='tr')
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_bytes = audio_buffer.getvalue()
                
                # Sesi sitede oynatıyoruz
                st.audio(audio_bytes, format="audio/mp3")
                
                # Botun cevabını ve sesini hafızaya kaydediyoruz
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": cevap_metni,
                    "audio": audio_bytes
                })
                
            except Exception as e:
                st.error(f"Bot cevap verirken bir hata çıktı kanka: {e}")