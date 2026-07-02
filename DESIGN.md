# Vettd — Design System ("Refined Dark")

Source of truth for visual decisions. Derived via the `ui-ux-pro-max` skill for a
premium B2B creator-intelligence SaaS. Goal: look trustworthy enough to charge brands.

All tokens live in `utils/styles.py` `:root{}`. **Use the CSS variables, not raw hex**,
so the whole app stays consistent. New HTML you add should reference `var(--token)`.

## Tokens

| Token | Value | Use |
|-------|-------|-----|
| `--bg-deep` | `#08080C` | page canvas |
| `--bg-base` | `#0C0C14` | section base / tab bar |
| `--surface` | `#131320` | cards |
| `--surface-2` | `#1A1A2B` | raised / hover |
| `--surface-inset` | `#0A0A12` | inputs, wells |
| `--border` | `rgba(255,255,255,.08)` | hairline default (everywhere) |
| `--border-strong` | `rgba(255,255,255,.14)` | hover / emphasis |
| `--text-1` | `#ECECF3` | primary |
| `--text-2` | `#9595AE` | secondary |
| `--text-3` | `#63637E` | muted / labels |
| `--text-4` | `#41415A` | faint / disabled |
| `--accent` | `#7C6BF0` | one refined violet — primary actions, active states |
| `--accent-2` | `#9C8DF7` | accent hover |
| `--accent-soft` | `rgba(124,107,240,.12)` | tints / focus rings |
| `--cyan` | `#22D3EE` | data accent, **sparingly** |
| `--success` `--warning` `--danger` | `#34D399` `#F5A623` `#F0616D` | functional only |
| `--radius` / `--radius-sm` / `--radius-lg` | `14 / 10 / 20px` | cards / controls / hero |
| `--ease` / `--dur` | `cubic-bezier(.16,1,.3,1)` / `.22s` | motion |

## Principles (what makes it read premium)

1. **One surface system.** Never invent new card hex (`#15151F`, `#0D0D1A`, etc. are retired). Card = `--surface` + `1px --border`.
2. **Hairline borders, not glow.** Gradients/glow are reserved for the **wordmark + hero headline only**. Cards and modules are calm; hover = `--border-strong`, nothing more.
3. **SVG icons, never emoji.** Use Lucide outline paths (`stroke="currentColor"`). Icon set already inlined in `0_Analyse.py` (`_ICON`) and `4_Dashboard.py` (`_svg`): zap, shield, users, bars, activity.
4. **Tabular figures** on all metrics/scores (`.tnum` / `font-variant-numeric: tabular-nums`).
5. **One primary action per view.** Primary = solid `--accent`; secondary = `--surface` + hairline.
6. **Fonts:** Sora (display `.disp`), Inter (body), Syne (wordmark `.brandmark`). Not the problem — kept.

## Type scale
12 · 13 · 14 · 16 · 20 · 28 · 40 · 56  (px)

## Spacing
4 · 8 · 12 · 16 · 24 · 32 · 48  (px)

## Status: applied vs pending
- ✅ Global tokens + all Streamlit widgets (buttons, inputs, sliders, number inputs, tabs, metrics, alerts, download buttons)
- ✅ Analyse: input cards, enterprise module cards, SVG icons
- ✅ Dashboard: enterprise Advanced tab (5 modules), SVG icons
- ⏳ Pending per-page inline-hex polish: landing sections below hero, About/Founder/Contact/Legal/Compare, Dashboard report header, footer border colors
