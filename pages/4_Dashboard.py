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
    calculate_market_fit_score, recommend_creators
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
    border: 1px solid #12121E;
    border-radius: 14px;
    padding: 1rem 1.25rem;
}
div[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    color: #333355 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
div[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #E8E8F0 !important;
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
        st.switch_page("app.py")
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
brand_fit = calculate_brand_fit_score(d["niche"], d["brand_industry"] or d["niche"], d["female_pct"], age_18_34, d["posting_freq"])
aud_quality = calculate_audience_quality_score(fake_score, engagement_rate, d["audience_authenticity"])
growth_score = calculate_growth_score(d["growth_rate_30d"])
consistency_score = calculate_consistency_score(d["posting_freq"])
vettd_score = calculate_vettd_score(engagement_rate, fake_score, brand_fit, aud_quality, consistency_score, growth_score)
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

# ── CREATOR HEADER ──
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:2rem;">
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="width:56px;height:56px;border-radius:50%;
        background:linear-gradient(135deg,#7C3AED,#06B6D4);
        display:flex;align-items:center;justify-content:center;
        font-size:20px;font-weight:800;color:white;">{initials}</div>
    <div>
      <div style="font-size:22px;font-weight:800;color:#E8E8F0;letter-spacing:-0.5px;">{d['creator_name']}</div>
      <div style="font-size:12px;color:#333355;margin-top:3px;">
        {d['username']} &nbsp;·&nbsp; {d['platform']} &nbsp;·&nbsp; {d['niche']}
        {f"&nbsp;·&nbsp; {d['brand_industry']}" if d['brand_industry'] else ""}
      </div>
    </div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:11px;color:#333355;margin-bottom:4px;">Vettd Score</div>
    <div style="font-size:48px;font-weight:900;line-height:1;
        background:linear-gradient(135deg,{score_color},{score_color}99);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{vettd_score}</div>
    <div style="font-size:12px;font-weight:700;color:{score_color};margin-top:2px;">{label}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TOP METRICS ROW ──
m1, m2, m3, m4, m5, m6, m7, m8 = st.columns(8)
m1.metric("Followers", f"{d['followers']:,}")
m2.metric("Engagement", f"{engagement_rate}%")
m3.metric("Fake score", f"{fake_score}/100")
m4.metric("Brand fit", f"{brand_fit}/100")
m5.metric("Avg likes", f"{d['avg_likes']:,}")
m6.metric("Avg comments", f"{d['avg_comments']:,}")
m7.metric("Est. cost/post", f"£{est_cost_per_post:,.0f}")
m8.metric("30d growth", f"{d['growth_rate_30d']}%")

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
        "Brand fit": brand_fit,
        "Aud. quality": aud_quality,
        "Consistency": consistency_score,
        "Growth": growth_score,
    }
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
        <span class="stat-value">£{est_cpe:.4f}</span></div>
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
                <span class="stat-value" style="color:#A78BFA;">{brand_fit}/100</span></div>
              <div class="stat-row"><span class="stat-label">Niche</span>
                <span class="stat-value">{d['niche']}</span></div>
              <div class="stat-row"><span class="stat-label">Brand industry</span>
                <span class="stat-value">{d['brand_industry'] or '—'}</span></div>
              <div class="stat-row"><span class="stat-label">Audience quality</span>
                <span class="stat-value">{aud_quality}/100</span></div>
              <div class="stat-row"><span class="stat-label">Consistency</span>
                <span class="stat-value">{consistency_score}/100</span></div>
              <div class="stat-row"><span class="stat-label">Growth score</span>
                <span class="stat-value">{growth_score}/100</span></div>
              <div class="stat-row"><span class="stat-label">Est. cost/post</span>
                <span class="stat-value">£{est_cost_per_post:,.0f}</span></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            fig_radar = go.Figure(go.Scatterpolar(
                r=[int(min(engagement_rate * 10, 100)), int(100 - fake_score), brand_fit, aud_quality, consistency_score, growth_score],
                theta=["Engagement", "Authenticity", "Brand fit", "Aud. quality", "Consistency", "Growth"],
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
            roi_estimate = round((engagement_rate * brand_fit * d["audience_authenticity"]) / 1000, 1)
            virality_score = round((d["avg_shares"] / max(d["followers"], 1)) * 1000 + d["growth_rate_30d"] * 5, 1)
            loyalty_score = round((d["avg_saves"] + d["avg_comments"]) / max(d["followers"] / 100, 1), 1)
            inactive_pct = round(100 - d["audience_authenticity"] * 0.8, 1)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="section-card">
                  <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                      color:#333355;margin-bottom:1rem;">Predictive intelligence</div>
                  <div class="stat-row"><span class="stat-label">ROI potential</span>
                    <span class="stat-value" style="color:#10B981;">{min(roi_estimate,100)}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Virality likelihood</span>
                    <span class="stat-value">{min(virality_score,100):.1f}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Audience loyalty</span>
                    <span class="stat-value">{min(loyalty_score,100):.1f}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Inactive follower est.</span>
                    <span class="stat-value" style="color:#F59E0B;">{inactive_pct}%</span></div>
                  <div class="stat-row"><span class="stat-label">Buyer intent</span>
                    <span class="stat-value">{d['buyer_intent']}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Comment sentiment</span>
                    <span class="stat-value">{d['sentiment_score']}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Brand safety</span>
                    <span class="stat-value" style="color:#10B981;">{d['brand_safety']}/100</span></div>
                  <div class="stat-row"><span class="stat-label">Crisis risk</span>
                    <span class="stat-value" style="color:{'#10B981' if d['crisis_risk']=='Low' else '#F59E0B' if d['crisis_risk']=='Medium' else '#EF4444'};">
                      {d['crisis_risk']}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="section-card">
                  <div style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                      color:#333355;margin-bottom:1rem;">Auto campaign brief</div>
                  <div class="brief-block">
                    <b style="color:#A78BFA;">Creator:</b> {d['creator_name']} ({d['username']})<br>
                    <b style="color:#A78BFA;">Platform:</b> {d['platform']} &nbsp;|&nbsp;
                    <b style="color:#A78BFA;">Niche:</b> {d['niche']}<br>
                    <b style="color:#A78BFA;">Recommended for:</b> {d['brand_industry'] or d['niche']} campaigns<br>
                    <b style="color:#A78BFA;">Audience:</b> {d['female_pct']}% female, peak age 18–34<br>
                    <b style="color:#A78BFA;">Post format:</b> {'Reels / short-form video' if d['platform'] in ['Instagram','TikTok'] else 'Long-form video'}<br>
                    <b style="color:#A78BFA;">Est. cost/post:</b> £{est_cost_per_post:,.0f}<br>
                    <b style="color:#A78BFA;">Key strength:</b> {'High engagement' if engagement_rate > 5 else 'Broad reach'}, {d['audience_authenticity']}% authentic<br>
                    <b style="color:#A78BFA;">Brand safety:</b> {d['crisis_risk']} risk
                  </div>
                </div>
                """, unsafe_allow_html=True)

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
with exp1:
    df = pd.DataFrame([report_data])
    st.download_button("↓ Download CSV", df.to_csv(index=False),
        f"vettd_{d['username'].replace('@','')}.csv", "text/csv", use_container_width=True)
with exp2:
    st.download_button("↓ Download report", json.dumps(report_data, indent=2),
        f"vettd_{d['username'].replace('@','')}.json", use_container_width=True)
with exp3:
    report_id = hashlib.md5(f"{d['creator_name']}{d['username']}".encode()).hexdigest()[:8]
    st.text_input("Share link", value=f"https://get-vettd.streamlit.app/r/{report_id}",
        disabled=True, label_visibility="collapsed")
with exp4:
    if st.button("← Analyse another creator", use_container_width=True):
        st.switch_page("app.py")
