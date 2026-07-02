# Vettd — Progress Log

Last updated: 2 July 2026

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
