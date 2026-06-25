import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.styles import GLOBAL_CSS

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
.block-container { padding: 0 !important; max-width: 100% !important; }

.input-section {
    background: #07070F;
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
div[data-testid="stSlider"] > div > div > div { background: #7C3AED !important; }
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
    background:rgba(4,4,10,0.95);backdrop-filter:blur(20px);">
  <a href="/" target="_self" style="font-size:20px;font-weight:800;letter-spacing:-0.5px;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;gap:2rem;align-items:center;">
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
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">Vet any creator</span><br>
    <span style="background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      in seconds.
    </span>
  </h1>
  <p style="font-size:16px;color:#44446A;max-width:440px;margin:0 auto;line-height:1.7;">
    Enter the creator's details below and click Run Analysis to get their full Vettd report.
  </p>
</div>
""", unsafe_allow_html=True)

# ── PLAN SELECTOR ──
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    tier_cols = st.columns(3)
    tiers = ["Starter", "Pro", "Enterprise"]
    tier_colors = {"Starter": "#555570", "Pro": "#A78BFA", "Enterprise": "#06B6D4"}

    if "selected_tier" not in st.session_state:
        st.session_state.selected_tier = "Pro"

    for i, t in enumerate(tiers):
        with tier_cols[i]:
            active = st.session_state.selected_tier == t
            color = tier_colors[t]
            bg = f"rgba({','.join(str(int(color.lstrip('#')[j:j+2], 16)) for j in (0,2,4))},0.15)" if active else "#07070F"
            border = color if active else "#1A1A2E"
            if st.button(t, key=f"tier_{t}", use_container_width=True):
                st.session_state.selected_tier = t
                st.rerun()

    tier = st.session_state.selected_tier
    TIERS = {"Starter": 1, "Pro": 2, "Enterprise": 3}

    def tier_gate(required):
        return TIERS[tier] >= TIERS[required]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SECTION 1: CREATOR ──
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">Creator details</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        creator_name = st.text_input("Creator name", placeholder="Emma Williams")
    with c2:
        username = st.text_input("Username", placeholder="@emmalifestyle")
    c3, c4, c5 = st.columns(3)
    with c3:
        platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
    with c4:
        niche = st.selectbox("Niche", ["Fashion", "Fitness", "Beauty", "Tech", "Food", "Travel", "Gaming", "Lifestyle", "Finance", "Parenting", "Other"])
    with c5:
        brand_industry = st.text_input("Your brand industry", placeholder="e.g. Fashion")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SECTION 2: PROFILE ──
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">Profile stats</div>', unsafe_allow_html=True)
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        followers = st.number_input("Followers", min_value=0, value=150000, step=1000)
    with p2:
        following = st.number_input("Following", min_value=0, value=800, step=10)
    with p3:
        post_count = st.number_input("Total posts", min_value=0, value=420)
    with p4:
        posting_freq = st.number_input("Posts per week", min_value=0.0, value=4.0, step=0.5)
    with p5:
        growth_rate_30d = st.number_input("Growth rate 30d %", min_value=-10.0, value=2.5, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SECTION 3: ENGAGEMENT ──
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">Engagement data</div>', unsafe_allow_html=True)
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        avg_likes = st.number_input("Avg likes / post", min_value=0, value=8500, step=100)
    with e2:
        avg_comments = st.number_input("Avg comments / post", min_value=0, value=320, step=10)
    with e3:
        avg_saves = st.number_input("Avg saves / post", min_value=0, value=1200, step=50)
    with e4:
        avg_shares = st.number_input("Avg shares / post", min_value=0, value=450, step=10)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SECTION 4: AUDIENCE (Pro+) ──
    if tier_gate("Pro"):
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown('<div class="input-label">Audience demographics — Pro</div>', unsafe_allow_html=True)
        a1, a2, a3 = st.columns(3)
        with a1:
            female_pct = st.slider("Female audience %", 0, 100, 65)
            male_pct = 100 - female_pct
            st.caption(f"Male {male_pct}% · Female {female_pct}%")
        with a2:
            audience_authenticity = st.slider("Audience authenticity %", 0, 100, 82)
        with a3:
            age_18_24 = st.slider("Age 18–24 %", 0, 100, 28)
            age_25_34 = st.slider("Age 25–34 %", 0, 100, 35)
            age_35_44 = st.slider("Age 35–44 %", 0, 100, 20)

        l1, l2, l3 = st.columns(3)
        with l1:
            loc1_name = st.text_input("Top location 1", value="United Kingdom")
            loc1_pct = st.slider("Location 1 %", 0, 100, 42)
        with l2:
            loc2_name = st.text_input("Top location 2", value="United States")
            loc2_pct = st.slider("Location 2 %", 0, 100, 28)
        with l3:
            loc3_name = st.text_input("Top location 3", value="Australia")
            loc3_pct = st.slider("Location 3 %", 0, 100, 12)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        female_pct, male_pct = 60, 40
        audience_authenticity = 75
        age_18_24, age_25_34, age_35_44 = 30, 35, 20
        loc1_name, loc1_pct = "United Kingdom", 42
        loc2_name, loc2_pct = "United States", 28
        loc3_name, loc3_pct = "Australia", 12

    # ── SECTION 5: ADVANCED (Enterprise+) ──
    if tier_gate("Enterprise"):
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown('<div class="input-label">Advanced signals — Enterprise</div>', unsafe_allow_html=True)
        adv1, adv2, adv3, adv4 = st.columns(4)
        with adv1:
            buyer_intent = st.slider("Buyer intent score", 0, 100, 65)
        with adv2:
            sentiment_score = st.slider("Comment sentiment", 0, 100, 78)
        with adv3:
            brand_safety = st.slider("Brand safety score", 0, 100, 88)
        with adv4:
            crisis_risk = st.selectbox("Crisis risk", ["Low", "Medium", "High"])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        buyer_intent, sentiment_score, brand_safety, crisis_risk = 60, 70, 80, "Low"

    # ── RUN BUTTON ──
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("✦ Run Analysis", use_container_width=True, type="primary")

    if run:
        if not creator_name:
            st.error("Please enter the creator's name.")
        else:
            st.session_state.vettd_data = {
                "tier": tier,
                "creator_name": creator_name,
                "username": username,
                "platform": platform,
                "niche": niche,
                "brand_industry": brand_industry,
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
            }
            st.switch_page("pages/4_Dashboard.py")
