# Vettd — Progress Log

Last updated: 2 July 2026

## Latest session (2 Jul 2026, cont.) — AI Analyst embedded (free + paid)
- Added **`utils/ai_analyst.py`**: an AI layer that *interprets* the creator's computed metrics into a written analysis (verdict, analysis, strengths, watch-outs, brand-fit, risk, recommended use, confidence). Structured JSON output, `st.cache_data` per-creator.
- **Dual provider, auto-detected, free-first:** uses **Google Gemini free tier** (`GEMINI_API_KEY`, `gemini-2.0-flash`, no credit card) if set; else **Claude** (`ANTHROPIC_API_KEY`, `claude-sonnet-5`, ~2c/report) if set; else rule-based fallback. Gemini wins if both are set.
- **Augments, never replaces** the transparent deterministic scores (the USP). Grounding: the model only sees the numbers Vettd computed — instructed not to invent facts about the person.
- Renders as a "Vettd AI Analyst" card on the Dashboard report (above the deep-dive). **Graceful fallback** with no key. Verified: AppTest green with/without keys; provider-detection + JSON-parse unit-tested.
- **Setup:** add ONE key to Streamlit secrets — free Gemini from https://aistudio.google.com/apikey (see `.streamlit/secrets.toml.example`). Deps: `google-generativeai>=0.8.0`, `anthropic>=0.40.0`.

## Latest session (2 Jul 2026, cont.) — Design system ("Refined Dark")
- Installed `ui-ux-pro-max` + `frontend-design` skills (manual copy into `~/.claude/skills/`, since `/plugin` isn't available in this app and the npm `uipro` binary is blocked in auto mode).
- Used ui-ux-pro-max engine to define a premium dark design system → **`DESIGN.md`** (source of truth). Goal: fix "looks unprofessional".
- **`utils/styles.py`**: added `:root` design tokens; refactored all shared component CSS to use them. Killed the ad-hoc card colors, replaced glow overload with hairline borders, calmed motion, added tabular figures, visible focus rings.
- **Emoji icons → inline Lucide SVGs** on Analyse module cards and the Dashboard enterprise tab (the #1 "unprofessional" signal per the skill).
- Verified live (Analyse module cards + landing hero screenshotted) and AppTest still green.
- **Whole-site polish DONE:** scripted remap of ~346 structural-gray/border/muted-text hexes → tokens across `app.py` + all pages (skipped any `gradient` line to preserve hero/wordmark gradients; left functional/semantic + chart colors untouched). Footer also tokenised. Verified live: hero, Compare, Founder all cohesive + premium; AppTest still green. Semantic accent violets (#A78BFA etc.) intentionally left as-is (already on-brand).
- If reverting/adjusting: tokens live in `utils/styles.py :root{}`; see `DESIGN.md`.

## Latest session (2 Jul 2026) — Enterprise Intelligence Suite rebuilt
- **Replaced the thin Predict/Match/Guard/Pulse modules** with 5 real, computed deliverables (researched vs HypeAuditor / CreatorIQ SafeIQ / Traackr / CreatorScore):
  1. **⚡ Forecast** — predictive campaign ROI: reach/impressions, **EMV (earned media value)**, est. conversions, ROI range + 3-tier budget scenario table.
  2. **🛡 Shield** — brand-safety & risk audit: fake-follower forensics, computed red-flag scan, crisis-risk score, **Go / Conditional / No-Go** verdict.
  3. **🧬 Audience DNA** — real-vs-suspicious split, **true-match to target persona %**, geo concentration, interest affinities, **roster-overlap / wasted-reach detector** (uses session saved-searches).
  4. **📊 Benchmark** — category **percentile rank**, cost-efficiency vs peers, saturation/exclusivity, 3 vetted lookalike alternatives (absorbs old Match).
  5. **✧ Pulse** — sentiment split, community-health tier (from real engagement depth), toxicity flag, dominant themes.
- Key upgrade: **outputs are computed from the creator's real stats + buyer context**, not echoed from sliders. Compute engine = `compute_forecast/shield/audience_dna/benchmark/pulse` in `utils/scoring.py`.
- Analyse page: 5 toggle-able module cards (`0_Analyse.py`) each showing what it produces + its own inputs (budget/objective, sensitivity/prohibited-keywords, target persona, product/competitors, sentiment/keywords).
- Dashboard Advanced tab (`4_Dashboard.py`) fully rewritten to render the 5 modules richly; legacy module names auto-migrate.
- **Bug fixed:** `generate_creator_report` crashed (`TypeError`) on None/string numeric fields; added `_num` coercion there **and** a defensive coercion pass at the top of `4_Dashboard.py` so no missing field can crash the report.
- Verified with Streamlit **AppTest** across 6 scenarios (all modules, roster overlap, legacy names, None-fields, Pro tier, single module) — all pass, no exceptions. Live browser confirmed the 5 Analyse cards render. (Driving Streamlit text-inputs programmatically to reach the Dashboard live is unreliable — AppTest is the source of truth.)
- **Not yet done:** enterprise module outputs are NOT in the exported HTML/CSV report yet (only on-screen). `.claude/launch.json` added for local preview (`python -m streamlit run app.py`).

---


**Vettd** is a creator-intelligence platform for brands: enter (or auto-fetch) a creator's stats and get a single transparent **Vettd Score (0–100)** plus a plain-English report, brand-fit, market-fit, reel analytics, comparison, and audience-overlap.

- **Live app:** https://get-vettd.streamlit.app
- **Repo:** https://github.com/jadepinto96-blip/vettd (deploys to Streamlit Community Cloud on push to `main`)
- **Stack:** Python + Streamlit, Plotly for charts, pandas, requests. Hosted free on Streamlit Community Cloud.
- **Founder:** Jade Pinto (Mumbai)

---

## What's been built

### Pages (Streamlit multipage app; `app.py` is the entry = landing page)
- **`app.py`** — marketing landing page (dark iridescent theme): sticky nav, hero, product mock-dashboard, capabilities grid, "What you actually get" feature showcase (3 alternating rows), Enterprise modules section, "how it works", "Why Vettd" comparison, stats band, pricing (4 tiers), testimonials, FAQ accordion, final CTA, multi-column footer.
- **`pages/0_Analyse.py`** — the core tool. Tier selector (Starter/Pro/Enterprise), live-fetch button, and input sections grouped into bordered cards: Creator details, Profile stats, Reel engagement, Audience demographics (Pro), Enterprise modules. Saved-searches (session history). Runs analysis → Dashboard.
- **`pages/4_Dashboard.py`** — the report. Circular gradient score ring, written verdict, MBTI-style report (archetype + summary + strengths/watch-outs + best-for + recommendation), highlight stats, deep-dive (metric strip, score breakdown, tabs: Engagement / Audience / Brand fit / Advanced). Advanced tab renders selected Enterprise modules (Predict/Match/Guard/Pulse). Exports: styled HTML report + readable CSV + share-link placeholder.
- **`pages/5_Compare.py`** — compare up to 3 creators; per-creator live fetch; reel-centric metrics (views/likes/comments/shares); winner pick; radar overlay; score bar chart; **audience-overlap detector**.
- **`pages/1_About.py`**, **`pages/2_Founder.py`**, **`pages/3_Contact.py`**, **`pages/6_Legal.py`** — marketing/info pages. Contact has a Formspree-backed form with mailto fallback.

### Core logic (`utils/`)
- **`utils/scoring.py`** — all scoring: engagement rate, fake-follower estimate, brand-fit, audience quality, growth, consistency, weighted **Vettd Score**, `estimate_cpe`, **Brand–Product Market Fit** + `recommend_creators`, **audience overlap**, and `generate_creator_report` (the MBTI-style narrative generator).
- **`utils/data_provider.py`** — pluggable live-data layer. `fetch_creator()` auto-selects **Modash** (full, incl. demographics), **RapidAPI** (basic + reels), or **manual** based on which secret is set. Wired to **Instagram Scraper Stable API** (RapidAPI): profile via `ig_get_fb_profile.php`, reels via `get_ig_user_reels.php` (averages likes/comments/views over last N reels). Also maps IG category → niche and pulls profile picture.
- **`utils/styles.py`** — `GLOBAL_CSS` (theme, gradient sliders, fonts) and reusable `SITE_FOOTER`.

### Key features working
- Vettd Score with transparent weighted breakdown
- **Live Instagram data** via RapidAPI (followers/following/posts + avg reel likes/comments/views) — CONFIRMED working
- Brand-fit **only computed when a brand is entered** (score reweights without it otherwise)
- Enterprise modules are selectable and gate the report sections
- HTML report export (printable to PDF) + readable Metric/Value CSV
- Saved searches (session), profile-picture avatar, auto-@ usernames, auto-niche from category

### Other artifacts
- **`ONEPAGER.md`** — pitch one-pager for incubators/grants.
- **`.streamlit/config.toml`** — dark theme, primaryColor #7C3AED (kills Streamlit's default red).

---

## Important technical decisions / architecture

1. **Streamlit multipage.** `app.py` (root) is the landing page; the analyse tool lives at `/Analyse`. Paid pricing CTAs → `/Contact`; Free → `/Analyse` (no checkout/auth built yet).
2. **HTML across `st.markdown` calls does NOT persist** — Streamlit auto-closes tags per call. This caused repeated bugs (empty boxes, raw-HTML leaks). **Rule: build any multi-element HTML block as ONE concatenated string in a single `st.markdown`, OR use `st.container(border=True)` to wrap real Streamlit widgets.** Do not open a `<div>` in one `st.markdown` and close it in another.
3. **No JS-dependent visibility.** Scroll-reveal was originally opacity:0 + IntersectionObserver; Streamlit often didn't run the JS, leaving content invisible (looked like "endless empty space"). Now uses a **CSS-only auto-playing animation** that ends visible.
4. **Decorative absolutely-positioned elements must be clipped** (`overflow:hidden` on their section/wrapper) or they inflate page scroll height.
5. **Data provider is pluggable** — swapping manual → RapidAPI → Modash is just a secret change; scoring functions take inputs from anywhere.
6. **Audience demographics can never be scraped** — only paid providers (Modash) have them. Manual/estimated for now.
7. Fonts: headings use **Sora** (`.disp`), logo uses **Syne** (`.brandmark`), body is Inter.

---

## Pending / incomplete

- **Self-serve billing + user accounts** — none. Paid plans route to Contact; onboarding is manual. This is the biggest gap before real revenue.
- **Persistent saved searches** — currently session-only (clears on reboot). Needs a DB (e.g. Supabase) + auth.
- **Modash integration** — code path exists but untested; field mapping in `_fetch_modash` will need adjusting to the real contract when subscribed.
- **Share link** (`/r/<id>`) is a placeholder — doesn't resolve to a real hosted report.
- **Custom domain** (e.g. vettd.com) — not set up; needs a paid host or proxy (Streamlit free tier can't map custom domains cleanly).
- **Contact form email delivery** — works only once `FORMSPREE_ID` is added to Streamlit Secrets; otherwise falls back to mailto.
- **Legal pages** — plain-language drafts, NOT lawyer-reviewed. Testimonials/some stats are illustrative placeholders — replace with real ones before pitching/charging.
- **Compare page** — inputs not yet wrapped in the premium bordered-card style used on Analyse; nav styling slightly differs from marketing pages.
- **TikTok/YouTube** — selectable but live fetch is Instagram-only.

## Known bugs / to verify next session

- **Analyse-page cards may still look flat.** We switched sections to `st.container(border=True)` and restyled `[data-testid="stVerticalBlockBorderWrapper"]` to a higher-contrast card (`#15151F`, visible border, shadow). User reported it "still looks the same" — needs verification after a hard refresh / app reboot. If still flat, inspect the live DOM (Chrome extension was not connected this session) to confirm the border-wrapper testid/selector on the deployed Streamlit version.
- **Streamlit Cloud caching** — CSS/theme changes (esp. `config.toml`) sometimes need a manual **Reboot app** (Manage app → ⋮ → Reboot) to show.
- **Instagram image URLs expire** — profile-pic avatars break on old/saved reports (fall back to initials). Fine for fresh fetches.
- **API key hygiene** — the RapidAPI key was pasted in chat/screenshots several times during setup; it should be **rotated** (RapidAPI → My Apps → Authorization → regenerate) and the new value put in Streamlit Secrets (`RAPIDAPI_KEY`, `RAPIDAPI_HOST`).

## Suggested next steps

1. Verify the analyse-page card styling on the live site (reboot + hard refresh); fix selector if needed.
2. Rotate the RapidAPI key.
3. Get 5–10 real brands/creators to try it; replace placeholder testimonials with real quotes.
4. Chase non-dilutive funding (SISFS grant / college incubator) using ONEPAGER.md; grab free cloud/AI credits.
5. When there's demand: add auth + Stripe + persistent saved searches; integrate Modash for real demographics.
