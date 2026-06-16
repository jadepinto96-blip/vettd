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
