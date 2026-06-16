import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="About — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<div style="max-width:860px;margin:0 auto;padding:3rem 1rem;">

    <div style="text-align:center;margin-bottom:4rem;">
        <div style="font-size:13px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;
            background:linear-gradient(135deg,#A78BFA,#06B6D4);-webkit-background-clip:text;
            -webkit-text-fill-color:transparent;margin-bottom:1rem;">
            Creator intelligence
        </div>
        <h1 style="font-size:52px;font-weight:800;letter-spacing:-2px;line-height:1.1;
            background:linear-gradient(135deg,#A78BFA 0%,#60A5FA 40%,#06B6D4 80%);
            background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
            margin:0 0 1.5rem;">
            The truth behind<br>every creator.
        </h1>
        <p style="font-size:17px;color:#6666AA;line-height:1.8;max-width:600px;margin:0 auto;">
            Brands spend millions on influencer campaigns every year — most of them guessing.
            Vettd exists to change that.
        </p>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:3rem;">
        <div style="background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.2);
            border-radius:20px;padding:1.75rem;">
            <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
                80%
            </div>
            <div style="font-size:14px;color:#8888A8;line-height:1.6;">
                of brands make influencer budget decisions based on gut feel, not data.
            </div>
        </div>
        <div style="background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.2);
            border-radius:20px;padding:1.75rem;">
            <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#60A5FA,#06B6D4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
                £21B
            </div>
            <div style="font-size:14px;color:#8888A8;line-height:1.6;">
                global influencer marketing spend in 2025 — growing 15% year on year.
            </div>
        </div>
        <div style="background:rgba(167,139,250,0.06);border:1px solid rgba(167,139,250,0.2);
            border-radius:20px;padding:1.75rem;">
            <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#7C3AED);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
                1 in 3
            </div>
            <div style="font-size:14px;color:#8888A8;line-height:1.6;">
                creators have a fake follower rate above 25%, invisible without the right tools.
            </div>
        </div>
        <div style="background:rgba(79,70,229,0.06);border:1px solid rgba(79,70,229,0.2);
            border-radius:20px;padding:1.75rem;">
            <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#4F46E5,#A78BFA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
                66%
            </div>
            <div style="font-size:14px;color:#8888A8;line-height:1.6;">
                better campaign outcomes for brands using AI-driven creator analytics.
            </div>
        </div>
    </div>

    <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:24px;padding:2.5rem;margin-bottom:3rem;">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
            color:#7C3AED;margin-bottom:1rem;">What Vettd does</div>
        <p style="font-size:16px;color:#9090B8;line-height:1.9;margin:0;">
            Vettd is a creator intelligence platform that gives brands a single, transparent score for any
            influencer — built from real engagement data, audience demographics, brand alignment, and
            predictive analytics. No more spreadsheets, no more guesswork, no more wasted budget.
            <br><br>
            From a creator's fake follower score to their audience's buying intent, Vettd surfaces
            everything a brand needs to make a confident decision — in seconds.
        </p>
    </div>

    <div style="margin-bottom:3rem;">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
            color:#555570;margin-bottom:1.5rem;">How the Vettd Score works</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
""", unsafe_allow_html=True)

score_components = [
    ("Engagement rate", "25%", "Real interaction vs follower count — the most honest signal of audience connection.", "#A78BFA"),
    ("Audience authenticity", "20%", "Fake follower detection and bot network analysis to protect your spend.", "#60A5FA"),
    ("Brand-fit alignment", "20%", "How closely the creator's niche, tone, and audience match your brand.", "#06B6D4"),
    ("Audience quality", "15%", "Intent signals, buyer behaviour, and audience loyalty — beyond just demographics.", "#7C3AED"),
    ("Content consistency", "10%", "Posting frequency and reliability as a long-term brand partner.", "#4F46E5"),
    ("Growth trajectory", "10%", "30-day follower momentum — is this creator on the rise?", "#A78BFA"),
]

for name, weight, desc, color in score_components:
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:1rem;background:#0D0D1A;border:1px solid #1A1A2E;
        border-radius:14px;padding:1.25rem;">
        <div style="min-width:52px;height:52px;border-radius:12px;
            background:linear-gradient(135deg,{color}22,{color}11);
            border:1px solid {color}44;display:flex;align-items:center;justify-content:center;
            font-size:15px;font-weight:800;color:{color};">{weight}</div>
        <div>
            <div style="font-size:14px;font-weight:600;color:#E8E8F0;margin-bottom:4px;">{name}</div>
            <div style="font-size:13px;color:#6666AA;line-height:1.6;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
        </div>
    </div>

    <div style="text-align:center;padding:3rem;background:linear-gradient(135deg,rgba(124,58,237,0.08),rgba(6,182,212,0.08));
        border:1px solid rgba(124,58,237,0.2);border-radius:24px;">
        <div style="font-size:28px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#06B6D4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;">
            Ready to vet your next creator?
        </div>
        <div style="font-size:14px;color:#6666AA;">
            Head back to the dashboard and run your first analysis.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)
