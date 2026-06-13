import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Novi AI", page_icon="🤖")

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# HATA ÇÖZÜMÜ: 'models/' ön ekini ve sürüm kısıtlamasını kaldıran en kararlı çağrı
model = genai.GenerativeModel('gemini-1.5-flash-002')

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Kritik Hata: {e}")