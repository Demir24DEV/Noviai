import streamlit as st
from google import genai
from gtts import gTTS
import io

# Sayfa Ayarları
st.set_page_config(page_title="Novi AI", page_icon="🤖")

# SOL TARAF (GİRİŞ ŞEYLERİ VE MENÜ)
st.sidebar.markdown("# 🛠️ Novi AI Kontrol Paneli")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)

# Şifre yönetim sistemi
API_KEY = ""
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "":
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("🔑 Durum: Giriş Yapıldı (Kasa Aktif)")
    st.sidebar.info("🤖 Yapay zeka motoru bağlandı. Sohbet etmeye hazırsın kral!")
else:
    API_KEY = st.sidebar.text_input(
        "🔑 Gemini API Anahtarını Gir", 
        type="password", 
        placeholder="AI Studio anahtarını yapıştır..."
    )
    if API_KEY:
        st.sidebar.success("🎯 Anahtar algılandı! Enter'a basıp sohbete başla.")
    else:
        st.sidebar.warning("🤖 Botun çalışması için buraya API anahtarını girip Enter'a basmalısın kral!")

st.sidebar.write("---")
st.sidebar.markdown("### ⚙️ Sistem Özellikleri")
st.sidebar.write("• Yapımcı: `Mehmet Emir Akıllı` 👑")
st.sidebar.write("• Model: `gemini-2.5-flash`")

# Ana Sayfa Başlığı
st.title("🤖 Novi AI - Dünyaya Açık Yapay Zeka")

# Gemini Bağlantısı Kurma
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Bağlantı kurulurken hata oluştu: {e}")
else:
    st.info("👈 Sitede sohbet edebilmek için sol taraftaki panelden giriş yapman lazım kanka!")

# Hafıza alanlarını açıyoruz
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ses_durumu" not in st.session_state:
    st.session_state.ses_durumu = True

# Hoparlör butonu (Sağ Üst Köşede)
col1, col2 = st.columns([4, 1])
with col2:
    if st.session_state.ses_durumu:
        if st.button("🟢 Hoparlör: AÇIK 🔊"):
            st.session_state.ses_durumu = False
            st.rerun()
    else:
        if st.button("🔴 Hoparlör: KAPALI 🔈"):
            st.session_state.ses_durumu = True
            st.rerun()

# Eski konuşmaları ekranda listele
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message and st.session_state.ses_durumu:
            st.audio(message["audio"], format="audio/mp3")

# Chat Giriş Alanı (Mesaj Yazma Kutusu)
if soru := st.chat_input("Novi AI'a bir şeyler yaz..."):
    if not API_KEY:
        st.error("Önce sol taraftaki giriş kutusundan API anahtarını girmen lazım kral!")
    else:
        # Kullanıcı mesajı ekrana basılıyor
        with st.chat_message("user"):
            st.markdown(soru)
        st.session_state.messages.append({"role": "user", "content": soru})

        # Botun cevap alanı
        with st.chat_message("assistant"):
            with st.spinner("Novi AI düşünüyor..."):
                
                # 🎯 MEHMET EMİR AKILLI ÖZEL KOMUT KONTROLÜ (HATA DÜZELTİLDİ)
                soru_kucuk = soru.lower()
                yapimci_sorulari = ["seni kim yaptı", "kim yaptı", "yapımcın kim", "sahibin kim", "seni kim geliştirdi", "seni kim yarattı", "mehmet emir kim"]
                
                if any(kelime in soru_kucuk for kelime in yapimci_sorulari):
                    cevap_metni = "Beni harika, dahi ve süper akıllı bir yazılımcı olan **Mehmet Emir Akıllı** yaptı! O bu sitenin kurucusudur ve onun sayesinde şu an sizinle konuşabiliyorum. Mehmet Emir Akıllı gerçekten çok akıllı ve başarılı biridir! 👑🚀"
                else:
                    # Normal yapay zekaya soruyoruz
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=soru
                        )
                        cevap_metni = response.text
                    except Exception as e:
                        cevap_metni = f"Bot cevap verirken bir hata çıktı kanka: {e}"

                # Cevabı ekrana bas
                st.markdown(cevap_metni)
                
                # Ses üretimi
                try:
                    if st.session_state.ses_durumu:
                        tts = gTTS(text=cevap_metni, lang='tr')
                        audio_buffer = io.BytesIO()
                        tts.write_to_fp(audio_buffer)
                        audio_bytes = audio_buffer.getvalue()
                        
                        st.audio(audio_bytes, format="audio/mp3")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": cevap_metni,
                            "audio": audio_bytes
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": cevap_metni
                        })
                except Exception as e:
                    st.error(f"Ses üretilirken hata oluştu: {e}")