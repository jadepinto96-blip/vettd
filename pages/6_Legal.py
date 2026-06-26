import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Legal — Vettd", page_icon="✦", layout="wide")
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
<a href="/Founder" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Founder</a>
<a href="/Contact" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Contact</a>
<a href="/Analyse" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;padding:9px 22px;border-radius:999px;background:linear-gradient(135deg,#7C3AED,#4F46E5);border:1px solid rgba(124,58,237,.5);">Launch app →</a>
</div>
</nav>

<div style="max-width:760px;margin:0 auto;padding:4rem 2rem 6rem;">

<div style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.25rem;">Legal</div>
<h1 class="disp" style="font-size:clamp(34px,6vw,52px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA 60%,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Terms &amp; policies.</h1>
<div style="font-size:12px;color:#3A3A52;margin-top:1rem;">Last updated 26 June 2026 · These are plain-language summaries, not formal legal advice.</div>
</div>

<div id="privacy" style="background:#0A0A14;border:1px solid #14142A;border-radius:18px;padding:1.75rem;margin-bottom:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#7C3AED;margin-bottom:12px;">Privacy Policy</div>
<p style="font-size:14px;color:#8888A8;line-height:1.85;margin:0;">Vettd collects only the information you provide — the creator details you enter and, if you contact us, your name and email. We use third-party data providers to retrieve publicly available creator metrics. We do not sell your personal data. Any data you enter is used solely to generate your report. You can request deletion of your data at any time by emailing <a href="mailto:jadepinto96@gmail.com" style="color:#A78BFA;text-decoration:none;">jadepinto96@gmail.com</a>.</p>
</div>

<div id="terms" style="background:#0A0A14;border:1px solid #14142A;border-radius:18px;padding:1.75rem;margin-bottom:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#60A5FA;margin-bottom:12px;">Terms &amp; Conditions</div>
<p style="font-size:14px;color:#8888A8;line-height:1.85;margin:0;">Vettd provides creator-intelligence estimates and scores for informational purposes to support — not replace — your own judgement. Scores are derived from available data and modelling, and we make no guarantee of campaign outcomes. By using Vettd you agree not to misuse the platform, scrape it, or resell its outputs without permission. Vettd is provided "as is" and we are not liable for decisions made based on its reports.</p>
</div>

<div id="refund" style="background:#0A0A14;border:1px solid #14142A;border-radius:18px;padding:1.75rem;margin-bottom:1.5rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#22D3EE;margin-bottom:12px;">Refund Policy</div>
<p style="font-size:14px;color:#8888A8;line-height:1.85;margin:0;">Paid plans can be cancelled at any time and will not renew for the next billing period. If you're unsatisfied within the first 14 days of a new subscription, email us and we'll arrange a full refund. Refunds for partial periods after 14 days are handled case by case. Contact <a href="mailto:jadepinto96@gmail.com" style="color:#A78BFA;text-decoration:none;">jadepinto96@gmail.com</a> for any billing question.</p>
</div>

<div style="text-align:center;font-size:12px;color:#3A3A52;margin-top:2rem;">© 2026 Vettd · Built in Mumbai.</div>

</div>
</div>
""", unsafe_allow_html=True)
