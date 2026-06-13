import streamlit as st
from google import genai
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="Novi AI", page_icon="🤖")
st.title("🤖 Novi AI - Dünyaya Açık Yapay Zeka")

# Sır kasasından API anahtarını çekiyoruz
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Kanka Streamlit Secrets kasasında anahtar bulunamadı!")

# Hafıza alanlarını açıyoruz
if "messages" not in st.session_state:
    st.session_state.messages = []

# ARADIĞIN O HOPARLÖR KOMUTLARI BURADA BAŞLIYOR:
if "ses_durumu" not in st.session_state:
    st.session_state.ses_durumu = True  # İlk açılışta ses açık olsun

# Sağ üst köşeye hoparlör butonunu koyuyoruz
col1, col2 = st.columns([4, 1])
with col2:
    if st.session_state.ses_durumu:
        if st.button("🟢 Hoparlör: AÇIK 🔊", help="Sadece metin moduna geçmek için tıkla"):
            st.session_state.ses_durumu = False
            st.rerun()
    else:
        if st.button("🔴 Hoparlör: KAPALI 🔈", help="Sesli yanıt moduna geçmek için tıkla"):
            st.session_state.ses_durumu = True
            st.rerun()

# Eski konuşmaları ekranda listele
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Ses hafızada varsa ve hoparlör açıksa çal
        if "audio" in message and st.session_state.ses_durumu:
            st.audio(message["audio"], format="audio/mp3")

# Chat Giriş Alanı
if soru := st.chat_input("Novi AI'a bir şeyler yaz..."):
    
    # Kullanıcı mesajı
    with st.chat_message("user"):
        st.markdown(soru)
    st.session_state.messages.append({"role": "user", "content": soru})

    # Botun cevap alanı
    with st.chat_message("assistant"):
        with st.spinner("Novi AI düşünüyor..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=soru
                )
                cevap_metni = response.text
                st.markdown(cevap_metni)
                
                # Eğer hoparlör AÇIK ise ses üret ve oynat
                if st.session_state.ses_durumu:
                    tts = gTTS(text=cevap_metni, lang='tr')
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_bytes = audio_buffer.getvalue()
                    
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # Hafızaya sesli kaydet
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": cevap_metni,
                        "audio": audio_bytes
                    })
                else:
                    # Hoparlör kapalıysa sadece metin olarak kaydet
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": cevap_metni
                    })
                
            except Exception as e:
                st.error(f"Bot cevap verirken bir hata çıktı kanka: {e}")