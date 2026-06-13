import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Novi AI", page_icon="🤖")

api_key = st.secrets.get("GEMINI_API_KEY")

# KRİTİK DEĞİŞİKLİK: API sürümünü 'v1' olarak zorluyoruz
genai.configure(api_key=api_key, api_version='v1')

# Modeli v1 üzerinden çağırıyoruz
model = genai.GenerativeModel('gemini-1.5-flash')

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Kritik Hata: {e}")