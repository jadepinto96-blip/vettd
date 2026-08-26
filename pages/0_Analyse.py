import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS, SITE_FOOTER
from utils.data_provider import fetch_creator, active_provider
from utils.scoring import (
    calculate_engagement_rate, estimate_fake_follower_score,
    calculate_brand_fit_score, calculate_audience_quality_score,
    calculate_growth_score, calculate_consistency_score,
    calculate_vettd_score, score_label,
)

st.set_page_config(page_title="Vettd — Analyse a Creator", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
header { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 1.5rem 1rem 0 !important; max-width: 880px !important; margin: 0 auto !important; }

/* ── tier selector: active = gradient, inactive = outline ── */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED, #4F46E5) !important;
    color: #fff !important; border: 1px solid rgba(124,58,237,.6) !important;
    border-radius: 12px !important; font-weight: 700 !important;
    box-shadow: 0 0 28px rgba(124,58,237,.45) !important;
    transform: translateY(-2px) !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
}
.stButton button[kind="secondary"] {
    background: var(--surface) !important; color: var(--text-2) !important;
    border: 1px solid var(--border) !important; border-radius: 12px !important;
    font-weight: 600 !important; box-shadow: none !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: rgba(124,58,237,.5) !important; color: #C8C8E0 !important;
    background: #14141F !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,.15) !important;
}

.input-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.input-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), transparent);
}
.input-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-4);
    margin-bottom: 1rem;
}
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-1) !important;
}
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-1) !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}
.stNumberInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-1) !important;
}
.stSlider [data-baseweb="slider"] { padding: 0.5rem 0; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
    color: var(--text-3) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:1.25rem 3rem;border-bottom:1px solid var(--surface);
    background:rgba(11,11,22,0.95);backdrop-filter:blur(20px);">
  <a href="/" target="_self" style="font-size:20px;font-weight:800;letter-spacing:-0.5px;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;gap:2rem;align-items:center;">
    <a href="/Compare" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Compare creators</a>
    <a href="/About" target="_self" style="font-size:13px;color:var(--text-3);text-decoration:none;">About</a>
    <a href="/Founder" target="_self" style="font-size:13px;color:var(--text-3);text-decoration:none;">Founder</a>
    <a href="/Contact" target="_self" style="font-size:13px;color:var(--text-3);text-decoration:none;">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div style="text-align:center;padding:4rem 2rem 2.5rem;">
  <div style="display:inline-flex;align-items:center;gap:8px;
      background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);
      border-radius:999px;padding:6px 18px;margin-bottom:1.5rem;">
    <div style="width:6px;height:6px;border-radius:50%;background:#A78BFA;
        box-shadow:0 0 6px #A78BFA;"></div>
    <span style="font-size:12px;font-weight:600;letter-spacing:0.12em;color:#A78BFA;text-transform:uppercase;">
      Creator analysis
    </span>
  </div>
  <h1 style="font-size:52px;font-weight:900;letter-spacing:-2.5px;line-height:1.05;margin:0 0 1rem;">
    <span style="background:linear-gradient(135deg,#FFFFFF,#E8E8F0);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">Vet any creator.</span><br>
    <span class="brandmark" style="background:linear-gradient(135deg,#A78BFA,#60A5FA,#22D3EE);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      Vettd in seconds.
    </span>
  </h1>
  <p style="font-size:16px;color:var(--text-3);max-width:440px;margin:0 auto;line-height:1.7;">
    Enter the creator's details below and click Run Analysis to get their full Vettd report.
  </p>
</div>
""", unsafe_allow_html=True)

# ── PLAN SELECTOR ──
col_center = st.container()

with col_center:
    tier_cols = st.columns(3)
    tiers = ["Starter", "Pro", "Enterprise"]
    tier_colors = {"Starter": "var(--text-3)", "Pro": "#A78BFA", "Enterprise": "#06B6D4"}

    if "selected_tier" not in st.session_state:
        st.session_state.selected_tier = "Pro"

    for i, t in enumerate(tiers):
        with tier_cols[i]:
            active = st.session_state.selected_tier == t
            if st.button(t, key=f"tier_{t}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.selected_tier = t
                st.rerun()

    tier = st.session_state.selected_tier
    st.markdown(f"""
    <div style="text-align:center;margin-top:-0.25rem;margin-bottom:0.5rem;
        font-size:12px;color:var(--text-3);">
      <span style="color:#A78BFA;font-weight:600;">{tier}</span> plan selected —
      {'core analytics' if tier=='Starter' else 'full demographics + brand fit' if tier=='Pro' else 'predictive intelligence + market fit'}
    </div>
    """, unsafe_allow_html=True)
    TIERS = {"Starter": 1, "Pro": 2, "Enterprise": 3}

    def tier_gate(required):
        return TIERS[tier] >= TIERS[required]

    # ── SAVED SEARCHES (this session) ──
    _hist = st.session_state.get("history", [])
    if _hist:
        with st.expander(f"⭑  Saved searches  ·  {len(_hist)}", expanded=False):
            for i, h in enumerate(_hist):
                hc1, hc2 = st.columns([4, 1])
                with hc1:
                    st.markdown(
                        f'<div style="padding:6px 0;">'
                        f'<span style="font-weight:600;color:var(--text-1);">{h["name"]}</span> '
                        f'<span style="color:var(--text-3);font-size:12px;">{h["username"]} · {h["niche"]}</span> '
                        f'<span style="float:right;font-weight:700;color:#A78BFA;">{h["score"]}'
                        f'<span style="font-size:11px;color:var(--text-3);font-weight:400;"> · {h["label"]}</span></span></div>',
                        unsafe_allow_html=True)
                with hc2:
                    if st.button("View", key=f"hist_{i}", use_container_width=True):
                        st.session_state.vettd_data = dict(h["data"])
                        st.switch_page("pages/4_Dashboard.py")
            if st.button("Clear history", key="clear_hist"):
                st.session_state.history = []
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # premium card styling for the input sections — uses global design tokens
    st.markdown("""<style>
    [data-testid="stVerticalBlockBorderWrapper"]{
      background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:var(--radius) !important;
      padding:1.5rem 1.75rem !important; margin-bottom:1rem !important;
      transition:border-color var(--dur) ease !important;}
    [data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:var(--border-strong) !important;}
    .input-label{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-3);display:flex;align-items:center;gap:9px;margin-bottom:.6rem;}
    .input-label::before{content:"";width:16px;height:2px;border-radius:2px;background:var(--accent);}
    /* inputs sit inset on the card */
    [data-testid="stVerticalBlockBorderWrapper"] .stTextInput input,
    [data-testid="stVerticalBlockBorderWrapper"] .stNumberInput input,
    [data-testid="stVerticalBlockBorderWrapper"] div[data-baseweb="select"]>div{
      background:var(--surface-inset) !important; border-color:var(--border) !important;}
    /* remove the +/- steppers on count fields — pointless on large numbers, and cleaner */
    [data-testid="stVerticalBlockBorderWrapper"] .stNumberInput button{ display:none !important; }
    [data-testid="stVerticalBlockBorderWrapper"] .stNumberInput input{
      border-top-right-radius:var(--radius-sm) !important; border-bottom-right-radius:var(--radius-sm) !important;
      text-align:left !important; font-variant-numeric:tabular-nums; }
    /* live engagement-rate readout chip */
    .er-chip{display:inline-flex;align-items:center;gap:10px;background:var(--surface-inset);
      border:1px solid var(--border);border-radius:999px;padding:7px 16px 7px 12px;font-size:13px;}
    .er-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
    .er-val{font-weight:700;font-variant-numeric:tabular-nums;}
    .er-lbl{color:var(--text-3);}
    </style>""", unsafe_allow_html=True)

    if "reels_n" not in st.session_state:
        st.session_state["reels_n"] = 10
    _provider = active_provider()

    # ── CREATOR DETAILS ──
    with st.container(border=True):
        st.markdown('<div class="input-label">Creator details</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            creator_name = st.text_input("Creator name (optional)", placeholder="Emma Williams")
        with c2:
            username = st.text_input("Username", placeholder="@emmalifestyle")
        c3, c4, c5 = st.columns(3)
        with c3:
            platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
        with c4:
            _niches = ["Fashion", "Fitness", "Beauty", "Tech", "Food", "Travel", "Gaming", "Lifestyle", "Finance", "Parenting", "Other"]
            _guess = (st.session_state.get("fetched") or {}).get("niche_guess")
            niche = st.selectbox("Niche", _niches, index=_niches.index(_guess) if _guess in _niches else 0)
        with c5:
            brand_industry = st.text_input("Your brand industry", placeholder="e.g. Fashion")
        brand_name = st.text_input("Your brand name (used in the report)", placeholder="e.g. Malabar Gold & Diamonds")

    # ── LIVE FETCH ──
    reels_n = st.session_state.get("reels_n", 10)
    with st.container(border=True):
        fc1, fc2 = st.columns([1, 2])
        with fc1:
            if _provider == "manual":
                st.button("⚡ Fetch live data", use_container_width=True, disabled=True, type="primary",
                          help="Add a MODASH_API_KEY or RAPIDAPI_KEY in Streamlit secrets to enable live fetch.")
            else:
                if st.button("⚡ Fetch live data", use_container_width=True, type="primary"):
                    with st.spinner(f"Fetching @{username.lstrip('@')} (last {reels_n} reels)…"):
                        prof = fetch_creator(username, platform, reels_n)
                    if prof:
                        st.session_state.fetched = prof
                        st.rerun()
                    else:
                        st.session_state.fetched = None
                        st.warning("Couldn't fetch that profile — fill in the details manually.")
        with fc2:
            if _provider == "manual":
                st.caption("Live fetch off — running on manual input. Add an API key in secrets to auto-fill.")
            else:
                f = st.session_state.get("fetched")
                if f:
                    tag = "full data" if not f.get("_partial") else "basic stats only"
                    st.caption(f"✓ Auto-filled from {f['_source']} ({tag}). Edit any field below.")
                else:
                    st.caption(f"Live fetch ready ({_provider}). Enter a username and click fetch.")

    # helper: prefer fetched value, else fall back to default
    _f = st.session_state.get("fetched") or {}
    def pref(key, default):
        v = _f.get(key)
        return v if v is not None else default

    # ── MANUAL / FETCHED INPUTS ──
    # Fetch-first: once live data is in, tuck the fields away (review mode);
    # open them by default when there's nothing to review or fetch is off.
    _has_fetch = bool(st.session_state.get("fetched"))
    if _provider == "manual":
        _manual_label = "Enter the creator's numbers"
    elif _has_fetch:
        _manual_label = "Adjust the numbers manually"
    else:
        _manual_label = "Or enter the numbers manually"
    _manual_expanded = (_provider == "manual") or (not _has_fetch)

    with st.expander(_manual_label, expanded=_manual_expanded):
        # ── PROFILE STATS ──
        with st.container(border=True):
            st.markdown('<div class="input-label">Profile stats</div>', unsafe_allow_html=True)
            p1, p2, p3, p4, p5 = st.columns(5)
            with p1:
                followers = st.number_input("Followers", min_value=0, value=int(pref("followers", 150000)), step=1000)
            with p2:
                following = st.number_input("Following", min_value=0, value=int(pref("following", 800)), step=10)
            with p3:
                post_count = st.number_input("Total posts", min_value=0, value=int(pref("post_count", 420)))
            with p4:
                posting_freq = st.number_input("Posts per week", min_value=0.0, value=float(pref("posting_freq", 4.0)), step=0.5)
            with p5:
                growth_rate_30d = st.number_input("Growth rate 30d %", min_value=-10.0, value=float(pref("growth_rate_30d", 2.5)), step=0.1)

        # ── REEL ENGAGEMENT (reels-to-average lives here now) ──
        with st.container(border=True):
            st.markdown('<div class="input-label">Reel engagement</div>', unsafe_allow_html=True)
            e1, e2, e3, e4 = st.columns(4)
            with e1:
                avg_likes = st.number_input("Avg likes / reel", min_value=0, value=int(pref("avg_likes", 8500)), step=100)
            with e2:
                avg_comments = st.number_input("Avg comments / reel", min_value=0, value=int(pref("avg_comments", 320)), step=10)
            with e3:
                avg_saves = st.number_input("Avg saves / reel", min_value=0, value=int(pref("avg_saves", 1200)), step=50)
            with e4:
                avg_shares = st.number_input("Avg shares / reel", min_value=0, value=int(pref("avg_shares", 450)), step=10)
            rr1, rr2 = st.columns([1, 3])
            with rr1:
                reels_n = st.selectbox("Average metrics over", [5, 10, 15, 20], key="reels_n",
                                       format_func=lambda n: f"Last {n} reels")

        # ── AUDIENCE (Pro+) ──
        if tier_gate("Pro"):
            with st.container(border=True):
                st.markdown('<div class="input-label">Audience demographics — Pro</div>', unsafe_allow_html=True)
                a1, a2, a3 = st.columns(3)
                with a1:
                    female_pct = st.slider("Female audience %", 0, 100, int(pref("female_pct", 65)))
                    male_pct = 100 - female_pct
                    st.caption(f"Male {male_pct}% · Female {female_pct}%")
                with a2:
                    audience_authenticity = st.slider("Audience authenticity %", 0, 100, int(pref("audience_authenticity", 82)))
                with a3:
                    age_18_24 = st.slider("Age 18–24 %", 0, 100, int(pref("age_18_24", 28)))
                    age_25_34 = st.slider("Age 25–34 %", 0, 100, int(pref("age_25_34", 35)))
                    age_35_44 = st.slider("Age 35–44 %", 0, 100, int(pref("age_35_44", 20)))
                l1, l2, l3 = st.columns(3)
                with l1:
                    loc1_name = st.text_input("Top location 1", value=pref("loc1_name", "United Kingdom"))
                    loc1_pct = st.slider("Location 1 %", 0, 100, int(pref("loc1_pct", 42)))
                with l2:
                    loc2_name = st.text_input("Top location 2", value=pref("loc2_name", "United States"))
                    loc2_pct = st.slider("Location 2 %", 0, 100, int(pref("loc2_pct", 28)))
                with l3:
                    loc3_name = st.text_input("Top location 3", value=pref("loc3_name", "Australia"))
                    loc3_pct = st.slider("Location 3 %", 0, 100, int(pref("loc3_pct", 12)))
        else:
            female_pct, male_pct = 60, 40
            audience_authenticity = 75
            age_18_24, age_25_34, age_35_44 = 30, 35, 20
            loc1_name, loc1_pct = "United Kingdom", 42
            loc2_name, loc2_pct = "United States", 28
            loc3_name, loc3_pct = "Australia", 12

    # ── LIVE ENGAGEMENT RATE (always visible — the headline signal) ──
    _er = calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves, _f.get("avg_views"))
    if _er >= 6:      _erc, _erl = "#34D399", "Excellent for this size"
    elif _er >= 3:    _erc, _erl = "#22D3EE", "Strong"
    elif _er >= 1.5:  _erc, _erl = "#F5A623", "Average"
    else:             _erc, _erl = "#F0616D", "Low — reach may not convert"
    st.markdown(
        f'<div style="margin:.25rem 0 1rem;">'
        f'<div class="er-chip"><span class="er-dot" style="background:{_erc};"></span>'
        f'<span class="er-lbl">Engagement rate</span>'
        f'<span class="er-val" style="color:{_erc};">{_er}%</span>'
        f'<span class="er-lbl">· {_erl}</span></div></div>',
        unsafe_allow_html=True)

    # ── ENTERPRISE MODULES ──
    if tier_gate("Enterprise"):
        st.markdown("""
        <style>
        .ent-section-header{
            display:flex;align-items:center;gap:10px;margin-bottom:1.25rem;
        }
        .ent-section-header span{
            font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#A9A9D0;
        }
        .ent-section-header::before{
            content:"";width:22px;height:3px;border-radius:3px;
            background:linear-gradient(90deg,#7C3AED,#22D3EE);flex-shrink:0;
        }
        .mod-card{
            background:var(--surface);
            border:1px solid var(--border);border-radius:var(--radius);
            padding:1.25rem 1.4rem 1.1rem;margin-bottom:.75rem;
            position:relative;overflow:hidden;transition:border-color var(--dur) ease;
        }
        .mod-card-active{ border-color:var(--accent-line) !important; }
        .mod-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.5rem;}
        .mod-icon{
            width:36px;height:36px;border-radius:10px;display:flex;align-items:center;
            justify-content:center;flex-shrink:0;
        }
        .mod-icon svg{width:19px;height:19px;}
        .mod-title{font-size:15px;font-weight:700;color:var(--text-1);letter-spacing:-.3px;}
        .mod-subtitle{font-size:12px;color:var(--text-3);margin-top:1px;}
        .mod-outputs{
            display:flex;flex-wrap:wrap;gap:6px;margin-top:.85rem;
        }
        .mod-output-tag{
            background:var(--surface-2);border:1px solid var(--border);
            color:var(--text-2);font-size:11px;font-weight:600;letter-spacing:.04em;
            border-radius:6px;padding:3px 10px;
        }
        .mod-divider{
            height:1px;background:var(--border);
            margin:.85rem 0 .9rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ent-section-header"><span>Enterprise intelligence suite — choose what to run</span></div>',
                    unsafe_allow_html=True)

        # Lucide outline icons (stroke = currentColor)
        _ICON = {
            "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
            "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
            "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
            "bars": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>',
            "activity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
        }
        MODULE_META = {
            "Forecast": {
                "icon": _ICON["zap"], "icon_bg": "rgba(245,166,35,.12)", "icon_color": "#F5A623",
                "title": "Forecast", "subtitle": "Predictive Campaign ROI",
                "description": "Models projected reach and impressions, computes Earned Media Value, estimated conversions and a full ROI range — then runs a 3-tier budget scenario so you can size the spend.",
                "outputs": ["Projected reach & impressions", "Earned Media Value (₹)", "Est. conversions", "ROI range", "Budget scenario table"],
            },
            "Shield": {
                "icon": _ICON["shield"], "icon_bg": "rgba(240,97,109,.12)", "icon_color": "#F0616D",
                "title": "Shield", "subtitle": "Brand Safety & Risk Audit",
                "description": "Runs fake-follower forensics, scans for red flags against your brand rules, scores crisis risk and returns a clear Go / Conditional / No-Go verdict your legal & comms teams can sign off on.",
                "outputs": ["Risk tier", "Fake-follower forensics", "Red-flag scan", "Crisis-risk score", "Go / Conditional / No-Go"],
            },
            "Audience": {
                "icon": _ICON["users"], "icon_bg": "rgba(34,211,238,.12)", "icon_color": "#22D3EE",
                "title": "Audience DNA", "subtitle": "Credibility & True-Match",
                "description": "Splits the audience into real vs suspicious, scores true-match to your exact target persona, maps geo concentration and interest affinities, and detects overlap with your existing roster (wasted reach).",
                "outputs": ["Audience Quality Score", "Real vs suspicious %", "True-match to target %", "Geo & interests", "Roster-overlap detector"],
            },
            "Benchmark": {
                "icon": _ICON["bars"], "icon_bg": "rgba(96,165,250,.12)", "icon_color": "#60A5FA",
                "title": "Benchmark", "subtitle": "Competitive & Category Positioning",
                "description": "Ranks this creator against category peers by percentile, measures cost-efficiency vs the category average, gauges brand saturation vs exclusivity, and surfaces 3 vetted lookalike alternatives.",
                "outputs": ["Category percentile rank", "Cost-efficiency vs peers", "Saturation / exclusivity", "3 vetted lookalikes"],
            },
            "Pulse": {
                "icon": _ICON["activity"], "icon_bg": "rgba(52,211,153,.12)", "icon_color": "#34D399",
                "title": "Pulse", "subtitle": "Comment Sentiment & Community Health",
                "description": "Reads comment tone into a positive / neutral / negative split, scores community health from real engagement depth (not just volume), flags toxicity and surfaces the dominant conversation themes.",
                "outputs": ["Sentiment split %", "Community health tier", "Toxicity flag", "Top comment themes"],
            },
        }

        if "active_modules" not in st.session_state:
            st.session_state.active_modules = {m: True for m in MODULE_META}
        # migrate any old module keys from a previous session
        for _m in list(st.session_state.active_modules.keys()):
            if _m not in MODULE_META:
                del st.session_state.active_modules[_m]
        for _m in MODULE_META:
            st.session_state.active_modules.setdefault(_m, True)

        modules = []
        # defaults for every enterprise input
        campaign_budget = 50000
        campaign_goal = "Awareness"
        brand_sensitivity = "Medium — mainstream brands"
        regulated_industry = False
        prohibited_keywords = ""
        target_age = "All ages"
        target_gender = "Any"
        target_geo = ""
        product_text = ""
        competitor_handles = ""
        sentiment_score = 75
        sentiment_keywords = ""

        for mod_key, meta in MODULE_META.items():
            is_on = st.session_state.active_modules.get(mod_key, True)
            card_class = "mod-card mod-card-active" if is_on else "mod-card"

            st.markdown(f"""
            <div class="{card_class}">
              <div class="mod-header">
                <div style="display:flex;align-items:center;gap:12px;">
                  <div class="mod-icon" style="background:{meta['icon_bg']};">
                    <span style="color:{meta['icon_color']};">{meta['icon']}</span>
                  </div>
                  <div>
                    <div class="mod-title">{meta['title']}</div>
                    <div class="mod-subtitle">{meta['subtitle']}</div>
                  </div>
                </div>
              </div>
              <div style="font-size:13px;color:#5A5A90;line-height:1.6;margin-top:.3rem;">{meta['description']}</div>
              <div class="mod-outputs">{''.join(f'<span class="mod-output-tag">{o}</span>' for o in meta['outputs'])}</div>
            </div>
            """, unsafe_allow_html=True)

            toggle_col, _ = st.columns([1, 4])
            with toggle_col:
                toggled = st.toggle(f"Run {meta['title']}", value=is_on, key=f"mod_toggle_{mod_key}",
                                    label_visibility="collapsed")
                st.session_state.active_modules[mod_key] = toggled
                if toggled:
                    st.markdown(f'<div style="font-size:11px;font-weight:600;color:#7C3AED;margin-top:-8px;margin-bottom:4px;">● ON</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-size:11px;font-weight:500;color:#3A3A5A;margin-top:-8px;margin-bottom:4px;">○ OFF</div>', unsafe_allow_html=True)

            if toggled:
                modules.append(mod_key)
                st.markdown('<div class="mod-divider"></div>', unsafe_allow_html=True)

                if mod_key == "Forecast":
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        campaign_budget = st.number_input(
                            "Campaign budget (₹)", min_value=5000, max_value=50000000,
                            value=50000, step=5000, key="ent_budget",
                            help="Total budget for this creator — drives the deliverable count and ROI scenarios")
                    with pc2:
                        campaign_goal = st.selectbox(
                            "Campaign objective",
                            ["Awareness", "Engagement", "Conversions", "App installs", "Product launch"],
                            key="ent_goal",
                            help="Shapes the click-through and conversion assumptions in the forecast")

                elif mod_key == "Shield":
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        brand_sensitivity = st.selectbox(
                            "Brand sensitivity",
                            ["Low — experimental brands", "Medium — mainstream brands", "High — regulated / conservative brands"],
                            index=1, key="ent_sensitivity",
                            help="How risk-averse your brand is — scales the crisis-risk score")
                    with sc2:
                        regulated_industry = st.checkbox(
                            "Regulated industry (finance, health, alcohol, kids)",
                            value=False, key="ent_regulated",
                            help="Adds a compliance-review flag to the audit")
                    prohibited_keywords = st.text_input(
                        "Prohibited topics / keywords to flag (optional)",
                        placeholder="e.g. gambling, crypto, political, competitor names",
                        key="ent_prohibited",
                        help="Comma-separated. Each becomes a manual-review flag in the Shield report.")

                elif mod_key == "Audience":
                    ac1, ac2, ac3 = st.columns(3)
                    with ac1:
                        target_age = st.selectbox(
                            "Target age group",
                            ["13–17", "18–24", "25–34", "35–44", "45+", "All ages"],
                            index=5, key="ent_target_age")
                    with ac2:
                        target_gender = st.selectbox(
                            "Target gender", ["Any", "Female", "Male"], key="ent_target_gender")
                    with ac3:
                        target_geo = st.text_input(
                            "Target market (optional)", placeholder="e.g. India, Mumbai",
                            key="ent_target_geo")
                    st.caption("Roster overlap is detected automatically against your saved searches this session.")

                elif mod_key == "Benchmark":
                    product_text = st.text_input(
                        "Product / category you're promoting",
                        placeholder="e.g. vitamin C serum, running shoes, fintech app",
                        key="ent_product",
                        help="Sharpens the lookalike recommendations and cost-efficiency read")
                    competitor_handles = st.text_input(
                        "Competitor brands or creators to compare (optional)",
                        placeholder="e.g. @competitorbrand, @rivalcreator",
                        key="ent_competitors",
                        help="Comma-separated. Used to frame competitive positioning.")

                elif mod_key == "Pulse":
                    sentiment_score = st.slider(
                        "Observed comment sentiment (0–100)", 0, 100, 75, key="ent_sentiment",
                        help="Your read on comment tone — the report blends this with real engagement depth")
                    sentiment_keywords = st.text_input(
                        "Keywords / themes to flag in comments (optional)",
                        placeholder="e.g. scam, fake, overpriced, love this, obsessed",
                        key="ent_sentiment_kw",
                        help="Comma-separated. Surfaced as recurring themes in the Pulse report.")

            st.markdown("<div style='margin-bottom:.5rem;'></div>", unsafe_allow_html=True)
    else:
        modules = []
        campaign_budget = 50000
        campaign_goal = "Awareness"
        brand_sensitivity = "Medium — mainstream brands"
        regulated_industry = False
        prohibited_keywords = ""
        target_age = "All ages"
        target_gender = "Any"
        target_geo = ""
        product_text = ""
        competitor_handles = ""
        sentiment_score = 75
        sentiment_keywords = ""

    # ── RUN BUTTON ──
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("✦ Run Analysis", use_container_width=True, type="primary")

    if run:
        if not creator_name and not username:
            st.error("Please enter at least a username or a name.")
        else:
            _fetched = st.session_state.get("fetched") or {}
            # name is optional — use fetched full name, else username (many IG profiles have no display name)
            if not creator_name:
                creator_name = _fetched.get("full_name") or username.lstrip("@") or "Creator"
            _user_display = ("@" + username.lstrip("@")) if username else ""
            st.session_state.vettd_data = {
                "tier": tier,
                "creator_name": creator_name,
                "username": _user_display,
                "platform": platform,
                "niche": niche,
                "brand_industry": brand_industry,
                "brand_name": brand_name,
                "followers": followers,
                "following": following,
                "post_count": post_count,
                "posting_freq": posting_freq,
                "growth_rate_30d": growth_rate_30d,
                "avg_likes": avg_likes,
                "avg_comments": avg_comments,
                "avg_saves": avg_saves,
                "avg_shares": avg_shares,
                "female_pct": female_pct,
                "male_pct": male_pct,
                "audience_authenticity": audience_authenticity,
                "age_18_24": age_18_24,
                "age_25_34": age_25_34,
                "age_35_44": age_35_44,
                "age_45_plus": max(0, 100 - age_18_24 - age_25_34 - age_35_44),
                "loc1_name": loc1_name, "loc1_pct": loc1_pct,
                "loc2_name": loc2_name, "loc2_pct": loc2_pct,
                "loc3_name": loc3_name, "loc3_pct": loc3_pct,
                # ── enterprise module inputs ──
                "campaign_budget": campaign_budget,
                "campaign_goal": campaign_goal,
                "brand_sensitivity": brand_sensitivity,
                "regulated_industry": regulated_industry,
                "prohibited_keywords": prohibited_keywords,
                "target_age": target_age,
                "target_gender": target_gender,
                "target_geo": target_geo,
                "product_text": product_text,
                "competitor_handles": competitor_handles,
                "sentiment_score": sentiment_score,
                "sentiment_keywords": sentiment_keywords,
                "profile_pic": _fetched.get("profile_pic"),
                "avg_views": _fetched.get("avg_views"),
                "reels_n": _fetched.get("reels_n"),
                "modules": modules,
            }
            # ── save to search history (most recent first, dedup by username) ──
            _er = calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves, _fetched.get("avg_views"))
            _fake = estimate_fake_follower_score(followers, following, avg_likes, avg_comments)
            _bf = calculate_brand_fit_score(niche, brand_industry or niche, female_pct, age_18_24 + age_25_34, posting_freq)
            _aq = calculate_audience_quality_score(_fake, _er, audience_authenticity)
            _vs = calculate_vettd_score(_er, _fake, _bf, _aq,
                                        calculate_consistency_score(posting_freq),
                                        calculate_growth_score(growth_rate_30d))
            _lbl, _ = score_label(_vs)
            entry = {"data": dict(st.session_state.vettd_data), "score": _vs, "label": _lbl,
                     "name": creator_name, "username": _user_display, "niche": niche}
            hist = [h for h in st.session_state.get("history", []) if h["username"] != _user_display]
            st.session_state.history = ([entry] + hist)[:12]
            st.switch_page("pages/4_Dashboard.py")

# ── FULL-WIDTH FOOTER ──
st.markdown(SITE_FOOTER, unsafe_allow_html=True)
