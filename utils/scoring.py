def calculate_engagement_rate(followers, avg_likes, avg_comments, avg_saves):
    if followers == 0:
        return 0
    return round(((avg_likes + avg_comments + avg_saves) / followers) * 100, 2)


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
