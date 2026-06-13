import streamlit as st
import requests

st.set_page_config(page_title="Novi AI", page_icon="🤖")

st.title("🤖 Novi AI")

# Hugging Face üzerinden ücretsiz model (Llama-3 tabanlı)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer hf_uLqB... "} # Buraya HuggingFace'ten ücretsiz bir token alıp koyabilirsin

if prompt := st.chat_input("Mesajını yaz..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Basit bir POST isteği ile modelden cevap alıyoruz
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            cevap = response.json()[0]['generated_text']
            st.markdown(cevap)
        except Exception as e:
            st.error("Model yükleniyor, lütfen 10 saniye bekle ve tekrar dene.")