GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@500;600;700;800&family=Syne:wght@600;700;800&display=swap');

/* ============================================================
   VETTD DESIGN TOKENS — "Refined Dark"
   One surface system, hairline borders, restrained accent.
   ============================================================ */
:root{
  --bg-deep:#08080C;          /* page canvas */
  --bg-base:#0C0C14;          /* section base */
  --surface:#131320;          /* cards */
  --surface-2:#1A1A2B;        /* raised / hover */
  --surface-inset:#0A0A12;    /* inputs, wells */

  --border:rgba(255,255,255,.08);       /* hairline default */
  --border-strong:rgba(255,255,255,.14);/* hover / emphasis */

  --text-1:#ECECF3;   /* primary */
  --text-2:#9595AE;   /* secondary */
  --text-3:#63637E;   /* muted / labels */
  --text-4:#41415A;   /* faint */

  --accent:#7C6BF0;                       /* refined violet */
  --accent-2:#9C8DF7;
  --accent-soft:rgba(124,107,240,.12);
  --accent-line:rgba(124,107,240,.35);
  --cyan:#22D3EE;                          /* data accent, sparingly */

  --success:#34D399;
  --warning:#F5A623;
  --danger:#F0616D;

  --radius:14px;
  --radius-sm:10px;
  --radius-lg:20px;
  --ease:cubic-bezier(.16,1,.3,1);
  --dur:.22s;

  --num:"Inter"; /* tabular figures applied where numbers matter */
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background: var(--bg-deep); color: var(--text-1); }

/* display face for headings/wordmark helpers */
.disp { font-family:'Sora',sans-serif !important; letter-spacing:-.02em; }
.brandmark { font-family: 'Syne', sans-serif !important; letter-spacing: -0.01em !important; font-weight: 800 !important; }
/* tabular figures for all data/metrics */
.stat-value, .score-number, div[data-testid="stMetricValue"], .tnum { font-variant-numeric: tabular-nums; font-feature-settings:"tnum" 1; }

/* softer, rounded alerts */
[data-testid="stAlert"], .stAlert { border-radius: var(--radius) !important; border: 1px solid var(--border) !important; }
[data-testid="stSidebar"] { background: var(--bg-base) !important; border-right: 1px solid var(--border); }
[data-testid="stSidebar"] * { color: #C8C8D8 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: var(--surface-inset) !important; border: 1px solid var(--border) !important;
    color: var(--text-1) !important; border-radius: var(--radius-sm) !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div { background: var(--accent) !important; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-base); border-radius: 12px; padding: 4px; gap: 4px; border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--text-2); border-radius: 8px;
    font-size: 13px; font-weight: 500; padding: 8px 20px; border: none;
}
.stTabs [aria-selected="true"] { background: var(--surface-2) !important; color: var(--text-1) !important; }

/* primary action — solid, restrained; single subtle accent lift on hover */
.stButton > button {
    background: var(--accent);
    color: #fff !important; border: 1px solid transparent; border-radius: var(--radius-sm);
    font-weight: 600; font-size: 14px; padding: 0.6rem 1.5rem; width: 100%;
}
.stButton > button:hover { background: var(--accent-2); color: #fff !important; }

div[data-testid="stMetric"] {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.25rem;
}
div[data-testid="stMetricLabel"] { font-size: 11px !important; color: var(--text-3) !important; text-transform: uppercase; letter-spacing: 0.08em; }
div[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 700 !important; color: var(--text-1) !important; }

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
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    z-index: -1;
}

.glass-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem;
}

/* reserved for the wordmark + hero headline only */
.iridescent-text {
    background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 40%, #22D3EE 70%, #A78BFA 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 5s linear infinite;
}

@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

@media (prefers-reduced-motion: reduce){
  .iridescent-text{ animation:none; }
  *{ transition:none !important; }
}

.section-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-bottom: 1rem;
}

.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--text-3); }
.stat-value { color: var(--text-1); font-weight: 600; }

.progress-bar-bg { background: var(--surface-inset); border-radius: 999px; height: 6px; margin: 4px 0 10px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 999px; background: var(--accent); }

.logo-text {
    font-size: 22px; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #22D3EE);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.sidebar-section {
    font-size: 10px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--text-4) !important; margin: 1.2rem 0 0.5rem;
}

.badge { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; }
.badge-starter { background: var(--surface-2); color: var(--text-2); }
.badge-pro { background: rgba(96,165,250,.12); color: #60A5FA; }
.badge-enterprise { background: var(--accent-soft); color: var(--accent-2); }

.divider { border-top: 1px solid var(--border); margin: 1.5rem 0; }

.score-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2rem 1.5rem; text-align: center;
}
.score-number {
    font-size: 72px; font-weight: 700; line-height: 1; font-family:'Sora',sans-serif;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.brief-block {
    background: var(--surface-inset); border: 1px solid var(--border); border-left: 2px solid var(--accent);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0; padding: 1rem 1.25rem;
    font-size: 13px; color: var(--text-2); line-height: 1.8; margin-top: 0.5rem;
}

[data-testid="stDownloadButton"] button {
    background: var(--surface-2) !important; color: var(--accent-2) !important;
    border: 1px solid var(--border) !important; font-size: 13px !important; border-radius: var(--radius-sm) !important;
}
[data-testid="stDownloadButton"] button:hover { border-color: var(--border-strong) !important; }

.stTextInput input[disabled] {
    background: var(--surface-inset) !important; border: 1px solid var(--border) !important;
    color: var(--text-3) !important; font-size: 12px !important;
}

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: var(--surface-inset) !important; border: 1px solid var(--border) !important;
    color: var(--text-1) !important; border-radius: var(--radius-sm) !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft) !important;
}

/* ============ SLIDERS ============ */
div[data-baseweb="slider"] > div > div {
    background: var(--surface-inset) !important; height: 5px !important; border-radius: 999px !important;
}
div[data-baseweb="slider"] > div > div > div {
    background: var(--accent) !important; height: 5px !important; border-radius: 999px !important;
}
div[data-baseweb="slider"] div[role="slider"] {
    background: #fff !important;
    border: 3px solid var(--accent) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
    transition: box-shadow var(--dur) ease, transform var(--dur) ease !important;
}
div[data-baseweb="slider"] div[role="slider"]:hover {
    box-shadow: 0 0 0 5px var(--accent-soft), 0 2px 10px rgba(0,0,0,0.5) !important;
    transform: scale(1.1) !important;
}
div[data-baseweb="slider"] div[role="slider"] + div,
div[data-testid="stThumbValue"] {
    color: var(--accent-2) !important; font-weight: 600 !important; background: transparent !important;
    font-variant-numeric: tabular-nums;
}
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {
    color: var(--text-4) !important; font-size: 11px !important;
}

/* ============ NUMBER INPUT ============ */
.stNumberInput button {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-2) !important;
    transition: background var(--dur) ease, border-color var(--dur) ease, color var(--dur) ease !important;
}
.stNumberInput button:hover {
    background: var(--accent-soft) !important;
    border-color: var(--accent-line) !important;
    color: var(--accent-2) !important;
}
.stNumberInput > div > div { border-radius: var(--radius-sm) !important; }

/* selectbox focus / dropdown accents */
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
li[role="option"][aria-selected="true"], div[data-baseweb="menu"] li:hover {
    background: var(--accent-soft) !important;
}

/* ============ MOTION — calm, consistent ============ */
.stButton > button {
    transition: background var(--dur) var(--ease), transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 8px 24px var(--accent-soft) !important; }
.stButton > button:active { transform: translateY(0) !important; }

.stTabs [data-baseweb="tab"] { transition: background var(--dur) ease, color var(--dur) ease !important; }
.section-card, div[data-testid="stMetric"] { transition: border-color var(--dur) ease !important; }
.section-card:hover, div[data-testid="stMetric"]:hover { border-color: var(--border-strong) !important; }
.navlink { transition: color var(--dur) ease !important; }
.navlink:hover { color: var(--accent-2) !important; }
a { transition: color var(--dur) ease, opacity var(--dur) ease !important; }

/* visible focus ring for keyboard nav (accessibility) */
*:focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
button:focus-visible, a:focus-visible { outline: 2px solid var(--accent-2) !important; outline-offset: 2px !important; }
</style>
"""

# Reusable site footer — drop into any page with st.markdown(SITE_FOOTER, unsafe_allow_html=True)
SITE_FOOTER = """
<div style="font-family:'Inter',sans-serif;margin-top:5rem;border-top:1px solid var(--border);position:relative;
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
      <div style="font-size:12px;color:var(--text-4);margin-top:1.5rem;">Built in Mumbai. Made for brands everywhere.</div>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--text-3);margin-bottom:1rem;">Company</div>
      <a href="/About" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">About us</a>
      <a href="/Founder" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">Founder</a>
      <a href="/" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">Pricing</a>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--text-3);margin-bottom:1rem;">Product</div>
      <a href="/Analyse" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">Analyse a creator</a>
      <a href="/Compare" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">Compare creators</a>
      <a href="/#how" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">How it works</a>
    </div>
    <div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--text-3);margin-bottom:1rem;">Contact</div>
      <a href="/Contact" target="_self" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">Get in touch</a>
      <a href="mailto:jadepinto96@gmail.com" style="display:block;font-size:13px;color:var(--text-2);text-decoration:none;margin-bottom:.7rem;">jadepinto96@gmail.com</a>
    </div>
  </div>
  <div style="max-width:1120px;margin:2.5rem auto 0;padding-top:1.75rem;border-top:1px solid var(--border);
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
    <div style="display:flex;gap:1.75rem;">
      <a href="/Legal" target="_self" style="font-size:12px;color:var(--text-4);text-decoration:none;">Privacy Policy</a>
      <a href="/Legal" target="_self" style="font-size:12px;color:var(--text-4);text-decoration:none;">Terms &amp; Conditions</a>
      <a href="/Legal" target="_self" style="font-size:12px;color:var(--text-4);text-decoration:none;">Refund Policy</a>
    </div>
    <div style="font-size:12px;color:var(--text-4);">© 2026 Vettd<sup style="font-size:8px;">®</sup></div>
  </div>
</div>
"""
