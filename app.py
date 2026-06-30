import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.styles import GLOBAL_CSS

st.set_page_config(page_title="Vettd — Creator Intelligence for Brands", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] { background: #0B0B16 !important; }
[data-testid="stSidebar"], [data-testid="collapsedControl"],
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
html { scroll-behavior: smooth; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0B0B16; }
::-webkit-scrollbar-thumb { background: #1A1A2E; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2A2A3E; }

.disp { font-family: 'Space Grotesk', 'Inter', sans-serif; }

@keyframes shimmer { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
@keyframes pulse-glow { 0%,100% { opacity:.35; transform:scale(1);} 50% { opacity:.65; transform:scale(1.08);} }
@keyframes spin-slow { from { transform:rotate(0);} to { transform:rotate(360deg);} }
@keyframes float-up { from { opacity:0; transform:translateY(40px);} to { opacity:1; transform:translateY(0);} }
@keyframes marquee { from { transform:translateX(0);} to { transform:translateX(-50%);} }
@keyframes gridmove { from { background-position:0 0;} to { background-position:60px 60px;} }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.2;} }

/* entrance fade — CSS-only (auto-plays, never depends on JS, so content is always visible) */
@keyframes reveal-in { from { opacity:0; transform:translateY(36px); } to { opacity:1; transform:translateY(0); } }
.reveal { opacity:1; animation:reveal-in .9s cubic-bezier(.16,1,.3,1) both; }
.reveal.d1 { animation-delay:.08s; } .reveal.d2 { animation-delay:.16s; }
.reveal.d3 { animation-delay:.24s; } .reveal.d4 { animation-delay:.32s; }
.reveal.d5 { animation-delay:.4s; }

/* hover lift cards */
.lift { transition: transform .5s cubic-bezier(.16,1,.3,1), border-color .4s, box-shadow .4s; }
.lift:hover { transform:translateY(-6px); }

.cursor-glow {
  position:fixed; width:500px; height:500px; border-radius:50%; pointer-events:none; z-index:1;
  background:radial-gradient(circle, rgba(124,58,237,0.07), transparent 65%);
  transform:translate(-50%,-50%); transition:left .25s ease-out, top .25s ease-out; left:50%; top:30%;
}
</style>
""", unsafe_allow_html=True)

st.markdown(r"""
<div style="font-family:'Inter',sans-serif;background:#0B0B16;color:#EDEDF5;overflow:hidden;position:relative;">

<canvas id="particles" style="position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:.55;"></canvas>
<div class="cursor-glow" id="cglow"></div>

<!-- animated grid overlay -->
<div style="position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.4;
  background-image:linear-gradient(rgba(124,58,237,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,.04) 1px,transparent 1px);
  background-size:60px 60px;animation:gridmove 8s linear infinite;
  mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,black,transparent 75%);
  -webkit-mask-image:radial-gradient(ellipse 80% 60% at 50% 0%,black,transparent 75%);"></div>

<!-- ════════════ NAV ════════════ -->
<nav style="position:fixed;top:0;left:0;right:0;z-index:200;padding:1.1rem 3.5rem;
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(11,11,22,.7);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.04);">
  <div class="brandmark" style="font-size:21px;font-weight:700;letter-spacing:-.5px;
    background:linear-gradient(135deg,#C4B5FD,#60A5FA,#22D3EE);background-size:200% auto;
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 5s linear infinite;">✦ VETTD</div>
  <div style="display:flex;gap:2.75rem;align-items:center;">
    <a href="/About" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;font-weight:500;letter-spacing:.02em;">About</a>
    <a href="/Founder" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;font-weight:500;letter-spacing:.02em;">Founder</a>
    <a href="/Contact" target="_self" class="navlink" style="font-size:13px;color:#7A7A98;text-decoration:none;font-weight:500;letter-spacing:.02em;">Contact</a>
    <a href="/Analyse" target="_self" style="font-size:13px;font-weight:600;color:white;text-decoration:none;padding:9px 22px;border-radius:999px;
      background:linear-gradient(135deg,#7C3AED,#4F46E5);border:1px solid rgba(124,58,237,.5);
      box-shadow:0 0 24px rgba(124,58,237,.3);transition:box-shadow .3s,transform .3s;"
      onmouseover="this.style.boxShadow='0 0 44px rgba(124,58,237,.65)';this.style.transform='scale(1.04)'"
      onmouseout="this.style.boxShadow='0 0 24px rgba(124,58,237,.3)';this.style.transform='scale(1)'">Launch app →</a>
  </div>
</nav>

<!-- ════════════ HERO ════════════ -->
<section style="display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:6rem 2rem 2rem;position:relative;z-index:2;overflow:hidden;">

  <div data-orb style="position:absolute;top:18%;left:12%;width:520px;height:520px;border-radius:50%;will-change:transform;transition:transform .6s cubic-bezier(.16,1,.3,1);
    background:radial-gradient(circle,rgba(124,58,237,.16),transparent 70%);animation:pulse-glow 7s ease-in-out infinite;"></div>
  <div data-orb style="position:absolute;top:32%;right:8%;width:420px;height:420px;border-radius:50%;will-change:transform;transition:transform .6s cubic-bezier(.16,1,.3,1);
    background:radial-gradient(circle,rgba(34,211,238,.1),transparent 70%);animation:pulse-glow 9s ease-in-out infinite 2s;"></div>

  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:760px;height:760px;border-radius:50%;
    border:1px solid rgba(124,58,237,.07);animation:spin-slow 34s linear infinite;">
    <div style="position:absolute;top:-4px;left:50%;width:8px;height:8px;border-radius:50%;background:#7C3AED;box-shadow:0 0 12px #7C3AED;transform:translateX(-50%);"></div></div>
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:1000px;height:1000px;border-radius:50%;
    border:1px solid rgba(34,211,238,.05);animation:spin-slow 55s linear infinite reverse;">
    <div style="position:absolute;top:-3px;left:50%;width:6px;height:6px;border-radius:50%;background:#22D3EE;box-shadow:0 0 10px #22D3EE;transform:translateX(-50%);"></div></div>

  <div style="animation:float-up .9s cubic-bezier(.16,1,.3,1) both;">
    <div style="display:inline-flex;align-items:center;gap:9px;background:rgba(124,58,237,.1);
      border:1px solid rgba(124,58,237,.28);border-radius:999px;padding:7px 18px;margin-bottom:2.25rem;">
      <span style="width:6px;height:6px;border-radius:50%;background:#A78BFA;box-shadow:0 0 7px #A78BFA;animation:blink 2s infinite;"></span>
      <span style="font-size:11.5px;font-weight:600;letter-spacing:.18em;color:#B9A7F7;text-transform:uppercase;">Creator intelligence for brands</span>
    </div>
  </div>

  <h1 class="disp" style="font-size:clamp(48px,9vw,108px);font-weight:700;letter-spacing:-.045em;line-height:.92;margin:0 0 2rem;max-width:1000px;
    animation:float-up 1s cubic-bezier(.16,1,.3,1) .08s both;">
    <span style="background:linear-gradient(135deg,#FFFFFF,#C8C8E0 60%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Know exactly</span><br>
    <span style="background:linear-gradient(120deg,#A78BFA 0%,#60A5FA 45%,#22D3EE 90%);background-size:200% auto;
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 6s linear infinite;">who you're paying.</span>
  </h1>

  <p style="font-size:clamp(16px,2vw,20px);color:#6A6A90;line-height:1.75;max-width:540px;margin:0 auto 3rem;font-weight:400;
    animation:float-up 1s cubic-bezier(.16,1,.3,1) .18s both;">
    One transparent score for any creator — engineered from real engagement, audience authenticity and brand alignment. No guesswork.</p>

  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:0;
    animation:float-up 1s cubic-bezier(.16,1,.3,1) .28s both;">
    <a href="/Analyse" target="_self" style="display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,#7C3AED,#4F46E5);
      color:white;font-weight:700;font-size:15px;padding:17px 38px;border-radius:999px;text-decoration:none;
      box-shadow:0 0 44px rgba(124,58,237,.42);border:1px solid rgba(124,58,237,.5);transition:transform .3s,box-shadow .3s;"
      onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 0 64px rgba(124,58,237,.7)'"
      onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 0 44px rgba(124,58,237,.42)'">Vet a creator free <span style="font-size:18px;">→</span></a>
    <a href="#how" style="display:inline-flex;align-items:center;gap:9px;background:rgba(255,255,255,.03);
      border:1px solid rgba(255,255,255,.1);color:#A0A0C0;font-weight:500;font-size:15px;padding:17px 38px;border-radius:999px;text-decoration:none;
      transition:background .3s,border-color .3s;" onmouseover="this.style.background='rgba(255,255,255,.06)';this.style.borderColor='rgba(255,255,255,.2)'"
      onmouseout="this.style.background='rgba(255,255,255,.03)';this.style.borderColor='rgba(255,255,255,.1)'">See how it works</a>
  </div>

</section>
""", unsafe_allow_html=True)

# ════════════ MOCK DASHBOARD ════════════
st.markdown(r"""
<section style="padding:2.5rem 3rem 3rem;position:relative;overflow:hidden;z-index:2;">
  <div class="reveal" style="text-align:center;margin-bottom:3rem;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">The product</div>
    <h2 class="disp" style="font-size:clamp(32px,5vw,52px);font-weight:700;letter-spacing:-.03em;margin:0;
      background:linear-gradient(135deg,#FFFFFF,#A78BFA 70%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">A full report. In one glance.</h2>
  </div>
  <div class="reveal d1 lift" style="max-width:1080px;margin:0 auto;background:rgba(255,255,255,.02);
    border:1px solid rgba(255,255,255,.08);border-radius:24px;overflow:hidden;
    box-shadow:0 40px 120px rgba(124,58,237,.18),0 0 60px rgba(34,211,238,.05);">
    <div style="background:#101019;padding:12px 20px;border-bottom:1px solid rgba(255,255,255,.05);display:flex;align-items:center;gap:12px;">
      <div style="display:flex;gap:6px;"><span style="width:10px;height:10px;border-radius:50%;background:#FF5F57;"></span>
        <span style="width:10px;height:10px;border-radius:50%;background:#FEBC2E;"></span>
        <span style="width:10px;height:10px;border-radius:50%;background:#28C840;"></span></div>
      <div style="flex:1;background:#12121E;border-radius:6px;padding:5px 12px;font-size:11px;color:#3A3A52;max-width:300px;margin:0 auto;text-align:center;">get-vettd.streamlit.app</div>
    </div>
    <div style="padding:1.5rem;display:flex;gap:1.5rem;min-height:380px;">
      <div style="width:180px;flex-shrink:0;background:#101019;border-radius:12px;padding:1rem;">
        <div class="brandmark" style="font-size:14px;font-weight:700;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.5rem;">✦ Vettd</div>
        <div style="font-size:10px;color:#222238;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem;">Creator</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:11px;color:#6A6A90;">@emmalifestyle</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:1rem;font-size:11px;color:#6A6A90;">Instagram</div>
        <div style="font-size:10px;color:#222238;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem;">Profile</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:11px;color:#6A6A90;">150,000 followers</div>
        <div style="background:#0D0D1A;border-radius:6px;padding:6px 8px;margin-bottom:1.5rem;font-size:11px;color:#6A6A90;">Fashion · 4×/week</div>
        <div style="background:linear-gradient(135deg,#7C3AED,#4F46E5);border-radius:8px;padding:8px;text-align:center;font-size:11px;font-weight:700;color:white;">✦ Run analysis</div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:1rem;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#4F46E5);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:white;">EW</div>
            <div><div style="font-size:15px;font-weight:700;color:#EDEDF5;">Emma Williams</div>
              <div style="font-size:11px;color:#3A3A52;">@emmalifestyle · Instagram · Fashion</div></div></div>
          <div style="background:#16122E;border:1px solid rgba(124,58,237,.3);border-radius:999px;padding:4px 14px;font-size:11px;font-weight:600;color:#A78BFA;">Pro</div></div>
        <div style="display:flex;gap:1rem;">
          <div style="background:#101019;border:1px solid #16162A;border-radius:14px;padding:1.25rem;text-align:center;min-width:120px;">
            <div style="font-size:10px;color:#3A3A52;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px;">Vettd Score</div>
            <div class="disp" style="font-size:54px;font-weight:700;line-height:1;background:linear-gradient(135deg,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">74</div>
            <div style="font-size:11px;font-weight:600;color:#60A5FA;margin-top:6px;">Strong fit</div></div>
          <div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;">""" + "".join([
    f'<div style="background:#101019;border:1px solid #16162A;border-radius:10px;padding:10px 12px;"><div style="font-size:9px;color:#3A3A52;text-transform:uppercase;letter-spacing:.1em;">{lbl}</div><div style="font-size:17px;font-weight:700;color:{clr};margin-top:4px;">{val}</div></div>'
    for lbl,val,clr in [("Followers","150K","#EDEDF5"),("Engagement","6.5%","#A78BFA"),("Brand fit","80/100","#22D3EE"),
                         ("Fake score","12/100","#10B981"),("Cost/post","$840","#EDEDF5"),("Growth 30d","+2.5%","#A78BFA")]
]) + r"""</div></div>
        <div style="background:#101019;border:1px solid #16162A;border-radius:12px;padding:1rem;display:flex;gap:1.5rem;">""" + "".join([
    f'<div style="flex:1;"><div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px;"><span style="color:#3A3A52;">{lbl}</span><span style="color:#A78BFA;">{v}</span></div><div style="background:#12121E;border-radius:999px;height:4px;"><div style="width:{v}%;height:100%;border-radius:999px;background:linear-gradient(90deg,#7C3AED,#22D3EE);"></div></div></div>'
    for lbl,v in [("Engagement",65),("Authenticity",88),("Brand fit",80),("Consistency",80)]
]) + r"""</div>
      </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ════════════ FEATURES ════════════
features = [
    ("✦","#A78BFA","#7C3AED","Vettd Score","One 0–100 number. Transparent, weighted, built from real data — not follower counts."),
    ("◈","#60A5FA","#4F46E5","Audience authenticity","Fake follower detection, bot networks and inactive estimates before you spend."),
    ("⬡","#22D3EE","#0891B2","Brand-fit alignment","Creator niche, tone and audience scored against your specific brand automatically."),
    ("◇","#A78BFA","#7C3AED","Deep demographics","Gender, age, locations and audience interests in one clean report."),
    ("✧","#60A5FA","#4F46E5","ROI prediction","Cost per post, cost per engagement and campaign ROI — before you sign anything."),
    ("⟡","#22D3EE","#0891B2","Multi-platform","Instagram, TikTok and YouTube unified. Compare creators side by side."),
]
feature_cards = "".join([
    f'<div class="lift" style="background:#101019;border:1px solid #14142A;border-radius:22px;padding:2.25rem;position:relative;overflow:hidden;"'
    f' onmouseover="this.style.borderColor=\'{color}40\';this.style.boxShadow=\'0 20px 60px {color}18\'"'
    f' onmouseout="this.style.borderColor=\'#14142A\';this.style.boxShadow=\'none\'">'
    f'<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{color}55,transparent);"></div>'
    f'<div style="width:52px;height:52px;border-radius:14px;margin-bottom:1.5rem;background:linear-gradient(135deg,{color}1f,{dark}10);'
    f'border:1px solid {color}35;display:flex;align-items:center;justify-content:center;font-size:22px;color:{color};">{icon}</div>'
    f'<div style="font-size:17px;font-weight:700;color:#EDEDF5;margin-bottom:10px;letter-spacing:-.01em;">{title}</div>'
    f'<div style="font-size:13.5px;color:#5A5A78;line-height:1.75;">{desc}</div></div>'
    for icon,color,dark,title,desc in features
])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;max-width:1120px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Capabilities</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,56px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA 65%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Everything a brand needs.</h2>
</div>
<div class="reveal d1" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">{feature_cards}</div>
</section>
""", unsafe_allow_html=True)

# ════════════ HOW IT WORKS ════════════
steps = [
    ("01","#7C3AED","Enter the creator","Type in any creator's stats. Takes under two minutes — no integrations required."),
    ("02","#60A5FA","Get their Vettd Score","Six weighted signals resolve into one clear 0–100 score with a full breakdown."),
    ("03","#22D3EE","Make the call","Download the report, share the link, decide with total confidence."),
]
step_cards = "".join([
    f'<div class="lift" style="background:#101019;border:1px solid #14142A;border-radius:22px;padding:2.25rem;position:relative;overflow:hidden;">'
    f'<div style="position:absolute;top:-20px;right:10px;font-size:120px;font-weight:800;color:{color}14;font-family:\'Space Grotesk\',sans-serif;line-height:1;">{num}</div>'
    f'<div class="disp" style="font-size:46px;font-weight:700;line-height:1;margin-bottom:1.25rem;background:linear-gradient(135deg,{color},{color}99);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;">{num}</div>'
    f'<div style="font-size:17px;font-weight:700;color:#EDEDF5;margin-bottom:10px;position:relative;">{title}</div>'
    f'<div style="font-size:13.5px;color:#5A5A78;line-height:1.75;position:relative;">{desc}</div></div>'
    for num,color,title,desc in steps
])
st.markdown(f"""
<section id="how" style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;border-top:1px solid #14142A;border-bottom:1px solid #14142A;background:linear-gradient(180deg,rgba(124,58,237,.05),transparent);">
<div style="max-width:1120px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Simple by design</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,56px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Three steps to a decision.</h2>
</div>
<div class="reveal d1" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;">{step_cards}</div>
</div>
</section>
""", unsafe_allow_html=True)

# ════════════ WHY VETTD (vs the old way) ════════════
old_way = [
    "Walls of vanity metrics — you interpret them",
    "Scores the creator in isolation",
    "Hands you a list; you decide who fits",
    "No warning when creators share an audience",
    "Built for big budgets and steep learning curves",
    "Data. No guidance.",
]
vettd_way = [
    "One transparent 0–100 Vettd Score",
    "Scores your product against their audience",
    "Tells you who to pick — and who instead",
    "Audience-overlap detector saves double spend",
    "Start free, get an answer in seconds",
    "A clear recommendation you can act on",
]
old_rows = "".join([
    f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:14px;">'
    f'<span style="flex-shrink:0;width:20px;height:20px;border-radius:50%;background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);color:#EF4444;display:flex;align-items:center;justify-content:center;font-size:11px;margin-top:1px;">✕</span>'
    f'<span style="font-size:14px;color:#8888A8;line-height:1.5;">{x}</span></div>' for x in old_way
])
new_rows = "".join([
    f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:14px;">'
    f'<span style="flex-shrink:0;width:20px;height:20px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#22D3EE);color:white;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-top:1px;">✓</span>'
    f'<span style="font-size:14px;color:#D2D2E4;line-height:1.5;font-weight:500;">{x}</span></div>' for x in vettd_way
])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;max-width:1120px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Why Vettd</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,56px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA 65%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">A decision, not a spreadsheet.</h2>
<p style="font-size:16px;color:#7A7A98;max-width:560px;margin:1.25rem auto 0;line-height:1.7;">Most creator tools hand you a database and a wall of metrics, then leave the hard part — the decision — to you. Vettd is built the other way around.</p>
</div>
<div class="reveal d1" style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start;">
<div style="background:#0D0D14;border:1px solid #14142A;border-radius:22px;padding:2.25rem;">
<div style="font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#7A7A98;margin-bottom:1.5rem;">Traditional creator tools</div>
{old_rows}
</div>
<div style="background:linear-gradient(160deg,rgba(124,58,237,.1),rgba(34,211,238,.05));border:1px solid rgba(124,58,237,.4);border-radius:22px;padding:2.25rem;position:relative;overflow:hidden;box-shadow:0 30px 80px rgba(124,58,237,.15);">
<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#60A5FA,#22D3EE);"></div>
<div class="brandmark" style="font-size:14px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;margin-bottom:1.5rem;background:linear-gradient(135deg,#A78BFA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">The Vettd way</div>
{new_rows}
</div>
</div>
</section>
""", unsafe_allow_html=True)

# ════════════ STATS BAND (count up) ════════════
stats = [("$21B","market we're fixing","#A78BFA"),("80%","of brands guess on spend","#60A5FA"),
         ("6×","faster than manual vetting","#22D3EE"),("0–100","one score, total clarity","#A78BFA")]
stat_cells = "".join([
    f'<div style="background:#101019;padding:2.25rem 1.5rem;text-align:center;">'
    f'<div class="disp" style="font-size:44px;font-weight:700;background:linear-gradient(135deg,{clr},#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{val}</div>'
    f'<div style="font-size:12px;color:#5A5A78;margin-top:8px;letter-spacing:.04em;">{lbl}</div></div>'
    for val,lbl,clr in stats
])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;max-width:1000px;margin:0 auto;">
<div class="reveal" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.08);border-radius:20px;overflow:hidden;">{stat_cells}</div>
</section>
""", unsafe_allow_html=True)

# ════════════ PRICING ════════════
plans = [
    ("Free","$0","","2 searches/month","#7A7A98","#101019",False,
     ["Vettd Score","Basic profile stats","Engagement rate","Try before you buy"]),
    ("Starter","$59","/mo","20 searches/month","#8888A8","#101019",False,
     ["Everything in Free","Fake follower score","Basic demographics","CSV export"]),
    ("Pro","$149","/mo","100 searches/month","#A78BFA","rgba(124,58,237,.08)",True,
     ["Everything in Starter","Full audience demographics","Brand-fit score","Multi-platform report","Competitor comparison","PDF report"]),
    ("Enterprise","Custom","","Unlimited searches","#22D3EE","#101019",False,
     ["Everything in Pro","ROI prediction","Market-fit + recommendations","Auto campaign brief","API access","White-label"]),
]
def _plan_card(name,price,period,searches,color,bg,featured,flist):
    border = "1px solid rgba(124,58,237,.45)" if featured else "1px solid #14142A"
    glow = "box-shadow:0 30px 80px rgba(124,58,237,.18);" if featured else ""
    topline = '<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#7C3AED,#60A5FA,#22D3EE);"></div>' if featured else ""
    popular = '<div style="position:absolute;top:16px;right:16px;background:rgba(124,58,237,.2);border:1px solid rgba(124,58,237,.4);color:#A78BFA;font-size:10px;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:.1em;">POPULAR</div>' if featured else ""
    checks = "".join([f'<div style="display:flex;gap:9px;align-items:center;font-size:13px;color:#8888A8;margin-bottom:11px;"><span style="width:15px;height:15px;border-radius:50%;background:linear-gradient(135deg,{color},{color}88);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:8px;color:white;font-weight:700;">✓</span>{f}</div>' for f in flist])
    price_html = (f'<span class="disp" style="font-size:42px;font-weight:700;background:linear-gradient(135deg,{color},#60A5FA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{price}</span><span style="font-size:15px;color:#5A5A78;">{period}</span>' if period else f'<span class="disp" style="font-size:42px;font-weight:700;color:#EDEDF5;">{price}</span>')
    cta = {'Free': 'Start free →', 'Starter': 'Get Starter →', 'Pro': 'Get Pro →'}.get(name, 'Contact us →')
    btn_bg = 'linear-gradient(135deg,#7C3AED,#4F46E5)' if featured else 'rgba(255,255,255,.04)'
    btn_border = 'none' if featured else '1px solid #16162A'
    btn_color = 'white' if featured else '#A8A8C0'
    # Free → open the tool; paid plans → Contact (no checkout yet)
    btn_link = "/Analyse" if name == "Free" else "/Contact"
    return (f'<div class="lift" style="background:{bg};border:{border};border-radius:22px;padding:2.25rem;position:relative;overflow:hidden;{glow}">'
            f'{topline}{popular}'
            f'<div style="font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:{color};margin-bottom:14px;">{name}</div>'
            f'<div style="margin-bottom:6px;">{price_html}</div>'
            f'<div style="font-size:12px;color:#5A5A78;margin-bottom:1.5rem;">{searches}</div>'
            f'<div style="border-top:1px solid #16162A;padding-top:1.4rem;">{checks}</div>'
            f'<a href="{btn_link}" target="_self" style="display:block;margin-top:1.5rem;text-align:center;background:{btn_bg};border:{btn_border};color:{btn_color};font-weight:600;font-size:14px;padding:13px;border-radius:999px;text-decoration:none;">{cta}</a></div>')
plan_cards = "".join([_plan_card(*p) for p in plans])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;">
<div style="max-width:1120px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Pricing</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,56px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Start free. Scale when ready.</h2>
</div>
<div class="reveal d1" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;align-items:start;">{plan_cards}</div>
</div>
</section>
""", unsafe_allow_html=True)

# ════════════ TESTIMONIALS ════════════
testimonials = [
    ("We wasted $40k on a campaign last year. Vettd would have told us in 30 seconds it was the wrong fit.","Priya S.","Head of Marketing, D2C Fashion","#A78BFA"),
    ("The brand-fit score is exactly what was missing. Something that thinks like a strategist, not just a data tool.","Marcus T.","Founder, Creative Agency — London","#60A5FA"),
    ("I showed the Vettd report in a board meeting. The ROI prediction alone justified the subscription 10×.","Ananya R.","CMO, Lifestyle Startup — Mumbai","#22D3EE"),
]
tcards = "".join([
    f'<div class="lift" style="background:#101019;border:1px solid #14142A;border-radius:22px;padding:2.25rem;position:relative;overflow:hidden;">'
    f'<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{color}44,transparent);"></div>'
    f'<div class="disp" style="font-size:48px;color:{color};line-height:.6;margin-bottom:1.25rem;opacity:.6;">&ldquo;</div>'
    f'<p style="font-size:14.5px;color:#A8A8C0;line-height:1.85;margin:0 0 1.5rem;">{quote}</p>'
    f'<div style="border-top:1px solid #14142A;padding-top:1rem;">'
    f'<div style="font-size:13px;font-weight:600;color:#EDEDF5;">{name}</div>'
    f'<div style="font-size:11px;color:#5A5A78;margin-top:3px;">{role}</div></div></div>'
    for quote,name,role,color in testimonials
])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;background:linear-gradient(180deg,transparent,rgba(124,58,237,.04),transparent);">
<div style="max-width:1120px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Early feedback</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,56px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Brands that get it.</h2>
</div>
<div class="reveal d1" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">{tcards}</div>
</div>
</section>
""", unsafe_allow_html=True)

# ════════════ FAQ ════════════
st.markdown("""
<style>
.faq-item { background:#0D0D14; border:1px solid #14142A; border-radius:16px; margin-bottom:12px;
  transition:border-color .35s ease, background .35s ease; overflow:hidden; }
.faq-item:hover { border-color:rgba(124,58,237,.35); }
.faq-item[open] { border-color:rgba(124,58,237,.4); background:#101019; }
.faq-item summary { list-style:none; cursor:pointer; padding:1.25rem 1.5rem;
  display:flex; justify-content:space-between; align-items:center; gap:1rem;
  font-size:15px; font-weight:600; color:#EDEDF5; }
.faq-item summary::-webkit-details-marker { display:none; }
.faq-item summary .chev { color:#7C3AED; font-size:20px; transition:transform .35s cubic-bezier(.16,1,.3,1); flex-shrink:0; }
.faq-item[open] summary .chev { transform:rotate(45deg); }
.faq-item .faq-body { padding:0 1.5rem 1.4rem; font-size:14px; color:#7A7A98; line-height:1.8; }
</style>
""", unsafe_allow_html=True)

faqs = [
    ("What exactly is the Vettd Score?",
     "A single 0–100 score for any creator, built from six weighted signals — engagement, audience authenticity, brand-fit, audience quality, consistency and growth. Instead of reading 30 metrics, you get one transparent number, with the full breakdown of how it's calculated."),
    ("Where does the data come from?",
     "Vettd works from real engagement and audience data. Today you can enter a creator's stats manually or connect a data provider to auto-fill them; audience demographics come from licensed third-party data, never from scraping."),
    ("How is this different from other influencer tools?",
     "Most tools hand you a database and a wall of metrics, then leave the decision to you. Vettd is built around the decision — it scores your product against the creator's audience, tells you who to pick (and who instead), and flags when two creators share the same followers."),
    ("Can I compare multiple creators?",
     "Yes. The Compare tool scores up to three creators side by side, picks a recommended winner, overlays their signals, and runs an audience-overlap check so you don't pay twice to reach the same people."),
    ("What's the Brand–Product Market Fit score?",
     "An Enterprise feature that scores how well your specific product fits a creator's audience — niche, gender, age, authenticity and price-point. If the fit is weak, Vettd recommends better-matched creators for that product."),
    ("Do I need to pay to try it?",
     "No. You can start free and run analyses right away. Paid tiers unlock deeper audience demographics, brand-fit, multi-platform reports and predictive intelligence as you scale."),
    ("Is my data private?",
     "Yes. We only use the details you enter to generate your report, we don't sell your data, and you can request deletion any time. See our Legal page for the full policy."),
]
faq_items = "".join([
    f'<details class="faq-item"><summary>{q}<span class="chev">+</span></summary><div class="faq-body">{a}</div></details>'
    for q, a in faqs
])
st.markdown(f"""
<section style="padding:3.5rem 3rem;position:relative;overflow:hidden;z-index:2;max-width:820px;margin:0 auto;">
<div class="reveal" style="text-align:center;margin-bottom:3rem;">
<div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#5A5A78;margin-bottom:1rem;">Questions</div>
<h2 class="disp" style="font-size:clamp(34px,5.5vw,52px);font-weight:700;letter-spacing:-.03em;margin:0;background:linear-gradient(135deg,#FFFFFF,#A78BFA 65%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Frequently asked.</h2>
</div>
<div class="reveal d1">{faq_items}</div>
</section>
""", unsafe_allow_html=True)

# ════════════ FINAL CTA + FOOTER ════════════
st.markdown(r"""
<section style="padding:3.5rem 3rem 3rem;position:relative;z-index:2;text-align:center;overflow:hidden;">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:850px;height:430px;border-radius:50%;
    background:radial-gradient(ellipse,rgba(124,58,237,.14),transparent 70%);"></div>
  <div class="reveal" style="max-width:720px;margin:0 auto;position:relative;">
    <h2 class="disp" style="font-size:clamp(40px,7vw,68px);font-weight:700;letter-spacing:-.04em;line-height:1;margin:0 0 1.5rem;
      background:linear-gradient(135deg,#FFFFFF 0%,#A78BFA 45%,#22D3EE 85%);background-size:200% auto;
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 6s linear infinite;">Ready to vet your next creator?</h2>
    <p style="font-size:17px;color:#5A5A78;line-height:1.7;margin:0 0 2.5rem;">Join brands using Vettd to make smarter influencer decisions.</p>
    <a href="/Analyse" target="_self" style="display:inline-block;background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;
      font-weight:700;font-size:16px;padding:19px 50px;border-radius:999px;text-decoration:none;
      box-shadow:0 0 64px rgba(124,58,237,.42);border:1px solid rgba(124,58,237,.5);transition:transform .3s,box-shadow .3s;"
      onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 0 90px rgba(124,58,237,.7)'"
      onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 0 64px rgba(124,58,237,.42)'">Start for free →</a>
    <div style="margin-top:1rem;font-size:12px;color:#222238;">No credit card required</div>
  </div>
</section>

<footer style="border-top:1px solid #14142A;padding:3rem 3.5rem 2rem;position:relative;z-index:2;">
  <div style="max-width:1120px;margin:0 auto;display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:2.5rem;align-items:start;">
    <div>
      <div class="brandmark" style="font-size:22px;font-weight:800;background:linear-gradient(135deg,#A78BFA,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1.25rem;">✦ VETTD</div>
      <a href="/About" target="_self" style="display:inline-flex;align-items:center;gap:10px;background:#101019;border:1px solid #1E1E32;
        color:#EDEDF5;font-size:13px;font-weight:600;padding:11px 20px;border-radius:999px;text-decoration:none;transition:border-color .3s,background .3s;"
        onmouseover="this.style.borderColor='rgba(124,58,237,.5)';this.style.background='#14141F'"
        onmouseout="this.style.borderColor='#1E1E32';this.style.background='#101019'">How Vettd works <span style="color:#A78BFA;">»</span></a>
      <div style="font-size:12px;color:#3A3A52;margin-top:1.75rem;line-height:1.6;">© 2026 Vettd. All rights reserved.<br>Built in Mumbai. Made for brands everywhere.</div>
    </div>
    <div>
      <div style="font-size:14px;font-weight:700;color:#EDEDF5;margin-bottom:1.1rem;">Product</div>
      <a href="/Analyse" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Analyse a creator</a>
      <a href="/Compare" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Compare creators</a>
      <a href="/#how" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">How it works</a>
      <a href="/About" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">About</a>
    </div>
    <div>
      <div style="font-size:14px;font-weight:700;color:#EDEDF5;margin-bottom:1.1rem;">Policy</div>
      <a href="/Legal" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Terms &amp; Conditions</a>
      <a href="/Legal" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Privacy Policy</a>
      <a href="/Legal" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Refund Policy</a>
    </div>
    <div>
      <div style="font-size:14px;font-weight:700;color:#EDEDF5;margin-bottom:1.1rem;">Connect</div>
      <a href="/Contact" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Contact us</a>
      <a href="/Founder" target="_self" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Founder</a>
      <a href="mailto:jadepinto96@gmail.com" style="display:block;font-size:13px;color:#7A7A98;text-decoration:none;margin-bottom:.8rem;">Email</a>
    </div>
  </div>
</footer>
</div>

<script>
(function(){
  // particles
  const c=document.getElementById('particles');
  if(c){const x=c.getContext('2d');function sz(){c.width=innerWidth;c.height=innerHeight;}sz();
    const P=[];for(let i=0;i<90;i++){P.push({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.5+.3,
      dx:(Math.random()-.5)*.3,dy:(Math.random()-.5)*.3,o:Math.random()*.5+.1,cl:['#A78BFA','#60A5FA','#22D3EE'][Math.floor(Math.random()*3)]});}
    (function d(){x.clearRect(0,0,c.width,c.height);P.forEach(p=>{x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fillStyle=p.cl;x.globalAlpha=p.o;x.fill();
      p.x+=p.dx;p.y+=p.dy;if(p.x<0||p.x>c.width)p.dx*=-1;if(p.y<0||p.y>c.height)p.dy*=-1;});requestAnimationFrame(d);})();
    addEventListener('resize',sz);}
  // cursor glow + subtle parallax drift on glow orbs
  const g=document.getElementById('cglow');
  const orbs=document.querySelectorAll('[data-orb]');
  if(g){addEventListener('mousemove',e=>{
    g.style.left=e.clientX+'px';g.style.top=e.clientY+'px';
    const mx=(e.clientX/innerWidth-.5),my=(e.clientY/innerHeight-.5);
    orbs.forEach((o,i)=>{const f=(i+1)*14;o.style.transform=`translate(${mx*f}px,${my*f}px)`;});
  });}
  // scroll reveal
  const io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});},{threshold:.12});
  function bind(){document.querySelectorAll('.reveal:not(.in)').forEach(el=>io.observe(el));}
  bind();setTimeout(bind,400);setTimeout(bind,1200);
  // count up
  function count(){document.querySelectorAll('.countup:not(.done)').forEach(el=>{
    const r=el.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0){el.classList.add('done');
      const t=parseFloat(el.dataset.target);let s=0;const step=t/45;
      const iv=setInterval(()=>{s+=step;if(s>=t){s=t;clearInterval(iv);}el.textContent=Number.isInteger(t)?Math.floor(s):s.toFixed(0);},22);}});}
  count();addEventListener('scroll',count);
})();
</script>
""", unsafe_allow_html=True)
