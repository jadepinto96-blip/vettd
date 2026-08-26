def calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves, avg_views=None):
    """Engagement rate as a %.

    For reels/video, engagement is measured against VIEWS (the reach that
    actually saw the content), not followers — otherwise a viral reel with far
    more views than followers produces a nonsensical >100% rate. When view data
    isn't available (manual / feed-only), fall back to followers.
    """
    engagements = (avg_likes or 0) + (avg_comments or 0) + (avg_saves or 0)
    denom = avg_views if (avg_views and avg_views > 0) else followers
    if not denom:
        return 0
    return round((engagements / denom) * 100, 2)


def generate_creator_report(d, engagement_rate, fake_score, brand_fit,
                            aud_quality, growth_score, consistency_score, vettd_score):
    """
    Produce an MBTI-style, plain-English report for a creator:
    an archetype label + description, a summary paragraph, strengths,
    watch-outs, who they're best for, and a recommendation.
    Everything is derived from the computed signals.
    """
    def _num(key, default=0):
        """Coerce a possibly-missing / None / string field to a float safely."""
        v = d.get(key, default)
        if v is None or v == "":
            return default
        try:
            return float(v)
        except (TypeError, ValueError):
            return default

    # normalise the numeric fields this report reads so nothing here can TypeError
    d = dict(d)
    for _k in ("followers", "audience_authenticity", "growth_rate_30d",
               "posting_freq", "avg_saves", "avg_comments"):
        d[_k] = _num(_k, 0)
    followers = int(d["followers"])
    auth = int(round(d["audience_authenticity"]))
    d["audience_authenticity"] = auth
    niche = d["niche"]
    name = d["creator_name"]
    brand = (d.get("brand_name") or "").strip() or (d.get("brand_industry") or "").strip()
    has_brand = bool(brand) and brand_fit is not None

    # tier by size
    if followers < 10_000:
        size = "nano"
    elif followers < 100_000:
        size = "micro"
    elif followers < 1_000_000:
        size = "mid-tier"
    else:
        size = "macro"

    high_eng = engagement_rate >= 5
    rising = d["growth_rate_30d"] >= 3
    authentic = auth >= 80

    # ── Archetype (the "personality type") ──
    if high_eng and authentic and size in ("nano", "micro"):
        archetype = "The Trusted Insider"
        arch_desc = "A tight-knit, highly engaged community that genuinely listens. Small but mighty — their word carries real weight."
    elif rising and high_eng:
        archetype = "The Rising Star"
        arch_desc = "Fast-growing momentum paired with strong engagement. Catch them now before they get expensive."
    elif size in ("mid-tier", "macro") and high_eng:
        archetype = "The Powerhouse"
        arch_desc = "Serious reach that still drives genuine interaction — the rare combination of scale and connection."
    elif size in ("mid-tier", "macro") and not high_eng:
        archetype = "The Broad Broadcaster"
        arch_desc = "Wide reach with lighter per-post engagement. Best for awareness plays, not deep conversion."
    elif not authentic:
        archetype = "The Question Mark"
        arch_desc = "The numbers look big, but audience quality raises flags worth checking before committing budget."
    else:
        archetype = "The Steady Contender"
        arch_desc = "A solid, dependable profile without a standout signal — a safe, mid-risk choice."

    # ── Summary paragraph ──
    summary = (
        f"{name} is a {size} {niche.lower()} creator with {followers:,} followers and a "
        f"{engagement_rate}% engagement rate — {'well above' if high_eng else 'around' if engagement_rate>=2 else 'below'} "
        f"the typical benchmark for this size. Their audience looks {auth}% authentic, "
        f"and the account is {'growing fast' if rising else 'growing steadily' if d['growth_rate_30d']>0 else 'flat or declining'} "
        f"month-on-month. Overall, this profile reads as “{archetype}”."
    )

    # ── Strengths ──
    strengths = []
    if high_eng:
        strengths.append(f"Strong engagement ({engagement_rate}%) — the audience genuinely interacts, not just follows.")
    if authentic:
        strengths.append(f"High audience authenticity ({auth}%) — low fake-follower risk, real people behind the numbers.")
    if rising:
        strengths.append(f"Rising fast (+{d['growth_rate_30d']}% in 30 days) — momentum on their side.")
    if has_brand and brand_fit >= 70:
        strengths.append(f"Strong alignment with {brand} ({brand_fit}/100 brand-fit).")
    if consistency_score >= 80:
        strengths.append(f"Posts consistently ({d['posting_freq']}/week) — a reliable, active partner.")
    if d["avg_saves"] > d["avg_comments"]:
        strengths.append("High save rate — content people want to come back to (a strong intent signal).")
    if not strengths:
        strengths.append("A balanced profile with no major red flags.")

    # ── Watch-outs ──
    watchouts = []
    if fake_score >= 40:
        watchouts.append(f"Elevated fake-follower score ({fake_score}/100) — vet the audience quality before committing.")
    if not high_eng and engagement_rate < 2:
        watchouts.append(f"Low engagement ({engagement_rate}%) — reach may not convert into action.")
    if has_brand and brand_fit < 55:
        watchouts.append(f"Weaker brand alignment ({brand_fit}/100) — the audience may not match {brand}'s target.")
    if d["growth_rate_30d"] <= 0:
        watchouts.append("Flat or declining growth — the audience isn't expanding right now.")
    if auth < 65:
        watchouts.append(f"Audience authenticity is on the lower side ({auth}%).")
    if not watchouts:
        watchouts.append("No significant concerns surfaced in the data.")

    # ── Best for ──
    if high_eng and size in ("nano", "micro"):
        best_for = "Conversion-focused campaigns, product launches, and authentic reviews where trust matters more than raw reach."
    elif size in ("mid-tier", "macro") and not high_eng:
        best_for = "Top-of-funnel awareness and broad reach campaigns."
    elif rising:
        best_for = "Brands wanting to lock in a creator early, before their rates climb."
    else:
        best_for = "Balanced campaigns combining reasonable reach with genuine engagement."

    # ── Recommendation ──
    _for = f" for {brand}" if has_brand else ""
    if vettd_score >= 70:
        rec = f"Recommended. {name} is a strong choice{_for} — worth reaching out."
    elif vettd_score >= 55:
        rec = f"Worth considering. {name} could work{_for} with the right brief and budget."
    elif vettd_score >= 40:
        rec = f"Proceed with caution. {name} has gaps{_for}; consider the recommended alternatives first."
    else:
        rec = f"Not recommended{_for} right now. The risks outweigh the upside."
    if not has_brand:
        rec += " Add your brand name to unlock brand-fit scoring."

    return {
        "archetype": archetype, "archetype_desc": arch_desc, "summary": summary,
        "strengths": strengths, "watchouts": watchouts, "best_for": best_for,
        "recommendation": rec, "size": size,
    }


def estimate_fake_follower_score(followers, following, avg_likes, avg_comments):
    if followers == 0:
        return 50
    engagement = (avg_likes + avg_comments) / followers
    ratio = followers / max(following, 1)
    fake_score = 100
    if engagement > 0.06:
        fake_score -= 35
    elif engagement > 0.03:
        fake_score -= 25
    elif engagement > 0.01:
        fake_score -= 10
    if ratio > 10:
        fake_score -= 20
    elif ratio > 3:
        fake_score -= 10
    if followers > 1_000_000 and engagement < 0.01:
        fake_score += 15
    return max(0, min(100, fake_score))


def calculate_brand_fit_score(niche, brand_industry, audience_female_pct, audience_age_18_34, posting_frequency_per_week):
    score = 50
    niche_map = {
        "fashion": ["fashion", "beauty", "lifestyle", "luxury"],
        "fitness": ["fitness", "health", "wellness", "sport"],
        "tech": ["tech", "gaming", "software", "electronics"],
        "food": ["food", "beverage", "restaurant", "fmcg"],
        "travel": ["travel", "hospitality", "airline", "tourism"],
        "beauty": ["beauty", "fashion", "skincare", "cosmetics"],
        "gaming": ["gaming", "tech", "esports", "entertainment"],
        "lifestyle": ["lifestyle", "fashion", "home", "wellness"],
    }
    niche_lower = niche.lower()
    brand_lower = brand_industry.lower()
    for key, related in niche_map.items():
        if key in niche_lower:
            if any(r in brand_lower for r in related):
                score += 25
            break
    if audience_age_18_34 > 60:
        score += 10
    elif audience_age_18_34 > 40:
        score += 5
    if posting_frequency_per_week >= 3:
        score += 10
    elif posting_frequency_per_week >= 1:
        score += 5
    return min(100, score)


def calculate_audience_quality_score(fake_follower_score, engagement_rate, audience_authenticity_pct):
    authenticity_component = audience_authenticity_pct * 0.4
    engagement_component = min(engagement_rate * 5, 40)
    fake_penalty = (fake_follower_score / 100) * 20
    score = authenticity_component + engagement_component - fake_penalty
    return max(0, min(100, round(score)))


def calculate_growth_score(growth_rate_30d):
    if growth_rate_30d >= 5:
        return 100
    elif growth_rate_30d >= 2:
        return 80
    elif growth_rate_30d >= 1:
        return 60
    elif growth_rate_30d >= 0:
        return 40
    else:
        return 20


def calculate_consistency_score(posting_frequency_per_week):
    if posting_frequency_per_week >= 5:
        return 100
    elif posting_frequency_per_week >= 3:
        return 80
    elif posting_frequency_per_week >= 1:
        return 60
    elif posting_frequency_per_week >= 0.5:
        return 40
    else:
        return 20


def calculate_vettd_score(engagement_rate, fake_follower_score, brand_fit_score,
                           audience_quality_score, consistency_score, growth_score):
    weights = {
        "engagement": 0.25,
        "authenticity": 0.20,
        "brand_fit": 0.20,
        "audience_quality": 0.15,
        "consistency": 0.10,
        "growth": 0.10,
    }
    engagement_normalized = min(engagement_rate * 10, 100)
    authenticity_normalized = 100 - fake_follower_score

    score = (
        engagement_normalized * weights["engagement"] +
        authenticity_normalized * weights["authenticity"] +
        brand_fit_score * weights["brand_fit"] +
        audience_quality_score * weights["audience_quality"] +
        consistency_score * weights["consistency"] +
        growth_score * weights["growth"]
    )
    return round(min(100, max(0, score)))


def score_label(score):
    if score >= 85:
        return "Exceptional", "#1D9E75"
    elif score >= 70:
        return "Strong fit", "#378ADD"
    elif score >= 55:
        return "Moderate fit", "#BA7517"
    elif score >= 40:
        return "Weak fit", "#D85A30"
    else:
        return "Not recommended", "#E24B4A"


def estimate_cpe(followers, engagement_rate):
    base_rate = 0.01
    if followers < 10_000:
        cpm = 15
    elif followers < 100_000:
        cpm = 25
    elif followers < 1_000_000:
        cpm = 40
    else:
        cpm = 70
    estimated_reach = followers * (engagement_rate / 100)
    cost_per_post = (estimated_reach / 1000) * cpm
    cost_per_engagement = cost_per_post / max(estimated_reach, 1)
    return round(cost_per_post, 2), round(cost_per_engagement, 4)


def estimate_audience_overlap(a, b):
    """
    Estimate how much two creators' audiences overlap (0–100%).
    Brands running multi-creator campaigns waste budget when overlap is high —
    they pay twice to reach the same people. Heuristic uses niche, platform,
    audience-size band and authenticity (no follower-level data needed).

    Each creator dict needs: niche, platform, followers, auth (authenticity %).
    """
    score = 0.0
    # 1. Same niche is the biggest driver of shared audience (up to 55)
    if a["niche"].lower() == b["niche"].lower():
        score += 55
    else:
        related = {
            "fashion": {"beauty", "lifestyle"}, "beauty": {"fashion", "lifestyle"},
            "lifestyle": {"fashion", "beauty", "travel", "food"},
            "fitness": {"food", "lifestyle"}, "food": {"lifestyle", "fitness"},
            "tech": {"gaming", "finance"}, "gaming": {"tech"},
            "travel": {"lifestyle"}, "finance": {"tech"},
        }
        if b["niche"].lower() in related.get(a["niche"].lower(), set()):
            score += 28
        else:
            score += 6
    # 2. Same platform → audiences can literally overlap (up to 20)
    if a.get("platform", "Instagram") == b.get("platform", "Instagram"):
        score += 20
    # 3. Similar audience size band → more likely to share the mainstream of the niche (up to 15)
    fa, fb = max(a["followers"], 1), max(b["followers"], 1)
    ratio = min(fa, fb) / max(fa, fb)
    score += ratio * 15
    # 4. Two highly authentic audiences in the same niche overlap a bit less
    #    (real, engaged niches fragment); low authenticity inflates apparent overlap
    avg_auth = (a.get("auth", 80) + b.get("auth", 80)) / 2
    score += (100 - avg_auth) * 0.1
    return round(max(0, min(100, score)))


def overlap_verdict(pct):
    if pct >= 65:
        return "High overlap", "#EF4444", "You'd likely pay twice to reach the same audience. Pick one."
    elif pct >= 45:
        return "Moderate overlap", "#F59E0B", "Some shared audience — fine if budgets are staggered."
    else:
        return "Low overlap", "#10B981", "Largely distinct audiences — strong combination for wider reach."


# ── Product category → ideal audience profile ──────────────────────────────
# Each product maps to: matching creator niches, ideal female %, ideal age band,
# and a typical price point (affects which audience size/affluence fits best).
PRODUCT_PROFILES = {
    "skincare":   {"niches": ["beauty", "fashion", "lifestyle"], "female": 75, "age": "18-34", "price": "mid"},
    "makeup":     {"niches": ["beauty", "fashion"], "female": 80, "age": "18-34", "price": "mid"},
    "fashion":    {"niches": ["fashion", "lifestyle", "beauty"], "female": 65, "age": "18-34", "price": "mid"},
    "luxury":     {"niches": ["fashion", "lifestyle", "travel"], "female": 60, "age": "25-44", "price": "high"},
    "fitness":    {"niches": ["fitness", "lifestyle"], "female": 50, "age": "18-34", "price": "mid"},
    "supplement": {"niches": ["fitness", "lifestyle", "food"], "female": 45, "age": "18-34", "price": "low"},
    "food":       {"niches": ["food", "lifestyle"], "female": 55, "age": "25-44", "price": "low"},
    "beverage":   {"niches": ["food", "lifestyle", "fitness"], "female": 50, "age": "18-34", "price": "low"},
    "tech":       {"niches": ["tech", "gaming"], "female": 30, "age": "18-34", "price": "high"},
    "gaming":     {"niches": ["gaming", "tech"], "female": 30, "age": "18-24", "price": "mid"},
    "travel":     {"niches": ["travel", "lifestyle"], "female": 55, "age": "25-44", "price": "high"},
    "finance":    {"niches": ["finance", "tech", "lifestyle"], "female": 40, "age": "25-44", "price": "high"},
    "baby":       {"niches": ["parenting", "lifestyle"], "female": 80, "age": "25-44", "price": "mid"},
    "home":       {"niches": ["lifestyle", "fashion", "food"], "female": 65, "age": "25-44", "price": "mid"},
}


def _match_product_profile(product_text, brand_industry):
    """Find the best product profile from free-text product / brand industry."""
    blob = f"{product_text} {brand_industry}".lower()
    for key, prof in PRODUCT_PROFILES.items():
        if key in blob:
            return key, prof
    # loose keyword fallbacks
    fallbacks = {
        "serum": "skincare", "cream": "skincare", "cosmetic": "makeup", "lipstick": "makeup",
        "clothing": "fashion", "apparel": "fashion", "watch": "luxury", "jewel": "luxury",
        "gym": "fitness", "protein": "supplement", "snack": "food", "drink": "beverage",
        "app": "tech", "software": "tech", "gadget": "tech", "console": "gaming",
        "hotel": "travel", "flight": "travel", "invest": "finance", "bank": "finance",
        "diaper": "baby", "toy": "baby", "furniture": "home", "decor": "home",
    }
    for kw, key in fallbacks.items():
        if kw in blob:
            return key, PRODUCT_PROFILES[key]
    return None, None


def calculate_market_fit_score(product_text, brand_industry, creator_niche,
                               audience_female_pct, age_18_24, age_25_34, age_35_44,
                               audience_authenticity, engagement_rate, followers):
    """
    Brand product ↔ creator-audience market fit (0–100).
    Scores how well THIS product fits THIS creator's specific audience,
    not just the creator in isolation.
    """
    key, prof = _match_product_profile(product_text, brand_industry)
    breakdown = {}

    # If we can't map the product, fall back to a neutral niche-only fit.
    if prof is None:
        niche_ok = creator_niche.lower() in (brand_industry or "").lower() or (brand_industry or "").lower() in creator_niche.lower()
        score = 62 if niche_ok else 48
        breakdown = {"Niche alignment": 70 if niche_ok else 40, "Audience match": 55,
                     "Authenticity": audience_authenticity, "Engagement": min(engagement_rate * 10, 100)}
        return round(score), breakdown, "general"

    # 1. Niche alignment (35%)
    niche_score = 100 if creator_niche.lower() in prof["niches"] else (55 if creator_niche.lower() in ["lifestyle"] else 30)

    # 2. Gender match (20%) — closeness of audience female% to product's ideal
    gender_score = max(0, 100 - abs(audience_female_pct - prof["female"]) * 1.8)

    # 3. Age match (20%) — does the dominant audience age band match the product target
    age_bands = {"18-24": age_18_24, "18-34": age_18_24 + age_25_34, "25-44": age_25_34 + age_35_44}
    target_band_pct = age_bands.get(prof["age"], 50)
    age_score = min(100, target_band_pct * 1.6)

    # 4. Audience authenticity (15%)
    auth_score = audience_authenticity

    # 5. Price-point ↔ audience size fit (10%)
    if prof["price"] == "high":
        price_score = 85 if followers >= 100_000 else 55
    elif prof["price"] == "low":
        price_score = 90 if followers <= 500_000 else 70
    else:
        price_score = 80

    score = (niche_score * 0.35 + gender_score * 0.20 + age_score * 0.20 +
             auth_score * 0.15 + price_score * 0.10)
    # engagement quality nudges ±5
    score += (min(engagement_rate * 10, 100) - 50) * 0.1
    score = round(max(0, min(100, score)))

    breakdown = {
        "Niche alignment": round(niche_score),
        "Gender match": round(gender_score),
        "Age match": round(age_score),
        "Authenticity": round(auth_score),
        "Price-point fit": round(price_score),
    }
    return score, breakdown, key


def recommend_creators(product_key, brand_industry, current_score):
    """
    When market fit is weak, suggest better-matched creator archetypes.
    Returns a list of dicts (synthetic but realistic suggestions).
    """
    pools = {
        "skincare": [("@gloskincare", "Skincare educator", 91, "75% female, 18–34, high save-rate"),
                     ("@dewyroutine", "Clean beauty creator", 88, "82% female, strong purchase intent"),
                     ("@derma.daily", "Dermatologist-led", 86, "Trusted, low fake-follower rate")],
        "makeup": [("@glambymaya", "MUA / tutorials", 90, "80% female, 18–34, high conversion"),
                   ("@boldlipco", "Colour-cosmetics niche", 87, "Younger skew, high engagement"),
                   ("@5minface", "Quick-look creator", 85, "Broad reach, strong saves")],
        "fashion": [("@thecuratedrail", "Capsule-wardrobe stylist", 90, "65% female, 25–34, affluent"),
                    ("@streetfitdaily", "Streetwear creator", 86, "Younger, high share-rate"),
                    ("@slowfashionedit", "Sustainable fashion", 84, "High-trust, engaged niche")],
        "luxury": [("@maisonmuse", "Luxury lifestyle", 92, "25–44, high-affluence audience"),
                   ("@quietluxe", "Quiet-luxury creator", 88, "Premium, low-saturation"),
                   ("@theatelierdiary", "Heritage-brand storyteller", 85, "Aspirational, loyal")],
        "fitness": [("@strongwithsam", "Strength coach", 90, "Balanced gender, 18–34, action-takers"),
                    ("@mobilitymatters", "Mobility/recovery", 86, "Engaged, high-trust"),
                    ("@homegymhero", "Home-fitness creator", 84, "Broad reach, budget-friendly")],
        "tech": [("@gadgetgrid", "Consumer-tech reviewer", 91, "30% female, 18–34, high intent"),
                 ("@buildmydesk", "Setup/productivity", 87, "Engaged, purchase-driven"),
                 ("@aitoolbox", "AI-tools creator", 85, "Fast-growing, early-adopter audience")],
        "food": [("@weeknightplates", "Easy-recipes creator", 90, "55% female, 25–44, high saves"),
                 ("@snackscout", "Snack/FMCG reviewer", 86, "Younger, impulse-buy audience"),
                 ("@brunchbible", "Café/food lifestyle", 84, "Local, engaged")],
        "travel": [("@slowmaps", "Slow-travel storyteller", 90, "25–44, affluent, aspirational"),
                   ("@weekendaways", "Short-break creator", 86, "High-intent, planning audience"),
                   ("@soloroutes", "Solo-travel niche", 84, "Loyal, high-trust")],
        "finance": [("@moneymapped", "Personal-finance educator", 91, "25–44, high-trust, action-takers"),
                    ("@investplainly", "Beginner investing", 87, "Engaged, growing fast"),
                    ("@sidehustlelab", "Income/side-hustle", 84, "Younger, ambitious audience")],
        "baby": [("@littlemilestones", "Parenting creator", 91, "80% female, 25–44, high-trust"),
                 ("@newmamadiary", "New-parent niche", 87, "Highly engaged, loyal"),
                 ("@tinytestkitchen", "Baby-product reviewer", 84, "Purchase-driven audience")],
    }
    pool = pools.get(product_key, [
        ("@nicheauthority", "Category specialist", 88, "Tightly matched, engaged audience"),
        ("@risingvoice", "Rising-star creator", 85, "High momentum, better fit"),
        ("@trustedreviewer", "Review-led creator", 83, "High-trust, purchase-intent audience"),
    ])
    # only meaningfully better than current
    return [p for p in pool if p[2] > current_score][:3] or pool[:2]


# ═══════════════════════════════════════════════════════════════════════════
#  ENTERPRISE INTELLIGENCE SUITE
#  Five modules — each returns a structured, defensible deliverable computed
#  from the creator's real stats + the buyer's campaign context.
#  Modules: Forecast · Shield · Audience DNA · Benchmark · Pulse
# ═══════════════════════════════════════════════════════════════════════════

# CPM benchmarks (₹) by follower tier — used for reach valuation / EMV.
_CPM_BENCHMARK = {"nano": 120, "micro": 260, "mid": 430, "macro": 620, "mega": 900}

# Typical engagement-rate benchmark (%) by niche — for percentile ranking.
_NICHE_ENGAGEMENT_BENCHMARK = {
    "beauty": 3.8, "fashion": 3.2, "fitness": 4.5, "food": 4.1, "travel": 3.5,
    "tech": 2.4, "gaming": 4.8, "finance": 2.8, "lifestyle": 3.4, "parenting": 4.2,
    "entertainment": 3.9, "education": 3.1, "default": 3.3,
}

# Niche → audience interest affinities (for Audience DNA).
_NICHE_INTERESTS = {
    "beauty": ["Skincare", "Cosmetics", "Self-care", "Wellness", "Fashion"],
    "fashion": ["Apparel", "Streetwear", "Luxury", "Beauty", "Lifestyle"],
    "fitness": ["Gym & training", "Nutrition", "Athleisure", "Supplements", "Wellness"],
    "food": ["Cooking", "Restaurants", "FMCG snacks", "Beverages", "Home"],
    "travel": ["Destinations", "Hospitality", "Aviation", "Outdoor gear", "Lifestyle"],
    "tech": ["Gadgets", "Software/apps", "Productivity", "Gaming", "AI tools"],
    "gaming": ["Consoles/PC", "Esports", "Tech gear", "Streaming", "Entertainment"],
    "finance": ["Investing", "Fintech", "Side hustles", "Insurance", "Crypto"],
    "lifestyle": ["Home & decor", "Fashion", "Wellness", "Food", "Travel"],
    "parenting": ["Baby care", "Kids products", "Family travel", "Home", "Education"],
    "default": ["Lifestyle", "Entertainment", "Shopping", "Food", "Travel"],
}


def _size_band(followers):
    if followers < 10_000:      return "nano"
    if followers < 100_000:     return "micro"
    if followers < 500_000:     return "mid"
    if followers < 1_000_000:   return "macro"
    return "mega"


def _niche_key(niche):
    n = (niche or "").lower()
    for k in _NICHE_ENGAGEMENT_BENCHMARK:
        if k in n:
            return k
    return "default"


def compute_forecast(d, engagement_rate, brand_fit, aud_quality):
    """
    Vettd Forecast — predictive campaign ROI.
    Reach/impressions → EMV (earned media value) → conversions → ROI, plus a
    3-tier budget scenario table. Uses avg reel views when available.
    """
    followers = int(d.get("followers", 0) or 0)
    band = _size_band(followers)
    cpm = _CPM_BENCHMARK[band]

    # reach per deliverable: prefer real reel views, else model from engagement
    avg_views = d.get("avg_views")
    if avg_views:
        reach = int(avg_views)
    else:
        reach = int(followers * (0.28 + min(engagement_rate, 12) / 100))
    impressions = int(reach * 1.35)

    # objective shapes conversion assumptions
    objective = d.get("campaign_goal", "Awareness")
    ctr = {"Awareness": 0.008, "Engagement": 0.015, "Conversions": 0.025,
           "App installs": 0.020, "Product launch": 0.018}.get(objective, 0.012)
    # audience quality nudges CTR ±30%
    ctr *= 0.7 + (aud_quality / 100) * 0.6
    clicks = int(impressions * ctr)
    cvr = 0.06 if objective in ("Conversions", "App installs") else 0.03
    est_conversions = int(clicks * cvr)

    emv_per_post = round((impressions / 1000) * cpm)

    # deliverables the budget buys (cost/post scales with size band)
    cost_per_post = {"nano": 4000, "micro": 14000, "mid": 45000,
                     "macro": 90000, "mega": 180000}[band]
    budget = int(d.get("campaign_budget", 50000) or 50000)
    deliverables = max(1, round(budget / cost_per_post))

    total_reach = reach * deliverables
    total_emv = emv_per_post * deliverables
    total_conversions = est_conversions * deliverables

    # ROI = (value returned − spend) / spend. Value = EMV blended with a fit factor.
    fit_factor = (brand_fit if brand_fit else aud_quality) / 100
    value_returned = total_emv * (0.8 + 0.4 * fit_factor)
    roi_mid = (value_returned - budget) / max(budget, 1) * 100
    roi_low, roi_high = round(roi_mid * 0.6), round(roi_mid * 1.5)

    # 3-tier scenario table (0.5×, 1×, 2× budget)
    scenarios = []
    for label, mult in [("Conservative", 0.5), ("Planned", 1.0), ("Aggressive", 2.0)]:
        b = int(budget * mult)
        dv = max(1, round(b / cost_per_post))
        scenarios.append({
            "label": label, "budget": b, "deliverables": dv,
            "reach": reach * dv, "emv": emv_per_post * dv,
            "roi": round(((emv_per_post * dv) * (0.8 + 0.4 * fit_factor) - b) / max(b, 1) * 100),
        })

    return {
        "reach_per_post": reach, "impressions_per_post": impressions,
        "emv_per_post": emv_per_post, "total_emv": total_emv,
        "deliverables": deliverables, "total_reach": total_reach,
        "est_conversions_per_post": est_conversions, "total_conversions": total_conversions,
        "cpm": cpm, "objective": objective, "budget": budget,
        "roi_mid": round(roi_mid), "roi_low": roi_low, "roi_high": roi_high,
        "scenarios": scenarios,
    }


def compute_shield(d, fake_score, engagement_rate):
    """
    Vettd Shield — brand safety & risk audit.
    Fake-follower forensics, red-flag scan, crisis risk, and a
    Go / Conditional / No-Go verdict computed from real signals.
    """
    followers = int(d.get("followers", 0) or 0)
    following = int(d.get("following", 0) or 0)
    auth = int(d.get("audience_authenticity", 80) or 80)
    growth = float(d.get("growth_rate_30d", 0) or 0)

    suspicious_pct = round(fake_score * 0.75 + (100 - auth) * 0.25)
    suspicious_pct = max(0, min(100, suspicious_pct))
    bot_followers = int(followers * suspicious_pct / 100)

    sensitivity = d.get("brand_sensitivity", "Medium")
    regulated = bool(d.get("regulated_industry", False))
    prohibited = [k.strip() for k in (d.get("prohibited_keywords", "") or "").split(",") if k.strip()]

    # ── red-flag scan (computed from data) ──
    flags = []
    if fake_score >= 45:
        flags.append(("High fake-follower signal", f"{fake_score}/100 — audience authenticity is questionable", "high"))
    elif fake_score >= 30:
        flags.append(("Moderate fake-follower signal", f"{fake_score}/100 — worth a manual spot-check", "med"))
    if following > 0 and followers / max(following, 1) < 1.2 and followers > 20000:
        flags.append(("Follow-for-follow pattern", "Follower/following ratio suggests growth tactics", "med"))
    if engagement_rate < 1.0 and followers > 100000:
        flags.append(("Engagement too low for reach", f"{engagement_rate}% on a large account — possible inflated reach", "high"))
    if auth < 60:
        flags.append(("Low audience authenticity", f"Only {auth}% estimated authentic", "high"))
    if growth > 40:
        flags.append(("Suspicious growth spike", f"+{growth}% in 30d — verify it isn't purchased", "med"))
    if regulated:
        flags.append(("Regulated-industry review needed", "Legal/compliance sign-off recommended before contracting", "med"))
    for kw in prohibited[:5]:
        flags.append((f"Manual check: “{kw}”", "Flagged keyword to review in the creator's content history", "med"))
    if not flags:
        flags.append(("No red flags detected", "Clean across authenticity, engagement and growth signals", "clear"))

    high_flags = sum(1 for _, _, sev in flags if sev == "high")
    med_flags = sum(1 for _, _, sev in flags if sev == "med")

    # crisis risk score (0–100, higher = riskier)
    crisis = fake_score * 0.4 + (100 - auth) * 0.3 + high_flags * 12 + med_flags * 5
    if sensitivity.startswith("High"):
        crisis *= 1.25
    elif sensitivity.startswith("Low"):
        crisis *= 0.85
    crisis = round(max(0, min(100, crisis)))
    safety_score = 100 - crisis

    # verdict
    if crisis >= 55 or high_flags >= 2:
        verdict, vcolor, vnote = "No-Go", "#EF4444", "Risk outweighs upside for this brand profile."
    elif crisis >= 30 or high_flags >= 1:
        verdict, vcolor, vnote = "Conditional", "#F59E0B", "Proceed only after manual content review and clear contract terms."
    else:
        verdict, vcolor, vnote = "Go", "#10B981", "Cleared to proceed — low risk across signals."

    return {
        "safety_score": safety_score, "crisis_score": crisis,
        "suspicious_pct": suspicious_pct, "bot_followers": bot_followers,
        "flags": flags, "verdict": verdict, "verdict_color": vcolor, "verdict_note": vnote,
        "sensitivity": sensitivity, "regulated": regulated,
    }


def compute_audience_dna(d, fake_score, aud_quality, roster=None):
    """
    Vettd Audience DNA — audience credibility & true-match.
    Real-vs-suspicious split, true-match to the buyer's target persona,
    geo concentration, interest affinities, and roster overlap (wasted reach).
    """
    auth = int(d.get("audience_authenticity", 80) or 80)
    female = int(d.get("female_pct", 50) or 50)
    age_18_24 = int(d.get("age_18_24", 0) or 0)
    age_25_34 = int(d.get("age_25_34", 0) or 0)
    age_35_44 = int(d.get("age_35_44", 0) or 0)

    real_pct = max(0, min(100, round(auth - fake_score * 0.2)))
    suspicious_pct = 100 - real_pct

    # true-match to target persona
    target_age = d.get("target_age", "All ages")
    target_gender = d.get("target_gender", "Any")
    age_bands = {"13–17": 0, "18–24": age_18_24, "25–34": age_25_34,
                 "35–44": age_35_44, "45+": max(0, 100 - age_18_24 - age_25_34 - age_35_44),
                 "All ages": 100}
    age_match = age_bands.get(target_age, 60) if target_age != "All ages" else 75
    if target_gender == "Female":
        gender_match = female
    elif target_gender == "Male":
        gender_match = 100 - female
    else:
        gender_match = 70
    true_match = round(age_match * 0.5 + gender_match * 0.3 + auth * 0.2)
    true_match = max(0, min(100, true_match))

    geo_conc = int(d.get("loc1_pct", 0) or 0)
    geo_name = d.get("loc1_name", "") or "Top market"
    interests = _NICHE_INTERESTS.get(_niche_key(d.get("niche")), _NICHE_INTERESTS["default"])

    # roster overlap (wasted reach) — compare vs saved creators
    overlap_hits = []
    if roster:
        me = {"niche": d.get("niche", ""), "platform": d.get("platform", "Instagram"),
              "followers": int(d.get("followers", 0) or 0), "auth": auth}
        for r in roster:
            other = {"niche": r.get("niche", ""), "platform": r.get("platform", "Instagram"),
                     "followers": int(r.get("followers", 0) or 0), "auth": int(r.get("auth", 80) or 80)}
            ov = estimate_audience_overlap(me, other)
            overlap_hits.append({"name": r.get("name", "Creator"), "overlap": ov})
        overlap_hits.sort(key=lambda x: -x["overlap"])

    return {
        "quality_score": aud_quality, "real_pct": real_pct, "suspicious_pct": suspicious_pct,
        "true_match": true_match, "target_age": target_age, "target_gender": target_gender,
        "geo_conc": geo_conc, "geo_name": geo_name, "interests": interests,
        "overlap_hits": overlap_hits[:3],
    }


def compute_benchmark(d, engagement_rate, vettd_score, fake_score):
    """
    Vettd Benchmark — competitive & category positioning.
    Percentile vs category peers, cost-efficiency, saturation/exclusivity,
    plus 3 vetted lookalike alternatives.
    """
    nkey = _niche_key(d.get("niche"))
    bench_er = _NICHE_ENGAGEMENT_BENCHMARK[nkey]
    followers = int(d.get("followers", 0) or 0)

    # engagement percentile vs niche benchmark (rough logistic-ish mapping)
    ratio = engagement_rate / max(bench_er, 0.1)
    if ratio >= 2.0:      er_percentile = 96
    elif ratio >= 1.5:    er_percentile = 88
    elif ratio >= 1.2:    er_percentile = 78
    elif ratio >= 1.0:    er_percentile = 65
    elif ratio >= 0.8:    er_percentile = 50
    elif ratio >= 0.6:    er_percentile = 35
    else:                 er_percentile = 20
    # blend with overall vettd score for a category rank
    percentile = round(er_percentile * 0.6 + vettd_score * 0.4)
    percentile = max(1, min(99, percentile))

    # cost-efficiency vs category: more engagement per unit reach = cheaper per
    # engagement. Derived from the same ER-vs-benchmark ratio for consistency.
    eff_ratio = max(ratio, 0.05)
    cost_delta = round((1 / eff_ratio - 1) * 100)  # negative = cheaper than peers
    cost_delta = max(-70, min(200, cost_delta))
    if cost_delta <= -15:   cost_verdict = "More cost-efficient than category average"
    elif cost_delta >= 15:  cost_verdict = "Pricier per engagement than category average"
    else:                   cost_verdict = "In line with category average"

    # saturation / exclusivity — how "used" this creator likely is
    posting = float(d.get("posting_freq", 0) or 0)
    growth = float(d.get("growth_rate_30d", 0) or 0)
    sat = 50 + (posting - 4) * 6 + (fake_score - 30) * 0.3 - growth * 0.8
    sat = round(max(5, min(95, sat)))
    if sat >= 65:   sat_label = "Likely saturated — appears in many brand feeds"
    elif sat >= 40: sat_label = "Moderately active with brands"
    else:           sat_label = "Low saturation — strong exclusivity upside"

    # lookalikes — reuse the recommendation pools keyed off niche
    key, _ = _match_product_profile("", d.get("niche", ""))
    lookalikes = recommend_creators(key or nkey, d.get("brand_industry", ""), 0)[:3]

    return {
        "percentile": percentile, "bench_er": bench_er, "creator_er": engagement_rate,
        "cost_delta": cost_delta, "cost_verdict": cost_verdict,
        "saturation": sat, "saturation_label": sat_label,
        "lookalikes": lookalikes, "category": d.get("niche", "category"),
    }


def compute_pulse(d, engagement_rate, fake_score):
    """
    Vettd Pulse — comment sentiment & community health.
    Sentiment split, community-health tier, toxicity flag, and top themes.
    """
    s = int(d.get("sentiment_score", 75) or 75)
    pos = max(0, min(100, s))
    neg = max(0, min(100 - pos, round((100 - s) * 0.55 + fake_score * 0.1)))
    neu = max(0, 100 - pos - neg)

    # community health: real engagement composition, not just volume
    saves = float(d.get("avg_saves", 0) or 0)
    comments = float(d.get("avg_comments", 0) or 0)
    likes = float(d.get("avg_likes", 1) or 1)
    depth = (saves + comments) / max(likes, 1)  # deeper = healthier
    health = round(min(100, s * 0.5 + min(depth * 100, 40) + (100 - fake_score) * 0.1))
    if health >= 75:   health_tier, htc = "Thriving", "#10B981"
    elif health >= 55: health_tier, htc = "Healthy", "#60A5FA"
    elif health >= 40: health_tier, htc = "Passive", "#F59E0B"
    else:              health_tier, htc = "At risk", "#EF4444"

    toxicity = max(0, round(neg * 0.6 + fake_score * 0.2 - 5))
    tox_flag = toxicity >= 30

    keywords = [k.strip() for k in (d.get("sentiment_keywords", "") or "").split(",") if k.strip()]
    base_themes = {
        "beauty": ["Loves the results", "Asks where to buy", "Shade/skin-type questions"],
        "fitness": ["Motivation", "Form questions", "Program requests"],
        "food": ["Recipe requests", "Tried it & loved it", "Ingredient swaps"],
        "tech": ["Spec questions", "Price/value debate", "Comparison requests"],
        "fashion": ["Outfit details", "Where to buy", "Fit/sizing questions"],
        "default": ["Positive reactions", "Product questions", "Tag-a-friend shares"],
    }
    themes = base_themes.get(_niche_key(d.get("niche")), base_themes["default"])
    if keywords:
        themes = [f"Flagged: “{k}”" for k in keywords[:2]] + themes[:2]

    return {
        "sentiment": s, "pos": pos, "neu": neu, "neg": neg,
        "health": health, "health_tier": health_tier, "health_color": htc,
        "toxicity": toxicity, "tox_flag": tox_flag, "themes": themes[:4],
    }
