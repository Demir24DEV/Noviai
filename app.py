import streamlit as st
import requests

st.set_page_config(page_title="Novi AI", page_icon="🤖")
st.title("🤖 Novi AI")

# Basit model bağlantısı
API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
# Token'ı tırnakların içine yapıştır
HEADERS = {"Authorization": "Bearer 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"}

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
            if response.status_code == 200:
                cevap = response.json()[0]['generated_text']
                st.markdown(cevap)
            else:
                st.write("Model şu an dinleniyor, lütfen 10 saniye sonra tekrar dene.")
        except:
            st.write("Bir hata oluştu, sayfayı yenile.")