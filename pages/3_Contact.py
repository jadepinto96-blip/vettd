import streamlit as st
import urllib.parse
import requests
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Contact — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Formspree endpoint — set FORMSPREE_ID in .streamlit/secrets.toml (or Streamlit Cloud → Settings → Secrets).
# Until then, submissions fall back to a pre-filled mailto link.
FORMSPREE_ID = st.secrets.get("FORMSPREE_ID", "") if hasattr(st, "secrets") else ""
CONTACT_EMAIL = "jadepinto96@gmail.com"

st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding:1rem 1.25rem 3rem !important; max-width:720px !important; margin:0 auto !important; }
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
.disp { font-family:'Space Grotesk','Inter',sans-serif; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'Inter',sans-serif;background:#0B0B16;">
<nav style="position:sticky;top:0;z-index:100;padding:1.1rem 3.5rem;display:flex;justify-content:space-between;align-items:center;background:rgba(11,11,22,.75);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.04);">
<a href="/" target="_self" class="brandmark" style="font-size:20px;font-weight:700;background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ VETTD</a>
<div style="display:flex;gap:2.5rem;align-items:center;">
<a href="/About" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">About</a>
<a href="/Founder" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;">Founder</a>
<a href="/Contact" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Contact</a>
<a href="/Analyse" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;padding:9px 22px;border-radius:999px;background:linear-gradient(135deg,#7C3AED,#4F46E5);border:1px solid rgba(124,58,237,.5);">Launch app →</a>
</div>
</nav>
</div>

<div style="max-width:720px;margin:0 auto;padding:4rem 2rem 1rem;">
<div style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.25rem;">Get in touch</div>
<h1 class="disp" style="font-size:clamp(40px,6vw,56px);font-weight:700;letter-spacing:-.03em;background:linear-gradient(135deg,#FFFFFF,#A78BFA 50%,#22D3EE 90%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 1rem;">Let's talk.</h1>
<p style="font-size:16px;color:#6A6A90;line-height:1.7;max-width:500px;margin:0 auto;">Whether you're a brand wanting to get started, a creator curious about your score, or a potential partner — we'd love to hear from you.</p>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:2.5rem;">
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.25rem;text-align:center;">
<div style="font-size:22px;margin-bottom:8px;color:#A78BFA;">✦</div>
<div style="font-size:13px;font-weight:600;color:#A78BFA;margin-bottom:4px;">General enquiries</div>
<div style="font-size:12px;color:#5A5A78;">Questions about Vettd</div>
</div>
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.25rem;text-align:center;">
<div style="font-size:22px;margin-bottom:8px;color:#60A5FA;">◈</div>
<div style="font-size:13px;font-weight:600;color:#60A5FA;margin-bottom:4px;">Enterprise sales</div>
<div style="font-size:12px;color:#5A5A78;">Custom plans for agencies</div>
</div>
<div style="background:#0A0A14;border:1px solid #14142A;border-radius:16px;padding:1.25rem;text-align:center;">
<div style="font-size:22px;margin-bottom:8px;color:#22D3EE;">⬡</div>
<div style="font-size:13px;font-weight:600;color:#22D3EE;margin-bottom:4px;">Partnerships</div>
<div style="font-size:12px;color:#5A5A78;">Integrations &amp; collaborations</div>
</div>
</div>

<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#3A3A52;margin-bottom:1rem;">Send a message</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Your name", placeholder="Alex Johnson")
with c2:
    email = st.text_input("Your email", placeholder="alex@brand.com")

subject = st.selectbox("What's this about?", [
    "General enquiry", "Enterprise / agency plan", "Partnership opportunity", "Press & media", "Other"
])
message = st.text_area("Message", placeholder="Tell us a bit about what you're looking for...", height=140)

send = st.button("✦ Send message")

if send:
    if not name or not email or not message:
        st.error("Please fill in your name, email, and message.")
    else:
        sent = False
        if FORMSPREE_ID:
            try:
                resp = requests.post(
                    f"https://formspree.io/f/{FORMSPREE_ID}",
                    data={
                        "name": name,
                        "email": email,
                        "subject": subject,
                        "message": message,
                        "_subject": f"[Vettd] {subject} — from {name}",
                    },
                    headers={"Accept": "application/json"},
                    timeout=10,
                )
                sent = resp.status_code in (200, 201)
            except Exception:
                sent = False

        if sent:
            st.success(f"Thanks {name.split()[0]}! Your message has been sent — we'll reply to {email} shortly.")
        else:
            # Fallback: pre-filled email the visitor can send from their own client
            body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
            mailto = f"mailto:{CONTACT_EMAIL}?subject={urllib.parse.quote('[Vettd] ' + subject)}&body={urllib.parse.quote(body)}"
            st.info("Click below to send your message — it'll open in your email app.")
            st.markdown(
                f'<a href="{mailto}" style="display:inline-block;background:linear-gradient(135deg,#7C3AED,#4F46E5);'
                f'color:white;font-weight:600;font-size:14px;padding:12px 28px;border-radius:999px;'
                f'text-decoration:none;">Open email to send →</a>',
                unsafe_allow_html=True,
            )

st.markdown("""
<div style="max-width:720px;margin:2.5rem auto 0;padding:2rem;border-top:1px solid #14142A;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
<div>
<div class="brandmark" style="font-size:16px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;">✦ VETTD</div>
<div style="font-size:12px;color:#33334A;">Built in Mumbai. Made for brands everywhere.</div>
</div>
<a href="mailto:jadepinto96@gmail.com" style="font-size:12px;color:#5A5A78;text-decoration:none;">jadepinto96@gmail.com</a>
</div>
""", unsafe_allow_html=True)
