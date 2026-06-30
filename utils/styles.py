GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] { background: #0B0B16; color: #E8E8F0; }

/* distinct logo wordmark */
.brandmark { font-family: 'Syne', sans-serif !important; letter-spacing: -0.01em !important; font-weight: 800 !important; }

/* softer, rounded alerts */
[data-testid="stAlert"], .stAlert { border-radius: 14px !important; border: 1px solid rgba(255,255,255,0.06) !important; }
[data-testid="stSidebar"] { background: #0A0A14 !important; border-right: 1px solid #1A1A2E; }
[data-testid="stSidebar"] * { color: #C8C8D8 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #12121E !important; border: 1px solid #2A2A3E !important;
    color: #E8E8F0 !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div { background: #7C3AED !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #0A0A14; border-radius: 12px; padding: 4px; gap: 4px; border: 1px solid #1A1A2E;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #8888A8; border-radius: 8px;
    font-size: 13px; font-weight: 500; padding: 8px 20px; border: none;
}
.stTabs [aria-selected="true"] { background: #1A1A2E !important; color: #A78BFA !important; }

.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #4F46E5);
    color: white !important; border: none; border-radius: 10px;
    font-weight: 600; font-size: 14px; padding: 0.6rem 1.5rem; width: 100%;
}
.stButton > button:hover { opacity: 0.85; color: white !important; }

div[data-testid="stMetric"] {
    background: #0D0D1A; border: 1px solid #1A1A2E; border-radius: 14px; padding: 1rem 1.25rem;
}
div[data-testid="stMetricLabel"] { font-size: 11px !important; color: #555570 !important; text-transform: uppercase; letter-spacing: 0.08em; }
div[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 700 !important; color: #E8E8F0 !important; }

.iris-border {
    border: 1px solid transparent;
    background-clip: padding-box;
    position: relative;
}
.iris-border::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: linear-gradient(135deg, #7C3AED, #06B6D4, #A78BFA, #4F46E5);
    z-index: -1;
}

.glass-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
}

.iridescent-text {
    background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 40%, #06B6D4 70%, #A78BFA 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
}

@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.section-card {
    background: #0D0D1A; border: 1px solid #1A1A2E; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
}

.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid #12121E; font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: #555570; }
.stat-value { color: #E8E8F0; font-weight: 600; }

.progress-bar-bg { background: #12121E; border-radius: 999px; height: 6px; margin: 4px 0 10px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #7C3AED, #06B6D4); }

.logo-text {
    font-size: 22px; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #06B6D4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.sidebar-section {
    font-size: 10px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #33334A !important; margin: 1.2rem 0 0.5rem;
}

.badge { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; }
.badge-starter { background: #12121E; color: #8888A8; }
.badge-pro { background: #12182E; color: #60A5FA; }
.badge-enterprise { background: #16122E; color: #A78BFA; }

.divider { border-top: 1px solid #1A1A2E; margin: 1.5rem 0; }

.score-card {
    background: #0D0D1A; border: 1px solid #1A1A2E; border-radius: 20px; padding: 2rem 1.5rem; text-align: center;
}
.score-number {
    font-size: 72px; font-weight: 700; line-height: 1;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.brief-block {
    background: #07070F; border: 1px solid #1A1A2E; border-left: 3px solid #7C3AED;
    border-radius: 0 12px 12px 0; padding: 1rem 1.25rem;
    font-size: 13px; color: #A0A0C0; line-height: 1.8; margin-top: 0.5rem;
}

[data-testid="stDownloadButton"] button {
    background: #12121E !important; color: #A78BFA !important;
    border: 1px solid #2A2A3E !important; font-size: 13px !important;
}

.stTextInput input[disabled] {
    background: #07070F !important; border: 1px solid #1A1A2E !important;
    color: #555570 !important; font-size: 12px !important;
}

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: #0D0D1A !important; border: 1px solid #1A1A2E !important;
    color: #E8E8F0 !important; border-radius: 10px !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #7C3AED !important; box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* ============ GRADIENT SLIDERS (kills the default red) ============ */
/* full track */
div[data-baseweb="slider"] > div > div {
    background: #16162A !important;
    height: 5px !important;
    border-radius: 999px !important;
}
/* filled portion of the track */
div[data-baseweb="slider"] > div > div > div {
    background: linear-gradient(90deg, #7C3AED, #4F46E5, #22D3EE) !important;
    height: 5px !important;
    border-radius: 999px !important;
}
/* the thumb */
div[data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(135deg, #A78BFA, #22D3EE) !important;
    border: 2px solid #050509 !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.3), 0 2px 8px rgba(0,0,0,0.5) !important;
    transition: box-shadow 0.25s ease, transform 0.2s ease !important;
}
div[data-baseweb="slider"] div[role="slider"]:hover {
    box-shadow: 0 0 0 5px rgba(124,58,237,0.4), 0 2px 12px rgba(124,58,237,0.5) !important;
    transform: scale(1.12) !important;
}
/* live value bubble above the thumb */
div[data-baseweb="slider"] div[role="slider"] + div,
div[data-testid="stThumbValue"] {
    color: #A78BFA !important;
    font-weight: 600 !important;
    background: transparent !important;
}
/* min/max tick labels */
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {
    color: #3A3A52 !important; font-size: 11px !important;
}

/* ============ NUMBER INPUT — gradient step buttons, no red ============ */
.stNumberInput button {
    background: #12121E !important;
    border: 1px solid #1E1E32 !important;
    color: #A78BFA !important;
    transition: background 0.25s ease, border-color 0.25s ease !important;
}
.stNumberInput button:hover {
    background: linear-gradient(135deg, #7C3AED, #4F46E5) !important;
    border-color: #7C3AED !important;
    color: #FFFFFF !important;
}
.stNumberInput > div > div { border-radius: 10px !important; }

/* selectbox focus / dropdown accents */
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}
li[role="option"][aria-selected="true"], div[data-baseweb="menu"] li:hover {
    background: rgba(124,58,237,0.15) !important;
}

/* ============ FLUIDITY — smooth global motion ============ */
.stButton > button {
    transition: transform 0.3s cubic-bezier(.16,1,.3,1), box-shadow 0.3s cubic-bezier(.16,1,.3,1), opacity 0.3s ease !important;
    box-shadow: 0 0 24px rgba(124,58,237,0.18) !important;
}
.stButton > button:hover {
    opacity: 1 !important;
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 0 40px rgba(124,58,237,0.45) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

.stTabs [data-baseweb="tab"] { transition: background 0.3s ease, color 0.3s ease !important; }
.section-card, div[data-testid="stMetric"] { transition: border-color 0.4s ease, transform 0.4s cubic-bezier(.16,1,.3,1) !important; }
.navlink { transition: color 0.3s ease !important; }
.navlink:hover { color: #A78BFA !important; }
a { transition: color 0.3s ease, opacity 0.3s ease !important; }

/* gradient focus ring on any focused input */
*:focus-visible { outline: none !important; }
</style>
"""

# Reusable site footer — drop into any page with st.markdown(SITE_FOOTER, unsafe_allow_html=True)
SITE_FOOTER = """
<div style="font-family:'Inter',sans-serif;margin-top:5rem;border-top:1px solid #1A1A2E;position:relative;
  background:linear-gradient(180deg,transparent,rgba(124,58,237,.03));padding:4rem 3.5rem 2.5rem;">
  <div style="position:absolute;top:-1px;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,.5),rgba(34,211,238,.4),transparent);"></div>
  <div style="max-width:1120px;margin:0 auto;display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:2.5rem;">
    <div>
      <div class="brandmark" style="font-size:24px;background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1rem;">✦ VETTD</div>
      <div style="font-size:22px;font-weight:600;color:#EDEDF5;line-height:1.3;letter-spacing:-.02em;">
        Creator intelligence.<br>Simplified.</div>
      <a href="/Analyse" target="_self" style="display:inline-flex;align-items:center;gap:8px;margin-top:1.5rem;
        background:linear-gradient(135deg,#7C3AED,#4F46E5);color:#fff;font-size:13px;font-weight:600;
        padding:10px 20px;border-radius:999px;text-decoration:none;border:1px solid rgba(124,58,237,.5);">Launch app →</a>
      <div style="font-size:12px;color:#3A3A52;margin-top:1.5rem;">Built in Mumbai. Made for brands everywhere.</div>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Company</div>
      <a href="/About" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">About us</a>
      <a href="/Founder" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">Founder</a>
      <a href="/" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">Pricing</a>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Product</div>
      <a href="/Analyse" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">Analyse a creator</a>
      <a href="/Compare" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">Compare creators</a>
      <a href="/#how" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">How it works</a>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Contact</div>
      <a href="/Contact" target="_self" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">Get in touch</a>
      <a href="mailto:jadepinto96@gmail.com" style="display:block;font-size:13px;color:#8888A8;text-decoration:none;margin-bottom:.7rem;">jadepinto96@gmail.com</a>
    </div>
  </div>
  <div style="max-width:1120px;margin:2.5rem auto 0;padding-top:1.75rem;border-top:1px solid #14142A;
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
    <div style="display:flex;gap:1.75rem;">
      <a href="/Legal" target="_self" style="font-size:12px;color:#4A4A66;text-decoration:none;">Privacy Policy</a>
      <a href="/Legal" target="_self" style="font-size:12px;color:#4A4A66;text-decoration:none;">Terms &amp; Conditions</a>
      <a href="/Legal" target="_self" style="font-size:12px;color:#4A4A66;text-decoration:none;">Refund Policy</a>
    </div>
    <div style="font-size:12px;color:#4A4A66;">© 2026 Vettd<sup style="font-size:8px;">®</sup></div>
  </div>
</div>
"""
