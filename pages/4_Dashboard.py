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
    generate_creator_report,
    compute_forecast, compute_shield, compute_audience_dna,
    compute_benchmark, compute_pulse,
)
from utils.ai_analyst import generate_ai_analysis, ai_available
from html import escape as _esc

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
    background: var(--surface);
    border: 1px solid var(--border);
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
    background: var(--surface);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
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
    background: var(--surface) !important;
    color: #A78BFA !important;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--surface);
    font-size: 13px;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: #444466; }
.stat-value { color: var(--text-1); font-weight: 600; }

.progress-bar-bg {
    background: var(--surface);
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
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
}

.brief-block {
    background: var(--bg-deep);
    border: 1px solid var(--border);
    border-left: 3px solid #7C3AED;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    font-size: 13px;
    color: #888899;
    line-height: 1.9;
}

[data-testid="stDownloadButton"] button {
    background: var(--surface) !important;
    color: #A78BFA !important;
    border: 1px solid var(--border) !important;
    font-size: 13px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── GUARD: redirect if no data ──
if "vettd_data" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem;color:var(--text-4);">
        <div style="font-size:48px;margin-bottom:1rem;">✦</div>
        <div style="font-size:18px;font-weight:600;color:var(--text-1);margin-bottom:8px;">No analysis data found</div>
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

# ── DEFENSIVE COERCION ──
# Core numeric fields must never be None/blank or downstream math crashes.
# (Real inputs come from number_inputs, but saved searches or partial live
# fetches can have gaps — coerce once here so the whole report is safe.)
def _num(key, default=0):
    v = d.get(key, default)
    if v is None or v == "":
        return default
    try:
        return float(v) if isinstance(v, str) and "." in v else (int(v) if not isinstance(v, float) else v)
    except (TypeError, ValueError):
        return default

for _k, _dflt in (("followers", 0), ("following", 0), ("post_count", 0),
                  ("posting_freq", 0), ("growth_rate_30d", 0), ("avg_likes", 0),
                  ("avg_comments", 0), ("avg_saves", 0), ("avg_shares", 0),
                  ("female_pct", 50), ("male_pct", 50), ("audience_authenticity", 80),
                  ("age_18_24", 0), ("age_25_34", 0), ("age_35_44", 0),
                  ("loc1_pct", 0), ("loc2_pct", 0), ("loc3_pct", 0),
                  ("sentiment_score", 75), ("campaign_budget", 50000)):
    d[_k] = _num(_k, _dflt)

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
axis_color = "var(--surface)"
text_color = "#444466"

initials = "".join([w[0].upper() for w in d["creator_name"].split()[:2]])
tier_colors = {"Starter": "var(--text-3)", "Pro": "#A78BFA", "Enterprise": "#06B6D4"}
tc = tier_colors[tier]

# ── NAV ──
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:1rem 0 1.5rem;border-bottom:1px solid var(--surface);margin-bottom:2rem;">
  <a href="/" target="_self" style="font-size:18px;font-weight:800;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="background:rgba({','.join(str(int(tc.lstrip('#')[j:j+2],16)) for j in (0,2,4))},0.15);
        border:1px solid {tc}44;color:{tc};font-size:11px;font-weight:700;
        padding:4px 14px;border-radius:999px;letter-spacing:0.08em;">{tier}</span>
    <span style="font-size:12px;color:var(--text-4);">{datetime.now().strftime('%d %b %Y · %H:%M')}</span>
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
<div style="font-size:22px;font-weight:800;color:var(--text-1);letter-spacing:-0.5px;">{d['creator_name']}</div>
<div style="font-size:12px;color:var(--text-3);margin-top:3px;">{d['username']} &nbsp;·&nbsp; {d['platform']} &nbsp;·&nbsp; {d['niche']} {_brand_suffix}</div>
</div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
<div style="position:relative;width:140px;height:140px;">
<svg width="140" height="140" viewBox="0 0 140 140">
<defs><linearGradient id="ringgrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#22D3EE"/></linearGradient></defs>
<circle cx="70" cy="70" r="{_R}" fill="none" stroke="var(--border)" stroke-width="10"/>
<circle class="score-ring-progress" cx="70" cy="70" r="{_R}" fill="none" stroke="url(#ringgrad)" stroke-width="10"
  stroke-linecap="round" stroke-dasharray="{_CIRC}" stroke-dashoffset="{_OFFSET}" transform="rotate(-90 70 70)"/>
</svg>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
<span class="disp" style="font-size:46px;font-weight:800;line-height:1;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{vettd_score}</span>
</div>
</div>
<div style="font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);margin-top:8px;">Vettd Score</div>
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
    f'<div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1.25rem;text-align:center;">'
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
<div style="font-size:15px;color:#D2D2E4;margin-top:1.1rem;border-top:1px solid var(--border);padding-top:1.1rem;">
<b style="color:var(--text-1);">{d['creator_name']}</b> · <b style="color:{score_color};">{_fit_phrase}</b>{_for} · <b style="color:#A78BFA;">{vettd_score}/100</b></div>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;margin-bottom:1.5rem;">{highlights_html}</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;">
<div style="background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#10B981;margin-bottom:1rem;">Strengths</div>
{strengths_html}
</div>
<div style="background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#F59E0B;margin-bottom:1rem;">Watch-outs</div>
{watchouts_html}
</div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;">
<div style="background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#60A5FA;margin-bottom:.6rem;">Best suited for</div>
<div style="font-size:14px;color:#C2C2D6;line-height:1.7;">{rep['best_for']}</div>
</div>
<div style="background:var(--surface);border:1px solid {score_color}55;border-radius:18px;padding:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:{score_color};margin-bottom:.6rem;">Recommendation</div>
<div style="font-size:14px;color:var(--text-1);line-height:1.7;font-weight:500;">{rep['recommendation']}</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── AI ANALYST (Claude-powered interpretation — augments the transparent scores) ──
if ai_available():
    with st.spinner("Vettd AI analyst reviewing the numbers…"):
        _ai = generate_ai_analysis(d, {
            "vettd_score": vettd_score, "engagement_rate": engagement_rate,
            "fake_score": fake_score, "brand_fit": brand_fit, "aud_quality": aud_quality,
            "consistency_score": consistency_score, "growth_score": growth_score,
            "est_cost_per_post": est_cost_per_post,
        })
    if _ai and "_error" not in _ai:
        _conf = str(_ai.get("confidence", "Medium")).split()[0]
        _confc = {"High": "#34D399", "Medium": "#F5A623", "Low": "#F0616D"}.get(_conf, "#F5A623")
        _spark = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;">'
                  '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z"/></svg>')

        def _li(items, color, mark):
            return "".join(
                f'<div style="display:flex;gap:9px;align-items:flex-start;margin-bottom:8px;">'
                f'<span style="color:{color};flex-shrink:0;margin-top:1px;font-size:13px;">{mark}</span>'
                f'<span style="font-size:13px;color:#C2C2D6;line-height:1.55;">{_esc(str(s))}</span></div>'
                for s in (items or [])[:4])

        _strengths = _li(_ai.get("strengths"), "#34D399", "✓")
        _watch = _li(_ai.get("watchouts"), "#F5A623", "!")

        def _facet(label, value, color):
            if not value:
                return ""
            return (f'<div style="background:var(--surface-inset);border:1px solid var(--border);border-radius:12px;padding:1rem 1.1rem;">'
                    f'<div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{color};margin-bottom:6px;">{label}</div>'
                    f'<div style="font-size:13px;color:#C8C8DC;line-height:1.6;">{_esc(str(value))}</div></div>')

        _facets = (_facet("Brand fit", _ai.get("brand_fit"), "#60A5FA")
                   + _facet("Risk read", _ai.get("risk"), "#F0616D")
                   + _facet("Recommended use", _ai.get("recommended_use"), "#34D399"))

        st.markdown(f"""
        <div class="section-card" style="border-color:var(--accent-line);margin-bottom:1.5rem;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--cyan),transparent);"></div>
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.75rem;margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:34px;height:34px;border-radius:9px;background:var(--accent-soft);display:flex;align-items:center;justify-content:center;color:var(--accent-2);">{_spark}</div>
              <div>
                <div style="font-size:15px;font-weight:700;color:var(--text-1);letter-spacing:-.3px;">Vettd AI Analyst</div>
                <div style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.1em;">AI interpretation of the signals</div>
              </div>
            </div>
            <span style="font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;background:{_confc}18;border:1px solid {_confc}44;color:{_confc};">{_conf} confidence</span>
          </div>
          <div class="disp" style="font-size:18px;font-weight:700;color:var(--text-1);line-height:1.4;margin-bottom:.75rem;">{_esc(str(_ai.get('verdict','')))}</div>
          <div style="font-size:14px;color:#C2C2D6;line-height:1.75;margin-bottom:1.25rem;">{_esc(str(_ai.get('analysis','')))}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.1rem;">
            <div><div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#34D399;margin-bottom:.7rem;">Strengths</div>{_strengths}</div>
            <div><div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#F5A623;margin-bottom:.7rem;">Watch-outs</div>{_watch}</div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.9rem;">{_facets}</div>
          <div style="font-size:11px;color:var(--text-4);margin-top:1rem;">AI interpretation of Vettd's computed signals. The scores above remain the transparent, rule-based source of truth.</div>
        </div>
        """, unsafe_allow_html=True)
    elif _ai and "_error" in _ai:
        st.caption("AI analyst is temporarily unavailable — the standard report above still applies.")

# ── DEEP DIVE (full data & charts, below the readable report) ──
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin:1rem 0 1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);white-space:nowrap;">🔍 Deep dive — full data &amp; charts</div>
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
.mstrip {{ display:grid; grid-template-columns:repeat(8,1fr); background:var(--surface);
  border:1px solid var(--border); border-radius:16px; overflow:hidden; }}
.mstrip-cell {{ padding:1.1rem .75rem; text-align:center; border-right:1px solid var(--border);
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
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:20px;
        padding:1.75rem;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
          background:linear-gradient(90deg,transparent,{score_color}55,transparent);"></div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
          color:var(--text-4);margin-bottom:1.5rem;">Score breakdown</div>
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
                <span style="color:var(--text-3);">{k}</span>
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
        st.markdown('<div style="font-size:12px;color:var(--text-4);padding:1rem 0;">Upgrade to Pro for score breakdown</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick stats card
    like_comment_ratio = round(d["avg_likes"] / max(d["avg_comments"], 1), 1)
    save_rate = round((d["avg_saves"] / max(d["followers"], 1)) * 100, 2)
    st.markdown(f"""
    <div class="section-card">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
          color:var(--text-4);margin-bottom:1rem;">Quick stats</div>
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
                  color:var(--text-4);margin-bottom:1rem;">Engagement signals</div>
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
                  color:var(--text-4);margin-bottom:1.25rem;">Top audience locations</div>
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
            st.markdown('<div style="text-align:center;padding:3rem;color:var(--text-4);">Upgrade to Pro for full audience demographics.</div>', unsafe_allow_html=True)

    with tab3:
        c1, c2 = st.columns([2, 3])
        with c1:
            st.markdown(f"""
            <div class="section-card">
              <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                  color:var(--text-4);margin-bottom:1rem;">Brand intelligence</div>
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
            # migrate any legacy module names from an older saved search
            _legacy = {"Predict": "Forecast", "Guard": "Shield", "Match": "Benchmark"}
            mods = [_legacy.get(m, m) for m in (d.get("modules") or ["Forecast", "Shield", "Audience", "Benchmark", "Pulse"])]

            _svg = {
                "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
                "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
                "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
                "bars": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>',
                "activity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
            }
            _MOD_DEF = {
                "Forecast":  (_svg["zap"], "#F5A623", "Forecast", "Predictive Campaign ROI"),
                "Shield":    (_svg["shield"], "#F0616D", "Shield", "Brand Safety & Risk Audit"),
                "Audience":  (_svg["users"], "#22D3EE", "Audience DNA", "Credibility & True-Match"),
                "Benchmark": (_svg["bars"], "#60A5FA", "Benchmark", "Competitive Positioning"),
                "Pulse":     (_svg["activity"], "#34D399", "Pulse", "Sentiment & Community Health"),
            }
            _ic_wrap = 'display:inline-flex;width:13px;height:13px;vertical-align:-2px;margin-right:5px;'

            # active-module chips
            chips = "".join([
                (f'<span style="font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;display:inline-flex;align-items:center;'
                 f'background:{clr}14;border:1px solid {clr}33;color:{clr};"><span style="{_ic_wrap}">{ic}</span>{title}</span>')
                if key in mods else
                f'<span style="font-size:11px;padding:5px 12px;border-radius:999px;border:1px solid var(--border);color:var(--text-4);text-decoration:line-through;">{title}</span>'
                for key, (ic, clr, title, _sub) in _MOD_DEF.items()])
            st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center;">'
                        f'<span style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.1em;margin-right:4px;">Suite:</span>{chips}</div>',
                        unsafe_allow_html=True)

            def _mod_header(key):
                ic, clr, title, sub = _MOD_DEF[key]
                return (f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:1.1rem;">'
                        f'<div style="width:34px;height:34px;border-radius:9px;background:{clr}1A;display:flex;'
                        f'align-items:center;justify-content:center;color:{clr};"><span style="width:18px;height:18px;display:inline-flex;">{ic}</span></div>'
                        f'<div><div style="font-size:15px;font-weight:700;color:var(--text-1);letter-spacing:-.3px;">{title}</div>'
                        f'<div style="font-size:11px;color:var(--text-3);text-transform:uppercase;letter-spacing:.1em;">{sub}</div></div></div>')

            # roster for overlap detection (this session's other saved searches)
            _roster = [
                {"name": h.get("name", "Creator"), "niche": h.get("niche", ""),
                 "platform": h.get("data", {}).get("platform", "Instagram"),
                 "followers": h.get("data", {}).get("followers", 0),
                 "auth": h.get("data", {}).get("audience_authenticity", 80)}
                for h in st.session_state.get("history", [])
                if h.get("username") != d.get("username")
            ]

            # ═══ FORECAST ═══
            if "Forecast" in mods:
                fc = compute_forecast(d, engagement_rate, brand_fit, aud_quality)
                _roi = fc["roi_mid"]; _roic = "#10B981" if _roi >= 0 else "#EF4444"
                scen_rows = "".join([
                    f'<tr style="border-top:1px solid var(--border);">'
                    f'<td style="padding:9px 6px;color:#C2C2D6;font-weight:600;">{s["label"]}</td>'
                    f'<td style="padding:9px 6px;text-align:right;color:var(--text-2);">₹{s["budget"]:,}</td>'
                    f'<td style="padding:9px 6px;text-align:right;color:var(--text-2);">{s["deliverables"]}</td>'
                    f'<td style="padding:9px 6px;text-align:right;color:var(--text-2);">{s["reach"]:,}</td>'
                    f'<td style="padding:9px 6px;text-align:right;color:#A78BFA;">₹{s["emv"]:,}</td>'
                    f'<td style="padding:9px 6px;text-align:right;color:{"#10B981" if s["roi"]>=0 else "#EF4444"};font-weight:700;">{s["roi"]:+d}%</td></tr>'
                    for s in fc["scenarios"]])
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:1.25rem;border-color:#FCD34D22;">
                  {_mod_header("Forecast")}
                  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:1.25rem;">
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:var(--text-1);">{fc["reach_per_post"]:,}</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Reach / deliverable</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:#A78BFA;">₹{fc["emv_per_post"]:,}</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">EMV / deliverable</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:var(--text-1);">{fc["total_conversions"]:,}</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Est. conversions</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:{_roic};">{_roi:+d}%</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Projected ROI</div></div>
                  </div>
                  <div style="font-size:12px;color:var(--text-2);margin-bottom:.75rem;line-height:1.6;">
                    For a <b style="color:var(--text-1);">₹{fc["budget"]:,}</b> {fc["objective"].lower()} campaign
                    (~{fc["deliverables"]} deliverables): projected total reach <b style="color:var(--text-1);">{fc["total_reach"]:,}</b>,
                    total EMV <b style="color:#A78BFA;">₹{fc["total_emv"]:,}</b>, ROI range
                    <b style="color:{_roic};">{fc["roi_low"]:+d}% to {fc["roi_high"]:+d}%</b>.</div>
                  <table style="width:100%;border-collapse:collapse;font-size:12px;">
                    <thead><tr style="color:var(--text-3);text-transform:uppercase;letter-spacing:.08em;font-size:10px;">
                      <th style="text-align:left;padding:6px;">Scenario</th><th style="text-align:right;padding:6px;">Budget</th>
                      <th style="text-align:right;padding:6px;">Posts</th><th style="text-align:right;padding:6px;">Reach</th>
                      <th style="text-align:right;padding:6px;">EMV</th><th style="text-align:right;padding:6px;">ROI</th></tr></thead>
                    <tbody>{scen_rows}</tbody>
                  </table>
                </div>
                """, unsafe_allow_html=True)

            # ═══ SHIELD ═══
            if "Shield" in mods:
                sh = compute_shield(d, fake_score, engagement_rate)
                _sevc = {"high": "#EF4444", "med": "#F59E0B", "clear": "#10B981"}
                flag_html = "".join([
                    f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:9px;">'
                    f'<span style="color:{_sevc.get(sev,"#F59E0B")};flex-shrink:0;margin-top:1px;font-size:13px;">'
                    f'{"●" if sev=="high" else "▲" if sev=="med" else "✓"}</span>'
                    f'<span style="font-size:12.5px;color:#C2C2D6;line-height:1.5;"><b style="color:var(--text-1);">{ttl}</b> — {desc}</span></div>'
                    for ttl, desc, sev in sh["flags"]])
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:1.25rem;border-color:{sh["verdict_color"]}33;position:relative;overflow:hidden;">
                  <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{sh["verdict_color"]},transparent);"></div>
                  {_mod_header("Shield")}
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1.25rem;">
                    <div style="flex:1;min-width:280px;">
                      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:1rem;">
                        <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:10px;padding:12px;">
                          <div style="font-size:20px;font-weight:800;color:#10B981;">{sh["safety_score"]}</div>
                          <div style="font-size:10px;color:var(--text-3);margin-top:2px;">Safety score</div></div>
                        <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:10px;padding:12px;">
                          <div style="font-size:20px;font-weight:800;color:#F59E0B;">{sh["suspicious_pct"]}%</div>
                          <div style="font-size:10px;color:var(--text-3);margin-top:2px;">Suspicious followers</div></div>
                        <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:10px;padding:12px;">
                          <div style="font-size:20px;font-weight:800;color:var(--text-1);">{sh["crisis_score"]}</div>
                          <div style="font-size:10px;color:var(--text-3);margin-top:2px;">Crisis risk</div></div>
                      </div>
                      <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin-bottom:.6rem;">Red-flag scan</div>
                      {flag_html}
                    </div>
                    <div style="text-align:center;min-width:150px;background:{sh["verdict_color"]}12;border:1px solid {sh["verdict_color"]}44;border-radius:14px;padding:1.25rem 1rem;">
                      <div style="font-size:10px;color:var(--text-2);text-transform:uppercase;letter-spacing:.1em;">Verdict</div>
                      <div class="disp" style="font-size:26px;font-weight:800;color:{sh["verdict_color"]};margin:6px 0;">{sh["verdict"]}</div>
                      <div style="font-size:11px;color:var(--text-2);line-height:1.5;">{sh["verdict_note"]}</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:8px;">~{sh["bot_followers"]:,} likely bot/inactive</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # ═══ AUDIENCE DNA ═══
            if "Audience" in mods:
                ad = compute_audience_dna(d, fake_score, aud_quality, roster=_roster)
                _tmc = "#10B981" if ad["true_match"] >= 65 else "#F59E0B" if ad["true_match"] >= 45 else "#EF4444"
                interest_tags = "".join([
                    f'<span style="font-size:11px;padding:4px 11px;border-radius:999px;background:#22D3EE12;'
                    f'border:1px solid #22D3EE33;color:#22D3EE;">{i}</span>' for i in ad["interests"]])
                if ad["overlap_hits"]:
                    ov_html = "".join([
                        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-top:1px solid var(--border);">'
                        f'<span style="font-size:12.5px;color:#C2C2D6;">{o["name"]}</span>'
                        f'<span style="font-size:12.5px;font-weight:700;color:{"#EF4444" if o["overlap"]>=65 else "#F59E0B" if o["overlap"]>=45 else "#10B981"};">{o["overlap"]}% overlap</span></div>'
                        for o in ad["overlap_hits"]])
                    ov_block = (f'<div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin:1rem 0 .3rem;">Roster overlap · wasted-reach detector</div>{ov_html}')
                else:
                    ov_block = '<div style="font-size:11px;color:var(--text-3);margin-top:1rem;">Analyse more creators this session to detect audience overlap across your roster.</div>'
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:1.25rem;border-color:#22D3EE22;">
                  {_mod_header("Audience")}
                  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:1rem;">
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:var(--text-1);">{ad["quality_score"]}</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Audience Quality</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:#10B981;">{ad["real_pct"]}%</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Real audience</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:{_tmc};">{ad["true_match"]}%</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">True-match to target</div></div>
                    <div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:14px;">
                      <div style="font-size:22px;font-weight:800;color:var(--text-1);">{ad["geo_conc"]}%</div>
                      <div style="font-size:11px;color:var(--text-3);margin-top:3px;">Top geo{(' · ' + ad["geo_name"]) if ad["geo_name"] else ''}</div></div>
                  </div>
                  <div style="font-size:12px;color:var(--text-2);line-height:1.6;margin-bottom:.75rem;">
                    Target: <b style="color:var(--text-1);">{ad["target_gender"]}, {ad["target_age"]}</b> —
                    {ad["true_match"]}% of this audience matches. {ad["suspicious_pct"]}% flagged suspicious.</div>
                  <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin-bottom:.5rem;">Interest affinities</div>
                  <div style="display:flex;flex-wrap:wrap;gap:6px;">{interest_tags}</div>
                  {ov_block}
                </div>
                """, unsafe_allow_html=True)

            # ═══ BENCHMARK ═══
            if "Benchmark" in mods:
                bm = compute_benchmark(d, engagement_rate, vettd_score, fake_score)
                _cd = bm["cost_delta"]; _cdc = "#10B981" if _cd < 0 else "#EF4444" if _cd > 0 else "var(--text-2)"
                look_cards = "".join([
                    f'<div style="background:var(--bg-deep);border:1px solid var(--border);border-radius:12px;padding:1rem 1.15rem;flex:1;min-width:190px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">'
                    f'<span style="font-size:13.5px;font-weight:700;color:var(--text-1);">{h}</span>'
                    f'<span style="font-size:13px;font-weight:800;color:#10B981;">{fit}</span></div>'
                    f'<div style="font-size:12px;color:#60A5FA;margin-bottom:4px;">{kind}</div>'
                    f'<div style="font-size:11px;color:var(--text-3);line-height:1.5;">{why}</div></div>'
                    for h, kind, fit, why in bm["lookalikes"]])
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:1.25rem;border-color:#60A5FA22;">
                  {_mod_header("Benchmark")}
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1.25rem;margin-bottom:1.25rem;">
                    <div style="text-align:center;min-width:150px;">
                      <div class="disp" style="font-size:52px;font-weight:800;line-height:1;color:#60A5FA;">{bm["percentile"]}<span style="font-size:20px;">th</span></div>
                      <div style="font-size:12px;color:var(--text-2);">percentile in <b style="color:var(--text-1);">{bm["category"]}</b></div>
                    </div>
                    <div style="flex:1;min-width:260px;">
                      <div class="stat-row"><span class="stat-label">Engagement vs category avg</span>
                        <span class="stat-value">{bm["creator_er"]}% vs {bm["bench_er"]}%</span></div>
                      <div class="stat-row"><span class="stat-label">Cost-efficiency</span>
                        <span class="stat-value" style="color:{_cdc};">{_cd:+d}%</span></div>
                      <div class="stat-row"><span class="stat-label">Brand saturation</span>
                        <span class="stat-value">{bm["saturation"]}/100</span></div>
                      <div style="font-size:12px;color:var(--text-2);line-height:1.6;margin-top:.75rem;">
                        {bm["cost_verdict"]}. {bm["saturation_label"]}.</div>
                    </div>
                  </div>
                  <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#10B981;margin-bottom:.6rem;">Vetted lookalike alternatives</div>
                  <div style="display:flex;gap:12px;flex-wrap:wrap;">{look_cards}</div>
                </div>
                """, unsafe_allow_html=True)

            # ═══ PULSE ═══
            if "Pulse" in mods:
                pl = compute_pulse(d, engagement_rate, fake_score)
                theme_tags = "".join([
                    f'<span style="font-size:11px;padding:4px 11px;border-radius:999px;background:#34D39912;'
                    f'border:1px solid #34D39933;color:#34D399;">{t}</span>' for t in pl["themes"]])
                _tox_c = "#EF4444" if pl["tox_flag"] else "#10B981"
                st.markdown(f"""
                <div class="section-card" style="margin-bottom:1.25rem;border-color:#34D39922;">
                  {_mod_header("Pulse")}
                  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;margin-bottom:1rem;">
                    <div style="flex:1;min-width:280px;">
                      <div style="display:flex;height:12px;border-radius:999px;overflow:hidden;">
                        <div style="width:{pl["pos"]}%;background:#10B981;"></div>
                        <div style="width:{pl["neu"]}%;background:#60A5FA;"></div>
                        <div style="width:{pl["neg"]}%;background:#EF4444;"></div></div>
                      <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-3);margin-top:7px;">
                        <span style="color:#10B981;">Positive {pl["pos"]}%</span>
                        <span style="color:#60A5FA;">Neutral {pl["neu"]}%</span>
                        <span style="color:#EF4444;">Negative {pl["neg"]}%</span></div>
                    </div>
                    <div style="text-align:center;min-width:130px;">
                      <div class="disp" style="font-size:24px;font-weight:800;color:{pl["health_color"]};">{pl["health_tier"]}</div>
                      <div style="font-size:11px;color:var(--text-3);">community health · {pl["health"]}/100</div>
                    </div>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
                    <span style="font-size:12px;color:var(--text-2);">Toxicity signal:</span>
                    <span style="font-size:12px;font-weight:700;color:{_tox_c};">{pl["toxicity"]}/100 {"⚠ flagged" if pl["tox_flag"] else "· clear"}</span>
                  </div>
                  <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin-bottom:.5rem;">Dominant comment themes</div>
                  <div style="display:flex;flex-wrap:wrap;gap:6px;">{theme_tags}</div>
                </div>
                """, unsafe_allow_html=True)

            if not mods:
                st.markdown('<div style="text-align:center;padding:3rem;color:var(--text-4);">No modules selected. Toggle modules on in the Analyse page to generate enterprise intelligence.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:var(--text-4);">Upgrade to Enterprise for the full intelligence suite — Forecast, Shield, Audience DNA, Benchmark and Pulse.</div>', unsafe_allow_html=True)

# ── EXPORTS + BACK BUTTON ──
st.markdown('<div style="border-top:1px solid var(--surface);margin-top:2rem;padding-top:1.5rem;"></div>', unsafe_allow_html=True)

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
*{{box-sizing:border-box;margin:0}} body{{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--border);background:#f4f4f8;padding:40px;}}
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
    _csv_rows = [
        ("Creator", d["creator_name"]), ("Username", d["username"]),
        ("Platform", d["platform"]), ("Niche", d["niche"]),
        ("Brand", _brand or "—"),
        ("Vettd Score", f"{vettd_score}/100"), ("Verdict", label),
        ("", ""),
        ("Followers", f"{d['followers']:,}"), ("Following", f"{d['following']:,}"),
        ("Total posts", f"{d['post_count']:,}"), ("Posts per week", d["posting_freq"]),
        ("Growth rate (30d)", f"{d['growth_rate_30d']}%"),
        ("", ""),
        ("Engagement rate", f"{engagement_rate}%"),
        ("Avg likes / reel", f"{d['avg_likes']:,}"), ("Avg comments / reel", f"{d['avg_comments']:,}"),
        ("Avg saves / reel", f"{d['avg_saves']:,}"), ("Avg shares / reel", f"{d['avg_shares']:,}"),
        ("Avg reel views", f"{d['avg_views']:,}" if d.get("avg_views") else "—"),
        ("", ""),
        ("Fake-follower score", f"{fake_score}/100"),
        ("Audience authenticity", f"{d['audience_authenticity']}%"),
        ("Brand-fit score", f"{brand_fit}/100" if has_brand else "n/a (no brand entered)"),
        ("Audience quality", f"{aud_quality}/100"),
    ]
    if tier_gate("Pro"):
        _csv_rows += [
            ("", ""),
            ("Female audience", f"{d['female_pct']}%"), ("Male audience", f"{d['male_pct']}%"),
            ("Age 18–24", f"{d['age_18_24']}%"), ("Age 25–34", f"{d['age_25_34']}%"),
            ("Age 35–44", f"{d['age_35_44']}%"), ("Age 45+", f"{d['age_45_plus']}%"),
            (f"Top location — {d['loc1_name']}", f"{d['loc1_pct']}%"),
            (f"Top location — {d['loc2_name']}", f"{d['loc2_pct']}%"),
            (f"Top location — {d['loc3_name']}", f"{d['loc3_pct']}%"),
        ]
    _csv_rows += [
        ("", ""),
        ("Est. cost / post", f"${est_cost_per_post:,.0f}"),
        ("Cost per engagement", f"${est_cpe:.4f}"),
        ("Report generated", datetime.now().strftime("%d %b %Y, %H:%M")),
    ]
    csv_df = pd.DataFrame(_csv_rows, columns=["Metric", "Value"])
    st.download_button("↓ CSV data", csv_df.to_csv(index=False),
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
