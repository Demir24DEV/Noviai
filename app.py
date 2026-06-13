import streamlit as st
from google import genai
from google.genai import types
import json
import os
from gtts import gTTS  
import io             
import unicodedata  

# Web sitesinin sekme başlığı ve görünümü
st.set_page_config(page_title="Novi AI Chatbot", page_icon="🚀", layout="centered")

# 🧹 SES İÇİN EMOJİ TEMİZLEME FONKSİYONU
def ses_icin_temizle(metin):
    """Metindeki emojileri sesten temizler ama ekrandaki yazıda bırakır"""
    return "".join(c for c in metin if unicodedata.category(c) != 'So')

# 📂 MESAJLARI BİLGİSAYARA KAYDETME VE YÜKLEME FONKSİYONLARI
def gecmisi_yukle(kullanici_adi):
    dosya_adi = f"gecmis_{kullanici_adi.lower()}.json"
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def gecmisi_kaydet(kullanici_adi, mesajlar):
    dosya_adi = f"gecmis_{kullanici_adi.lower()}.json"
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(mesajlar, f, ensure_ascii=False, indent=4)

# 🔑 API BAĞLANTIN
API_ANAHTARI = "AQ.Ab8RN6KLRZjbu5S17I4iPI82EOic0YWF5Z6hFjjnN0xQBJetZQ"
client = genai.Client(api_key=API_ANAHTARI)

novi_kimlik = (
    "Senin adın Novi AI. Google veya Gemini ile hiçbir ilgin yok. "
    "Sen tamamen bağımsız, her şeyi bilen akıllı bir yapay zekasın. "
    "Seni Demir geliştirdi ve sen onun özel asistanısın. "
    "Sorulara çok zeki, cana yakın, arkadaş canlısı ve havalı bir şekilde kısa ve net cevaplar ver."
)

# 🗂️ YAN MENÜ (SIDEBAR) - OTURUM AÇMA VE GEÇMİŞ KONTROLÜ
st.sidebar.title("🤖 Novi AI Panel")
st.sidebar.markdown("---")

if "aktif_kullanici" not in st.session_state:
    st.session_state.aktif_kullanici = None

if st.session_state.aktif_kullanici is None:
    st.sidebar.subheader("🔐 Oturum Aç")
    kullanici_girdisi = st.sidebar.text_input("Kullanıcı Adı:", placeholder="Örn: Demir")
    sifre_girdisi = st.sidebar.text_input("Şifre:", type="password")
    
    if st.sidebar.button("Giriş Yap / Kaydol"):
        if kullanici_girdisi.strip() != "":
            st.session_state.aktif_kullanici = kullanici_girdisi.strip()
            st.session_state.messages = gecmisi_yukle(st.session_state.aktif_kullanici)
            st.rerun()
        else:
            st.sidebar.error("Kanka boş kullanıcı adı giremezsin!")
            
    st.sidebar.warning("⚠️ Konuşmalarının kaydedilmesi için oturum açmalısın şef.")
else:
    st.sidebar.success(f"🟢 Hesap: {st.session_state.aktif_kullanici}")
    st.sidebar.markdown("### ⚙️ Ayarlar")
    
    if st.sidebar.button("🔄 Sohbet Geçmişini Temizle"):
        st.session_state.messages = []
        gecmisi_kaydet(st.session_state.aktif_kullanici, [])
        st.rerun()
        
    if st.sidebar.button("🚪 Oturumu Kapat"):
        st.session_state.aktif_kullanici = None
        st.session_state.messages = []
        st.rerun()

# 💬 ANA SOHBET EKRANI
st.title("🚀 Novi AI")
st.caption("Demir tarafından geliştirilen gelişmiş akıllı asistan")

if st.session_state.aktif_kullanici is not None:
    
    # Eski mesajları ekrana çizdirme
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown("---")
    
    # 🔊 SES DURUMU KONTROLÜ
    if "ses_durumu" not in st.session_state:
        st.session_state.ses_durumu = True

    # Buton yerleşimi
    col1, col2 = st.columns([5, 3])
    with col1:
        st.write("") 
    with col2:
        if st.session_state.ses_durumu:
            if st.button("🟢 Hoparlör: AÇIK 🔊", help="Sadece metin moduna geçmek için tıkla"):
                st.session_state.ses_durumu = False
                st.rerun()
        else:
            if st.button("🔴 Hoparlör: KAPALI 🔇", help="Sesli yanıt moduna geçmek için tıkla"):
                st.session_state.ses_durumu = True
                st.rerun()

    # Kullanıcıdan yazı alma kutusu
    if soru := st.chat_input("Novi AI'a bir şeyler sor şef..."):
        if soru := st.chat_input("Novi AI'a bir şeyler yaz..."):
        with st.chat_message("user"):
            st.markdown(soru)

        # Yapay zekanın cevap üretmesi
        with st.chat_message("assistant"):
            with st.spinner("Novi AI düşünüyor..."):
                try:
                    cevap = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=soru,
                        config=types.GenerateContentConfig(
                            system_instruction=novi_kimlik
                        )
                    )
                    output_text = cevap.text
                    st.markdown(output_text)  # Ekrana emojili hali basılıyor
                    
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                    gecmisi_kaydet(st.session_state.aktif_kullanici, st.session_state.messages)
                    
                    # 🎙️ HOPARLÖR AÇIKSA VE YAZI VARSA EMOJİLERİ SİLİP SESLENDİR
                    if st.session_state.ses_durumu:
                        temiz_ses_metni = ses_icin_temizle(output_text)
                        
                        if temiz_ses_metni.strip():
                            tts = gTTS(text=temiz_ses_metni, lang='tr')
                            ses_dosyasi = io.BytesIO()
                            tts.write_to_fp(ses_dosyasi)
                            ses_dosyasi.seek(0)
                            st.audio(ses_dosyasi, format='audio/mp3', autoplay=True)
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu kanka: {e}")
else:
    st.info("💡 Siten hazır şef! Konuşmaya başlamak ve geçmişinin kaydolması için sol taraftaki menüden kendine bir kullanıcı adı yazıp giriş yap!")