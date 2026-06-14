import streamlit as st
import requests

st.set_page_config(page_title="Novi AI", page_icon="🤖")
st.title("🤖 Novi AI")

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Halka açık ücretsiz API
            response = requests.get(f"https://api.popcat.xyz/chatbot?msg={prompt}", timeout=10)
            if response.status_code == 200:
                cevap = response.json().get('response', 'Hata oluştu.')
                st.markdown(cevap)
            else:
                st.write("Sistem şu an çok yoğun, lütfen 5 saniye bekle ve tekrar yaz.")
        except Exception as e:
            st.write("Bağlantı hatası oluştu, lütfen tekrar dene.")