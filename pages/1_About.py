import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="About — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
.disp { font-family:'Space Grotesk','Inter',sans-serif; }
.stat-tile { transition: transform .4s cubic-bezier(.16,1,.3,1), border-color .4s ease, box-shadow .4s ease; }
.stat-tile:hover { transform: translateY(-6px); box-shadow: 0 20px 50px rgba(124,58,237,.18); }
.score-row { transition: transform .4s cubic-bezier(.16,1,.3,1), border-color .4s ease, background .4s ease; }
.score-row:hover { transform: translateX(8px); border-color: rgba(124,58,237,.4) !important; background:#101019 !important; }
.score-row:hover .score-badge { transform: scale(1.12) rotate(-3deg); }
.score-badge { transition: transform .4s cubic-bezier(.34,1.56,.64,1); }
</style>
""", unsafe_allow_html=True)

score_components = [
    ("Engagement rate", "25%", "Real interaction vs follower count — the most honest signal of audience connection.", "#A78BFA"),
    ("Audience authenticity", "20%", "Fake follower detection and bot network analysis to protect your spend.", "#60A5FA"),
    ("Brand-fit alignment", "20%", "How closely the creator's niche, tone, and audience match your brand.", "#22D3EE"),
    ("Audience quality", "15%", "Intent signals, buyer behaviour, and audience loyalty — beyond just demographics.", "#7C3AED"),
    ("Content consistency", "10%", "Posting frequency and reliability as a long-term brand partner.", "#4F46E5"),
    ("Growth trajectory", "10%", "30-day follower momentum — is this creator on the rise?", "#A78BFA"),
]
score_rows = ""
for name, weight, desc, color in score_components:
    score_rows += f"""<div class="score-row" style="display:flex;align-items:flex-start;gap:1rem;background:#0A0A14;border:1px solid #14142A;border-radius:14px;padding:1.25rem;">
<div class="score-badge" style="min-width:52px;height:52px;border-radius:12px;background:linear-gradient(135deg,{color}22,{color}11);border:1px solid {color}44;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:{color};">{weight}</div>
<div><div style="font-size:14px;font-weight:600;color:#EDEDF5;margin-bottom:4px;">{name}</div>
<div style="font-size:13px;color:#6A6A90;line-height:1.6;">{desc}</div></div>
</div>"""

st.markdown(f"""
<div style="font-family:'Inter',sans-serif;background:#0B0B16;color:#EDEDF5;min-height:100vh;">

<nav style="position:sticky;top:0;z-index:100;padding:1.1rem 3.5rem;display:flex;justify-content:space-between;align-items:center;background:rgba(11,11,22,.75);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.04);">
<a href="/" target="_self" class="brandmark" style="font-size:20px;font-weight:700;background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ VETTD</a>
<div style="display:flex;gap:2.5rem;align-items:center;">
<a href="/About" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">About</a>
<a href="/Founder" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Founder</a>
<a href="/Contact" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Contact</a>
<a href="/Analyse" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;padding:9px 22px;border-radius:999px;background:linear-gradient(135deg,#7C3AED,#4F46E5);border:1px solid rgba(124,58,237,.5);">Launch app →</a>
</div>
</nav>

<div style="max-width:880px;margin:0 auto;padding:5rem 2rem 6rem;">

<div style="text-align:center;margin-bottom:4rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.25rem;">Creator intelligence</div>
<h1 class="disp" style="font-size:clamp(40px,7vw,64px);font-weight:700;letter-spacing:-.04em;line-height:1.05;background:linear-gradient(135deg,#FFFFFF 0%,#A78BFA 45%,#22D3EE 85%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 1.5rem;">The truth behind<br>every creator.</h1>
<p style="font-size:17px;color:#6A6A90;line-height:1.8;max-width:600px;margin:0 auto;">Brands spend millions on influencer campaigns every year — most of them guessing. Vettd exists to change that.</p>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:3rem;">
<div class="stat-tile" style="background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.2);border-radius:20px;padding:1.75rem;">
<div class="disp" style="font-size:36px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">£21B</div>
<div style="font-size:14px;color:#7A7A98;line-height:1.6;">global influencer marketing spend in 2025 — growing 15% year on year.</div>
</div>
<div class="stat-tile" style="background:rgba(34,211,238,.06);border:1px solid rgba(34,211,238,.2);border-radius:20px;padding:1.75rem;">
<div class="disp" style="font-size:36px;font-weight:700;background:linear-gradient(135deg,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">80%</div>
<div style="font-size:14px;color:#7A7A98;line-height:1.6;">of brands make influencer budget decisions on gut feel, not data.</div>
</div>
<div class="stat-tile" style="background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.2);border-radius:20px;padding:1.75rem;">
<div class="disp" style="font-size:36px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">1 in 3</div>
<div style="font-size:14px;color:#7A7A98;line-height:1.6;">creators have a fake follower rate above 25%, invisible without the right tools.</div>
</div>
<div class="stat-tile" style="background:rgba(79,70,229,.06);border:1px solid rgba(79,70,229,.2);border-radius:20px;padding:1.75rem;">
<div class="disp" style="font-size:36px;font-weight:700;background:linear-gradient(135deg,#4F46E5,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">66%</div>
<div style="font-size:14px;color:#7A7A98;line-height:1.6;">better campaign outcomes for brands using AI-driven creator analytics.</div>
</div>
</div>

<div style="background:#0A0A14;border:1px solid #14142A;border-radius:24px;padding:2.5rem;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#7C3AED;margin-bottom:1rem;">What Vettd does</div>
<p style="font-size:16px;color:#8888A8;line-height:1.9;margin:0;">Vettd is a creator intelligence platform that gives brands a single, transparent score for any influencer — built from real engagement data, audience demographics, brand alignment, and predictive analytics. No more spreadsheets, no more guesswork, no more wasted budget.<br><br>From a creator's fake follower score to their audience's buying intent, Vettd surfaces everything a brand needs to make a confident decision — in seconds.</p>
</div>

<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#5A5A78;margin-bottom:1.25rem;">How the Vettd Score works</div>
<div style="display:flex;flex-direction:column;gap:12px;margin-bottom:3rem;">
{score_rows}
</div>

<div style="text-align:center;padding:3rem;margin-top:1rem;background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(34,211,238,.08));border:1px solid rgba(124,58,237,.2);border-radius:24px;">
<div class="disp" style="font-size:28px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;">Ready to vet your next creator?</div>
<a href="/Analyse" target="_self" style="display:inline-block;margin-top:8px;background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;font-weight:600;font-size:14px;padding:12px 32px;border-radius:999px;text-decoration:none;">Launch the app →</a>
</div>

</div>
</div>
""", unsafe_allow_html=True)
