import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Founder — Vettd", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<div style="max-width:800px;margin:0 auto;padding:3rem 1rem;">

    <div style="text-align:center;margin-bottom:3.5rem;">
        <div style="font-size:13px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;
            background:linear-gradient(135deg,#A78BFA,#06B6D4);-webkit-background-clip:text;
            -webkit-text-fill-color:transparent;margin-bottom:1rem;">
            The person behind Vettd
        </div>
        <h1 style="font-size:44px;font-weight:800;letter-spacing:-1.5px;
            background:linear-gradient(135deg,#A78BFA 0%,#60A5FA 50%,#06B6D4 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">
            Built from frustration.<br>Driven by data.
        </h1>
    </div>

    <div style="display:flex;align-items:flex-start;gap:2rem;margin-bottom:3rem;
        background:#0D0D1A;border:1px solid #1A1A2E;border-radius:24px;padding:2rem;">
        <div style="flex-shrink:0;">
            <div style="width:88px;height:88px;border-radius:50%;
                background:linear-gradient(135deg,#7C3AED,#06B6D4);
                display:flex;align-items:center;justify-content:center;
                font-size:28px;font-weight:800;color:white;letter-spacing:-1px;">JP</div>
            <div style="text-align:center;margin-top:10px;">
                <div style="font-size:12px;color:#6666AA;">Mumbai, India</div>
            </div>
        </div>
        <div>
            <div style="font-size:20px;font-weight:700;color:#E8E8F0;margin-bottom:4px;">Jade Pinto</div>
            <div style="font-size:13px;background:linear-gradient(135deg,#A78BFA,#60A5FA);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                font-weight:600;margin-bottom:14px;">Founder & CEO, Vettd</div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span style="background:#16122E;border:1px solid #2A2040;color:#A78BFA;
                    font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Brand Strategy</span>
                <span style="background:#0E1A2E;border:1px solid #1A3040;color:#60A5FA;
                    font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Creator Economy</span>
                <span style="background:#0A1A1E;border:1px solid #10303A;color:#06B6D4;
                    font-size:11px;font-weight:600;padding:4px 12px;border-radius:999px;">Data & Analytics</span>
            </div>
        </div>
    </div>

    <div style="display:flex;flex-direction:column;gap:1.5rem;margin-bottom:3rem;">

        <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:18px;padding:1.75rem;">
            <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                color:#7C3AED;margin-bottom:10px;">The background</div>
            <p style="font-size:15px;color:#9090B8;line-height:1.9;margin:0;">
                Before Vettd, Jade spent five years working in brand strategy and digital marketing
                across Mumbai's fast-growing consumer landscape — running campaigns for D2C brands,
                fashion labels, and lifestyle startups across India and the UK. She became the person
                brands came to when they needed to figure out where to spend their marketing budget.
            </p>
        </div>

        <div style="background:#0D0D1A;border:1px solid rgba(124,58,237,0.3);
            border-radius:18px;padding:1.75rem;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#7C3AED,#06B6D4,#A78BFA);"></div>
            <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                color:#06B6D4;margin-bottom:10px;">The problem she kept hitting</div>
            <p style="font-size:15px;color:#9090B8;line-height:1.9;margin:0;">
                Time and again, brands would hand over significant budgets to influencers based on
                follower counts and aesthetics — only to get campaigns with barely any real return.
                The data existed somewhere, but it was scattered, expensive to access, and completely
                inaccessible to smaller brands who needed it most. There was no single place to get
                a clear, honest answer: <em style="color:#A78BFA;">is this creator actually right for us?</em>
            </p>
        </div>

        <div style="background:#0D0D1A;border:1px solid #1A1A2E;border-radius:18px;padding:1.75rem;">
            <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;
                color:#60A5FA;margin-bottom:10px;">Why she built Vettd</div>
            <p style="font-size:15px;color:#9090B8;line-height:1.9;margin:0;">
                Jade built Vettd to be the tool she always wished existed — a platform that cuts through
                the noise and gives brands a single, trustworthy score they can act on. Not another
                dashboard full of vanity metrics. A real decision-making tool. Built in Mumbai,
                designed for brands everywhere.
            </p>
        </div>

    </div>

    <div style="background:linear-gradient(135deg,rgba(124,58,237,0.08),rgba(6,182,212,0.06));
        border:1px solid rgba(124,58,237,0.15);border-radius:20px;padding:2rem;text-align:center;">
        <div style="font-size:18px;font-weight:600;color:#E8E8F0;margin-bottom:8px;line-height:1.6;">
            "The influencer marketing industry is built on trust.<br>
            <span style="background:linear-gradient(135deg,#A78BFA,#06B6D4);-webkit-background-clip:text;
                -webkit-text-fill-color:transparent;">Vettd makes sure that trust is earned."</span>
        </div>
        <div style="font-size:12px;color:#44445A;margin-top:12px;">— Jade Pinto, Founder of Vettd</div>
    </div>

</div>
""", unsafe_allow_html=True)
