"""
Vettd AI Analyst — an AI layer that *interprets* the creator's computed metrics
into a written analysis. It augments (never replaces) the transparent
deterministic scores.

Two providers, auto-detected from whichever key is set:
  • FREE  — Google Gemini  (GEMINI_API_KEY)   ← default, free tier, no card
  • PAID  — Anthropic Claude (ANTHROPIC_API_KEY) ← premium, ~2c/report

Grounding rule: the model only ever sees the quantitative signals Vettd already
computed. It interprets numbers; it must not invent facts about the person.

Falls back to None when no key is configured, so the app keeps working on free
hosting (the Dashboard then uses the rule-based report in utils/scoring.py).
"""
import json
import os
import streamlit as st

CLAUDE_MODEL = "claude-sonnet-5"
GEMINI_MODEL_DEFAULT = "gemini-2.0-flash"

SYSTEM_PROMPT = """You are Vettd's senior creator-intelligence analyst. Brands pay Vettd to decide whether to work with a social-media creator, so your read must be sharp, honest, and useful.

You are given ONLY quantitative signals and self-reported campaign inputs about one creator. You do NOT have their actual posts, captions, or biography.

Hard rules:
- Interpret the numbers you are given. Do NOT invent facts about the person, their content, specific posts, controversies, sponsors, or life events.
- Reference the actual figures in your reasoning (e.g. "a 6.2% engagement rate on 250k followers").
- When a signal is estimated, missing, or self-reported, treat it with appropriate caution and reflect that in your confidence.
- Be specific and decisive. Avoid generic filler that would apply to any creator.
- Write in plain, professional English for a brand-marketing audience. No hype, no emoji.

You must respond with ONLY a single JSON object (no prose, no code fences) with exactly these keys:
{
  "verdict": "one punchy sentence — the headline recommendation",
  "analysis": "2-4 sentences interpreting what this creator's numbers actually mean for a brand",
  "strengths": ["2-4 short, specific strengths grounded in the data"],
  "watchouts": ["2-4 short, specific risks or caveats grounded in the data"],
  "brand_fit": "1-2 sentences on fit for the given brand/product; if no brand was provided, say what kind of brand this creator suits",
  "risk": "1-2 sentences on authenticity / fake-follower / consistency risk",
  "recommended_use": "1-2 sentences on the campaign types, objectives, or funnel stage this creator is best for",
  "confidence": "High | Medium | Low — your confidence given how complete and reliable the data is"
}"""


def _secret(name):
    try:
        v = st.secrets.get(name)
        if v:
            return v
    except Exception:
        pass
    return os.environ.get(name)


def _provider():
    """Prefer the free provider; use Claude only if its key is set."""
    if _secret("GEMINI_API_KEY"):
        return "gemini"
    if _secret("ANTHROPIC_API_KEY"):
        return "claude"
    return None


def ai_available() -> bool:
    return _provider() is not None


def _build_payload(d: dict, metrics: dict) -> str:
    brand = (d.get("brand_name") or "").strip() or (d.get("brand_industry") or "").strip()
    payload = {
        "creator": {
            "name": d.get("creator_name"), "username": d.get("username"),
            "platform": d.get("platform"), "niche": d.get("niche"),
            "followers": d.get("followers"), "following": d.get("following"),
            "total_posts": d.get("post_count"), "posts_per_week": d.get("posting_freq"),
            "growth_rate_30d_pct": d.get("growth_rate_30d"),
        },
        "reel_engagement": {
            "avg_likes": d.get("avg_likes"), "avg_comments": d.get("avg_comments"),
            "avg_saves": d.get("avg_saves"), "avg_shares": d.get("avg_shares"),
            "avg_views": d.get("avg_views"),
        },
        "audience": {
            "female_pct": d.get("female_pct"), "male_pct": d.get("male_pct"),
            "authenticity_pct": d.get("audience_authenticity"),
            "age_18_24_pct": d.get("age_18_24"), "age_25_34_pct": d.get("age_25_34"),
            "age_35_44_pct": d.get("age_35_44"),
            "top_locations": [
                {"name": d.get("loc1_name"), "pct": d.get("loc1_pct")},
                {"name": d.get("loc2_name"), "pct": d.get("loc2_pct")},
                {"name": d.get("loc3_name"), "pct": d.get("loc3_pct")},
            ],
        },
        "vettd_computed_scores": {
            "vettd_score_0_100": metrics.get("vettd_score"),
            "engagement_rate_pct": metrics.get("engagement_rate"),
            "fake_follower_score_0_100_higher_worse": metrics.get("fake_score"),
            "brand_fit_0_100": metrics.get("brand_fit"),
            "audience_quality_0_100": metrics.get("aud_quality"),
            "consistency_0_100": metrics.get("consistency_score"),
            "growth_0_100": metrics.get("growth_score"),
            "est_cost_per_post": metrics.get("est_cost_per_post"),
        },
        "brand_context": {
            "brand": brand or None, "brand_industry": d.get("brand_industry") or None,
            "product": d.get("product_text") or None,
        },
        "plan_tier": d.get("tier"),
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def _extract_json(text: str):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                return None
    return None


def _call_gemini(payload_json: str) -> dict:
    key = _secret("GEMINI_API_KEY")
    try:
        import google.generativeai as genai
    except ImportError:
        return {"_error": "google-generativeai not installed."}
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel(
            _secret("GEMINI_MODEL") or GEMINI_MODEL_DEFAULT,
            system_instruction=SYSTEM_PROMPT,
        )
        resp = model.generate_content(
            f"Analyse this creator brief and respond with ONLY the JSON object described.\n\n{payload_json}",
            generation_config={
                "response_mime_type": "application/json",
                "max_output_tokens": 1500,
                "temperature": 0.4,
            },
        )
        text = resp.text
    except Exception as e:
        return {"_error": str(e)[:200]}
    parsed = _extract_json(text)
    return parsed or {"_error": "Could not parse the model response."}


def _call_claude(payload_json: str) -> dict:
    key = _secret("ANTHROPIC_API_KEY")
    try:
        import anthropic
    except ImportError:
        return {"_error": "anthropic not installed."}
    try:
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            output_config={"effort": "low"},
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Analyse this creator brief and respond with ONLY the JSON object described.\n\n{payload_json}",
            }],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    except Exception as e:
        return {"_error": str(e)[:200]}
    parsed = _extract_json(text)
    return parsed or {"_error": "Could not parse the model response."}


@st.cache_data(show_spinner=False, ttl=3600)
def _cached_call(provider: str, payload_json: str) -> dict | None:
    if provider == "gemini":
        return _call_gemini(payload_json)
    if provider == "claude":
        return _call_claude(payload_json)
    return None


def generate_ai_analysis(d: dict, metrics: dict) -> dict | None:
    """Returns the analysis dict, an {'_error': ...} dict, or None when no AI
    provider is configured."""
    provider = _provider()
    if not provider:
        return None
    return _cached_call(provider, _build_payload(d, metrics))
