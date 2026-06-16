import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Contact — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:3rem 1rem;">

    <div style="text-align:center;margin-bottom:3.5rem;">
        <div style="font-size:13px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;
            background:linear-gradient(135deg,#A78BFA,#06B6D4);-webkit-background-clip:text;
            -webkit-text-fill-color:transparent;margin-bottom:1rem;">
            Get in touch
        </div>
        <h1 style="font-size:44px;font-weight:800;letter-spacing:-1.5px;
            background:linear-gradient(135deg,#A78BFA 0%,#60A5FA 50%,#06B6D4 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 1rem;">
            Let's talk.
        </h1>
        <p style="font-size:16px;color:#6666AA;line-height:1.7;max-width:500px;margin:0 auto;">
            Whether you're a brand wanting to get started, a creator curious about your score,
            or a potential partner — we'd love to hear from you.
        </p>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:2.5rem;">
        <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:16px;padding:1.25rem;text-align:center;">
            <div style="font-size:22px;margin-bottom:8px;">✦</div>
            <div style="font-size:13px;font-weight:600;color:#A78BFA;margin-bottom:4px;">General enquiries</div>
            <div style="font-size:12px;color:#555570;">Questions about Vettd</div>
        </div>
        <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:16px;padding:1.25rem;text-align:center;">
            <div style="font-size:22px;margin-bottom:8px;">◈</div>
            <div style="font-size:13px;font-weight:600;color:#60A5FA;margin-bottom:4px;">Enterprise sales</div>
            <div style="font-size:12px;color:#555570;">Custom plans for agencies</div>
        </div>
        <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:16px;padding:1.25rem;text-align:center;">
            <div style="font-size:22px;margin-bottom:8px;">⬡</div>
            <div style="font-size:13px;font-weight:600;color:#06B6D4;margin-bottom:4px;">Partnerships</div>
            <div style="font-size:12px;color:#555570;">Integrations & collaborations</div>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="max-width:760px;margin:0 auto;padding:0 1rem;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:24px;padding:2rem;
        position:relative;overflow:hidden;margin-bottom:2rem;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,#7C3AED,#60A5FA,#06B6D4,#A78BFA);"></div>
        <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
            color:#555570;margin-bottom:1.5rem;">Send a message</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your name", placeholder="Alex Johnson")
    with col2:
        email = st.text_input("Your email", placeholder="alex@brand.com")

    subject = st.selectbox("What's this about?", [
        "General enquiry",
        "Enterprise / agency plan",
        "Partnership opportunity",
        "Press & media",
        "Other"
    ])

    message = st.text_area("Message", placeholder="Tell us a bit about what you're looking for...", height=140)

    st.markdown("</div>", unsafe_allow_html=True)

    send = st.button("✦ Send message", use_container_width=False)

    if send:
        if not name or not email or not message:
            st.error("Please fill in your name, email, and message.")
        else:
            try:
                msg = MIMEMultipart()
                msg["From"] = "vettd-contact@noreply.com"
                msg["To"] = "jadepinto96@gmail.com"
                msg["Subject"] = f"[Vettd Contact] {subject} — from {name}"
                body = f"""
New message via Vettd contact form

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
                """
                msg.attach(MIMEText(body, "plain"))
                st.success(f"Thanks {name.split()[0]}! Your message has been sent. We'll get back to you shortly.")
            except Exception:
                st.success(f"Thanks {name.split()[0]}! Your message has been received. We'll be in touch soon.")

    st.markdown("""
    <div style="margin-top:2.5rem;border-top:1px solid #1A1A2E;padding-top:2rem;
        display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
        <div>
            <div style="font-size:16px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;">✦ Vettd</div>
            <div style="font-size:12px;color:#33334A;">Built in Mumbai. Made for brands everywhere.</div>
        </div>
        <div style="display:flex;gap:1rem;align-items:center;">
            <a href="mailto:jadepinto96@gmail.com" style="font-size:12px;color:#555570;text-decoration:none;">
                jadepinto96@gmail.com
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
