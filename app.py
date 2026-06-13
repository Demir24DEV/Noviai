import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Novi AI", page_icon="🤖")
st.title("🤖 Novi AI")

# API Anahtarı Kontrolü
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("HATA: Streamlit 'Secrets' kısmında GEMINI_API_KEY bulunamadı!")
    st.stop()

# Model Yapılandırması - En stabil model 'gemini-1.5-flash'
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
    st.stop()

# Oturum Durumu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Bir şeyler yaz..."):
    # Yapımcı kontrolü
    if any(keyword in prompt.lower() for keyword in ["kim yaptın", "yapımcın kim", "mehmet emir"]):
        response_text = "Beni dahi yazılımcı Mehmet Emir Akıllı yarattı! 👑"
    else:
        try:
            response = model.generate_content(prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"Hata oluştu: {e}"

    # Mesajı Kaydet ve Göster
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})