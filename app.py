import streamlit as st
import requests

st.title("🤖 Novi AI")

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # En basit public API
            response = requests.get(f"https://api.popcat.xyz/chatbot?msg={prompt}")
            if response.status_code == 200:
                cevap = response.json().get('response', 'Hata...')
                st.markdown(cevap)
            else:
                st.write("Sistem şu an meşgul, bir daha dene.")
        except:
            st.write("İnternet bağlantısı veya sunucu hatası.")