import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Vettd — Creator Intelligence for Brands", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] { background: #04040A !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
header { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(1deg); }
  66% { transform: translateY(-10px) rotate(-1deg); }
}
@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes pulse-glow {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes counters {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes iris-move {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div id="vettd-landing" style="font-family:'Inter',sans-serif;background:#04040A;color:#E8E8F0;overflow-x:hidden;">

<!-- ═══════════════════════════════ PARTICLES BG ═══════════════════════════ -->
<canvas id="particles" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.6;"></canvas>

<!-- ══════════════════════════════════ NAV ════════════════════════════════ -->
<nav style="position:fixed;top:0;left:0;right:0;z-index:100;padding:1.25rem 3rem;
    display:flex;justify-content:space-between;align-items:center;
    background:rgba(4,4,10,0.85);backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(255,255,255,0.05);">
  <div style="font-size:20px;font-weight:800;letter-spacing:-0.5px;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
      animation:shimmer 4s linear infinite;">✦ Vettd</div>
  <div style="display:flex;gap:2.5rem;align-items:center;">
    <a href="/About" target="_self" style="font-size:13px;color:#666688;text-decoration:none;font-weight:500;transition:color 0.2s;"
       onmouseover="this.style.color='#A78BFA'" onmouseout="this.style.color='#666688'">About</a>
    <a href="/Founder" target="_self" style="font-size:13px;color:#666688;text-decoration:none;font-weight:500;"
       onmouseover="this.style.color='#A78BFA'" onmouseout="this.style.color='#666688'">Founder</a>
    <a href="/Contact" target="_self" style="font-size:13px;color:#666688;text-decoration:none;font-weight:500;"
       onmouseover="this.style.color='#A78BFA'" onmouseout="this.style.color='#666688'">Contact</a>
    <a href="/app" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;
        padding:9px 22px;border-radius:8px;
        background:linear-gradient(135deg,#7C3AED,#4F46E5);
        border:1px solid rgba(124,58,237,0.5);
        box-shadow:0 0 20px rgba(124,58,237,0.3);
        transition:box-shadow 0.2s;"
       onmouseover="this.style.boxShadow='0 0 40px rgba(124,58,237,0.6)'"
       onmouseout="this.style.boxShadow='0 0 20px rgba(124,58,237,0.3)'">
      Launch app →
    </a>
  </div>
</nav>

<!-- ══════════════════════════════════ HERO ═══════════════════════════════ -->
<section style="min-height:100vh;display:flex;flex-direction:column;align-items:center;
    justify-content:center;text-align:center;padding:8rem 2rem 4rem;position:relative;z-index:1;">

  <!-- Glow orbs -->
  <div style="position:absolute;top:20%;left:15%;width:500px;height:500px;border-radius:50%;
      background:radial-gradient(circle,rgba(124,58,237,0.15),transparent 70%);
      animation:pulse-glow 6s ease-in-out infinite;pointer-events:none;"></div>
  <div style="position:absolute;top:30%;right:10%;width:400px;height:400px;border-radius:50%;
      background:radial-gradient(circle,rgba(6,182,212,0.1),transparent 70%);
      animation:pulse-glow 8s ease-in-out infinite 2s;pointer-events:none;"></div>

  <!-- Rotating ring -->
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
      width:700px;height:700px;border-radius:50%;
      border:1px solid rgba(124,58,237,0.08);
      animation:spin-slow 30s linear infinite;pointer-events:none;">
    <div style="position:absolute;top:-4px;left:50%;width:8px;height:8px;
        border-radius:50%;background:#7C3AED;box-shadow:0 0 10px #7C3AED;
        transform:translateX(-50%);"></div>
  </div>
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
      width:900px;height:900px;border-radius:50%;
      border:1px solid rgba(6,182,212,0.05);
      animation:spin-slow 50s linear infinite reverse;pointer-events:none;">
    <div style="position:absolute;top:-3px;left:50%;width:6px;height:6px;
        border-radius:50%;background:#06B6D4;box-shadow:0 0 8px #06B6D4;
        transform:translateX(-50%);"></div>
  </div>

  <div style="animation:fadeInUp 0.8s ease-out both;">
    <div style="display:inline-flex;align-items:center;gap:8px;
        background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);
        border-radius:999px;padding:7px 18px;margin-bottom:2rem;">
      <div style="width:6px;height:6px;border-radius:50%;background:#A78BFA;
          box-shadow:0 0 6px #A78BFA;animation:pulse-glow 2s ease-in-out infinite;"></div>
      <span style="font-size:12px;font-weight:600;letter-spacing:0.12em;color:#A78BFA;text-transform:uppercase;">
        Creator intelligence for brands
      </span>
    </div>
  </div>

  <div style="animation:fadeInUp 0.8s ease-out 0.1s both;">
    <h1 style="font-size:80px;font-weight:900;letter-spacing:-4px;line-height:0.95;
        margin:0 0 2rem;max-width:900px;">
      <span style="background:linear-gradient(135deg,#FFFFFF 0%,#E8E8F0 30%);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Know exactly
      </span><br>
      <span style="background:linear-gradient(135deg,#A78BFA 0%,#60A5FA 40%,#06B6D4 80%);
          background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
          animation:shimmer 5s linear infinite;">
        who you're paying.
      </span>
    </h1>
  </div>

  <div style="animation:fadeInUp 0.8s ease-out 0.2s both;">
    <p style="font-size:19px;color:#5555AA;line-height:1.8;max-width:520px;margin:0 auto 3rem;font-weight:400;">
      A single, transparent score for any creator — built from real engagement,
      audience authenticity, and brand alignment.
    </p>
  </div>

  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:5rem;
      animation:fadeInUp 0.8s ease-out 0.3s both;">
    <a href="/app" target="_self" style="display:inline-flex;align-items:center;gap:8px;
        background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;
        font-weight:700;font-size:15px;padding:16px 36px;border-radius:12px;
        text-decoration:none;box-shadow:0 0 40px rgba(124,58,237,0.4);
        border:1px solid rgba(124,58,237,0.5);">
      Try Vettd free <span style="font-size:18px;">→</span>
    </a>
    <a href="#how" style="display:inline-flex;align-items:center;gap:8px;
        background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);
        color:#9090B8;font-weight:500;font-size:15px;padding:16px 36px;
        border-radius:12px;text-decoration:none;">
      See how it works
    </a>
  </div>

  <!-- Stats row -->
  <div style="display:flex;gap:0;animation:fadeInUp 0.8s ease-out 0.4s both;
      background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
      border-radius:16px;overflow:hidden;backdrop-filter:blur(10px);">
    <div style="padding:1.5rem 2.5rem;border-right:1px solid rgba(255,255,255,0.06);text-align:center;">
      <div style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">£21B</div>
      <div style="font-size:11px;color:#333355;margin-top:4px;letter-spacing:0.05em;">market we're fixing</div>
    </div>
    <div style="padding:1.5rem 2.5rem;border-right:1px solid rgba(255,255,255,0.06);text-align:center;">
      <div style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#60A5FA,#06B6D4);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">80%</div>
      <div style="font-size:11px;color:#333355;margin-top:4px;letter-spacing:0.05em;">of brands guess on spend</div>
    </div>
    <div style="padding:1.5rem 2.5rem;border-right:1px solid rgba(255,255,255,0.06);text-align:center;">
      <div style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#06B6D4,#A78BFA);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">0–100</div>
      <div style="font-size:11px;color:#333355;margin-top:4px;letter-spacing:0.05em;">one score, total clarity</div>
    </div>
    <div style="padding:1.5rem 2.5rem;text-align:center;">
      <div style="font-size:32px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#7C3AED);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">3</div>
      <div style="font-size:11px;color:#333355;margin-top:4px;letter-spacing:0.05em;">tiers, any brand size</div>
    </div>
  </div>
</section>

<!-- ════════════════════════ MOCK DASHBOARD PREVIEW ══════════════════════ -->
<section style="padding:4rem 3rem;position:relative;z-index:1;">
  <div style="max-width:1100px;margin:0 auto;
      background:rgba(255,255,255,0.02);
      border:1px solid rgba(255,255,255,0.07);
      border-radius:24px;overflow:hidden;
      box-shadow:0 0 80px rgba(124,58,237,0.15),0 0 40px rgba(6,182,212,0.05);">
    <!-- Mock browser bar -->
    <div style="background:#0A0A14;padding:12px 20px;border-bottom:1px solid rgba(255,255,255,0.05);
        display:flex;align-items:center;gap:12px;">
      <div style="display:flex;gap:6px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#FF5F57;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#FEBC2E;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#28C840;"></div>
      </div>
      <div style="flex:1;background:#12121E;border-radius:6px;padding:5px 12px;
          font-size:11px;color:#333355;max-width:300px;margin:0 auto;">
        get-vettd.streamlit.app
      </div>
    </div>
    <!-- Mock dashboard content -->
    <div style="padding:1.5rem;display:flex;gap:1.5rem;min-height:380px;">
      <!-- Sidebar mock -->
      <div style="width:180px;flex-shrink:0;background:#07070F;border-radius:12px;padding:1rem;">
        <div style="font-size:14px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#06B6D4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.5rem;">✦ Vettd</div>
        <div style="font-size:10px;color:#222240;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Creator</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:11px;color:#6666AA;">@emmalifestyle</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:1rem;font-size:11px;color:#6666AA;">Instagram</div>
        <div style="font-size:10px;color:#222240;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Profile</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:11px;color:#6666AA;">150,000 followers</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:1.5rem;font-size:11px;color:#6666AA;">Fashion · 4x/week</div>
        <div style="background:linear-gradient(135deg,#7C3AED,#4F46E5);border-radius:8px;
            padding:8px;text-align:center;font-size:11px;font-weight:700;color:white;">
          ✦ Run analysis
        </div>
      </div>
      <!-- Main content mock -->
      <div style="flex:1;display:flex;flex-direction:column;gap:1rem;">
        <!-- Header -->
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;border-radius:50%;
                background:linear-gradient(135deg,#7C3AED,#4F46E5);
                display:flex;align-items:center;justify-content:center;
                font-size:14px;font-weight:700;color:white;">EW</div>
            <div>
              <div style="font-size:15px;font-weight:700;color:#E8E8F0;">Emma Williams</div>
              <div style="font-size:11px;color:#333355;">@emmalifestyle · Instagram · Fashion</div>
            </div>
          </div>
          <div style="background:#16122E;border:1px solid rgba(124,58,237,0.3);
              border-radius:999px;padding:4px 14px;font-size:11px;font-weight:600;color:#A78BFA;">Pro</div>
        </div>
        <!-- Score + metrics row -->
        <div style="display:flex;gap:1rem;">
          <!-- Score card -->
          <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:14px;
              padding:1.25rem;text-align:center;min-width:120px;">
            <div style="font-size:10px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Vettd Score</div>
            <div style="font-size:52px;font-weight:900;line-height:1;
                background:linear-gradient(135deg,#60A5FA,#06B6D4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">74</div>
            <div style="font-size:11px;font-weight:600;color:#60A5FA;margin-top:6px;">Strong fit</div>
          </div>
          <!-- Metric cards -->
          <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Followers</div>
              <div style="font-size:17px;font-weight:700;color:#E8E8F0;margin-top:4px;">150K</div>
            </div>
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Engagement</div>
              <div style="font-size:17px;font-weight:700;color:#A78BFA;margin-top:4px;">6.5%</div>
            </div>
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Brand fit</div>
              <div style="font-size:17px;font-weight:700;color:#06B6D4;margin-top:4px;">80/100</div>
            </div>
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Fake score</div>
              <div style="font-size:17px;font-weight:700;color:#10B981;margin-top:4px;">12/100</div>
            </div>
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Cost/post</div>
              <div style="font-size:17px;font-weight:700;color:#E8E8F0;margin-top:4px;">£840</div>
            </div>
            <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:10px;padding:10px 12px;">
              <div style="font-size:9px;color:#333355;text-transform:uppercase;letter-spacing:0.1em;">Growth 30d</div>
              <div style="font-size:17px;font-weight:700;color:#A78BFA;margin-top:4px;">+2.5%</div>
            </div>
          </div>
        </div>
        <!-- Score bar breakdown -->
        <div style="background:#07070F;border:1px solid #1A1A2E;border-radius:12px;padding:1rem;display:flex;gap:1.5rem;">
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px;"><span style="color:#444466;">Engagement</span><span style="color:#A78BFA;">65</span></div>
            <div style="background:#12121E;border-radius:999px;height:4px;"><div style="width:65%;height:100%;border-radius:999px;background:linear-gradient(90deg,#7C3AED,#60A5FA);"></div></div>
          </div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px;"><span style="color:#444466;">Authenticity</span><span style="color:#A78BFA;">88</span></div>
            <div style="background:#12121E;border-radius:999px;height:4px;"><div style="width:88%;height:100%;border-radius:999px;background:linear-gradient(90deg,#7C3AED,#06B6D4);"></div></div>
          </div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px;"><span style="color:#444466;">Brand fit</span><span style="color:#A78BFA;">80</span></div>
            <div style="background:#12121E;border-radius:999px;height:4px;"><div style="width:80%;height:100%;border-radius:999px;background:linear-gradient(90deg,#4F46E5,#A78BFA);"></div></div>
          </div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px;"><span style="color:#444466;">Consistency</span><span style="color:#A78BFA;">80</span></div>
            <div style="background:#12121E;border-radius:999px;height:4px;"><div style="width:80%;height:100%;border-radius:999px;background:linear-gradient(90deg,#60A5FA,#06B6D4);"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════════════════════ FEATURES ═══════════════════════════════ -->
<section style="padding:6rem 3rem;position:relative;z-index:1;max-width:1100px;margin:0 auto;">
  <div style="text-align:center;margin-bottom:4rem;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#333355;margin-bottom:1rem;">What Vettd gives you</div>
    <h2 style="font-size:48px;font-weight:900;letter-spacing:-2px;margin:0;
        background:linear-gradient(135deg,#FFFFFF,#A78BFA 60%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      Everything a brand needs.
    </h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
""", unsafe_allow_html=True)

features = [
    ("✦", "#A78BFA", "#7C3AED", "Vettd Score", "One 0–100 number. Transparent, weighted, built from real data — not follower counts."),
    ("◈", "#60A5FA", "#4F46E5", "Audience authenticity", "Fake follower detection, bot networks, and inactive follower estimates before you spend."),
    ("⬡", "#06B6D4", "#0891B2", "Brand-fit alignment", "Creator niche, tone, and audience scored against your specific brand automatically."),
    ("◇", "#A78BFA", "#7C3AED", "Deep demographics", "Gender, age, locations, and audience interest categories in one clean report."),
    ("✧", "#60A5FA", "#4F46E5", "ROI prediction", "Cost per post, cost per engagement, and campaign ROI — before you sign anything."),
    ("⟡", "#06B6D4", "#0891B2", "Multi-platform", "Instagram, TikTok, and YouTube unified in one report. Compare side by side."),
]

for icon, color, dark, title, desc in features:
    st.markdown(f"""
    <div style="background:#07070F;border:1px solid #12121E;border-radius:20px;padding:2rem;
        transition:border-color 0.3s,transform 0.3s;cursor:default;position:relative;overflow:hidden;"
        onmouseover="this.style.borderColor='{color}33';this.style.transform='translateY(-4px)'"
        onmouseout="this.style.borderColor='#12121E';this.style.transform='translateY(0)'">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
          background:linear-gradient(90deg,transparent,{color}44,transparent);"></div>
      <div style="width:48px;height:48px;border-radius:12px;margin-bottom:1.25rem;
          background:linear-gradient(135deg,{color}18,{dark}10);
          border:1px solid {color}30;
          display:flex;align-items:center;justify-content:center;
          font-size:20px;color:{color};">{icon}</div>
      <div style="font-size:16px;font-weight:700;color:#E8E8F0;margin-bottom:8px;">{title}</div>
      <div style="font-size:13px;color:#444466;line-height:1.7;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></section>", unsafe_allow_html=True)

# HOW IT WORKS
st.markdown("""
<section id="how" style="padding:6rem 3rem;position:relative;z-index:1;
    border-top:1px solid #0D0D1A;border-bottom:1px solid #0D0D1A;
    background:linear-gradient(180deg,rgba(124,58,237,0.03),transparent);">
  <div style="max-width:1100px;margin:0 auto;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
        color:#333355;margin-bottom:1rem;">Simple by design</div>
    <h2 style="font-size:48px;font-weight:900;letter-spacing:-2px;margin:0 0 4rem;
        background:linear-gradient(135deg,#FFFFFF,#60A5FA);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      Three steps to a decision.
    </h2>
    <div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:center;gap:1rem;">
""", unsafe_allow_html=True)

steps = [
    ("01", "#7C3AED", "Enter the creator", "Type in any creator's stats. Takes under 2 minutes."),
    ("02", "#60A5FA", "Get their Vettd Score", "6 weighted signals. One clear 0–100 score with full breakdown."),
    ("03", "#06B6D4", "Make the call", "Download the report, share the link, decide with confidence."),
]
for i, (num, color, title, desc) in enumerate(steps):
    st.markdown(f"""
    <div style="background:#07070F;border:1px solid #12121E;border-radius:20px;padding:2rem;">
      <div style="font-size:48px;font-weight:900;line-height:1;margin-bottom:1rem;
          background:linear-gradient(135deg,{color},{color}55);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{num}</div>
      <div style="font-size:16px;font-weight:700;color:#E8E8F0;margin-bottom:8px;">{title}</div>
      <div style="font-size:13px;color:#444466;line-height:1.7;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    if i < 2:
        st.markdown(f"""
        <div style="font-size:24px;color:#1A1A2E;font-weight:300;">→</div>
        """, unsafe_allow_html=True)

st.markdown("</div></div></section>", unsafe_allow_html=True)

# PRICING
st.markdown("""
<section style="padding:6rem 3rem;position:relative;z-index:1;">
  <div style="max-width:1100px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:4rem;">
      <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
          color:#333355;margin-bottom:1rem;">Pricing</div>
      <h2 style="font-size:48px;font-weight:900;letter-spacing:-2px;margin:0;
          background:linear-gradient(135deg,#FFFFFF,#A78BFA);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Start free. Scale when ready.
      </h2>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;align-items:start;">
""", unsafe_allow_html=True)

plans = [
    ("Starter", "£29", "/mo", "5 searches/month", "#555570", "#12121E", False,
     ["Vettd Score", "Engagement analytics", "Fake follower score", "Basic demographics", "CSV export"]),
    ("Pro", "£99", "/mo", "50 searches/month", "#A78BFA", "rgba(124,58,237,0.15)", True,
     ["Everything in Starter", "Full audience demographics", "Brand-fit score", "Multi-platform report", "Competitor comparison", "PDF brand report"]),
    ("Enterprise", "Custom", "", "Unlimited searches", "#06B6D4", "#07070F", False,
     ["Everything in Pro", "ROI prediction", "Buyer intent signals", "Auto campaign brief", "API access", "White-label reports"]),
]

for name, price, period, searches, color, bg, featured, features_list in plans:
    border = f"1px solid rgba(124,58,237,0.4)" if featured else "1px solid #12121E"
    glow = "box-shadow:0 0 60px rgba(124,58,237,0.15);" if featured else ""
    top_line = f'<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#60A5FA,#06B6D4);"></div>' if featured else ""
    popular = '<div style="position:absolute;top:16px;right:16px;background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.4);color:#A78BFA;font-size:10px;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:0.1em;">POPULAR</div>' if featured else ""
    checks = "".join([f'<div style="display:flex;gap:8px;align-items:center;font-size:13px;color:#555577;margin-bottom:10px;"><div style="width:14px;height:14px;border-radius:50%;background:linear-gradient(135deg,{color},{color}88);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:8px;color:white;font-weight:700;">✓</div>{f}</div>' for f in features_list])
    price_html = f'<span style="font-size:40px;font-weight:900;background:linear-gradient(135deg,{color},#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{price}</span><span style="font-size:15px;color:#444466;">{period}</span>' if period else f'<span style="font-size:40px;font-weight:900;color:#E8E8F0;">{price}</span>'

    st.markdown(f"""
    <div style="background:{bg};border:{border};border-radius:20px;padding:2rem;
        position:relative;overflow:hidden;{glow}">
      {top_line}{popular}
      <div style="font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:{color};margin-bottom:12px;">{name}</div>
      <div style="margin-bottom:6px;">{price_html}</div>
      <div style="font-size:12px;color:#333355;margin-bottom:1.5rem;">{searches}</div>
      <div style="border-top:1px solid #1A1A2E;padding-top:1.25rem;">{checks}</div>
      <a href="/app" target="_self" style="display:block;margin-top:1.5rem;text-align:center;
          background:{'linear-gradient(135deg,#7C3AED,#4F46E5)' if featured else 'rgba(255,255,255,0.04)'};
          border:{'none' if featured else '1px solid #1A1A2E'};
          color:{'white' if featured else '#8888AA'};font-weight:600;font-size:14px;
          padding:12px;border-radius:10px;text-decoration:none;">
        {'Get started →' if name == 'Starter' else 'Get Pro →' if name == 'Pro' else 'Contact us →'}
      </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div></section>", unsafe_allow_html=True)

# TESTIMONIALS
st.markdown("""
<section style="padding:6rem 3rem;position:relative;z-index:1;
    background:linear-gradient(180deg,transparent,rgba(124,58,237,0.04),transparent);">
  <div style="max-width:1100px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:4rem;">
      <div style="font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;
          color:#333355;margin-bottom:1rem;">Early feedback</div>
      <h2 style="font-size:48px;font-weight:900;letter-spacing:-2px;margin:0;
          background:linear-gradient(135deg,#FFFFFF,#06B6D4);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Brands that get it.
      </h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
""", unsafe_allow_html=True)

testimonials = [
    ("We wasted £40k on a campaign last year. Vettd would have told us in 30 seconds it was the wrong fit.", "Priya S.", "Head of Marketing, D2C Fashion Brand", "#A78BFA"),
    ("The brand-fit score is exactly what was missing. Something that thinks like a strategist, not just a data tool.", "Marcus T.", "Founder, Creative Agency — London", "#60A5FA"),
    ("I showed the Vettd report in a board meeting. The ROI prediction alone justified the subscription 10x.", "Ananya R.", "CMO, Lifestyle Startup — Mumbai", "#06B6D4"),
]
for quote, name, role, color in testimonials:
    st.markdown(f"""
    <div style="background:#07070F;border:1px solid #12121E;border-radius:20px;padding:2rem;
        position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:1px;
          background:linear-gradient(90deg,transparent,{color}44,transparent);"></div>
      <div style="font-size:36px;color:{color};line-height:1;margin-bottom:1rem;opacity:0.6;">"</div>
      <p style="font-size:14px;color:#666688;line-height:1.8;margin:0 0 1.5rem;font-style:italic;">{quote}</p>
      <div style="border-top:1px solid #12121E;padding-top:1rem;">
        <div style="font-size:13px;font-weight:600;color:#E8E8F0;">{name}</div>
        <div style="font-size:11px;color:#333355;margin-top:3px;">{role}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div></section>", unsafe_allow_html=True)

# FINAL CTA
st.markdown("""
<section style="padding:8rem 3rem;position:relative;z-index:1;text-align:center;">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
      width:800px;height:400px;border-radius:50%;
      background:radial-gradient(ellipse,rgba(124,58,237,0.12),transparent 70%);
      pointer-events:none;"></div>
  <div style="max-width:700px;margin:0 auto;position:relative;">
    <h2 style="font-size:56px;font-weight:900;letter-spacing:-2.5px;line-height:1.05;margin:0 0 1.5rem;
        background:linear-gradient(135deg,#FFFFFF 0%,#A78BFA 40%,#06B6D4 80%);
        background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        animation:shimmer 5s linear infinite;">
      Ready to vet your next creator?
    </h2>
    <p style="font-size:17px;color:#44446A;line-height:1.7;margin:0 0 2.5rem;">
      Join brands using Vettd to make smarter influencer decisions.
    </p>
    <a href="/app" target="_self" style="display:inline-block;
        background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;
        font-weight:700;font-size:16px;padding:18px 48px;border-radius:14px;
        text-decoration:none;box-shadow:0 0 60px rgba(124,58,237,0.4);
        border:1px solid rgba(124,58,237,0.5);">
      Start for free →
    </a>
    <div style="margin-top:1rem;font-size:12px;color:#222240;">No credit card required</div>
  </div>
</section>

<!-- FOOTER -->
<footer style="border-top:1px solid #0D0D1A;padding:2rem 3rem;
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;
    position:relative;z-index:1;">
  <div style="font-size:16px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#60A5FA,#06B6D4);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">✦ Vettd</div>
  <div style="font-size:12px;color:#222240;">Built in Mumbai. Made for brands everywhere.</div>
  <div style="display:flex;gap:1.5rem;">
    <a href="/About" target="_self" style="font-size:12px;color:#333355;text-decoration:none;">About</a>
    <a href="/Founder" target="_self" style="font-size:12px;color:#333355;text-decoration:none;">Founder</a>
    <a href="/Contact" target="_self" style="font-size:12px;color:#333355;text-decoration:none;">Contact</a>
    <a href="mailto:jadepinto96@gmail.com" style="font-size:12px;color:#333355;text-decoration:none;">jadepinto96@gmail.com</a>
  </div>
</footer>

</div>

<script>
// Particle background
const canvas = document.getElementById('particles');
if (canvas) {
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const particles = [];
  for (let i = 0; i < 80; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.5 + 0.3,
      dx: (Math.random() - 0.5) * 0.3,
      dy: (Math.random() - 0.5) * 0.3,
      opacity: Math.random() * 0.5 + 0.1,
      color: ['#A78BFA','#60A5FA','#06B6D4'][Math.floor(Math.random()*3)]
    });
  }
  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.opacity;
      ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
    });
    requestAnimationFrame(drawParticles);
  }
  drawParticles();
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
}
</script>
""", unsafe_allow_html=True)
