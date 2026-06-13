import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Novi AI", page_icon="🤖")

# API Anahtarı Ayarı
API_KEY = st.secrets.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Lütfen Streamlit Secrets kısmına GEMINI_API_KEY ekle!")
    st.stop()

st.title("🤖 Novi AI")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if soru := st.chat_input("Bir şeyler yaz..."):
    st.chat_message("user").markdown(soru)
    st.session_state.messages.append({"role": "user", "content": soru})
    
    with st.chat_message("assistant"):
        # Yapımcı kontrolü
        if any(x in soru.lower() for x in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
            cevap = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
        else:
            try:
                response = model.generate_content(soru)
                cevap = response.text
            except Exception as e:
                cevap = f"Bir hata oldu kanka: {e}"
        
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})