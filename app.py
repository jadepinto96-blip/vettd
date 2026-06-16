import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import hashlib
from datetime import datetime
from utils.styles import GLOBAL_CSS
from utils.scoring import (
    calculate_engagement_rate, estimate_fake_follower_score,
    calculate_brand_fit_score, calculate_audience_quality_score,
    calculate_growth_score, calculate_consistency_score,
    calculate_vettd_score, score_label, estimate_cpe
)

st.set_page_config(page_title="Vettd — Creator Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #0A0A0F;
    color: #E8E8F0;
}

[data-testid="stSidebar"] {
    background: #0F0F18 !important;
    border-right: 1px solid #1E1E2E;
}

[data-testid="stSidebar"] * {
    color: #C8C8D8 !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #1A1A28 !important;
    border: 1px solid #2A2A3E !important;
    color: #E8E8F0 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stSlider > div > div > div {
    background: #7C3AED !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0F0F18;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E1E2E;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8888A8;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    padding: 8px 20px;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: #1E1E3A !important;
    color: #A78BFA !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #4F46E5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    padding: 0.6rem 1.5rem;
    width: 100%;
    transition: opacity 0.2s;
}

.stButton > button:hover {
    opacity: 0.85;
    color: white;
}

div[data-testid="stMetric"] {
    background: #0F0F18;
    border: 1px solid #1E1E2E;
    border-radius: 14px;
    padding: 1rem 1.25rem;
}

div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: #666688 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

div[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #E8E8F0 !important;
}

div[data-testid="stMetricDelta"] {
    font-size: 11px !important;
}

.score-card {
    background: #0F0F18;
    border: 1px solid #1E1E2E;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
}

.score-number {
    font-size: 72px;
    font-weight: 700;
    line-height: 1;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.score-label-text {
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 8px;
}

.section-card {
    background: #0F0F18;
    border: 1px solid #1E1E2E;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1A1A28;
    font-size: 13px;
}

.stat-row:last-child { border-bottom: none; }

.stat-label { color: #666688; }
.stat-value { color: #E8E8F0; font-weight: 600; }

.progress-bar-bg {
    background: #1A1A28;
    border-radius: 999px;
    height: 6px;
    margin: 4px 0 10px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #7C3AED, #60A5FA);
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.badge-starter { background: #1A1A28; color: #8888A8; }
.badge-pro { background: #1E2A3E; color: #60A5FA; }
.badge-enterprise { background: #1E1A2E; color: #A78BFA; }

.header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 0;
    border-bottom: 1px solid #1E1E2E;
    margin-bottom: 1.5rem;
}

.creator-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED, #4F46E5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    color: white;
}

.insight-pill {
    display: inline-block;
    background: #1A1A28;
    border: 1px solid #2A2A3E;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 12px;
    color: #A0A0C0;
    margin: 3px;
}

.brief-block {
    background: #0A0A14;
    border: 1px solid #1E1E2E;
    border-left: 3px solid #7C3AED;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    font-size: 13px;
    color: #B0B0CC;
    line-height: 1.8;
    margin-top: 0.5rem;
}

.divider { border-top: 1px solid #1E1E2E; margin: 1.5rem 0; }

.logo-text {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-section {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #44445A !important;
    margin: 1.2rem 0 0.5rem;
}

[data-testid="stDownloadButton"] button {
    background: #1A1A28 !important;
    color: #A78BFA !important;
    border: 1px solid #2A2A3E !important;
    font-size: 13px !important;
}

.stTextInput input[disabled] {
    background: #0A0A14 !important;
    border: 1px solid #1E1E2E !important;
    color: #6666AA !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

TIERS = {"Starter": 1, "Pro": 2, "Enterprise": 3}

def tier_gate(required, current):
    return TIERS[current] >= TIERS[required]

with st.sidebar:
    st.markdown('<div class="logo-text">✦ Vettd</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#44445A;margin-top:2px;margin-bottom:1rem;">Creator intelligence for brands</div>', unsafe_allow_html=True)

    tier = st.selectbox("Plan", ["Starter", "Pro", "Enterprise"], index=1)

    st.markdown('<div class="sidebar-section">Creator</div>', unsafe_allow_html=True)
    creator_name = st.text_input("Name", placeholder="Emma Williams")
    username = st.text_input("Username", placeholder="@emmalifestyle")
    platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
    niche = st.selectbox("Niche", ["Fashion", "Fitness", "Beauty", "Tech", "Food", "Travel", "Gaming", "Lifestyle", "Finance", "Parenting", "Other"])
    brand_industry = st.text_input("Your brand industry", placeholder="e.g. Fashion, Beauty")

    st.markdown('<div class="sidebar-section">Profile</div>', unsafe_allow_html=True)
    followers = st.number_input("Followers", min_value=0, value=150000, step=1000)
    following = st.number_input("Following", min_value=0, value=800, step=10)
    post_count = st.number_input("Total posts", min_value=0, value=420)
    posting_freq = st.slider("Posts per week", 0.0, 14.0, 4.0, 0.5)
    growth_rate_30d = st.slider("Growth rate 30d %", -5.0, 20.0, 2.5, 0.1)

    st.markdown('<div class="sidebar-section">Engagement</div>', unsafe_allow_html=True)
    avg_likes = st.number_input("Avg likes", min_value=0, value=8500, step=100)
    avg_comments = st.number_input("Avg comments", min_value=0, value=320, step=10)
    avg_saves = st.number_input("Avg saves", min_value=0, value=1200, step=50)
    avg_shares = st.number_input("Avg shares", min_value=0, value=450, step=10)

    if tier_gate("Pro", tier):
        st.markdown('<div class="sidebar-section">Audience</div>', unsafe_allow_html=True)
        female_pct = st.slider("Female %", 0, 100, 65)
        male_pct = 100 - female_pct
        audience_authenticity = st.slider("Authenticity %", 0, 100, 82)
        age_18_24 = st.slider("Age 18–24 %", 0, 100, 28)
        age_25_34 = st.slider("Age 25–34 %", 0, 100, 35)
        age_35_44 = st.slider("Age 35–44 %", 0, 100, 20)
        age_45_plus = max(0, 100 - age_18_24 - age_25_34 - age_35_44)
        loc1_name = st.text_input("Top location 1", value="United Kingdom")
        loc1_pct = st.slider("Location 1 %", 0, 100, 42)
        loc2_name = st.text_input("Top location 2", value="United States")
        loc2_pct = st.slider("Location 2 %", 0, 100, 28)
        loc3_name = st.text_input("Top location 3", value="Australia")
        loc3_pct = st.slider("Location 3 %", 0, 100, 12)
    else:
        female_pct, male_pct = 60, 40
        audience_authenticity = 75
        age_18_24, age_25_34, age_35_44, age_45_plus = 30, 35, 20, 15
        loc1_name, loc1_pct = "United Kingdom", 42
        loc2_name, loc2_pct = "United States", 28
        loc3_name, loc3_pct = "Australia", 12

    if tier_gate("Enterprise", tier):
        st.markdown('<div class="sidebar-section">Advanced</div>', unsafe_allow_html=True)
        buyer_intent = st.slider("Buyer intent score", 0, 100, 65)
        sentiment_score = st.slider("Comment sentiment", 0, 100, 78)
        brand_safety = st.slider("Brand safety score", 0, 100, 88)
        crisis_risk = st.selectbox("Crisis risk", ["Low", "Medium", "High"])
    else:
        buyer_intent, sentiment_score, brand_safety, crisis_risk = 60, 70, 80, "Low"

    st.markdown("<br>", unsafe_allow_html=True)
    analyse = st.button("✦ Run analysis", use_container_width=True)

if not creator_name:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:70vh;text-align:center;">
        <div style="font-size:48px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-2px;">✦ Vettd</div>
        <div style="font-size:16px;color:#44445A;margin-top:8px;">Creator intelligence for brands</div>
        <div style="margin-top:2rem;font-size:13px;color:#33334A;background:#0F0F18;border:1px solid #1E1E2E;border-radius:12px;padding:1rem 2rem;">Enter creator details in the sidebar to generate a report</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

engagement_rate = calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves)
fake_score = estimate_fake_follower_score(followers, following, avg_likes, avg_comments)
age_18_34 = age_18_24 + age_25_34
brand_fit = calculate_brand_fit_score(niche, brand_industry or niche, female_pct, age_18_34, posting_freq)
aud_quality = calculate_audience_quality_score(fake_score, engagement_rate, audience_authenticity)
growth_score = calculate_growth_score(growth_rate_30d)
consistency_score = calculate_consistency_score(posting_freq)
vettd_score = calculate_vettd_score(engagement_rate, fake_score, brand_fit, aud_quality, consistency_score, growth_score)
label, label_color = score_label(vettd_score)
est_cost_per_post, est_cpe = estimate_cpe(followers, engagement_rate)

score_colors = {
    "Exceptional": "#10B981",
    "Strong fit": "#60A5FA",
    "Moderate fit": "#F59E0B",
    "Weak fit": "#F97316",
    "Not recommended": "#EF4444",
}
score_color = score_colors.get(label, "#A78BFA")

initials = "".join([w[0].upper() for w in creator_name.split()[:2]])
badge_class = tier.lower() + "-badge"

st.markdown(f"""
<div class="header-bar">
    <div style="display:flex;align-items:center;gap:14px;">
        <div class="creator-avatar">{initials}</div>
        <div>
            <div style="font-size:20px;font-weight:700;color:#E8E8F0;">{creator_name}</div>
            <div style="font-size:12px;color:#44445A;margin-top:2px;">{username} &nbsp;·&nbsp; {platform} &nbsp;·&nbsp; {niche} &nbsp;·&nbsp; {datetime.now().strftime('%d %b %Y')}</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
        <span class="badge badge-{tier.lower()}">{tier}</span>
        <div style="font-size:11px;color:#44445A;">powered by <span style="color:#7C3AED;font-weight:600;">Vettd</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

col_score, col_right = st.columns([1, 3], gap="large")

with col_score:
    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#44445A;margin-bottom:12px;">Vettd Score</div>
        <div class="score-number" style="background:linear-gradient(135deg,{score_color},{score_color}AA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{vettd_score}</div>
        <div class="score-label-text" style="color:{score_color};">{label}</div>
        <div style="margin-top:1.5rem;border-top:1px solid #1E1E2E;padding-top:1.25rem;">
    """, unsafe_allow_html=True)

    components = {
        "Engagement": min(engagement_rate * 10, 100),
        "Authenticity": 100 - fake_score,
        "Brand fit": brand_fit,
        "Aud. quality": aud_quality,
        "Consistency": consistency_score,
        "Growth": growth_score,
    }

    if tier_gate("Pro", tier):
        for k, v in components.items():
            v_int = int(round(v))
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;">
                <span style="color:#666688;">{k}</span>
                <span style="color:#A0A0C0;font-weight:600;">{v_int}</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{v_int}%"></div></div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px;color:#44445A;text-align:center;padding:0.5rem 0;">Score breakdown unlocked in Pro</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

with col_right:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Followers", f"{followers:,}")
    m2.metric("Engagement rate", f"{engagement_rate}%")
    m3.metric("Fake follower score", f"{fake_score}/100")
    m4.metric("Brand fit", f"{brand_fit}/100")

    m5, m6, m7, m8 = st.columns(4)
    m5.metric("Avg likes", f"{avg_likes:,}")
    m6.metric("Avg comments", f"{avg_comments:,}")
    m7.metric("Est. cost/post", f"£{est_cost_per_post:,.0f}")
    m8.metric("30d growth", f"{growth_rate_30d}%")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["  Engagement  ", "  Audience  ", "  Brand fit  ", "  Advanced  "])

    plot_bg = "rgba(0,0,0,0)"
    plot_paper = "rgba(0,0,0,0)"
    axis_color = "#2A2A3E"
    text_color = "#8888A8"

    with tab1:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig = go.Figure(go.Bar(
                x=["Likes", "Comments", "Saves", "Shares"],
                y=[avg_likes, avg_comments, avg_saves, avg_shares],
                marker=dict(
                    color=["#7C3AED", "#4F46E5", "#60A5FA", "#A78BFA"],
                    line=dict(width=0)
                ),
                text=[f"{v:,}" for v in [avg_likes, avg_comments, avg_saves, avg_shares]],
                textposition="outside",
                textfont=dict(color=text_color, size=11),
            ))
            fig.update_layout(
                title=dict(text="Avg interactions per post", font=dict(color=text_color, size=12)),
                height=260, margin=dict(t=40, b=10, l=10, r=10),
                paper_bgcolor=plot_paper, plot_bgcolor=plot_bg,
                xaxis=dict(showgrid=False, color=text_color, tickfont=dict(color=text_color)),
                yaxis=dict(showgrid=True, gridcolor=axis_color, color=text_color, tickfont=dict(color=text_color)),
                bargap=0.3,
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            like_comment_ratio = round(avg_likes / max(avg_comments, 1), 1)
            save_rate = round((avg_saves / max(followers, 1)) * 100, 2)
            share_rate = round((avg_shares / max(followers, 1)) * 100, 2)
            st.markdown(f"""
            <div class="section-card">
                <div class="stat-row"><span class="stat-label">Like:comment ratio</span><span class="stat-value">{like_comment_ratio}:1</span></div>
                <div class="stat-row"><span class="stat-label">Save rate</span><span class="stat-value">{save_rate}%</span></div>
                <div class="stat-row"><span class="stat-label">Share rate</span><span class="stat-value">{share_rate}%</span></div>
                <div class="stat-row"><span class="stat-label">Posts/week</span><span class="stat-value">{posting_freq}</span></div>
                <div class="stat-row"><span class="stat-label">Est. cost/post</span><span class="stat-value">£{est_cost_per_post:,.0f}</span></div>
                <div class="stat-row"><span class="stat-label">Cost per engagement</span><span class="stat-value">£{est_cpe:.4f}</span></div>
                <div class="stat-row"><span class="stat-label">Total posts</span><span class="stat-value">{post_count:,}</span></div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if tier_gate("Pro", tier):
            c1, c2 = st.columns(2)
            with c1:
                fig_gender = go.Figure(go.Pie(
                    labels=["Female", "Male"],
                    values=[female_pct, male_pct],
                    marker=dict(colors=["#7C3AED", "#4F46E5"], line=dict(width=0)),
                    hole=0.65,
                    textfont=dict(color="white", size=12),
                ))
                fig_gender.add_annotation(text=f"{female_pct}%<br>Female", x=0.5, y=0.5, font=dict(size=14, color="#A78BFA"), showarrow=False)
                fig_gender.update_layout(
                    title=dict(text="Gender split", font=dict(color=text_color, size=12)),
                    height=240, margin=dict(t=40, b=10, l=10, r=10),
                    paper_bgcolor=plot_paper, showlegend=True,
                    legend=dict(font=dict(color=text_color), bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig_gender, use_container_width=True)
            with c2:
                age_labels = ["18–24", "25–34", "35–44", "45+"]
                age_values = [age_18_24, age_25_34, age_35_44, age_45_plus]
                fig_age = go.Figure(go.Bar(
                    x=age_labels, y=age_values,
                    marker=dict(color=["#7C3AED","#5B4FCC","#4F46E5","#3730A3"], line=dict(width=0)),
                    text=[f"{v}%" for v in age_values],
                    textposition="outside",
                    textfont=dict(color=text_color, size=11),
                ))
                fig_age.update_layout(
                    title=dict(text="Age breakdown", font=dict(color=text_color, size=12)),
                    height=240, margin=dict(t=40, b=10, l=10, r=10),
                    paper_bgcolor=plot_paper, plot_bgcolor=plot_bg,
                    xaxis=dict(showgrid=False, color=text_color, tickfont=dict(color=text_color)),
                    yaxis=dict(showgrid=True, gridcolor=axis_color, tickfont=dict(color=text_color)),
                    bargap=0.3,
                )
                st.plotly_chart(fig_age, use_container_width=True)

            st.markdown(f"""
            <div class="section-card">
                <div style="font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#44445A;margin-bottom:12px;">Top audience locations</div>
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;"><span style="color:#8888A8;">{loc1_name}</span><span style="color:#A78BFA;font-weight:600;">{loc1_pct}%</span></div>
                <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{loc1_pct}%"></div></div>
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;"><span style="color:#8888A8;">{loc2_name}</span><span style="color:#A78BFA;font-weight:600;">{loc2_pct}%</span></div>
                <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{loc2_pct}%"></div></div>
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;"><span style="color:#8888A8;">{loc3_name}</span><span style="color:#A78BFA;font-weight:600;">{loc3_pct}%</span></div>
                <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{loc3_pct}%"></div></div>
                <div style="margin-top:12px;border-top:1px solid #1A1A28;padding-top:12px;">
                    <div class="stat-row"><span class="stat-label">Audience authenticity</span><span class="stat-value" style="color:#10B981;">{audience_authenticity}%</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:#44445A;font-size:14px;">Upgrade to Pro to unlock audience demographics</div>', unsafe_allow_html=True)

    with tab3:
        c1, c2 = st.columns([2, 3])
        with c1:
            st.markdown(f"""
            <div class="section-card">
                <div style="font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#44445A;margin-bottom:12px;">Brand intelligence</div>
                <div class="stat-row"><span class="stat-label">Brand-fit score</span><span class="stat-value" style="color:#A78BFA;">{brand_fit}/100</span></div>
                <div class="stat-row"><span class="stat-label">Creator niche</span><span class="stat-value">{niche}</span></div>
                <div class="stat-row"><span class="stat-label">Brand industry</span><span class="stat-value">{brand_industry or "—"}</span></div>
                <div class="stat-row"><span class="stat-label">Audience quality</span><span class="stat-value">{aud_quality}/100</span></div>
                <div class="stat-row"><span class="stat-label">Consistency score</span><span class="stat-value">{consistency_score}/100</span></div>
                <div class="stat-row"><span class="stat-label">Growth score</span><span class="stat-value">{growth_score}/100</span></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            fig_radar = go.Figure(go.Scatterpolar(
                r=[int(min(engagement_rate * 10, 100)), int(100 - fake_score), brand_fit, aud_quality, consistency_score, growth_score],
                theta=["Engagement", "Authenticity", "Brand fit", "Aud. quality", "Consistency", "Growth"],
                fill="toself",
                fillcolor="rgba(124, 58, 237, 0.15)",
                line=dict(color="#7C3AED", width=2),
                marker=dict(color="#A78BFA", size=6),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color=text_color, size=9), gridcolor=axis_color, linecolor=axis_color),
                    angularaxis=dict(tickfont=dict(color=text_color, size=11), gridcolor=axis_color, linecolor=axis_color),
                ),
                height=300, margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor=plot_paper,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    with tab4:
        if tier_gate("Enterprise", tier):
            c1, c2 = st.columns(2)
            roi_estimate = round((engagement_rate * brand_fit * audience_authenticity) / 1000, 1)
            virality_score = round((avg_shares / max(followers, 1)) * 1000 + growth_rate_30d * 5, 1)
            loyalty_score = round((avg_saves + avg_comments) / max(followers / 100, 1), 1)
            inactive_pct = round(100 - audience_authenticity * 0.8, 1)
            with c1:
                st.markdown(f"""
                <div class="section-card">
                    <div style="font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#44445A;margin-bottom:12px;">Predictive intelligence</div>
                    <div class="stat-row"><span class="stat-label">ROI potential</span><span class="stat-value" style="color:#10B981;">{min(roi_estimate,100)}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Virality likelihood</span><span class="stat-value">{min(virality_score,100):.1f}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Audience loyalty</span><span class="stat-value">{min(loyalty_score,100):.1f}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Inactive follower est.</span><span class="stat-value" style="color:#F59E0B;">{inactive_pct}%</span></div>
                    <div class="stat-row"><span class="stat-label">Buyer intent</span><span class="stat-value">{buyer_intent}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Comment sentiment</span><span class="stat-value">{sentiment_score}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Brand safety</span><span class="stat-value" style="color:#10B981;">{brand_safety}/100</span></div>
                    <div class="stat-row"><span class="stat-label">Crisis risk</span><span class="stat-value" style="color:{'#10B981' if crisis_risk=='Low' else '#F59E0B' if crisis_risk=='Medium' else '#EF4444'};">{crisis_risk}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="section-card">
                    <div style="font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#44445A;margin-bottom:12px;">Auto campaign brief</div>
                    <div class="brief-block">
                        <b style="color:#A78BFA;">Creator:</b> {creator_name} ({username})<br>
                        <b style="color:#A78BFA;">Platform:</b> {platform} &nbsp;|&nbsp; <b style="color:#A78BFA;">Niche:</b> {niche}<br>
                        <b style="color:#A78BFA;">Recommended for:</b> {brand_industry or niche} campaigns<br>
                        <b style="color:#A78BFA;">Audience:</b> {female_pct}% female, peak age 18–34<br>
                        <b style="color:#A78BFA;">Post format:</b> {'Reels / short-form video' if platform in ['Instagram','TikTok'] else 'Long-form video'}<br>
                        <b style="color:#A78BFA;">Est. cost/post:</b> £{est_cost_per_post:,.0f}<br>
                        <b style="color:#A78BFA;">Strength:</b> {'High engagement' if engagement_rate > 5 else 'Broad reach'}, {audience_authenticity}% authentic audience<br>
                        <b style="color:#A78BFA;">Brand safety:</b> {crisis_risk} risk
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:3rem;color:#44445A;font-size:14px;">Upgrade to Enterprise to unlock predictive intelligence and campaign briefs</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

report_data = {
    "creator": creator_name, "username": username, "platform": platform, "niche": niche,
    "followers": followers, "engagement_rate": engagement_rate,
    "fake_follower_score": fake_score, "brand_fit_score": brand_fit,
    "vettd_score": vettd_score, "vettd_label": label,
    "est_cost_per_post": est_cost_per_post,
    "generated_at": datetime.now().isoformat()
}

col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    df = pd.DataFrame([report_data])
    st.download_button("↓ Download CSV", df.to_csv(index=False), f"vettd_{username.replace('@','')}.csv", "text/csv", use_container_width=True)
with col_e2:
    report_id = hashlib.md5(f"{creator_name}{username}".encode()).hexdigest()[:8]
    st.text_input("Shareable link", value=f"https://vettd.app/r/{report_id}", disabled=True, label_visibility="collapsed")
with col_e3:
    if tier_gate("Pro", tier):
        st.download_button("↓ Download report", json.dumps(report_data, indent=2), f"vettd_{username.replace('@','')}.json", use_container_width=True)
    else:
        st.button("↓ PDF report (Pro+)", disabled=True, use_container_width=True)
