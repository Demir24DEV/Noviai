import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

st.set_page_config(page_title="Novi AI", page_icon="🤖")

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 🎯 BURASI KRİTİK: Modeli isme göre değil, doğrudan tanımlıyoruz
model = genai.GenerativeModel('models/gemini-1.5-flash')

if prompt := st.chat_input("Mesajını yaz..."):
    with st.chat_message("assistant"):
        try:
            # generate_content metodunu en sade haliyle çağırıyoruz
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"HATA KODU: {e}")