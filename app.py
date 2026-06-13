import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Novi AI", page_icon="🤖")

api_key = st.secrets.get("GEMINI_API_KEY")

# API'yi v1 sürümüne zorlayan yapılandırma
genai.configure(api_key=api_key, client_options={'api_endpoint': 'https://generativelanguage.googleapis.com/v1'})

# Model tanımı
model = genai.GenerativeModel('gemini-1.5-flash')

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Kritik Hata: {e}")