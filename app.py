import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Novi AI", page_icon="🤖")

# API Anahtarını al
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Anahtarı 'Secrets' kısmında bulunamadı!")
    st.stop()

# API Yapılandırması
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Konfigürasyon hatası: {e}")
    st.stop()

# Sohbet kısmı
if prompt := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Model hatası: {e}")