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
        "profile_pic": None, "full_name": None, "niche_guess": None,
        "avg_views": None,
        "_source": "manual", "_partial": True,
    }


def _category_to_niche(category):
    """Map an Instagram profile category to one of Vettd's niches."""
    if not category:
        return None
    c = category.lower()
    table = [
        (("beauty", "cosmetic", "skincare", "makeup"), "Beauty"),
        (("cloth", "apparel", "fashion", "shoe", "footwear", "jewel", "accessor"), "Fashion"),
        (("fitness", "gym", "sport", "athlete", "trainer", "yoga"), "Fitness"),
        (("food", "restaurant", "grocery", "beverage", "cafe", "kitchen", "chef"), "Food"),
        (("travel", "hotel", "tourism", "airline"), "Travel"),
        (("tech", "software", "electronic", "gadget", "app", "computer"), "Tech"),
        (("game", "gaming", "esport"), "Gaming"),
        (("financ", "bank", "invest", "money"), "Finance"),
        (("baby", "parent", "kid", "child", "mother"), "Parenting"),
    ]
    for keys, niche in table:
        if any(k in c for k in keys):
            return niche
    return "Lifestyle"


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


# ── Provider 2: RapidAPI — Instagram Scraper Stable API (basic stats only) ──
def _fetch_rapidapi(username, platform):
    key = _secret("RAPIDAPI_KEY")
    host = _secret("RAPIDAPI_HOST", "instagram-scraper-stable-api.p.rapidapi.com")
    handle = username.lstrip("@")
    try:
        r = requests.post(
            f"https://{host}/ig_get_fb_profile.php",
            data={"username_or_url": handle, "data": "basic"},
            headers={
                "x-rapidapi-key": key,
                "x-rapidapi-host": host,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=20,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        # response may be the profile dict directly, or nested under data/user
        if isinstance(data, dict) and isinstance(data.get("data"), dict):
            data = data["data"]
        if isinstance(data, dict) and isinstance(data.get("user"), dict):
            data = data["user"]

        def first(*keys):
            for k in keys:
                v = data.get(k)
                if isinstance(v, dict):
                    v = v.get("count")
                if v not in (None, "", 0):
                    return v
            return None

        prof = _empty_profile()
        prof["_source"] = "rapidapi"
        prof["_partial"] = True  # demographics not available from scrapers
        prof["followers"] = first("follower_count", "followers", "followers_count")
        prof["following"] = first("following_count", "following", "follows_count")
        prof["post_count"] = first("media_count", "posts", "post_count")
        prof["full_name"] = data.get("full_name") or None
        # prefer the HD pic if present, else the standard one
        hd = data.get("hd_profile_pic_url_info") or {}
        prof["profile_pic"] = (hd.get("url") if isinstance(hd, dict) else None) or data.get("profile_pic_url")
        prof["niche_guess"] = _category_to_niche(data.get("category"))
        if prof["followers"] is None:
            return None
        # second call: recent reels → real avg likes / comments / views
        media = _fetch_recent_media(handle, key, host)
        if media:
            if media.get("avg_likes"):
                prof["avg_likes"] = media["avg_likes"]
            if media.get("avg_comments"):
                prof["avg_comments"] = media["avg_comments"]
            if media.get("avg_views"):
                prof["avg_views"] = media["avg_views"]
        return prof
    except Exception:
        return None


def _fetch_recent_media(handle, key, host):
    """Pull recent reels and average their likes / comments / views. Robust to field-name variation."""
    try:
        r = requests.post(
            f"https://{host}/get_ig_user_reels.php",
            data={"username_or_url": handle, "amount": 12, "pagination_token": ""},
            headers={"x-rapidapi-key": key, "x-rapidapi-host": host,
                     "Content-Type": "application/x-www-form-urlencoded"},
            timeout=25,
        )
        if r.status_code != 200:
            return None
        payload = r.json()

        # find the list of media items wherever it lives
        items = None
        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            for key_ in ("items", "data", "reels", "edges", "media"):
                v = payload.get(key_)
                if isinstance(v, list):
                    items = v
                    break
                if isinstance(v, dict):
                    for k2 in ("items", "data", "reels", "edges"):
                        if isinstance(v.get(k2), list):
                            items = v[k2]
                            break
                if items:
                    break
        if not items:
            return None

        def grab(node, *needles):
            """find a numeric count whose key contains any needle; recurses through node/media wrappers."""
            if not isinstance(node, dict):
                return None
            for k, val in node.items():
                kl = k.lower()
                if any(n in kl for n in needles) and "disabl" not in kl:
                    if isinstance(val, bool):           # skip flags like like_and_view_counts_disabled
                        continue
                    if isinstance(val, (int, float)):
                        return val
                    if isinstance(val, dict) and isinstance(val.get("count"), (int, float)):
                        return val["count"]
            # one level deeper (e.g. node["node"] -> node["media"])
            for k in ("media", "node", "item"):
                if isinstance(node.get(k), dict):
                    deep = grab(node[k], *needles)
                    if deep is not None:
                        return deep
            return None

        likes, comments, views = [], [], []
        for it in items:
            l = grab(it, "like")
            c = grab(it, "comment")
            v = grab(it, "play", "view")
            if isinstance(l, (int, float)): likes.append(l)
            if isinstance(c, (int, float)): comments.append(c)
            if isinstance(v, (int, float)): views.append(v)

        def avg(xs):
            return int(sum(xs) / len(xs)) if xs else None

        return {"avg_likes": avg(likes), "avg_comments": avg(comments), "avg_views": avg(views)}
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
