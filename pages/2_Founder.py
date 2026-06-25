import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Founder — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
.disp { font-family:'Space Grotesk','Inter',sans-serif; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'Inter',sans-serif;background:#0B0B16;color:#EDEDF5;min-height:100vh;">

<nav style="position:sticky;top:0;z-index:100;padding:1.1rem 3.5rem;display:flex;justify-content:space-between;align-items:center;background:rgba(11,11,22,.75);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.04);">
<a href="/" target="_self" class="brandmark" style="font-size:20px;font-weight:700;background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ VETTD</a>
<div style="display:flex;gap:2.5rem;align-items:center;">
<a href="/About" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">About</a>
<a href="/Founder" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Founder</a>
<a href="/Contact" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Contact</a>
<a href="/Analyse" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;padding:9px 22px;border-radius:999px;background:linear-gradient(135deg,#7C3AED,#4F46E5);border:1px solid rgba(124,58,237,.5);">Launch app →</a>
</div>
</nav>

<div style="max-width:820px;margin:0 auto;padding:5rem 2rem 6rem;">

<div style="text-align:center;margin-bottom:4rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.25rem;">The person behind Vettd</div>
<h1 class="disp" style="font-size:clamp(34px,6vw,54px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA 50%,#22D3EE 90%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">A strategist who<br>became a creator.</h1>
</div>

<div style="display:flex;align-items:flex-start;gap:2rem;margin-bottom:2rem;background:#0A0A14;border:1px solid #14142A;border-radius:24px;padding:2rem;">
<div style="flex-shrink:0;text-align:center;">
<div style="width:88px;height:88px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#22D3EE);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:white;letter-spacing:-1px;">JP</div>
<div style="font-size:12px;color:#5A5A78;margin-top:10px;">Mumbai, India</div>
</div>
<div>
<div style="font-size:21px;font-weight:700;color:#EDEDF5;margin-bottom:4px;">Jade Pinto</div>
<div style="font-size:13px;background:linear-gradient(135deg,#A78BFA,#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:600;margin-bottom:16px;">Founder, Vettd &nbsp;·&nbsp; Management Consultant</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;">
<span style="background:#16122E;border:1px solid #2A2040;color:#A78BFA;font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Strategy &amp; Consulting</span>
<span style="background:#0E1A2E;border:1px solid #1A3040;color:#60A5FA;font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Creator · 75K</span>
<span style="background:#0A1A1E;border:1px solid #10303A;color:#22D3EE;font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">AI &amp; Transformation</span>
<span style="background:#16122E;border:1px solid #2A2040;color:#A78BFA;font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Finance · CMA</span>
</div>
</div>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:3rem;">
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.5rem;text-align:center;">
<div class="disp" style="font-size:30px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">0→75K</div>
<div style="font-size:12px;color:#5A5A78;margin-top:4px;">followers in 5 months</div>
</div>
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.5rem;text-align:center;">
<div class="disp" style="font-size:30px;font-weight:700;background:linear-gradient(135deg,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Fortune 500</div>
<div style="font-size:12px;color:#5A5A78;margin-top:4px;">clients advised at Accenture</div>
</div>
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.5rem;text-align:center;">
<div class="disp" style="font-size:30px;font-weight:700;background:linear-gradient(135deg,#22D3EE,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">2×</div>
<div style="font-size:12px;color:#5A5A78;margin-top:4px;">Champion of the Quarter</div>
</div>
</div>

<div style="display:flex;flex-direction:column;gap:1.5rem;margin-bottom:3rem;">

<div style="background:#0A0A14;border:1px solid #14142A;border-radius:18px;padding:1.75rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#7C3AED;margin-bottom:10px;">The strategist</div>
<p style="font-size:15px;color:#8888A8;line-height:1.9;margin:0;">By day, Jade is a management consultant at Accenture Strategy &amp; Consulting, where she designs large-scale transformation and AI-adoption strategies for Fortune Global 500 clients. With a finance degree, a US CMA in progress, and two "Champion of the Quarter" awards, she's spent her career turning messy data into decisions executives can actually act on — and seeing, first-hand, how much marketing budget gets spent on instinct rather than evidence.</p>
</div>

<div style="background:#0A0A14;border:1px solid rgba(124,58,237,.3);border-radius:18px;padding:1.75rem;position:relative;overflow:hidden;">
<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#22D3EE,#A78BFA);"></div>
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#22D3EE;margin-bottom:10px;">The creator</div>
<p style="font-size:15px;color:#8888A8;line-height:1.9;margin:0;">Then she crossed to the other side. Creating content on motivation and the way people think and behave, Jade grew her own page <b style="color:#EDEDF5;">from 0 to 75,000 followers in just five months</b>. Living the creator journey herself showed her exactly how brands evaluate creators — and how often great, well-matched creators get overlooked while the numbers tell only half the story.</p>
</div>

<div style="background:#0A0A14;border:1px solid #14142A;border-radius:18px;padding:1.75rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#60A5FA;margin-bottom:10px;">Why she built Vettd</div>
<p style="font-size:15px;color:#8888A8;line-height:1.9;margin:0;">Sitting at the rare intersection of brand strategy and creator life, Jade kept seeing the same gap: brands guessing, and creators judged on vanity metrics. Vettd is the tool she wished existed on both sides of the table — one transparent score that tells a brand whether a creator is genuinely right for them. Built in Mumbai, designed for brands everywhere.</p>
</div>

</div>

<div style="background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(34,211,238,.06));border:1px solid rgba(124,58,237,.15);border-radius:20px;padding:2.5rem;text-align:center;">
<div class="disp" style="font-size:20px;font-weight:600;color:#EDEDF5;margin-bottom:8px;line-height:1.6;">"I've been the strategist deciding the budget, and the creator on the other side of it.<br><span style="background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Vettd is what both sides needed."</span></div>
<div style="font-size:12px;color:#3A3A52;margin-top:14px;">— Jade Pinto, Founder of Vettd</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)
