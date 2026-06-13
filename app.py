import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

st.set_page_config(page_title="Novi AI", page_icon="🤖")

# API Anahtarını kontrol et
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

# Hata ayıklama için try-except bloğu
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Config hatası: {e}")

if prompt := st.chat_input("Mesajını yaz..."):
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            # HATAYI BURAYA YAZDIRIYORUZ
            st.error(f"TAM HATA KODU: {e}")