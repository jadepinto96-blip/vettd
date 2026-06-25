import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS, SITE_FOOTER
from utils.scoring import (
    calculate_engagement_rate, estimate_fake_follower_score,
    calculate_brand_fit_score, calculate_audience_quality_score,
    calculate_growth_score, calculate_consistency_score,
    calculate_vettd_score, score_label, estimate_cpe
)

st.set_page_config(page_title="Compare creators — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding:0 2rem 3rem !important; max-width:100% !important; }
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
.disp { font-family:'Space Grotesk','Inter',sans-serif; }
.cmp-card { background:#101019; border:1px solid #14142A; border-radius:18px; padding:1.5rem;
  transition:border-color .4s, transform .4s cubic-bezier(.16,1,.3,1); }
.cmp-stat { display:flex; justify-content:space-between; align-items:center; padding:8px 0;
  border-bottom:1px solid #0D0D1A; font-size:13px; }
.cmp-stat:last-child { border-bottom:none; }
.cmp-label { color:#5A5A78; } .cmp-val { color:#EDEDF5; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div style="font-family:'Inter',sans-serif;">
<nav style="position:sticky;top:0;z-index:100;padding:1.1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;background:rgba(11,11,22,.75);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.04);margin:0 -2rem 0;">
<a href="/" target="_self" class="brandmark" style="font-size:20px;font-weight:700;background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ VETTD</a>
<div style="display:flex;gap:2rem;align-items:center;">
<a href="/Analyse" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Analyse one</a>
<a href="/Compare" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Compare</a>
<a href="/About" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">About</a>
<a href="/Contact" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Contact</a>
</div>
</nav>
</div>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div style="text-align:center;padding:3rem 1rem 2rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1rem;">Side by side</div>
<h1 class="disp" style="font-size:clamp(34px,5vw,52px);font-weight:700;letter-spacing:-.03em;margin:0 0 .75rem;background:linear-gradient(135deg,#FFFFFF,#A78BFA 60%,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Compare creators.</h1>
<p style="font-size:15px;color:#5A5A78;max-width:520px;margin:0 auto;line-height:1.7;">Enter up to three creators and Vettd will score each, overlay them, and tell you who to pick.</p>
</div>
""", unsafe_allow_html=True)

# ── SHARED BRAND INDUSTRY ──
mid = st.columns([1, 2, 1])[1]
with mid:
    brand_industry = st.text_input("Your brand industry (used for brand-fit scoring)", placeholder="e.g. Fashion, Beauty, Tech")

st.markdown("<br>", unsafe_allow_html=True)

# ── THREE INPUT COLUMNS ──
defaults = [
    {"name": "Creator A", "user": "@creatora", "niche": "Fashion", "followers": 150000, "following": 800,
     "likes": 8500, "comments": 320, "saves": 1200, "shares": 450, "freq": 4.0, "growth": 2.5, "auth": 82},
    {"name": "Creator B", "user": "@creatorb", "niche": "Lifestyle", "followers": 320000, "following": 1500,
     "likes": 11000, "comments": 280, "saves": 900, "shares": 300, "freq": 3.0, "growth": 1.2, "auth": 70},
    {"name": "Creator C", "user": "@creatorc", "niche": "Beauty", "followers": 85000, "following": 400,
     "likes": 6800, "comments": 410, "saves": 1500, "shares": 620, "freq": 5.0, "growth": 4.8, "auth": 90},
]
niches = ["Fashion", "Fitness", "Beauty", "Tech", "Food", "Travel", "Gaming", "Lifestyle", "Finance", "Parenting", "Other"]

cols = st.columns(3, gap="medium")
accent = ["#A78BFA", "#60A5FA", "#22D3EE"]
inputs = []

for i, col in enumerate(cols):
    with col:
        dft = defaults[i]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:.75rem;">
          <div style="width:10px;height:10px;border-radius:50%;background:{accent[i]};box-shadow:0 0 8px {accent[i]};"></div>
          <span style="font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:{accent[i]};">Creator {chr(65+i)}</span>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Name", value=dft["name"], key=f"name{i}")
        user = st.text_input("Username", value=dft["user"], key=f"user{i}")
        niche = st.selectbox("Niche", niches, index=niches.index(dft["niche"]), key=f"niche{i}")
        followers = st.number_input("Followers", min_value=0, value=dft["followers"], step=1000, key=f"fol{i}")
        following = st.number_input("Following", min_value=0, value=dft["following"], step=10, key=f"flw{i}")
        likes = st.number_input("Avg likes", min_value=0, value=dft["likes"], step=100, key=f"lk{i}")
        comments = st.number_input("Avg comments", min_value=0, value=dft["comments"], step=10, key=f"cm{i}")
        saves = st.number_input("Avg saves", min_value=0, value=dft["saves"], step=50, key=f"sv{i}")
        shares = st.number_input("Avg shares", min_value=0, value=dft["shares"], step=10, key=f"sh{i}")
        freq = st.number_input("Posts/week", min_value=0.0, value=dft["freq"], step=0.5, key=f"fq{i}")
        growth = st.number_input("Growth 30d %", min_value=-10.0, value=dft["growth"], step=0.1, key=f"gr{i}")
        auth = st.slider("Audience authenticity %", 0, 100, dft["auth"], key=f"au{i}")
        inputs.append(dict(name=name, user=user, niche=niche, followers=followers, following=following,
                           likes=likes, comments=comments, saves=saves, shares=shares,
                           freq=freq, growth=growth, auth=auth))

st.markdown("<br>", unsafe_allow_html=True)
run = st.columns([1, 2, 1])[1].button("✦ Compare creators", use_container_width=True)

if run:
    results = []
    for c in inputs:
        er = calculate_engagement_rate(c["followers"], c["likes"], c["comments"], c["saves"])
        fake = estimate_fake_follower_score(c["followers"], c["following"], c["likes"], c["comments"])
        bf = calculate_brand_fit_score(c["niche"], brand_industry or c["niche"], 60, 60, c["freq"])
        aq = calculate_audience_quality_score(fake, er, c["auth"])
        gs = calculate_growth_score(c["growth"])
        cs = calculate_consistency_score(c["freq"])
        vs = calculate_vettd_score(er, fake, bf, aq, cs, gs)
        label, _ = score_label(vs)
        cpp, cpe = estimate_cpe(c["followers"], er)
        results.append(dict(**c, er=er, fake=fake, bf=bf, aq=aq, gs=gs, cs=cs, vs=vs, label=label, cpp=cpp, cpe=cpe))

    winner = max(range(len(results)), key=lambda k: results[k]["vs"])
    w = results[winner]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── WINNER BANNER ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(124,58,237,.12),rgba(34,211,238,.08));
      border:1px solid rgba(124,58,237,.35);border-radius:20px;padding:1.75rem 2rem;margin-bottom:2rem;
      display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#60A5FA,#22D3EE);"></div>
      <div>
        <div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#22D3EE;margin-bottom:6px;">Recommended pick</div>
        <div class="disp" style="font-size:26px;font-weight:700;color:#EDEDF5;">{w['name']} <span style="color:#5A5A78;font-size:15px;font-weight:400;">{w['user']}</span></div>
        <div style="font-size:13px;color:#8888A8;margin-top:6px;max-width:520px;line-height:1.6;">
          Highest Vettd Score of the group at <b style="color:#A78BFA;">{w['vs']}/100</b> —
          {'strong engagement' if w['er']>5 else 'solid reach'}, {w['auth']}% authentic audience,
          and the best balance of brand-fit and growth for {brand_industry or w['niche']}.
        </div>
      </div>
      <div style="text-align:center;flex-shrink:0;">
        <div class="disp" style="font-size:56px;font-weight:700;line-height:1;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{w['vs']}</div>
        <div style="font-size:12px;font-weight:600;color:#22D3EE;">{w['label']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── COMPARISON CARDS ──
    rcols = st.columns(3, gap="medium")
    for i, (col, r) in enumerate(zip(rcols, results)):
        is_w = i == winner
        border = f"2px solid {accent[i]}" if is_w else "1px solid #14142A"
        crown = '<span style="font-size:11px;font-weight:700;color:#22D3EE;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.3);padding:2px 10px;border-radius:999px;">★ TOP PICK</span>' if is_w else ''
        with col:
            st.markdown(f"""
            <div class="cmp-card" style="border:{border};">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
                <div>
                  <div style="font-size:16px;font-weight:700;color:#EDEDF5;">{r['name']}</div>
                  <div style="font-size:12px;color:#3A3A52;">{r['user']} · {r['niche']}</div>
                </div>{crown}
              </div>
              <div style="text-align:center;padding:1rem 0;border-top:1px solid #0D0D1A;border-bottom:1px solid #0D0D1A;margin-bottom:1rem;">
                <div class="disp" style="font-size:44px;font-weight:700;line-height:1;background:linear-gradient(135deg,{accent[i]},#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{r['vs']}</div>
                <div style="font-size:12px;font-weight:600;color:{accent[i]};margin-top:4px;">{r['label']}</div>
              </div>
              <div class="cmp-stat"><span class="cmp-label">Followers</span><span class="cmp-val">{r['followers']:,}</span></div>
              <div class="cmp-stat"><span class="cmp-label">Engagement</span><span class="cmp-val">{r['er']}%</span></div>
              <div class="cmp-stat"><span class="cmp-label">Fake score</span><span class="cmp-val">{r['fake']}/100</span></div>
              <div class="cmp-stat"><span class="cmp-label">Brand fit</span><span class="cmp-val">{r['bf']}/100</span></div>
              <div class="cmp-stat"><span class="cmp-label">Aud. quality</span><span class="cmp-val">{r['aq']}/100</span></div>
              <div class="cmp-stat"><span class="cmp-label">Growth</span><span class="cmp-val">{r['gs']}/100</span></div>
              <div class="cmp-stat"><span class="cmp-label">Est. cost/post</span><span class="cmp-val">£{r['cpp']:,.0f}</span></div>
              <div class="cmp-stat"><span class="cmp-label">Cost/engagement</span><span class="cmp-val">£{r['cpe']:.4f}</span></div>
            </div>
            """, unsafe_allow_html=True)

    # ── RADAR OVERLAY ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#3A3A52;margin-bottom:.5rem;">Signal overlay</div>', unsafe_allow_html=True)
    cats = ["Engagement", "Authenticity", "Brand fit", "Aud. quality", "Consistency", "Growth"]
    accent_rgba = ["rgba(167,139,250,0.10)", "rgba(96,165,250,0.10)", "rgba(34,211,238,0.10)"]
    fig = go.Figure()
    for i, r in enumerate(results):
        fig.add_trace(go.Scatterpolar(
            r=[int(min(r["er"]*10, 100)), int(100-r["fake"]), r["bf"], r["aq"], r["cs"], r["gs"]],
            theta=cats, fill="toself", name=r["name"],
            line=dict(color=accent[i], width=2),
            fillcolor=accent_rgba[i],
        ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#3A3A52", size=9), gridcolor="#14142A", linecolor="#14142A"),
            angularaxis=dict(tickfont=dict(color="#5A5A78", size=11), gridcolor="#14142A", linecolor="#14142A")),
        height=420, margin=dict(t=30,b=30,l=60,r=60), paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#8888A8"), bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.1),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── SCORE BAR COMPARISON ──
    fig2 = go.Figure()
    names = [r["name"] for r in results]
    fig2.add_trace(go.Bar(
        x=names, y=[r["vs"] for r in results],
        marker=dict(color=accent[:len(results)], line=dict(width=0)),
        text=[f"{r['vs']}" for r in results], textposition="outside",
        textfont=dict(color="#8888A8", size=14),
    ))
    fig2.update_layout(
        title=dict(text="Vettd Score comparison", font=dict(color="#5A5A78", size=12)),
        height=300, margin=dict(t=40,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#5A5A78", tickfont=dict(color="#8888A8", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#14142A", range=[0,100], tickfont=dict(color="#3A3A52")),
        bargap=0.5,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── FOOTER ──
st.markdown(SITE_FOOTER, unsafe_allow_html=True)
