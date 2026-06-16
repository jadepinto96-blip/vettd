import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Vettd — Creator Intelligence for Brands", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
.hero-glow {
    position: absolute;
    width: 600px; height: 600px;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.12;
    pointer-events: none;
}
.feature-card {
    background: #0D0D1A;
    border: 1px solid #1A1A2E;
    border-radius: 20px;
    padding: 1.75rem;
    height: 100%;
    transition: border-color 0.2s;
}
.feature-card:hover { border-color: #7C3AED44; }
.iris-line {
    height: 2px;
    background: linear-gradient(90deg, #7C3AED, #60A5FA, #06B6D4, #A78BFA);
    border: none;
    margin: 0;
}
.pricing-card {
    background: #0D0D1A;
    border: 1px solid #1A1A2E;
    border-radius: 20px;
    padding: 2rem;
}
.pricing-card-featured {
    background: linear-gradient(145deg, #0F0D1F, #0D1220);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
}
.pricing-card-featured::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7C3AED, #60A5FA, #06B6D4);
}
.check-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    font-size: 13px;
    color: #8888A8;
    margin-bottom: 10px;
}
.check-dot {
    width: 16px; height: 16px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED, #06B6D4);
    flex-shrink: 0;
    margin-top: 2px;
    display: flex; align-items: center; justify-content: center;
    font-size: 9px; color: white; font-weight: 700;
}
.testimonial-card {
    background: #0D0D1A;
    border: 1px solid #1A1A2E;
    border-radius: 16px;
    padding: 1.5rem;
}
.nav-logo {
    font-size: 20px; font-weight: 700;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #06B6D4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:1.25rem 0 1.5rem;border-bottom:1px solid #1A1A2E;margin-bottom:0;">
    <div class="nav-logo">✦ Vettd</div>
    <div style="display:flex;gap:2rem;align-items:center;">
        <a href="/About" target="_self" style="font-size:13px;color:#6666AA;text-decoration:none;">About</a>
        <a href="/Founder" target="_self" style="font-size:13px;color:#6666AA;text-decoration:none;">Founder</a>
        <a href="/Contact" target="_self" style="font-size:13px;color:#6666AA;text-decoration:none;">Contact</a>
        <a href="/app" target="_self" style="font-size:13px;font-weight:600;
            background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;
            padding:7px 18px;border-radius:8px;text-decoration:none;">Launch app →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:6rem 1rem 4rem;position:relative;">
    <div style="display:inline-block;background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.3);
        border-radius:999px;padding:6px 18px;font-size:12px;font-weight:600;letter-spacing:0.1em;
        color:#A78BFA;margin-bottom:1.5rem;text-transform:uppercase;">
        Creator intelligence for brands
    </div>
    <h1 style="font-size:64px;font-weight:800;letter-spacing:-3px;line-height:1.05;
        background:linear-gradient(135deg,#FFFFFF 0%,#A78BFA 40%,#60A5FA 70%,#06B6D4 100%);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        margin:0 0 1.5rem;max-width:900px;margin-left:auto;margin-right:auto;">
        Know exactly who<br>you're paying.
    </h1>
    <p style="font-size:18px;color:#6666AA;line-height:1.8;max-width:560px;margin:0 auto 2.5rem;">
        Vettd gives brands a single, transparent score for any creator —
        built from real engagement, audience authenticity, and brand alignment.
        No more guesswork.
    </p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="/app" target="_self" style="display:inline-block;
            background:linear-gradient(135deg,#7C3AED,#4F46E5);
            color:white;font-weight:600;font-size:15px;
            padding:14px 32px;border-radius:12px;text-decoration:none;">
            Try Vettd free →
        </a>
        <a href="/About" target="_self" style="display:inline-block;
            background:transparent;border:1px solid #2A2A3E;
            color:#A0A0C0;font-weight:500;font-size:15px;
            padding:14px 32px;border-radius:12px;text-decoration:none;">
            Learn more
        </a>
    </div>
    <div style="margin-top:3rem;display:flex;justify-content:center;gap:3rem;flex-wrap:wrap;">
        <div style="text-align:center;">
            <div style="font-size:28px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">£21B</div>
            <div style="font-size:12px;color:#44445A;margin-top:4px;">market we're fixing</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:28px;font-weight:800;background:linear-gradient(135deg,#60A5FA,#06B6D4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">80%</div>
            <div style="font-size:12px;color:#44445A;margin-top:4px;">of brands guess on spend</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:28px;font-weight:800;background:linear-gradient(135deg,#06B6D4,#A78BFA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">0–100</div>
            <div style="font-size:12px;color:#44445A;margin-top:4px;">one score, total clarity</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="iris-line">', unsafe_allow_html=True)

# ── FEATURES ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0 2rem;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#44445A;margin-bottom:1rem;">What Vettd gives you</div>
    <h2 style="font-size:36px;font-weight:800;letter-spacing:-1px;
        background:linear-gradient(135deg,#E8E8F0,#A78BFA);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 3rem;">
        Everything a brand needs.<br>Nothing it doesn't.
    </h2>
</div>
""", unsafe_allow_html=True)

features = [
    ("✦", "#A78BFA", "Vettd Score", "One 0–100 score per creator. Transparent, weighted, and built from real data — not follower counts."),
    ("◈", "#60A5FA", "Audience authenticity", "Fake follower detection, bot network analysis, and inactive follower estimates before you commit a penny."),
    ("⬡", "#06B6D4", "Brand-fit alignment", "See how closely a creator's niche, tone, and audience match your brand — scored automatically."),
    ("◇", "#A78BFA", "Deep demographics", "Gender split, age breakdown, top locations, and audience interest categories in one clean report."),
    ("✧", "#60A5FA", "ROI prediction", "Estimated cost per post, cost per engagement, and campaign ROI potential — before you sign anything."),
    ("⟡", "#06B6D4", "Multi-platform view", "Instagram, TikTok, and YouTube in a single unified report. Compare creators side by side."),
]

col1, col2, col3 = st.columns(3, gap="medium")
cols = [col1, col2, col3]
for i, (icon, color, title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card" style="margin-bottom:1rem;">
            <div style="width:40px;height:40px;border-radius:10px;
                background:linear-gradient(135deg,{color}22,{color}11);
                border:1px solid {color}44;
                display:flex;align-items:center;justify-content:center;
                font-size:18px;color:{color};margin-bottom:1rem;">{icon}</div>
            <div style="font-size:15px;font-weight:600;color:#E8E8F0;margin-bottom:8px;">{title}</div>
            <div style="font-size:13px;color:#6666AA;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="iris-line" style="margin-top:2rem;">', unsafe_allow_html=True)

# ── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0 2rem;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#44445A;margin-bottom:1rem;">Simple by design</div>
    <h2 style="font-size:36px;font-weight:800;letter-spacing:-1px;
        background:linear-gradient(135deg,#E8E8F0,#60A5FA);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 3rem;">
        Three steps to a decision.
    </h2>
</div>
""", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3, gap="large")
steps = [
    ("01", "#7C3AED", "Enter the creator", "Type in any creator's stats — followers, engagement, audience details. Takes under 2 minutes."),
    ("02", "#60A5FA", "Get their Vettd Score", "Our engine analyses 6 weighted signals and returns a single 0–100 score with a full breakdown."),
    ("03", "#06B6D4", "Make the call", "Download the PDF report, share the link with your team, or export the data. Decide with confidence."),
]
for col, (num, color, title, desc) in zip([s1, s2, s3], steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:1.5rem;">
            <div style="font-size:48px;font-weight:800;
                background:linear-gradient(135deg,{color},{color}66);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                line-height:1;margin-bottom:1rem;">{num}</div>
            <div style="font-size:16px;font-weight:600;color:#E8E8F0;margin-bottom:10px;">{title}</div>
            <div style="font-size:13px;color:#6666AA;line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="iris-line">', unsafe_allow_html=True)

# ── PRICING ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0 2rem;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#44445A;margin-bottom:1rem;">Pricing</div>
    <h2 style="font-size:36px;font-weight:800;letter-spacing:-1px;
        background:linear-gradient(135deg,#E8E8F0,#A78BFA);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 3rem;">
        Start free. Scale when ready.
    </h2>
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3, gap="medium")

with p1:
    st.markdown("""
    <div class="pricing-card">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#555570;margin-bottom:12px;">Starter</div>
        <div style="font-size:36px;font-weight:800;color:#E8E8F0;margin-bottom:4px;">£29<span style="font-size:16px;font-weight:400;color:#555570;">/mo</span></div>
        <div style="font-size:12px;color:#44445A;margin-bottom:1.5rem;">5 searches per month</div>
        <div style="border-top:1px solid #1A1A2E;padding-top:1.25rem;">
            <div class="check-item"><div class="check-dot">✓</div>Vettd Score</div>
            <div class="check-item"><div class="check-dot">✓</div>Engagement analytics</div>
            <div class="check-item"><div class="check-dot">✓</div>Fake follower score</div>
            <div class="check-item"><div class="check-dot">✓</div>Basic demographics</div>
            <div class="check-item"><div class="check-dot">✓</div>CSV export</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="pricing-card-featured">
        <div style="position:absolute;top:14px;right:14px;background:rgba(124,58,237,0.2);
            border:1px solid rgba(124,58,237,0.4);color:#A78BFA;
            font-size:10px;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:0.1em;">
            MOST POPULAR
        </div>
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#A78BFA;margin-bottom:12px;">Pro</div>
        <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;">
            £99<span style="font-size:16px;font-weight:400;color:#555570;-webkit-text-fill-color:#555570;">/mo</span>
        </div>
        <div style="font-size:12px;color:#44445A;margin-bottom:1.5rem;">50 searches per month</div>
        <div style="border-top:1px solid #2A2040;padding-top:1.25rem;">
            <div class="check-item"><div class="check-dot">✓</div>Everything in Starter</div>
            <div class="check-item"><div class="check-dot">✓</div>Full audience demographics</div>
            <div class="check-item"><div class="check-dot">✓</div>Brand-fit score</div>
            <div class="check-item"><div class="check-dot">✓</div>Multi-platform report</div>
            <div class="check-item"><div class="check-dot">✓</div>Competitor comparison</div>
            <div class="check-item"><div class="check-dot">✓</div>PDF brand report</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="pricing-card">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#555570;margin-bottom:12px;">Enterprise</div>
        <div style="font-size:36px;font-weight:800;color:#E8E8F0;margin-bottom:4px;">Custom</div>
        <div style="font-size:12px;color:#44445A;margin-bottom:1.5rem;">Unlimited searches</div>
        <div style="border-top:1px solid #1A1A2E;padding-top:1.25rem;">
            <div class="check-item"><div class="check-dot">✓</div>Everything in Pro</div>
            <div class="check-item"><div class="check-dot">✓</div>ROI prediction</div>
            <div class="check-item"><div class="check-dot">✓</div>Buyer intent signals</div>
            <div class="check-item"><div class="check-dot">✓</div>Auto campaign brief</div>
            <div class="check-item"><div class="check-dot">✓</div>API access</div>
            <div class="check-item"><div class="check-dot">✓</div>White-label reports</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="iris-line" style="margin-top:3rem;">', unsafe_allow_html=True)

# ── TESTIMONIALS ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4rem 0 2rem;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#44445A;margin-bottom:1rem;">Early feedback</div>
    <h2 style="font-size:36px;font-weight:800;letter-spacing:-1px;
        background:linear-gradient(135deg,#E8E8F0,#06B6D4);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 3rem;">
        Brands that get it.
    </h2>
</div>
""", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3, gap="medium")
testimonials = [
    ("We wasted £40k on an influencer campaign last year. Vettd would have told us in 30 seconds it was the wrong fit.", "Priya S.", "Head of Marketing, D2C Fashion Brand"),
    ("The brand-fit score is exactly what was missing. Finally something that thinks like a strategist, not just a data tool.", "Marcus T.", "Founder, Creative Agency — London"),
    ("I showed the Vettd report in a board meeting. The ROI prediction alone justified the subscription 10 times over.", "Ananya R.", "CMO, Lifestyle Startup — Mumbai"),
]
for col, (quote, name, role) in zip([t1, t2, t3], testimonials):
    with col:
        st.markdown(f"""
        <div class="testimonial-card">
            <div style="font-size:24px;color:#7C3AED;margin-bottom:12px;line-height:1;">"</div>
            <p style="font-size:13px;color:#9090B8;line-height:1.8;margin:0 0 1.25rem;font-style:italic;">{quote}</p>
            <div style="border-top:1px solid #1A1A2E;padding-top:12px;">
                <div style="font-size:13px;font-weight:600;color:#E8E8F0;">{name}</div>
                <div style="font-size:11px;color:#44445A;margin-top:2px;">{role}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="iris-line" style="margin-top:3rem;">', unsafe_allow_html=True)

# ── CTA ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:5rem 1rem;">
    <h2 style="font-size:44px;font-weight:800;letter-spacing:-1.5px;line-height:1.1;
        background:linear-gradient(135deg,#FFFFFF,#A78BFA 40%,#06B6D4 80%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 1.25rem;">
        Ready to vet your<br>next creator?
    </h2>
    <p style="font-size:16px;color:#6666AA;margin:0 0 2.5rem;">
        Join brands using Vettd to make smarter influencer decisions.
    </p>
    <a href="/app" target="_self" style="display:inline-block;
        background:linear-gradient(135deg,#7C3AED,#4F46E5);
        color:white;font-weight:600;font-size:16px;
        padding:16px 40px;border-radius:14px;text-decoration:none;">
        Start for free →
    </a>
    <div style="margin-top:1rem;font-size:12px;color:#33334A;">No credit card required</div>
</div>

<div style="border-top:1px solid #1A1A2E;padding:2rem 0;
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
    <div style="font-size:16px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">✦ Vettd</div>
    <div style="font-size:12px;color:#33334A;">Built in Mumbai. Made for brands everywhere.</div>
    <div style="display:flex;gap:1.5rem;">
        <a href="/About" target="_self" style="font-size:12px;color:#33334A;text-decoration:none;">About</a>
        <a href="/Founder" target="_self" style="font-size:12px;color:#33334A;text-decoration:none;">Founder</a>
        <a href="/Contact" target="_self" style="font-size:12px;color:#33334A;text-decoration:none;">Contact</a>
        <a href="mailto:jadepinto96@gmail.com" style="font-size:12px;color:#33334A;text-decoration:none;">jadepinto96@gmail.com</a>
    </div>
</div>
""", unsafe_allow_html=True)
