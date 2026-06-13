import streamlit as st
import google.generativeai as genai

st.title("Novi AI Test")

# Secrets'tan anahtarı çek
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Secrets içerisinde GEMINI_API_KEY bulunamadı!")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if prompt := st.chat_input("Bir şeyler yaz..."):
        try:
            # En sade çağrı
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"HATA OLUŞTU: {e}")