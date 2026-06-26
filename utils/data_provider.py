"""
Vettd data provider layer.

Goal: one function — fetch_creator(username, platform) — that returns a normalised
dict the rest of the app already understands. Today it can run in three modes,
selected automatically by which secrets are configured:

  1. "modash"   — full data incl. audience demographics (paid, best)
  2. "rapidapi" — basic public stats only (cheap; demographics left blank)
  3. "manual"   — no API configured; returns None so the UI keeps manual input

Add keys in .streamlit/secrets.toml (or Streamlit Cloud → Settings → Secrets):

  # Option A — Modash (recommended once you have paying users)
  MODASH_API_KEY = "xxxx"

  # Option B — RapidAPI Instagram scraper (cheap, basic stats)
  RAPIDAPI_KEY  = "xxxx"
  RAPIDAPI_HOST = "instagram-scraper-api2.p.rapidapi.com"   # whichever endpoint you subscribe to

Nothing else in the app changes — the analyse page calls fetch_creator() and,
if it returns data, pre-fills the form; otherwise the user fills it in manually.
"""

import streamlit as st
import requests


def _secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def active_provider():
    """Which provider is configured right now."""
    if _secret("MODASH_API_KEY"):
        return "modash"
    if _secret("RAPIDAPI_KEY"):
        return "rapidapi"
    return "manual"


# Normalised shape every fetcher must return (None for unknown fields).
def _empty_profile():
    return {
        "followers": None, "following": None, "post_count": None,
        "avg_likes": None, "avg_comments": None, "avg_saves": None, "avg_shares": None,
        "posting_freq": None, "growth_rate_30d": None,
        "female_pct": None, "audience_authenticity": None,
        "age_18_24": None, "age_25_34": None, "age_35_44": None,
        "loc1_name": None, "loc1_pct": None,
        "loc2_name": None, "loc2_pct": None,
        "loc3_name": None, "loc3_pct": None,
        "_source": "manual", "_partial": True,
    }


# ── Provider 1: Modash (full data, incl. demographics) ──────────────────────
def _fetch_modash(username, platform):
    key = _secret("MODASH_API_KEY")
    handle = username.lstrip("@")
    plat = platform.lower()  # instagram / tiktok / youtube
    try:
        # Modash report endpoint (shape may vary by plan — adjust to your contract).
        r = requests.get(
            f"https://api.modash.io/v1/{plat}/profile/{handle}/report",
            headers={"Authorization": f"Bearer {key}"},
            timeout=15,
        )
        if r.status_code != 200:
            return None
        d = r.json().get("profile", r.json())

        prof = _empty_profile()
        prof["_source"] = "modash"
        prof["_partial"] = False
        prof["followers"] = d.get("followers")
        prof["following"] = d.get("following")
        prof["post_count"] = d.get("postsCount")
        prof["avg_likes"] = d.get("avgLikes")
        prof["avg_comments"] = d.get("avgComments")
        prof["avg_saves"] = d.get("avgSaves") or 0
        prof["avg_shares"] = d.get("avgShares") or 0

        aud = d.get("audience", {}) or {}
        genders = {g["code"]: g["weight"] for g in aud.get("genders", [])}
        if genders:
            prof["female_pct"] = round(genders.get("FEMALE", 0.5) * 100)
        ages = {a["code"]: a["weight"] for a in aud.get("ages", [])}
        if ages:
            prof["age_18_24"] = round(ages.get("18-24", 0) * 100)
            prof["age_25_34"] = round(ages.get("25-34", 0) * 100)
            prof["age_35_44"] = round(ages.get("35-44", 0) * 100)
        prof["audience_authenticity"] = round((1 - (aud.get("credibility", 0.2))) * 100) if "credibility" in aud else None

        geo = aud.get("geoCountries", [])[:3]
        for i, g in enumerate(geo, start=1):
            prof[f"loc{i}_name"] = g.get("name")
            prof[f"loc{i}_pct"] = round(g.get("weight", 0) * 100)
        return prof
    except Exception:
        return None


# ── Provider 2: RapidAPI Instagram scraper (basic stats only) ───────────────
def _fetch_rapidapi(username, platform):
    key = _secret("RAPIDAPI_KEY")
    host = _secret("RAPIDAPI_HOST", "instagram-scraper-api2.p.rapidapi.com")
    handle = username.lstrip("@")
    try:
        r = requests.get(
            f"https://{host}/v1/info",
            params={"username_or_id_or_url": handle},
            headers={"x-rapidapi-key": key, "x-rapidapi-host": host},
            timeout=15,
        )
        if r.status_code != 200:
            return None
        payload = r.json()
        # Instagram Scraper API2 nests under data -> (sometimes) user.
        data = payload.get("data", payload)
        if isinstance(data, dict) and isinstance(data.get("user"), dict):
            data = data["user"]

        def first(*keys):
            for k in keys:
                v = data.get(k)
                if isinstance(v, dict):  # e.g. {"count": 1234}
                    v = v.get("count")
                if v not in (None, "", 0):
                    return v
            return None

        prof = _empty_profile()
        prof["_source"] = "rapidapi"
        prof["_partial"] = True  # demographics not available from scrapers
        prof["followers"] = first("follower_count", "followers", "followers_count", "edge_followed_by")
        prof["following"] = first("following_count", "following", "follows_count", "edge_follow")
        prof["post_count"] = first("media_count", "posts", "post_count", "edge_owner_to_timeline_media")
        prof["avg_likes"] = first("avg_likes", "average_likes")
        prof["avg_comments"] = first("avg_comments", "average_comments")
        # only return if we actually got the core number
        return prof if prof["followers"] is not None else None
    except Exception:
        return None


def fetch_creator(username, platform):
    """
    Returns a normalised profile dict, or None if no provider is configured
    or the lookup failed (caller then keeps manual input).
    """
    if not username:
        return None
    provider = active_provider()
    if provider == "modash":
        return _fetch_modash(username, platform)
    if provider == "rapidapi":
        return _fetch_rapidapi(username, platform)
    return None  # manual mode
