import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styles import GLOBAL_CSS, SITE_FOOTER
from utils.modules import MODULES, MODULES_BY_KEY

st.set_page_config(page_title="Vettd — Enterprise Intelligence", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"], #MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
.feat-wrap { max-width:1000px; margin:0 auto; padding:0 2rem; }
.feat-out { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:1.4rem 1.5rem; transition:border-color var(--dur) ease; }
.feat-out:hover { border-color:var(--border-strong); }
.feat-step-n { width:30px;height:30px;border-radius:9px;background:var(--accent-soft);border:1px solid var(--accent-line);color:var(--accent-2);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0; }
</style>
""", unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:1.25rem 2.5rem;
    border-bottom:1px solid var(--border);background:rgba(8,8,12,0.9);backdrop-filter:blur(20px);">
  <a href="/" target="_self" class="brandmark" style="font-size:20px;font-weight:800;letter-spacing:-.02em;
      background:linear-gradient(135deg,#A78BFA,#60A5FA,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;">✦ Vettd</a>
  <div style="display:flex;gap:1.75rem;align-items:center;">
    <a href="/Analyse" target="_self" style="font-size:13px;color:#A78BFA;text-decoration:none;font-weight:600;">Analyse a creator</a>
    <a href="/Compare" target="_self" style="font-size:13px;color:var(--text-3);text-decoration:none;">Compare</a>
    <a href="/Contact" target="_self" style="font-size:13px;color:var(--text-3);text-decoration:none;">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)

key = st.query_params.get("m")
mod = MODULES_BY_KEY.get(key)


def _tool_switcher(active_key):
    chips = ""
    for m in MODULES:
        on = m["key"] == active_key
        chips += (
            f'<a href="/Feature?m={m["key"]}" target="_self" style="display:inline-flex;align-items:center;gap:8px;text-decoration:none;'
            f'font-size:13px;font-weight:600;padding:8px 15px;border-radius:999px;'
            f'{"background:"+m["color"]+"1A;border:1px solid "+m["color"]+"55;color:"+m["color"]+";" if on else "background:var(--surface);border:1px solid var(--border);color:var(--text-2);"}">'
            f'<span style="width:15px;height:15px;display:inline-flex;color:{m["color"]};">{m["icon"]}</span>{m["name"]}</a>'
        )
    return f'<div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">{chips}</div>'


if not mod:
    # index — pick a tool
    cards = ""
    for m in MODULES:
        cards += (
            f'<a href="/Feature?m={m["key"]}" target="_self" class="lift" style="text-decoration:none;background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:1.75rem;display:block;">'
            f'<div style="width:44px;height:44px;border-radius:12px;background:{m["color"]}1A;display:flex;align-items:center;justify-content:center;color:{m["color"]};margin-bottom:1rem;"><span style="width:22px;height:22px;display:inline-flex;">{m["icon"]}</span></div>'
            f'<div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{m["color"]};margin-bottom:4px;">{m["sub"]}</div>'
            f'<div class="disp" style="font-size:22px;font-weight:700;color:var(--text-1);margin-bottom:.6rem;">{m["name"]}</div>'
            f'<div style="font-size:13.5px;color:var(--text-2);line-height:1.65;">{m["short"]}</div>'
            f'<div style="font-size:13px;font-weight:600;color:{m["color"]};margin-top:1rem;">Explore {m["name"]} →</div></a>'
        )
    st.markdown(f"""
    <div class="feat-wrap" style="padding-top:4rem;padding-bottom:4rem;">
      <div style="text-align:center;margin-bottom:2.5rem;">
        <div style="font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#22D3EE;margin-bottom:1rem;">Enterprise intelligence</div>
        <h1 class="disp" style="font-size:clamp(34px,5vw,52px);font-weight:800;letter-spacing:-.03em;margin:0 0 1rem;color:var(--text-1);">Five ways to vet smarter.</h1>
        <p style="font-size:16px;color:var(--text-3);max-width:560px;margin:0 auto;line-height:1.7;">Each module turns raw creator data into one clear, defensible decision. Pick one to see exactly what it does.</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.25rem;">{cards}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(SITE_FOOTER, unsafe_allow_html=True)
    st.stop()

# ── DETAIL PAGE FOR ONE MODULE ──
c = mod["color"]
outputs_html = "".join(
    f'<div class="feat-out"><div style="font-size:14.5px;font-weight:700;color:var(--text-1);margin-bottom:5px;">{title}</div>'
    f'<div style="font-size:13px;color:var(--text-2);line-height:1.6;">{desc}</div></div>'
    for title, desc in mod["outputs"]
)
steps_html = "".join(
    f'<div style="display:flex;gap:14px;align-items:flex-start;margin-bottom:1.1rem;">'
    f'<div class="feat-step-n">{i+1}</div>'
    f'<div><div style="font-size:15px;font-weight:700;color:var(--text-1);">{t}</div>'
    f'<div style="font-size:13.5px;color:var(--text-2);line-height:1.6;margin-top:3px;">{dsc}</div></div></div>'
    for i, (t, dsc) in enumerate(mod["how"])
)
what_html = "".join(
    f'<p style="font-size:15.5px;color:#C2C2D6;line-height:1.85;margin:0 0 1.1rem;">{p}</p>' for p in mod["what"]
)

st.markdown(f"""
<div class="feat-wrap">
  <!-- HERO -->
  <div style="text-align:center;padding:4rem 0 2.5rem;">
    <div style="width:60px;height:60px;border-radius:16px;background:{c}1A;border:1px solid {c}44;display:inline-flex;align-items:center;justify-content:center;color:{c};margin-bottom:1.25rem;"><span style="width:30px;height:30px;display:inline-flex;">{mod['icon']}</span></div>
    <div style="font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:{c};margin-bottom:.75rem;">Vettd {mod['name']} · {mod['sub']}</div>
    <h1 class="disp" style="font-size:clamp(32px,5vw,52px);font-weight:800;letter-spacing:-.03em;line-height:1.08;margin:0 auto 1.1rem;max-width:760px;color:var(--text-1);">{mod['hero']}</h1>
    <p style="font-size:16.5px;color:var(--text-3);max-width:620px;margin:0 auto 1.75rem;line-height:1.75;">{mod['short']}</p>
    <a href="/Analyse" target="_self" style="display:inline-block;background:var(--accent);color:#fff;font-weight:600;font-size:14px;padding:12px 26px;border-radius:999px;text-decoration:none;">Try {mod['name']} free →</a>
  </div>

  <!-- WHAT IT DOES -->
  <div style="border-top:1px solid var(--border);padding:3rem 0;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{c};margin-bottom:1rem;">What it does</div>
    <div style="max-width:720px;">{what_html}</div>
  </div>

  <!-- WHAT YOU GET -->
  <div style="border-top:1px solid var(--border);padding:3rem 0;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{c};margin-bottom:1.5rem;">What you get</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;">{outputs_html}</div>
  </div>

  <!-- HOW IT WORKS -->
  <div style="border-top:1px solid var(--border);padding:3rem 0;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{c};margin-bottom:1.5rem;">How it works</div>
    <div style="max-width:640px;">{steps_html}</div>
    <div style="margin-top:1.5rem;background:var(--surface);border:1px solid var(--border);border-left:2px solid {c};border-radius:0 12px 12px 0;padding:1rem 1.25rem;font-size:13.5px;color:var(--text-2);line-height:1.6;">
      <b style="color:var(--text-1);">Best for:</b> {mod['who']}</div>
  </div>

  <!-- OTHER TOOLS -->
  <div style="border-top:1px solid var(--border);padding:3rem 0 1rem;text-align:center;">
    <div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);margin-bottom:1.25rem;">The rest of the suite</div>
    {_tool_switcher(mod['key'])}
  </div>

  <!-- CTA -->
  <div style="margin:2rem 0 4rem;text-align:center;background:linear-gradient(160deg,{c}14,transparent);border:1px solid {c}33;border-radius:24px;padding:3rem 2rem;">
    <h2 class="disp" style="font-size:clamp(26px,4vw,38px);font-weight:800;letter-spacing:-.02em;margin:0 0 .75rem;color:var(--text-1);">Vet your next creator with {mod['name']}.</h2>
    <p style="font-size:15px;color:var(--text-3);margin:0 auto 1.5rem;max-width:460px;line-height:1.7;">Run a free analysis and see {mod['name']} in your report in seconds.</p>
    <a href="/Analyse" target="_self" style="display:inline-block;background:var(--accent);color:#fff;font-weight:600;font-size:15px;padding:13px 30px;border-radius:999px;text-decoration:none;">Start free →</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(SITE_FOOTER, unsafe_allow_html=True)
