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
    background: #101019 !important; color: #8888A8 !important;
    border: 1px solid #1E1E32 !important; border-radius: 12px !important;
    font-weight: 600 !important; box-shadow: none !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: rgba(124,58,237,.5) !important; color: #C8C8E0 !important;
    background: #14141F !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,.15) !important;
}

.input-section {
    background: #101019;
    border: 1px solid #1A1A2E;
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
    color: #333355;
    margin-bottom: 1rem;
}
.stSelectbox > div > div {
    background: #0D0D1A !important;
    border: 1px solid #1A1A2E !important;
    border-radius: 10px !important;
    color: #E8E8F0 !important;
}
.stTextInput > div > div > input {
    background: #0D0D1A !important;
    border: 1px solid #1A1A2E !important;
    border-radius: 10px !important;
    color: #E8E8F0 !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}
.stNumberInput > div > div > input {
    background: #0D0D1A !important;
    border: 1px solid #1A1A2E !important;
    border-radius: 10px !important;
    color: #E8E8F0 !important;
}
.stSlider [data-baseweb="slider"] { padding: 0.5rem 0; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
    color: #666688 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:1.25rem 3rem;border-bottom:1px solid #0D0D1A;
    background:rgba(11,11,22,0.95);backdrop-filter:blur(20px);">
  <a href="/" target="_self" style="font-size:20px;font-weight:800;letter-spacing:-0.5px;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;gap:2rem;align-items:center;">
    <a href="/Compare" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Compare creators</a>
    <a href="/About" target="_self" style="font-size:13px;color:#555570;text-decoration:none;">About</a>
    <a href="/Founder" target="_self" style="font-size:13px;color:#555570;text-decoration:none;">Founder</a>
    <a href="/Contact" target="_self" style="font-size:13px;color:#555570;text-decoration:none;">Contact</a>
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
  <p style="font-size:16px;color:#44446A;max-width:440px;margin:0 auto;line-height:1.7;">
    Enter the creator's details below and click Run Analysis to get their full Vettd report.
  </p>
</div>
""", unsafe_allow_html=True)

# ── PLAN SELECTOR ──
col_center = st.container()

with col_center:
    tier_cols = st.columns(3)
    tiers = ["Starter", "Pro", "Enterprise"]
    tier_colors = {"Starter": "#555570", "Pro": "#A78BFA", "Enterprise": "#06B6D4"}

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
        font-size:12px;color:#5A5A78;">
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
                        f'<span style="font-weight:600;color:#EDEDF5;">{h["name"]}</span> '
                        f'<span style="color:#5A5A78;font-size:12px;">{h["username"]} · {h["niche"]}</span> '
                        f'<span style="float:right;font-weight:700;color:#A78BFA;">{h["score"]}'
                        f'<span style="font-size:11px;color:#5A5A78;font-weight:400;"> · {h["label"]}</span></span></div>',
                        unsafe_allow_html=True)
                with hc2:
                    if st.button("View", key=f"hist_{i}", use_container_width=True):
                        st.session_state.vettd_data = dict(h["data"])
                        st.switch_page("pages/4_Dashboard.py")
            if st.button("Clear history", key="clear_hist"):
                st.session_state.history = []
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SECTION 1: CREATOR ──
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

    # ── live data fetch (auto-fill when an API key is configured) ──
    _provider = active_provider()
    fcol0, fcol1, fcol2 = st.columns([1, 1, 2])
    with fcol0:
        reels_n = st.selectbox("Average over", [5, 10, 15, 20],
                               index=1, format_func=lambda n: f"Last {n} reels")
    with fcol1:
        if _provider == "manual":
            st.button("⚡ Fetch live data", use_container_width=True, disabled=True,
                      help="Add a MODASH_API_KEY or RAPIDAPI_KEY in Streamlit secrets to enable live fetch.")
        else:
            if st.button("⚡ Fetch live data", use_container_width=True):
                with st.spinner(f"Fetching @{username.lstrip('@')} (last {reels_n} reels)…"):
                    prof = fetch_creator(username, platform, reels_n)
                if prof:
                    st.session_state.fetched = prof
                    st.rerun()
                else:
                    st.session_state.fetched = None
                    st.warning("Couldn't fetch that profile — fill in the details manually.")
    with fcol2:
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

    # ── SECTION 2: PROFILE ──
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

    # ── SECTION 3: REEL ENGAGEMENT ──
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

    # ── SECTION 4: AUDIENCE (Pro+) ──
    if tier_gate("Pro"):
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

    # ── SECTION 5: ENTERPRISE MODULES ──
    ALL_MODULES = ["Predict", "Match", "Guard", "Pulse"]
    if tier_gate("Enterprise"):
        st.markdown('<div class="input-label">Enterprise modules — choose what to run</div>', unsafe_allow_html=True)
        modules = st.multiselect(
            "Active modules",
            ALL_MODULES, default=ALL_MODULES,
            format_func=lambda m: {"Predict": "⚡ Predict — ROI forecast",
                                   "Match": "◈ Match — product-fit + recommendations",
                                   "Guard": "⬡ Guard — safety & fake-follower risk",
                                   "Pulse": "✧ Pulse — comment sentiment"}[m],
        )
        # module-specific inputs (only show what the chosen modules need)
        if "Match" in modules:
            product_text = st.text_input("Match · product you're selling",
                                         placeholder="e.g. vitamin C serum, running shoes, budgeting app")
        else:
            product_text = ""
        g1, g2, g3 = st.columns(3)
        with g1:
            buyer_intent = st.slider("Predict · buyer intent", 0, 100, 65) if "Predict" in modules else 60
        with g2:
            brand_safety = st.slider("Guard · brand safety", 0, 100, 88) if "Guard" in modules else 80
            crisis_risk = st.selectbox("Guard · crisis risk", ["Low", "Medium", "High"]) if "Guard" in modules else "Low"
        with g3:
            sentiment_score = st.slider("Pulse · comment sentiment", 0, 100, 78) if "Pulse" in modules else 70
    else:
        modules = []
        buyer_intent, sentiment_score, brand_safety, crisis_risk = 60, 70, 80, "Low"
        product_text = ""

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
                "buyer_intent": buyer_intent,
                "sentiment_score": sentiment_score,
                "brand_safety": brand_safety,
                "crisis_risk": crisis_risk,
                "product_text": product_text,
                "profile_pic": _fetched.get("profile_pic"),
                "avg_views": _fetched.get("avg_views"),
                "reels_n": _fetched.get("reels_n"),
                "modules": modules,
            }
            # ── save to search history (most recent first, dedup by username) ──
            _er = calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves)
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
