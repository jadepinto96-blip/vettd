"""Single source of truth for the 5 enterprise intelligence modules.

Both the landing page (short cards) and the per-tool detail page
(pages/7_Feature.py) read from here, so names/copy never drift.
"""

_ICON = {
    "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "bars": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>',
    "activity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
}

MODULES = [
    {
        "key": "forecast", "name": "Forecast", "sub": "Predictive Campaign ROI",
        "color": "#F5A623", "icon": _ICON["zap"],
        "short": "Forecast a campaign's return before you spend — projected reach, Earned Media Value, conversions and a full ROI range.",
        "hero": "Know the return before you spend a rupee.",
        "what": [
            "Most brands greenlight a creator on gut feel and hope the numbers work out. Forecast turns that gut-feel into a model: it takes the creator's real reach and engagement profile, your budget and objective, and projects what a campaign would actually return.",
            "You get a defensible number to take into a planning meeting — not just “they have 250k followers,” but “this budget buys ~X deliverables, ~Y reach, ₹Z in earned media value, and an ROI in this range.” Then it sizes three budget scenarios so you can see where the spend stops paying off.",
        ],
        "outputs": [
            ("Projected reach & impressions", "Modelled from the creator's real reel views and engagement, not their follower count."),
            ("Earned Media Value (EMV)", "What that reach would cost you to buy as paid media — the campaign's headline value."),
            ("Estimated conversions", "Click-through and conversion estimates shaped by your objective (awareness vs conversions)."),
            ("ROI range", "A low–mid–high return band, so you plan around a realistic spread, not a single optimistic number."),
            ("3-tier budget scenarios", "Conservative / planned / aggressive spends side by side — find the point of diminishing returns."),
        ],
        "how": [
            ("Enter the campaign", "Budget and objective (awareness, conversions, launch…)."),
            ("We model the outcome", "Reach, EMV and conversions are derived from the creator's real performance signals."),
            ("Size the spend", "Compare budget scenarios and lock the one with the best projected ROI."),
        ],
        "who": "Brand and performance marketers who need to justify a creator budget before committing it.",
    },
    {
        "key": "shield", "name": "Shield", "sub": "Brand Safety & Risk Audit",
        "color": "#F0616D", "icon": _ICON["shield"],
        "short": "Fake-follower forensics, a red-flag scan against your brand rules, a crisis-risk score, and a clear Go / Conditional / No-Go verdict.",
        "hero": "De-risk the partnership before you sign it.",
        "what": [
            "A creator can look great on the surface and still be a liability — bought followers, engagement pods, or content that clashes with your brand. Shield runs the checks your legal and comms teams would want, and turns them into one decision.",
            "It scores fake-follower risk, scans for red flags against the categories you care about, and weighs it all by how sensitive your brand is. The output isn't a vague warning — it's a Go, Conditional, or No-Go, with the reasons written out so anyone can sign off.",
        ],
        "outputs": [
            ("Risk tier & safety score", "A single 0–100 safety read plus a tier your team can act on."),
            ("Fake-follower forensics", "Estimated suspicious / bot follower share, with the likely count."),
            ("Red-flag scan", "Data-driven flags (engagement anomalies, growth spikes, follow-for-follow patterns) plus your own prohibited-topic checks."),
            ("Crisis-risk score", "How exposed this partnership is to controversy, scaled to your brand's sensitivity."),
            ("Go / Conditional / No-Go", "A clear verdict with rationale — the thing you actually put in the deck."),
        ],
        "how": [
            ("Set your guardrails", "Brand sensitivity, regulated-industry flag, and any prohibited topics."),
            ("We audit the signals", "Authenticity, engagement, growth and follower quality are scored for risk."),
            ("Get the verdict", "Go, Conditional, or No-Go — with the reasoning your team can sign off on."),
        ],
        "who": "Brand, legal, and comms teams who need sign-off before a creator goes live.",
    },
    {
        "key": "audience", "name": "Audience DNA", "sub": "Credibility & True-Match",
        "color": "#22D3EE", "icon": _ICON["users"],
        "short": "Split the audience into real vs suspicious, score true-match to your exact target, map geo and interests, and detect overlap with your roster.",
        "hero": "See who's really on the other side of the follows.",
        "what": [
            "Follower count tells you how big an audience is, not whether it's the right one — or even real. Audience DNA breaks the audience down so you know how much of it is authentic and how much of it actually matches the customer you're trying to reach.",
            "It scores true-match against your target persona (age, gender, geography), maps interest affinities, and — crucially — detects overlap with the other creators in your roster, so you don't pay twice to reach the same people.",
        ],
        "outputs": [
            ("Audience Quality Score", "One number for how healthy and engaged the audience is."),
            ("Real vs suspicious split", "The share of the audience that reads as genuine versus bot/inactive."),
            ("True-match to target", "How much of the audience matches your specific persona — not just the raw size."),
            ("Geo & interest affinities", "Where the audience concentrates and what else they care about."),
            ("Roster-overlap detector", "Flags wasted reach when a creator's audience overlaps others you already work with."),
        ],
        "how": [
            ("Describe your target", "Age, gender and market you're trying to reach."),
            ("We decode the audience", "Authenticity, true-match, geo and interests are computed from the profile."),
            ("Spot the overlap", "See how much this audience duplicates the rest of your roster."),
        ],
        "who": "Brands running multi-creator rosters who care about real, non-duplicated reach.",
    },
    {
        "key": "benchmark", "name": "Benchmark", "sub": "Competitive & Category Positioning",
        "color": "#60A5FA", "icon": _ICON["bars"],
        "short": "Rank a creator against category peers by percentile, measure cost-efficiency, gauge saturation, and surface vetted lookalike alternatives.",
        "hero": "Is this the best creator for the money — or just the first one you found?",
        "what": [
            "A creator can look strong in isolation and still be a weak choice next to their peers. Benchmark places them in their category: where they rank, whether they're priced fairly for what they deliver, and how saturated they already are with brand deals.",
            "When the fit is only okay, it doesn't leave you stuck — it surfaces vetted lookalike creators who may convert better, so every analysis ends with a next move, not a dead end.",
        ],
        "outputs": [
            ("Category percentile rank", "Where this creator sits versus peers in their niche."),
            ("Cost-efficiency vs peers", "Whether they're a bargain or a premium for the engagement they drive."),
            ("Saturation / exclusivity", "How ‘used’ they already are by brands — and the exclusivity upside if they're not."),
            ("Vetted lookalike alternatives", "Three similar creators worth considering when the fit is only moderate."),
        ],
        "how": [
            ("Pick the category", "The niche and any competitors you want to frame against."),
            ("We rank & price-check", "Percentile, cost-efficiency and saturation are computed against category norms."),
            ("Get alternatives", "Vetted lookalikes surface when there's a stronger-fit option."),
        ],
        "who": "Brands and agencies deciding between creators, not just evaluating one in a vacuum.",
    },
    {
        "key": "pulse", "name": "Pulse", "sub": "Sentiment & Community Health",
        "color": "#34D399", "icon": _ICON["activity"],
        "short": "Read comment tone into a positive / neutral / negative split, score community health from real engagement depth, and flag toxicity.",
        "hero": "Numbers say how many. Pulse says how they feel.",
        "what": [
            "A big, engaged-looking audience can still be a bad room for your brand — lukewarm, cynical, or bot-inflated. Pulse looks past the vanity metrics at how the community actually behaves and how it feels.",
            "It reads comment tone into a clear positive / neutral / negative split, scores community health from genuine engagement depth (saves and comments, not just likes), and flags toxicity so you know what your brand would be walking into.",
        ],
        "outputs": [
            ("Sentiment split", "Positive / neutral / negative share of the conversation."),
            ("Community health tier", "Thriving, healthy, passive or at-risk — from real engagement depth, not volume."),
            ("Toxicity flag", "A heads-up when the comment culture could be a brand-safety issue."),
            ("Dominant themes", "The recurring topics your brand would be showing up next to."),
        ],
        "how": [
            ("Point us at the signals", "Observed sentiment and any keywords you want flagged."),
            ("We read the room", "Tone, health and toxicity are scored from engagement composition."),
            ("Know the vibe", "A clear read on whether this community is a good home for your brand."),
        ],
        "who": "Brands who care what conversation their campaign will actually land in.",
    },
]

MODULES_BY_KEY = {m["key"]: m for m in MODULES}
