import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json, hashlib
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS
from utils.scoring import (
    calculate_engagement_rate, estimate_fake_follower_score,
    calculate_brand_fit_score, calculate_audience_quality_score,
    calculate_growth_score, calculate_consistency_score,
    calculate_vettd_score, score_label, estimate_cpe,
    calculate_market_fit_score, recommend_creators,
    generate_creator_report
)

st.set_page_config(page_title="Vettd — Report", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
header { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 2rem 3rem !important; max-width: 100% !important; }

div[data-testid="stMetric"] {
    background: #101019;
    border: 1px solid #1A1A2E;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    position: relative;
    overflow: hidden;
    transition: transform .35s cubic-bezier(.16,1,.3,1), border-color .35s ease, box-shadow .35s ease, background .35s ease;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #7C3AED, #22D3EE);
    opacity: 0; transition: opacity .35s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(124,58,237,.45);
    background: #12121F;
    box-shadow: 0 14px 40px rgba(124,58,237,.18);
}
div[data-testid="stMetric"]:hover::before { opacity: 1; }
div[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    color: #6A6A90 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
div[data-testid="stMetricValue"] {
    font-size: 23px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #EDEDF5, #A78BFA) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #101019;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #12121E;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #444466;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    padding: 8px 20px;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #0D0D1A !important;
    color: #A78BFA !important;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #0D0D1A;
    font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: #444466; }
.stat-value { color: #E8E8F0; font-weight: 600; }

.progress-bar-bg {
    background: #0D0D1A;
    border-radius: 999px;
    height: 5px;
    margin: 3px 0 10px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #7C3AED, #06B6D4);
}

.section-card {
    background: #101019;
    border: 1px solid #12121E;
    border-radius: 16px;
    padding: 1.5rem;
}

.brief-block {
    background: #0B0B16;
    border: 1px solid #12121E;
    border-left: 3px solid #7C3AED;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    font-size: 13px;
    color: #888899;
    line-height: 1.9;
}

[data-testid="stDownloadButton"] button {
    background: #101019 !important;
    color: #A78BFA !important;
    border: 1px solid #1A1A2E !important;
    font-size: 13px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── GUARD: redirect if no data ──
if "vettd_data" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem;color:#333355;">
        <div style="font-size:48px;margin-bottom:1rem;">✦</div>
        <div style="font-size:18px;font-weight:600;color:#E8E8F0;margin-bottom:8px;">No analysis data found</div>
        <div style="font-size:14px;color:#444466;margin-bottom:2rem;">Run an analysis first to see the dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("← Go back to analysis", use_container_width=False):
        st.switch_page("pages/0_Analyse.py")
    st.stop()

d = st.session_state.vettd_data
tier = d["tier"]
TIERS = {"Starter": 1, "Pro": 2, "Enterprise": 3}

def tier_gate(required):
    return TIERS[tier] >= TIERS[required]

# ── CALCULATIONS ──
engagement_rate = calculate_engagement_rate(d["followers"], d["avg_likes"], d["avg_comments"], d["avg_saves"])
fake_score = estimate_fake_follower_score(d["followers"], d["following"], d["avg_likes"], d["avg_comments"])
age_18_34 = d["age_18_24"] + d["age_25_34"]
aud_quality = calculate_audience_quality_score(fake_score, engagement_rate, d["audience_authenticity"])
growth_score = calculate_growth_score(d["growth_rate_30d"])
consistency_score = calculate_consistency_score(d["posting_freq"])

# brand-fit only exists when the brand is actually specified
brand_text = (d.get("brand_name") or "").strip() or (d.get("brand_industry") or "").strip()
has_brand = bool(brand_text)
if has_brand:
    brand_fit = calculate_brand_fit_score(d["niche"], d.get("brand_industry") or brand_text, d["female_pct"], age_18_34, d["posting_freq"])
    vettd_score = calculate_vettd_score(engagement_rate, fake_score, brand_fit, aud_quality, consistency_score, growth_score)
else:
    brand_fit = None
    # score without the brand-fit component — redistribute its 20% across the other five signals
    _eng_n = min(engagement_rate * 10, 100); _auth_n = 100 - fake_score
    vettd_score = round((_eng_n*0.25 + _auth_n*0.20 + aud_quality*0.15 + consistency_score*0.10 + growth_score*0.10) / 0.80)
label, _ = score_label(vettd_score)
est_cost_per_post, est_cpe = estimate_cpe(d["followers"], engagement_rate)

score_colors = {
    "Exceptional": "#10B981", "Strong fit": "#60A5FA",
    "Moderate fit": "#F59E0B", "Weak fit": "#F97316", "Not recommended": "#EF4444"
}
score_color = score_colors.get(label, "#A78BFA")

plot_bg = "rgba(0,0,0,0)"
axis_color = "#0D0D1A"
text_color = "#444466"

initials = "".join([w[0].upper() for w in d["creator_name"].split()[:2]])
tier_colors = {"Starter": "#555570", "Pro": "#A78BFA", "Enterprise": "#06B6D4"}
tc = tier_colors[tier]

# ── NAV ──
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:1rem 0 1.5rem;border-bottom:1px solid #0D0D1A;margin-bottom:2rem;">
  <a href="/" target="_self" style="font-size:18px;font-weight:800;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="background:rgba({','.join(str(int(tc.lstrip('#')[j:j+2],16)) for j in (0,2,4))},0.15);
        border:1px solid {tc}44;color:{tc};font-size:11px;font-weight:700;
        padding:4px 14px;border-radius:999px;letter-spacing:0.08em;">{tier}</span>
    <span style="font-size:12px;color:#333355;">{datetime.now().strftime('%d %b %Y · %H:%M')}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CREATOR HEADER + CIRCULAR SCORE RING ──
_brand_suffix = f"&nbsp;·&nbsp; {d['brand_industry']}" if d['brand_industry'] else ""
import math
_R = 56
_CIRC = round(2 * math.pi * _R, 1)
_OFFSET = round(_CIRC * (1 - vettd_score / 100), 1)
st.markdown(f"""
<style>
@keyframes ringfill {{ from {{ stroke-dashoffset: {_CIRC}; }} to {{ stroke-dashoffset: {_OFFSET}; }} }}
.score-ring-progress {{ animation: ringfill 1.4s cubic-bezier(.16,1,.3,1) forwards; }}
</style>
<div style="display:flex;align-items:center;justify-content:space-between;gap:2rem;margin-bottom:2rem;">
<div style="display:flex;align-items:center;gap:16px;">
{(f'<img src="{d["profile_pic"]}" style="width:56px;height:56px;border-radius:50%;object-fit:cover;border:2px solid #7C3AED;flex-shrink:0;" referrerpolicy="no-referrer" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';"/><div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#06B6D4);display:none;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:white;flex-shrink:0;">{initials}</div>') if d.get("profile_pic") else (f'<div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#06B6D4);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:white;flex-shrink:0;">{initials}</div>')}
<div>
<div style="font-size:22px;font-weight:800;color:#E8E8F0;letter-spacing:-0.5px;">{d['creator_name']}</div>
<div style="font-size:12px;color:#5A5A78;margin-top:3px;">{d['username']} &nbsp;·&nbsp; {d['platform']} &nbsp;·&nbsp; {d['niche']} {_brand_suffix}</div>
</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
<div style="position:relative;width:140px;height:140px;">
<svg width="140" height="140" viewBox="0 0 140 140">
<defs><linearGradient id="ringgrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#22D3EE"/></linearGradient></defs>
<circle cx="70" cy="70" r="{_R}" fill="none" stroke="#1A1A2E" stroke-width="10"/>
<circle class="score-ring-progress" cx="70" cy="70" r="{_R}" fill="none" stroke="url(#ringgrad)" stroke-width="10"
  stroke-linecap="round" stroke-dasharray="{_CIRC}" stroke-dashoffset="{_OFFSET}" transform="rotate(-90 70 70)"/>
</svg>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
<span class="disp" style="font-size:46px;font-weight:800;line-height:1;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{vettd_score}</span>
</div>
</div>
<div style="font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#5A5A78;margin-top:8px;">Vettd Score</div>
<div style="font-size:13px;font-weight:700;color:{score_color};margin-top:2px;">{label}</div>
</div>
</div>
""", unsafe_allow_html=True)

# brand + one-line fit phrase (used in the report header)
_brand = brand_text
if has_brand:
    _fit_phrase = ("an excellent fit" if vettd_score >= 85 else
                   "a strong fit" if vettd_score >= 70 else
                   "a moderate fit" if vettd_score >= 55 else
                   "a weak fit" if vettd_score >= 40 else "not recommended")
else:
    _fit_phrase = ("an exceptional profile" if vettd_score >= 85 else
                   "a strong profile" if vettd_score >= 70 else
                   "a solid profile" if vettd_score >= 55 else
                   "a weak profile" if vettd_score >= 40 else "a poor profile")
_for = f' for <b style="color:#A78BFA;">{_brand}</b>' if has_brand else ''

# ── PERSONALISED REPORT (MBTI-style) ──
rep = generate_creator_report(d, engagement_rate, fake_score, brand_fit,
                              aud_quality, growth_score, consistency_score, vettd_score)
strengths_html = "".join([
    f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:9px;">'
    f'<span style="color:#10B981;flex-shrink:0;margin-top:2px;">✓</span>'
    f'<span style="font-size:13.5px;color:#C2C2D6;line-height:1.55;">{s}</span></div>' for s in rep["strengths"][:3]
])
watchouts_html = "".join([
    f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:9px;">'
    f'<span style="color:#F59E0B;flex-shrink:0;margin-top:2px;">!</span>'
    f'<span style="font-size:13.5px;color:#C2C2D6;line-height:1.55;">{w}</span></div>' for w in rep["watchouts"][:3]
])

# highlight stats — a few key numbers WITH plain-English meaning (data + text mix)
def _human(n):
    return f"{n/1_000_000:.1f}M" if n >= 1_000_000 else f"{n/1_000:.1f}K" if n >= 1_000 else str(n)
_eng_word = "above average" if engagement_rate > 5 else "around average" if engagement_rate >= 2 else "below average"
_auth_word = "real, low fake risk" if d["audience_authenticity"] >= 80 else "worth a closer look" if d["audience_authenticity"] >= 60 else "quality concerns"
_growth_word = "growing fast" if d["growth_rate_30d"] >= 3 else "growing steadily" if d["growth_rate_30d"] > 0 else "flat / declining"
highlights = [
    (_human(d["followers"]), "Followers", f"{rep['size']} creator", "#A78BFA"),
    (f"{engagement_rate}%", "Engagement", _eng_word, "#60A5FA"),
    (f"{d['audience_authenticity']}%", "Authenticity", _auth_word, "#22D3EE"),
    (f"${est_cost_per_post:,.0f}", "Est. cost / post", f"~${est_cpe:.3f}/engagement", "#A78BFA"),
]
if d.get("avg_views"):
    _rn = d.get("reels_n")
    highlights.append((_human(d["avg_views"]), "Avg reel views",
                       f"avg of last {_rn} reels" if _rn else "live from recent reels", "#60A5FA"))
highlights_html = "".join([
    f'<div style="background:#101019;border:1px solid #14142A;border-radius:16px;padding:1.25rem;text-align:center;">'
    f'<div class="disp" style="font-size:30px;font-weight:800;line-height:1;background:linear-gradient(135deg,{clr},#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{val}</div>'
    f'<div style="font-size:11px;color:#6A6A90;text-transform:uppercase;letter-spacing:.08em;margin-top:8px;">{lbl}</div>'
    f'<div style="font-size:12px;color:#A8A8C0;margin-top:6px;line-height:1.4;">{note}</div></div>'
    for val, lbl, note, clr in highlights
])
st.markdown(f"""
<div style="background:linear-gradient(160deg,rgba(124,58,237,.1),rgba(34,211,238,.04));
  border:1px solid rgba(124,58,237,.3);border-radius:20px;padding:2rem;margin-bottom:1.5rem;position:relative;overflow:hidden;">
<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#60A5FA,#22D3EE);"></div>
<div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#22D3EE;margin-bottom:6px;">Creator archetype</div>
<div class="disp" style="font-size:30px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1;">{rep['archetype']}</div>
<div style="font-size:14px;color:#9090B0;margin-top:8px;line-height:1.6;font-style:italic;">{rep['archetype_desc']}</div>
<div style="font-size:15px;color:#D2D2E4;margin-top:1.1rem;border-top:1px solid #1A1A2E;padding-top:1.1rem;">
<b style="color:#EDEDF5;">{d['creator_name']}</b> · <b style="color:{score_color};">{_fit_phrase}</b>{_for} · <b style="color:#A78BFA;">{vettd_score}/100</b></div>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;margin-bottom:1.5rem;">{highlights_html}</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;">
<div style="background:#101019;border:1px solid #14142A;border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#10B981;margin-bottom:1rem;">Strengths</div>
{strengths_html}
</div>
<div style="background:#101019;border:1px solid #14142A;border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#F59E0B;margin-bottom:1rem;">Watch-outs</div>
{watchouts_html}
</div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;">
<div style="background:#101019;border:1px solid #14142A;border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;">Best suited for</div>
<div style="font-size:14px;color:#C2C2D6;line-height:1.7;">{rep['best_for']}</div>
</div>
<div style="background:#101019;border:1px solid {score_color}55;border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:{score_color};margin-bottom:.6rem;">Recommendation</div>
<div style="font-size:14px;color:#EDEDF5;line-height:1.7;font-weight:500;">{rep['recommendation']}</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── DEEP DIVE (full data & charts, below the readable report) ──
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin:1rem 0 1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#5A5A78;white-space:nowrap;">🔍 Deep dive — full data &amp; charts</div>
<div style="flex:1;height:1px;background:linear-gradient(90deg,#1A1A2E,transparent);"></div>
</div>
""", unsafe_allow_html=True)

# ── TOP METRICS STRIP (numbers in a row, labels beneath) ──
top_metrics = [
    ("Followers", f"{d['followers']:,}"),
    ("Engagement", f"{engagement_rate}%"),
    ("Fake score", f"{fake_score}/100"),
    ("Brand fit", f"{brand_fit}/100" if has_brand else "—"),
    ("Avg likes", f"{d['avg_likes']:,}"),
    ("Avg comments", f"{d['avg_comments']:,}"),
    ("Est. cost/post", f"${est_cost_per_post:,.0f}"),
    ("30d growth", f"{d['growth_rate_30d']}%"),
]
metric_cells = "".join([
    f'<div class="mstrip-cell">'
    f'<div class="mstrip-num">{val}</div>'
    f'<div class="mstrip-lbl">{lbl}</div></div>'
    for lbl, val in top_metrics
])
st.markdown(f"""
<style>
.mstrip {{ display:grid; grid-template-columns:repeat(8,1fr); background:#101019;
  border:1px solid #1A1A2E; border-radius:16px; overflow:hidden; }}
.mstrip-cell {{ padding:1.1rem .75rem; text-align:center; border-right:1px solid #16162A;
  transition:background .3s ease; }}
.mstrip-cell:last-child {{ border-right:none; }}
.mstrip-cell:hover {{ background:#14141F; }}
.mstrip-num {{ font-size:21px; font-weight:800; line-height:1;
  background:linear-gradient(135deg,#EDEDF5,#A78BFA); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.mstrip-lbl {{ font-size:10px; color:#6A6A90; text-transform:uppercase; letter-spacing:.08em; margin-top:8px; }}
</style>
<div class="mstrip">{metric_cells}</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SCORE BREAKDOWN + TABS ──
col_score, col_main = st.columns([1, 3], gap="large")

with col_score:
    st.markdown(f"""
    <div style="background:#101019;border:1px solid #12121E;border-radius:20px;
        padding:1.75rem;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
          background:linear-gradient(90deg,transparent,{score_color}55,transparent);"></div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
          color:#333355;margin-bottom:1.5rem;">Score breakdown</div>
    """, unsafe_allow_html=True)

    components = {
        "Engagement": int(min(engagement_rate * 10, 100)),
        "Authenticity": int(100 - fake_score),
    }
    if has_brand:
        components["Brand fit"] = brand_fit
    components.update({
        "Aud. quality": aud_quality,
        "Consistency": consistency_score,
        "Growth": growth_score,
    })
    weights = {"Engagement": "25%", "Authenticity": "20%", "Brand fit": "20%",
               "Aud. quality": "15%", "Consistency": "10%", "Growth": "10%"}

    if tier_gate("Pro"):
        for k, v in components.items():
            st.markdown(f"""
            <div style="margin-bottom:2px;">
              <div style="display:flex;justify-content:space-between;font-size:12px;">
                <span style="color:#555570;">{k}</span>
                <span style="color:#888899;font-size:10px;">{weights[k]} &nbsp;
                  <span style="color:#A78BFA;font-weight:700;">{int(v)}</span>
                </span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{int(v)}%"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px;color:#333355;padding:1rem 0;">Upgrade to Pro for score breakdown</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats card
    like_comment_ratio = round(d["avg_likes"] / max(d["avg_comments"], 1), 1)
    save_rate = round((d["avg_saves"] / max(d["followers"], 1)) * 100, 2)
    st.markdown(f"""
    <div class="section-card">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
          color:#333355;margin-bottom:1rem;">Quick stats</div>
      <div class="stat-row"><span class="stat-label">Follower ratio</span>
        <span class="stat-value">{round(d['followers']/max(d['following'],1),1)}:1</span></div>
      <div class="stat-row"><span class="stat-label">Like:comment</span>
        <span class="stat-value">{like_comment_ratio}:1</span></div>
      <div class="stat-row"><span class="stat-label">Save rate</span>
        <span class="stat-value">{save_rate}%</span></div>
      <div class="stat-row"><span class="stat-label">Posts/week</span>
        <span class="stat-value">{d['posting_freq']}</span></div>
      <div class="stat-row"><span class="stat-label">Total posts</span>
        <span class="stat-value">{d['post_count']:,}</span></div>
      <div class="stat-row"><span class="stat-label">Cost/engagement</span>
        <span class="stat-value">${est_cpe:.4f}</span></div>
    </div>
    """, unsafe_allow_html=True)

with col_main:
    tab1, tab2, tab3, tab4 = st.tabs(["  Engagement  ", "  Audience  ", "  Brand fit  ", "  Advanced  "])

    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig = go.Figure(go.Bar(
                x=["Likes", "Comments", "Saves", "Shares"],
                y=[d["avg_likes"], d["avg_comments"], d["avg_saves"], d["avg_shares"]],
                marker=dict(color=["#7C3AED","#4F46E5","#60A5FA","#A78BFA"], line=dict(width=0)),
                text=[f"{v:,}" for v in [d["avg_likes"], d["avg_comments"], d["avg_saves"], d["avg_shares"]]],
                textposition="outside", textfont=dict(color=text_color, size=11),
            ))
            fig.update_layout(
                title=dict(text="Avg interactions per post", font=dict(color=text_color, size=12)),
                height=280, margin=dict(t=40,b=10,l=10,r=10),
                paper_bgcolor=plot_bg, plot_bgcolor=plot_bg,
                xaxis=dict(showgrid=False, color=text_color, tickfont=dict(color=text_color)),
                yaxis=dict(showgrid=True, gridcolor=axis_color, tickfont=dict(color=text_color)),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            share_rate = round((d["avg_shares"] / max(d["followers"], 1)) * 100, 2)
            st.markdown(f"""
            <div class="section-card" style="height:100%;">
              <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                  color:#333355;margin-bottom:1rem;">Engagement signals</div>
              <div class="stat-row"><span class="stat-label">Engagement rate</span>
                <span class="stat-value" style="color:#A78BFA;">{engagement_rate}%</span></div>
              <div class="stat-row"><span class="stat-label">Like:comment ratio</span>
                <span class="stat-value">{like_comment_ratio}:1</span></div>
              <div class="stat-row"><span class="stat-label">Save rate</span>
                <span class="stat-value">{save_rate}%</span></div>
              <div class="stat-row"><span class="stat-label">Share rate</span>
                <span class="stat-value">{share_rate}%</span></div>
              <div class="stat-row"><span class="stat-label">Consistency score</span>
                <span class="stat-value">{consistency_score}/100</span></div>
              <div class="stat-row"><span class="stat-label">Growth score</span>
                <span class="stat-value">{growth_score}/100</span></div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if tier_gate("Pro"):
            c1, c2 = st.columns(2)
            with c1:
                fig_gender = go.Figure(go.Pie(
                    labels=["Female", "Male"],
                    values=[d["female_pct"], d["male_pct"]],
                    marker=dict(colors=["#7C3AED","#4F46E5"], line=dict(width=0)),
                    hole=0.65, textfont=dict(color="white", size=12),
                ))
                fig_gender.add_annotation(
                    text=f"{d['female_pct']}%<br><span style='font-size:10px'>Female</span>",
                    x=0.5, y=0.5, font=dict(size=14, color="#A78BFA"), showarrow=False
                )
                fig_gender.update_layout(
                    title=dict(text="Gender split", font=dict(color=text_color, size=12)),
                    height=260, margin=dict(t=40,b=10,l=10,r=10),
                    paper_bgcolor=plot_bg, showlegend=True,
                    legend=dict(font=dict(color=text_color), bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig_gender, use_container_width=True)
            with c2:
                age_labels = ["18–24", "25–34", "35–44", "45+"]
                age_values = [d["age_18_24"], d["age_25_34"], d["age_35_44"], d["age_45_plus"]]
                fig_age = go.Figure(go.Bar(
                    x=age_labels, y=age_values,
                    marker=dict(color=["#7C3AED","#5B4FCC","#4F46E5","#3730A3"], line=dict(width=0)),
                    text=[f"{v}%" for v in age_values],
                    textposition="outside", textfont=dict(color=text_color, size=11),
                ))
                fig_age.update_layout(
                    title=dict(text="Age breakdown", font=dict(color=text_color, size=12)),
                    height=260, margin=dict(t=40,b=10,l=10,r=10),
                    paper_bgcolor=plot_bg, plot_bgcolor=plot_bg,
                    xaxis=dict(showgrid=False, color=text_color, tickfont=dict(color=text_color)),
                    yaxis=dict(showgrid=True, gridcolor=axis_color, tickfont=dict(color=text_color)),
                    bargap=0.3,
                )
                st.plotly_chart(fig_age, use_container_width=True)

            st.markdown(f"""
            <div class="section-card">
              <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                  color:#333355;margin-bottom:1.25rem;">Top audience locations</div>
              <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                <span style="color:#888899;">{d['loc1_name']}</span>
                <span style="color:#A78BFA;font-weight:600;">{d['loc1_pct']}%</span>
              </div>
              <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{d['loc1_pct']}%"></div></div>
              <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                <span style="color:#888899;">{d['loc2_name']}</span>
                <span style="color:#A78BFA;font-weight:600;">{d['loc2_pct']}%</span>
              </div>
              <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{d['loc2_pct']}%"></div></div>
              <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                <span style="color:#888899;">{d['loc3_name']}</span>
                <span style="color:#A78BFA;font-weight:600;">{d['loc3_pct']}%</span>
              </div>
              <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{d['loc3_pct']}%"></div></div>
              <div class="stat-row" style="margin-top:8px;"><span class="stat-label">Audience authenticity</span>
                <span class="stat-value" style="color:#10B981;">{d['audience_authenticity']}%</span></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:#333355;">Upgrade to Pro for full audience demographics.</div>', unsafe_allow_html=True)

    with tab3:
        c1, c2 = st.columns([2, 3])
        with c1:
            st.markdown(f"""
            <div class="section-card">
              <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                  color:#333355;margin-bottom:1rem;">Brand intelligence</div>
              <div class="stat-row"><span class="stat-label">Brand-fit score</span>
                <span class="stat-value" style="color:#A78BFA;">{f'{brand_fit}/100' if has_brand else 'add a brand'}</span></div>
              <div class="stat-row"><span class="stat-label">Niche</span>
                <span class="stat-value">{d['niche']}</span></div>
              <div class="stat-row"><span class="stat-label">Brand</span>
                <span class="stat-value">{_brand or '—'}</span></div>
              <div class="stat-row"><span class="stat-label">Audience quality</span>
                <span class="stat-value">{aud_quality}/100</span></div>
              <div class="stat-row"><span class="stat-label">Consistency</span>
                <span class="stat-value">{consistency_score}/100</span></div>
              <div class="stat-row"><span class="stat-label">Growth score</span>
                <span class="stat-value">{growth_score}/100</span></div>
              <div class="stat-row"><span class="stat-label">Est. cost/post</span>
                <span class="stat-value">${est_cost_per_post:,.0f}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            _rvals = [int(min(engagement_rate * 10, 100)), int(100 - fake_score)]
            _rtheta = ["Engagement", "Authenticity"]
            if has_brand:
                _rvals.append(brand_fit); _rtheta.append("Brand fit")
            _rvals += [aud_quality, consistency_score, growth_score]
            _rtheta += ["Aud. quality", "Consistency", "Growth"]
            fig_radar = go.Figure(go.Scatterpolar(
                r=_rvals,
                theta=_rtheta,
                fill="toself",
                fillcolor="rgba(124,58,237,0.1)",
                line=dict(color="#7C3AED", width=2),
                marker=dict(color="#A78BFA", size=6),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor=plot_bg,
                    radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color=text_color, size=9), gridcolor=axis_color, linecolor=axis_color),
                    angularaxis=dict(tickfont=dict(color=text_color, size=11), gridcolor=axis_color, linecolor=axis_color),
                ),
                height=320, margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor=plot_bg,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    with tab4:
        if tier_gate("Enterprise"):
            mods = d.get("modules") or ["Predict", "Match", "Guard", "Pulse"]
            _fit_for_roi = brand_fit if has_brand else aud_quality
            roi_estimate = round((engagement_rate * _fit_for_roi * d["audience_authenticity"]) / 1000, 1)
            virality_score = round((d["avg_shares"] / max(d["followers"], 1)) * 1000 + d["growth_rate_30d"] * 5, 1)
            loyalty_score = round((d["avg_saves"] + d["avg_comments"]) / max(d["followers"] / 100, 1), 1)
            inactive_pct = round(100 - d["audience_authenticity"] * 0.8, 1)

            # active-module chips
            _mdefs = {"Predict": ("⚡", "#A78BFA"), "Match": ("◈", "#60A5FA"), "Guard": ("⬡", "#22D3EE"), "Pulse": ("✧", "#A78BFA")}
            chips = "".join([
                f'<span style="font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;'
                f'background:{clr}18;border:1px solid {clr}44;color:{clr};">{ic} {m}</span>'
                if m in mods else
                f'<span style="font-size:11px;padding:5px 12px;border-radius:999px;border:1px solid #16162A;color:#3A3A52;text-decoration:line-through;">{m}</span>'
                for m, (ic, clr) in _mdefs.items()])
            st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:1.25rem;align-items:center;">'
                        f'<span style="font-size:11px;color:#5A5A78;text-transform:uppercase;letter-spacing:.1em;margin-right:4px;">Modules:</span>{chips}</div>',
                        unsafe_allow_html=True)

            _cards = []
            if "Predict" in mods:
                _cards.append(f'<div class="section-card"><div style="font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#A78BFA;margin-bottom:1rem;">⚡ Vettd Predict</div>'
                    f'<div class="stat-row"><span class="stat-label">ROI potential</span><span class="stat-value" style="color:#10B981;">{min(roi_estimate,100)}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Virality likelihood</span><span class="stat-value">{min(virality_score,100):.1f}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Audience loyalty</span><span class="stat-value">{min(loyalty_score,100):.1f}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Buyer intent</span><span class="stat-value">{d["buyer_intent"]}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Est. cost / post</span><span class="stat-value">${est_cost_per_post:,.0f}</span></div></div>')
            if "Guard" in mods:
                _cr = d["crisis_risk"]; _crc = '#10B981' if _cr=='Low' else '#F59E0B' if _cr=='Medium' else '#EF4444'
                _cards.append(f'<div class="section-card"><div style="font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#22D3EE;margin-bottom:1rem;">⬡ Vettd Guard</div>'
                    f'<div class="stat-row"><span class="stat-label">Brand safety</span><span class="stat-value" style="color:#10B981;">{d["brand_safety"]}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Fake follower score</span><span class="stat-value">{fake_score}/100</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Inactive follower est.</span><span class="stat-value" style="color:#F59E0B;">{inactive_pct}%</span></div>'
                    f'<div class="stat-row"><span class="stat-label">Crisis risk</span><span class="stat-value" style="color:{_crc};">{_cr}</span></div></div>')
            if "Pulse" in mods:
                _s = d["sentiment_score"]; _pos=_s; _neg=max(0,100-_s-15); _neu=100-_pos-_neg
                _cards.append(f'<div class="section-card"><div style="font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#A78BFA;margin-bottom:1rem;">✧ Vettd Pulse</div>'
                    f'<div class="stat-row"><span class="stat-label">Comment sentiment</span><span class="stat-value" style="color:#10B981;">{_s}/100</span></div>'
                    f'<div style="margin-top:12px;display:flex;height:10px;border-radius:999px;overflow:hidden;">'
                    f'<div style="width:{_pos}%;background:#10B981;"></div><div style="width:{_neu}%;background:#60A5FA;"></div><div style="width:{_neg}%;background:#EF4444;"></div></div>'
                    f'<div style="display:flex;justify-content:space-between;font-size:11px;color:#5A5A78;margin-top:6px;"><span>Positive {_pos}%</span><span>Neutral {_neu}%</span><span>Negative {_neg}%</span></div></div>')
            # campaign brief always included as a general Enterprise deliverable
            _cards.append(f'<div class="section-card"><div style="font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Auto campaign brief</div>'
                f'<div class="brief-block"><b style="color:#A78BFA;">Creator:</b> {d["creator_name"]} ({d["username"]})<br>'
                f'<b style="color:#A78BFA;">Platform:</b> {d["platform"]} &nbsp;|&nbsp; <b style="color:#A78BFA;">Niche:</b> {d["niche"]}<br>'
                f'<b style="color:#A78BFA;">Recommended for:</b> {d["brand_industry"] or d["niche"]} campaigns<br>'
                f'<b style="color:#A78BFA;">Audience:</b> {d["female_pct"]}% female, peak age 18–34<br>'
                f'<b style="color:#A78BFA;">Est. cost/post:</b> ${est_cost_per_post:,.0f}<br>'
                f'<b style="color:#A78BFA;">Key strength:</b> {"High engagement" if engagement_rate > 5 else "Broad reach"}, {d["audience_authenticity"]}% authentic</div></div>')
            st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">{"".join(_cards)}</div>', unsafe_allow_html=True)

            # ── VETTD MATCH: BRAND–PRODUCT MARKET FIT ──
            if "Match" in mods:
              # ── BRAND–PRODUCT MARKET FIT (flagship Enterprise metric) ──
              mf_score, mf_breakdown, mf_key = calculate_market_fit_score(
                  d.get("product_text", ""), d["brand_industry"], d["niche"],
                  d["female_pct"], d["age_18_24"], d["age_25_34"], d["age_35_44"],
                  d["audience_authenticity"], engagement_rate, d["followers"],
              )
              if mf_score >= 75:
                  mf_color, mf_verdict = "#10B981", "Excellent product–audience match"
              elif mf_score >= 60:
                  mf_color, mf_verdict = "#60A5FA", "Good match"
              elif mf_score >= 45:
                  mf_color, mf_verdict = "#F59E0B", "Weak match — consider alternatives"
              else:
                  mf_color, mf_verdict = "#EF4444", "Poor match — not recommended"

              product_label = (d.get("product_text") or d["brand_industry"] or "your product")

              bars = "".join([
                  f'<div style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;">'
                  f'<span style="color:#5A5A78;">{k}</span><span style="color:{mf_color};font-weight:600;">{v}</span></div>'
                  f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{v}%;background:linear-gradient(90deg,{mf_color},{mf_color}88);"></div></div></div>'
                  for k, v in mf_breakdown.items()
              ])

              st.markdown(f"""
              <div class="section-card" style="margin-top:1.5rem;position:relative;overflow:hidden;border-color:{mf_color}33;">
                <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{mf_color},transparent);"></div>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                  <div style="flex:1;min-width:260px;">
                    <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:{mf_color};margin-bottom:6px;">★ Brand–Product Market Fit</div>
                    <div style="font-size:13px;color:#8888A8;line-height:1.6;margin-bottom:1rem;">
                      How well <b style="color:#EDEDF5;">{product_label}</b> fits {d['creator_name']}'s specific audience —
                      niche, gender, age, authenticity and price-point alignment.</div>
                    {bars}
                  </div>
                  <div style="text-align:center;min-width:140px;">
                    <div class="disp" style="font-size:56px;font-weight:800;line-height:1;color:{mf_color};">{mf_score}</div>
                    <div style="font-size:12px;font-weight:600;color:{mf_color};max-width:150px;">{mf_verdict}</div>
                  </div>
                </div>
              </div>
              """, unsafe_allow_html=True)

              # Recommended alternative creators when fit is weak
              if mf_score < 60:
                  recs = recommend_creators(mf_key, d["brand_industry"], mf_score)
                  rec_cards = "".join([
                      f'<div style="background:#0B0B16;border:1px solid #16162A;border-radius:12px;padding:1rem 1.25rem;flex:1;min-width:200px;">'
                      f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                      f'<span style="font-size:14px;font-weight:700;color:#EDEDF5;">{handle}</span>'
                      f'<span style="font-size:13px;font-weight:800;color:#10B981;">{fit}</span></div>'
                      f'<div style="font-size:12px;color:#A78BFA;margin-bottom:4px;">{kind}</div>'
                      f'<div style="font-size:11px;color:#5A5A78;line-height:1.5;">{why}</div></div>'
                      for handle, kind, fit, why in recs
                  ])
                  st.markdown(f"""
                  <div class="section-card" style="margin-top:1rem;border-color:rgba(16,185,129,0.2);">
                    <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#10B981;margin-bottom:4px;">Recommended creators — better fit for {product_label}</div>
                    <div style="font-size:12px;color:#5A5A78;margin-bottom:1rem;">{d['creator_name']} scored {mf_score}/100 for this product. These creators are a stronger match:</div>
                    <div style="display:flex;gap:12px;flex-wrap:wrap;">{rec_cards}</div>
                  </div>
                  """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:#333355;">Upgrade to Enterprise for predictive intelligence, Brand–Product Market Fit, and campaign briefs.</div>', unsafe_allow_html=True)

# ── EXPORTS + BACK BUTTON ──
st.markdown('<div style="border-top:1px solid #0D0D1A;margin-top:2rem;padding-top:1.5rem;"></div>', unsafe_allow_html=True)

exp1, exp2, exp3, exp4 = st.columns(4)
report_data = {
    "creator": d["creator_name"], "username": d["username"], "platform": d["platform"],
    "niche": d["niche"], "followers": d["followers"], "engagement_rate": engagement_rate,
    "fake_follower_score": fake_score, "brand_fit_score": brand_fit,
    "vettd_score": vettd_score, "vettd_label": label,
    "est_cost_per_post": est_cost_per_post, "generated_at": datetime.now().isoformat()
}

# ── build a proper, printable HTML report ──
_metrics = [("Followers", f"{d['followers']:,}"), ("Engagement rate", f"{engagement_rate}%"),
            ("Audience authenticity", f"{d['audience_authenticity']}%"), ("Fake-follower score", f"{fake_score}/100")]
if has_brand:
    _metrics.append(("Brand-fit score", f"{brand_fit}/100"))
if d.get("avg_views"):
    _metrics.append(("Avg reel views", f"{d['avg_views']:,}"))
_metrics.append(("Est. cost / post", f"${est_cost_per_post:,.0f}"))
_metric_html = "".join(
    f'<div class="m"><div class="mv">{v}</div><div class="ml">{l}</div></div>' for l, v in _metrics)
_bd = {"Engagement": int(min(engagement_rate*10,100)), "Authenticity": int(100-fake_score)}
if has_brand: _bd["Brand fit"] = brand_fit
_bd.update({"Audience quality": aud_quality, "Consistency": consistency_score, "Growth": growth_score})
_bar_html = "".join(
    f'<div class="brow"><span>{k}</span><div class="bt"><div class="bf" style="width:{int(x)}%"></div></div><b>{int(x)}</b></div>'
    for k, x in _bd.items())
_str_li = "".join(f"<li>{s}</li>" for s in rep["strengths"])
_watch_li = "".join(f"<li>{w}</li>" for w in rep["watchouts"])
_brand_row = f'<span>Brand&nbsp;·&nbsp;<b>{_brand}</b></span>' if has_brand else ''
html_report = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Vettd report — {d['creator_name']}</title>
<style>
*{{box-sizing:border-box;margin:0}} body{{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1a1a2e;background:#f4f4f8;padding:40px;}}
.wrap{{max-width:820px;margin:0 auto;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.08)}}
.hd{{background:linear-gradient(135deg,#7C3AED,#4F46E5);color:#fff;padding:28px 36px;display:flex;justify-content:space-between;align-items:center}}
.hd .logo{{font-size:22px;font-weight:800;letter-spacing:-.5px}} .hd .dt{{font-size:12px;opacity:.8}}
.body{{padding:32px 36px}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap;border-bottom:1px solid #eee;padding-bottom:24px;margin-bottom:24px}}
.nm{{font-size:24px;font-weight:800}} .sub{{font-size:13px;color:#777;margin-top:4px;display:flex;gap:10px;flex-wrap:wrap}}
.score{{text-align:center}} .score .n{{font-size:56px;font-weight:800;color:{score_color};line-height:1}} .score .l{{font-size:13px;font-weight:700;color:{score_color}}}
.score .c{{font-size:11px;color:#999;text-transform:uppercase;letter-spacing:.1em}}
.verdict{{background:#f7f5ff;border-left:4px solid {score_color};border-radius:0 10px 10px 0;padding:16px 20px;font-size:15px;line-height:1.6;margin-bottom:28px}}
.arch{{font-size:13px;font-weight:700;color:#7C3AED;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px}}
h3{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:#999;margin:28px 0 14px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.m{{background:#f7f7fb;border-radius:12px;padding:14px}} .mv{{font-size:22px;font-weight:800;color:#4F46E5}} .ml{{font-size:11px;color:#888;margin-top:4px}}
.brow{{display:flex;align-items:center;gap:12px;margin-bottom:10px;font-size:13px}} .brow span{{width:130px;color:#666}} .brow b{{width:32px;text-align:right;color:#4F46E5}}
.bt{{flex:1;background:#eee;border-radius:999px;height:8px;overflow:hidden}} .bf{{height:100%;background:linear-gradient(90deg,#7C3AED,#22D3EE);border-radius:999px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:24px}} ul{{margin:0;padding-left:18px}} li{{font-size:13px;color:#444;line-height:1.7;margin-bottom:6px}}
.rec{{background:{score_color}12;border:1px solid {score_color}44;border-radius:12px;padding:18px 20px;font-size:15px;font-weight:600;margin-top:24px}}
.ft{{text-align:center;font-size:11px;color:#aaa;padding:20px;border-top:1px solid #eee}}
@media print{{body{{background:#fff;padding:0}} .wrap{{box-shadow:none}}}}
</style></head><body><div class="wrap">
<div class="hd"><div class="logo">✦ VETTD</div><div class="dt">Creator report · {datetime.now().strftime('%d %b %Y')}</div></div>
<div class="body">
<div class="top">
<div><div class="nm">{d['creator_name']}</div><div class="sub"><span>{d['username']}</span><span>{d['platform']}</span><span>{d['niche']}</span>{_brand_row}</div></div>
<div class="score"><div class="c">Vettd Score</div><div class="n">{vettd_score}</div><div class="l">{label}</div></div>
</div>
<div class="verdict"><div class="arch">{rep['archetype']}</div>{rep['summary']}</div>
<h3>Key metrics</h3><div class="grid">{_metric_html}</div>
<h3>Score breakdown</h3>{_bar_html}
<div class="cols"><div><h3>Strengths</h3><ul>{_str_li}</ul></div><div><h3>Watch-outs</h3><ul>{_watch_li}</ul></div></div>
<div class="rec">{rep['recommendation']}</div>
</div>
<div class="ft">Generated by Vettd · get-vettd.streamlit.app · This report is an estimate to support, not replace, your judgement.</div>
</div></body></html>"""

with exp1:
    df = pd.DataFrame([report_data])
    st.download_button("↓ CSV data", df.to_csv(index=False),
        f"vettd_{d['username'].replace('@','')}.csv", "text/csv", use_container_width=True)
with exp2:
    st.download_button("↓ Download report", html_report,
        f"vettd_{d['username'].replace('@','')}.html", mime="text/html", use_container_width=True)
with exp3:
    report_id = hashlib.md5(f"{d['creator_name']}{d['username']}".encode()).hexdigest()[:8]
    st.text_input("Share link", value=f"https://get-vettd.streamlit.app/r/{report_id}",
        disabled=True, label_visibility="collapsed")
with exp4:
    if st.button("← Analyse another creator", use_container_width=True):
        st.switch_page("pages/0_Analyse.py")
