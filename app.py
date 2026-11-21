import json
import random
import re
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Duygu Analizi Eğitim Modülü", page_icon="🎭", layout="centered")

MODEL = "qwen/qwen3.8-27b"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp {
  background: radial-gradient(circle at 10% 10%, #ffe1f0 0%, transparent 40%),
              radial-gradient(circle at 90% 20%, #d9f4ff 0%, transparent 40%),
              radial-gradient(circle at 50% 100%, #fff3c4 0%, transparent 45%),
              #fdfbff;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #4f46e5 0%, #9333ea 55%, #db2777 100%);
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebar"] input { color: #1e1b4b !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #1e1b4b !important; }
[data-testid="stSidebar"] .stAlert { background: rgba(255,255,255,.18); border-radius: 14px; }

.hero {
  background: linear-gradient(120deg, #f43f5e, #f97316, #eab308, #22c55e, #06b6d4, #8b5cf6, #f43f5e);
  background-size: 300% 300%; animation: akis 10s ease infinite;
  padding: 1.8rem; border-radius: 22px; color: white; margin-bottom: 1.4rem;
  box-shadow: 0 14px 40px rgba(244,63,94,.35);
}
@keyframes akis { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.hero h1 { margin: 0; font-weight: 800; font-size: 2.1rem; color: white; text-shadow: 0 2px 8px rgba(0,0,0,.2); }
.hero p { margin: .35rem 0 0; font-size: 1.05rem; }

.baslik { font-weight: 700; font-size: 1.05rem; margin: .4rem 0 .5rem;
  background: linear-gradient(90deg,#7c3aed,#db2777); -webkit-background-clip: text; color: transparent; }

.card { background: rgba(255,255,255,.85); backdrop-filter: blur(8px);
  border-radius: 18px; padding: 1.2rem 1.4rem; margin: .9rem 0;
  box-shadow: 0 8px 28px rgba(124,58,237,.12); animation: belir .5s ease both; }
.card h3 { margin-top: 0; color: #1e1b4b; }
.c1 { border-top: 6px solid #f43f5e; } .c2 { border-top: 6px solid #06b6d4; } .c3 { border-top: 6px solid #8b5cf6; }
@keyframes belir { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }

.badge { display:inline-block; padding:.45rem 1.1rem; border-radius:999px; font-weight:800; color:white;
  font-size: 1.1rem; box-shadow: 0 4px 14px rgba(0,0,0,.18); }
.chip { display:inline-block; padding:.25rem .7rem; margin:.2rem; border-radius:10px; font-size:.92rem; font-weight:600; }
.pos { background: linear-gradient(90deg,#bbf7d0,#a7f3d0); color:#065f46; }
.neg { background: linear-gradient(90deg,#fecdd3,#fbcfe8); color:#9f1239; }

.stButton>button { border-radius: 14px; font-weight: 700; border: none; color: white;
  background: linear-gradient(135deg,#6366f1,#a855f7); transition: all .2s;
  box-shadow: 0 4px 14px rgba(99,102,241,.3); }
.stButton>button:hover { transform: translateY(-3px) scale(1.02); color: white;
  box-shadow: 0 8px 22px rgba(168,85,247,.45); }
.stButton>button[kind="primary"] { background: linear-gradient(135deg,#f43f5e,#f97316,#eab308);
  font-size: 1.1rem; padding: .7rem; box-shadow: 0 6px 20px rgba(249,115,22,.4); }
.stTextArea textarea { border-radius: 14px; border: 2px solid #e9d5ff; }
.stTextArea textarea:focus { border-color: #a855f7; }
/* Yazı yazılan tüm alanlar (metin kutusu, API anahtarı, model kutusu) açık renkli */
.stTextArea textarea, .stTextInput input,
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"],
[data-baseweb="select"] > div {
  background-color: #fffaff !important; color: #1e1b4b !important;
  -webkit-text-fill-color: #1e1b4b !important; caret-color: #7c3aed;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {
  color: #a78bfa !important; -webkit-text-fill-color: #a78bfa !important;
}
[data-baseweb="input"] button, [data-baseweb="input"] svg { color: #7c3aed !important; fill: #7c3aed !important; }
.stTextArea label, .stTextArea label p { color: #4c1d95 !important; font-weight: 600; }
.stProgress > div > div > div > div { background: linear-gradient(90deg,#22c55e,#eab308,#f43f5e); }
/* Ana alandaki tüm yazılar siyah */
[data-testid="stMain"] p, [data-testid="stMain"] li, [data-testid="stMain"] label,
[data-testid="stMain"] span, [data-testid="stMain"] h3, [data-testid="stMain"] b,
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stStatusWidget"], [data-testid="stExpander"] * { color: #000000 !important; }
.stTextArea textarea, .stTextInput input, [data-baseweb="select"] * {
  color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
[data-testid="stMain"] .hero h1, [data-testid="stMain"] .hero p, [data-testid="stMain"] span.badge,
.stButton>button, [data-testid="stMain"] .stButton>button * { color: #ffffff !important; }
[data-testid="stMain"] span.pos { color: #065f46 !important; }
[data-testid="stMain"] span.neg { color: #9f1239 !important; }
/* Analiz sonuç kartları: tüm yazılar siyah ve tam opak */
[data-testid="stMain"] div.card, [data-testid="stMain"] div.card h3, [data-testid="stMain"] div.card p,
[data-testid="stMain"] div.card b, [data-testid="stMain"] div.card i {
  color: #000000 !important; opacity: 1 !important; }
[data-testid="stMain"] div.card span.badge { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# Kategori başına birden fazla örnek: her tıklamada rastgele biri gelir
ORNEKLER = {
    "😊 Pozitif": [
        "Bu restorana bayıldım! Yemekler harikaydı, garsonlar çok güler yüzlüydü. Kesinlikle tekrar geleceğim.",
        "Kursu bitirdim ve hayatım değişti. Eğitmen çok sabırlı, anlatımı muhteşemdi. Herkese tavsiye ederim!",
        "Kargo ertesi gün geldi, paketleme özenliydi. Satıcıya çok teşekkürler, beş yıldızı hak ediyor.",
    ],
    "😠 Negatif": [
        "Kargo bir hafta gecikti, ürün kırık geldi ve müşteri hizmetleri hiç yardımcı olmadı. Tam bir hayal kırıklığı.",
        "Film inanılmaz sıkıcıydı, yarısında uyuyakaldım. Paramıza ve zamanımıza yazık oldu.",
        "Otel odası kirliydi, klima çalışmıyordu ve resepsiyon görevlisi son derece kabaydı.",
    ],
    "🙃 İronik": [
        "Harika! Telefonum ilk günden bozuldu, tam da beklediğim kalite. Ama en azından kutusu çok şıktı.",
        "Ne güzel, iki saattir sırada bekliyorum. Hayatımın en verimli günü olabilir.",
        "Bravo belediyeye, yol çalışması tam bayram trafiğine denk getirilmiş. Muhteşem planlama!",
    ],
    "😐 Nötr": [
        "Toplantı yarın saat 14:00'te üçüncü kattaki salonda yapılacaktır.",
        "Ürün 250 gram ağırlığında olup mavi ve siyah renk seçenekleriyle satılmaktadır.",
        "Kütüphane hafta içi 09:00 ile 18:00 saatleri arasında açıktır.",
    ],
    "🤔 Karışık": [
        "Kameranın fotoğraf kalitesi mükemmel ama bataryası yarım günde bitiyor.",
        "Mekânın manzarası büyüleyiciydi, fakat yemekler soğuk ve fiyatlar çok yüksekti.",
        "Oyunun grafikleri nefes kesici ancak hikâyesi zayıf ve sürekli takılıyor.",
    ],
    "📱 Sosyal Medya": [
        "Konser efsaneydiii 🔥🔥 sesim gitti ama değdi 😍 #enİyiGece",
        "Yine mi zam?? 🤦‍♂️ maaş aynı fiyatlar uçuyor 😤",
        "Pazartesi sabahı + yağmur + metro arızası = harika bir başlangıç 🙂",
    ],
}
RENK = {"Pozitif": "linear-gradient(135deg,#22c55e,#10b981)", "Negatif": "linear-gradient(135deg,#f43f5e,#dc2626)",
        "Nötr": "linear-gradient(135deg,#64748b,#94a3b8)", "Karışık": "linear-gradient(135deg,#f59e0b,#f97316)"}

# Sidebar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.selectbox("Model Seçin", [MODEL], index=0, disabled=True)
    st.markdown("---")
    st.subheader("📘 Duygu Analizi Nedir?")
    st.info(
        "Duygu analizi, bir metindeki duygusal tonu (olumlu, olumsuz veya nötr) otomatik olarak "
        "belirleyen bir doğal dil işleme tekniğidir. Model; kelimeleri, bağlamı ve cümle yapısını "
        "inceleyerek yazarın tutumunu tahmin eder. Ürün yorumları, sosyal medya ve müşteri geri "
        "bildirimlerinin analizinde yaygın olarak kullanılır. İroni ve alay gibi durumlar ise bu "
        "alandaki en zor problemlerdendir."
    )

st.markdown('<div class="hero"><h1>🎭 Duygu Analizi Eğitim Modülü</h1>'
            '<p>Bir metin girin, yapay zekâ analiz etsin ve size nasıl çalıştığını öğretsin. ✨</p></div>',
            unsafe_allow_html=True)

if "metin" not in st.session_state:
    st.session_state.metin = ""

st.markdown('<div class="baslik">🧪 Hazır örneklerle deneyin (her tıklamada farklı örnek!)</div>',
            unsafe_allow_html=True)
kategoriler = list(ORNEKLER)
for satir in (kategoriler[:3], kategoriler[3:]):
    for col, kat in zip(st.columns(3), satir):
        if col.button(kat, use_container_width=True):
            secenekler = [m for m in ORNEKLER[kat] if m != st.session_state.metin]
            st.session_state.metin = random.choice(secenekler)

metin = st.text_area("Analiz edilecek metin", key="metin", height=140,
                     placeholder="Bir yorum, tweet veya cümle yazın...")

PROMPT = """Duygu analizi eğitmenisin. Metni analiz et, ironiye dikkat et. Kısa ve net ol. Türkçe yanıt ver.
Sadece JSON döndür:
{{"genel_duygu":"Pozitif|Negatif|Nötr|Karışık","guven_skoru":0-100,
"olumlu_ipuclari":["en fazla 4 kısa ifade"],"olumsuz_ipuclari":["en fazla 4 kısa ifade"],
"ipucu_aciklamasi":"tek cümle","egitmen_notu":"en fazla 2-3 cümle: neden bu sonuç ve analiz nasıl çalıştı"}}

Metin: \"\"\"{metin}\"\"\""""


def analiz_et(client, metin):
    """Groq üzerinden JSON modunda kısa ve hızlı yanıt alır."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT.format(metin=metin)}],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=500,
    )
    icerik = resp.choices[0].message.content or ""
    # Qwen modelleri yanıta <think> bloğu ekleyebilir; JSON'u temizle
    icerik = re.sub(r"<think>.*?</think>", "", icerik, flags=re.S)
    eslesme = re.search(r"\{.*\}", icerik, flags=re.S)
    return eslesme.group(0) if eslesme else icerik


if st.button("🚀 Analiz Et ve Öğret", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Lütfen sol menüden Groq API anahtarınızı girin.")
    elif not metin.strip():
        st.warning("Lütfen analiz edilecek bir metin girin.")
    else:
        try:
            with st.status("🔍 Metin inceleniyor...", expanded=True) as durum:
                st.write("✍️ Duygu yüklü kelimeler aranıyor...")
                client = Groq(api_key=api_key)
                st.write(f"🤖 {MODEL} bağlamı ve ironiyi değerlendiriyor...")
                yanit = analiz_et(client, metin)
                st.write("📚 Eğitmen notu hazırlanıyor...")
                s = json.loads(yanit)
                durum.update(label="✅ Analiz tamamlandı!", state="complete", expanded=False)

            duygu = s.get("genel_duygu", "Nötr")
            skor = int(s.get("guven_skoru", 0))
            K = "color:#000000 !important;opacity:1;"
            st.markdown(
                f'<div class="card c1" style="{K}"><h3 style="{K}">🎯 Genel Duygu</h3>'
                f'<span class="badge" style="background:{RENK.get(duygu, RENK["Nötr"])}">{duygu}</span>'
                f'&nbsp; <span style="{K}">Güven Skoru: <b style="{K}">%{skor}</b></span></div>',
                unsafe_allow_html=True)
            st.progress(min(max(skor, 0), 100) / 100)

            pos = "".join(f'<span class="chip pos">✅ {k}</span>' for k in s.get("olumlu_ipuclari", [])) or f'<i style="{K}">Yok</i>'
            neg = "".join(f'<span class="chip neg">❌ {k}</span>' for k in s.get("olumsuz_ipuclari", [])) or f'<i style="{K}">Yok</i>'
            st.markdown(
                f'<div class="card c2" style="{K}"><h3 style="{K}">🔑 Anahtar İpuçları</h3>'
                f'<p style="{K}"><b style="{K}">Olumlu duygu yaratanlar:</b><br>{pos}</p>'
                f'<p style="{K}"><b style="{K}">Olumsuz duygu yaratanlar:</b><br>{neg}</p>'
                f'<p style="{K}">{s.get("ipucu_aciklamasi", "")}</p></div>',
                unsafe_allow_html=True)

            st.markdown(
                f'<div class="card c3" style="{K}"><h3 style="{K}">👩‍🏫 Eğitmen Notu</h3>'
                f'<p style="{K}">{s.get("egitmen_notu", "")}</p></div>',
                unsafe_allow_html=True)
        except json.JSONDecodeError:
            st.error("Model yanıtı çözümlenemedi. Lütfen tekrar deneyin.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
