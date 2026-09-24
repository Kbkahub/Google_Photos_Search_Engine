"""
Google Photos Discovery Engine
AI-Powered User Research Tool for Photo Retrieval Problems
"""

import streamlit as st
import json
import re
import urllib.request
import urllib.error
from collections import Counter
from math import log

# ─────────────────────────────────────────────
# 0. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Discovery Engine — Google Photos Retrieval",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 1. CSS / THEME  —  Google-inspired minimal
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] { font-family: 'Inter', 'Google Sans', sans-serif !important; }
h1, h2, h3, h4 { font-family: 'Inter', 'Google Sans', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
button[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stSidebarCollapse"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.stSidebar button[kind="header"] { display: none !important; }

/* ── Main content area ── */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}

/* ── Force sidebar open ── */
[data-testid="stSidebar"] { min-width: 280px !important; width: 280px !important; }
[data-testid="stSidebar"][aria-expanded="false"] {
    min-width: 280px !important; width: 280px !important;
    transform: none !important; display: block !important;
}

/* ── Sidebar ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A73E8 0%, #1557B0 100%) !important;
}
div[data-testid="stSidebar"] * { color: #FFFFFF !important; }
div[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }

/* ── Nav buttons ── */
div[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: rgba(255,255,255,0.9) !important;
    border: none !important;
    border-radius: 24px !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    text-align: left !important;
    padding: 10px 20px !important;
    transition: background 0.2s !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
}
div[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(255,255,255,0.2) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* ── Google-style metric cards ── */
.g-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.3), 0 1px 3px rgba(60,64,67,0.15);
    text-align: center;
    transition: box-shadow 0.2s;
}
.g-card:hover { box-shadow: 0 1px 3px rgba(60,64,67,0.4), 0 4px 8px rgba(60,64,67,0.15); }
.g-card .g-num { font-size: 2.2rem; font-weight: 700; margin: 0; line-height: 1.2; }
.g-card .g-label { color: #5F6368; font-size: 0.8rem; font-weight: 500; margin-top: 4px; }

/* ── Platform box cards ── */
.plat-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}
.plat-card .plat-name { font-size: 0.9rem; font-weight: 600; color: #202124; }
.plat-card .plat-count { font-size: 1.4rem; font-weight: 700; color: #1A73E8; }
.plat-card .plat-bar {
    height: 3px; background: #E8EAED; border-radius: 2px;
    width: 100%; margin-top: 8px;
}
.plat-card .plat-bar-fill { height: 3px; border-radius: 2px; }

/* ── AI answer box ── */
.ai-answer {
    background: #FFFFFF;
    border: 1px solid #DADCE0;
    border-left: 4px solid #4285F4;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1);
}
.ai-answer b { color: #4285F4; }

/* ── Review card ── */
.review-card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid #DADCE0;
    transition: box-shadow 0.15s;
}
.review-card:hover { box-shadow: 0 1px 3px rgba(60,64,67,0.2); }
.review-card .platform-tag {
    display: inline-block; background: #E8F0FE; color: #1A73E8;
    font-size: 0.7rem; padding: 3px 10px; border-radius: 12px;
    font-weight: 600; margin-right: 6px;
}
.review-card .theme-tag {
    display: inline-block; background: #F1F3F4; color: #5F6368;
    font-size: 0.68rem; padding: 2px 8px; border-radius: 12px;
    margin-right: 4px; font-weight: 500;
}
.review-card .review-text {
    color: #3C4043; font-size: 0.9rem; line-height: 1.6;
    margin: 10px 0 8px 0;
}
.review-card .review-meta { color: #9AA0A6; font-size: 0.75rem; }
.sentiment-pos { color: #34A853; font-weight: 600; }
.sentiment-neg { color: #EA4335; font-weight: 600; }
.sentiment-mix { color: #F9AB00; font-weight: 600; }

/* ── Section header — Google style thin line ── */
.section-hdr {
    font-size: 1.3rem;
    font-weight: 700;
    color: #202124;
    margin-top: 36px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 3px solid #4285F4;
    letter-spacing: -0.01em;
}

/* ── Opportunity card ── */
.opp-card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 12px;
    border: 1px solid #DADCE0;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1);
}
.opp-card h4 { color: #202124; margin: 0 0 6px 0; font-size: 1rem; font-weight: 600; }
.opp-card .score { color: #4285F4; font-weight: 700; font-size: 1.4rem; }

/* ── Google-style progress bars ── */
.stProgress > div > div > div { background: #4285F4 !important; border-radius: 4px !important; }

/* ── Expander ── */
div[data-testid="stExpander"] {
    border: 1px solid #DADCE0;
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1);
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    border-radius: 24px !important;
    border: 1px solid #DADCE0 !important;
    padding: 10px 20px !important;
    font-size: 0.9rem !important;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4285F4 !important;
    box-shadow: 0 1px 6px rgba(66,133,244,0.3) !important;
}

/* ── Primary buttons ── */
.stButton > button[kind="primary"] {
    background: #4285F4 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 24px !important;
    font-weight: 600 !important;
    padding: 8px 24px !important;
    font-size: 0.85rem !important;
    box-shadow: 0 1px 2px rgba(60,64,67,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #3367D6 !important;
    box-shadow: 0 1px 3px rgba(60,64,67,0.4) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div { border-radius: 8px !important; }

/* ── Multiselect ── */
.stMultiSelect > div > div { border-radius: 8px !important; }

/* ── Page title ── */
.page-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #202124;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
}
.page-subtitle {
    font-size: 0.95rem;
    color: #5F6368;
    margin-bottom: 28px;
    font-weight: 400;
}

/* ── Google 4-color accent bar ── */
.g-accent {
    display: flex; gap: 0; margin-bottom: 24px; border-radius: 4px; overflow: hidden; height: 4px;
}
.g-accent div { flex: 1; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 2. DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_reviews():
    with open("data/reviews.json", "r") as f:
        return json.load(f)

@st.cache_data
def load_survey():
    try:
        with open("data/survey.json", "r") as f:
            data = json.load(f)
            return data if data else []
    except Exception:
        return []

REVIEWS = load_reviews()
SURVEY = load_survey()

# ─────────────────────────────────────────────
# 3. TF-IDF SEARCH ENGINE
# ─────────────────────────────────────────────
class MiniSearch:
    def __init__(self, docs, field="text"):
        self.docs = docs
        self.n = len(docs)
        self.tokens = []
        self.df = Counter()
        for doc in docs:
            toks = set(re.findall(r"[a-z0-9]+", doc.get(field, "").lower()))
            self.tokens.append(toks)
            for t in toks:
                self.df[t] += 1

    def search(self, query, top_k=15):
        q_toks = set(re.findall(r"[a-z0-9]+", query.lower()))
        scores = []
        for i, doc in enumerate(self.docs):
            score = sum(
                log(self.n / self.df[t])
                for t in q_toks
                if t in self.tokens[i] and self.df[t] > 0
            )
            if score > 0:
                scores.append((score, i))
        scores.sort(reverse=True)
        return [self.docs[i] for _, i in scores[:top_k]]


review_engine = MiniSearch(REVIEWS, field="text")
survey_engine = MiniSearch(SURVEY, field="searchable_text") if SURVEY else None

# ─────────────────────────────────────────────
# 4. GROQ LLM
# ─────────────────────────────────────────────
GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

def call_groq(system_prompt, user_msg, api_key):
    last_error = ""
    for model in GROQ_MODELS:
        body = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
            "max_tokens": 1500,
            "temperature": 0.4,
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "DiscoveryEngine/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode()
            except Exception:
                pass
            last_error = f"Model {model}: HTTP {e.code} — {error_body[:200]}"
            continue
        except Exception as e:
            last_error = f"Model {model}: {e}"
            continue
    return f"__ERROR__: {last_error}"

REVIEW_SYSTEM_PROMPT = """You are a senior user researcher analyzing Google Photos user feedback about photo retrieval problems.
Answer grounded ONLY in the provided reviews. Do NOT number the sections.

Start with a direct 2-3 sentence answer — no heading, no label, just the answer.

Then a section headed **Key Themes** listing 3-5 prominent patterns with evidence.

Then a section headed **User Segments Affected** listing which types of users are most impacted.

Then a section headed **Retrieval Gap** explaining what users remember vs what the search system requires.

Quote specific reviews as evidence. Be specific, not generic."""

SURVEY_SYSTEM_PROMPT = """You are a senior user researcher analyzing a primary user survey about Google Photos usage and photo retrieval behavior.
Answer grounded ONLY in the provided survey data. Do NOT number the sections.

Start with a direct 2-3 sentence finding — no heading, no label, just the finding.

Then a section headed **Supporting Data** referencing specific responses.

Then a section headed **Demographic Patterns** noting differences by age, gender, etc.

Be specific. Reference respondent demographics when quoting."""

# ─────────────────────────────────────────────
# 5. HELPERS
# ─────────────────────────────────────────────
GOOGLE_COLORS = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]

def google_accent_bar():
    st.markdown(
        '<div class="g-accent">'
        '<div style="background:#4285F4;"></div>'
        '<div style="background:#EA4335;"></div>'
        '<div style="background:#FBBC05;"></div>'
        '<div style="background:#34A853;"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None

def sentiment_class(s):
    return {"positive": "sentiment-pos", "negative": "sentiment-neg"}.get(s, "sentiment-mix")

def render_review_card(r):
    s_cls = sentiment_class(r.get("sentiment", ""))
    themes_html = "".join(
        f'<span class="theme-tag">{t.replace("_"," ")}</span>' for t in r.get("themes", [])
    )
    rating_str = f"⭐ {r['rating']}/5" if r.get("rating") else ""
    st.markdown(f"""
    <div class="review-card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
            <div><span class="platform-tag">{r.get('platform','')}</span>{themes_html}</div>
            <span class="{s_cls}" style="font-size:0.78rem;">{r.get('sentiment','').upper()} {rating_str}</span>
        </div>
        <div class="review-text">"{r.get('text','')}"</div>
        <div class="review-meta">{r.get('date','')} · {r.get('user_segment','')}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6. OPPORTUNITY AREAS
# ─────────────────────────────────────────────
THEME_LABELS = {
    "vague_memory_retrieval": "Vague Memory → Failed Retrieval",
    "search_accuracy": "Search Accuracy & Relevance",
    "ai_search_regression": "AI/Gemini Search Regression",
    "face_recognition": "Face Recognition Issues",
    "temporal_navigation": "Time-Based Navigation Gaps",
    "screenshot_document_search": "Screenshot & Document Retrieval",
    "location_search": "Location-Based Search Gaps",
    "organization_friction": "Organization & Structure Friction",
}

THEME_DESCRIPTIONS = {
    "vague_memory_retrieval": "Users remember visual details, emotions, or context about a photo but cannot translate these into keyword searches. The gap between human episodic memory and text-based search is the core retrieval problem.",
    "search_accuracy": "Search returns too many results, irrelevant results, or misses photos entirely. Combining criteria (person + place + time) is not supported. Users distrust search completeness.",
    "ai_search_regression": "Gemini/Ask Photos integration degraded the classic search experience. Users report slower results, AI-generated summaries instead of photos, and less accurate matches. Many disabled it.",
    "face_recognition": "Face grouping errors, splitting one person into multiple groups, merging different people, poor recognition for children aging, people of color, and group photos. Core people-search breaks down.",
    "temporal_navigation": "Incorrect timestamps from scans, downloads, or cross-device transfers. No date-range filtering in search. Scrolling fatigue in large libraries. Seasonal/relative time references not understood.",
    "screenshot_document_search": "Photos of medicines, receipts, documents, menus, and other functional captures are hard to retrieve. OCR doesn't work on older photos, handwritten text, or non-English text. No 'document type' category.",
    "location_search": "Indoor photos lack GPS data. Location services turned off means no geotagging. No location inference from nearby photos. Can't search within shared album locations.",
    "organization_friction": "Albums are incomplete, manual organization is tedious, screenshots pollute libraries, archived photos vanish from search, no custom tags, no folder structure, deleted photos resurface.",
}

def compute_opportunity_areas():
    theme_counts = Counter()
    theme_platforms = {}
    for r in REVIEWS:
        for t in r.get("themes", []):
            theme_counts[t] += 1
            theme_platforms.setdefault(t, Counter())
            theme_platforms[t][r.get("platform", "Unknown")] += 1

    max_count = max(theme_counts.values()) if theme_counts else 1
    areas = []
    for theme, count in theme_counts.most_common():
        if theme in THEME_LABELS:
            impact = round(min(10, (count / max_count) * 10), 1)
            areas.append({
                "theme": theme,
                "label": THEME_LABELS[theme],
                "description": THEME_DESCRIPTIONS.get(theme, ""),
                "impact": impact,
                "evidence_count": count,
                "platforms": dict(theme_platforms.get(theme, {})),
            })
    return areas

# ─────────────────────────────────────────────
# 7. SIDEBAR + NAVIGATION
# ─────────────────────────────────────────────
NAV_ITEMS = [
    ("dashboard", "DASHBOARD"),
    ("kpi_tree", "FOCUSED REVIEWS (KPI TREE)"),
    ("public_reviews", "ASK INSIGHTS — PUBLIC REVIEWS"),
    ("user_survey", "ASK INSIGHTS — USER SURVEY"),
    ("explorer", "REVIEW EXPLORER"),
    ("comparison", "COMPARISON MATRIX"),
]

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

with st.sidebar:
    st.markdown(
        '<div style="padding:4px 0 0 0;">'
        '<h2 style="margin:0;font-size:1.4rem;font-weight:700;letter-spacing:-0.02em;">Discovery Engine</h2>'
        '<p style="font-size:0.78rem;opacity:0.8;margin:2px 0 0 0;font-weight:400;">'
        'AI Powered · Google Photos · Photo Retrieval Research</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    for key, label in NAV_ITEMS:
        is_active = st.session_state["page"] == key
        if st.button(
            label, key=f"nav_{key}", use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state["page"] = key
            st.rerun()

    st.markdown("---")
    platforms = set(r.get("platform") for r in REVIEWS)
    st.markdown(
        f'<div style="font-size:0.8rem;opacity:0.85;line-height:1.8;">'
        f'<b>{len(REVIEWS)}</b> reviews · <b>{len(SURVEY)}</b> survey responses · <b>{len(platforms)}</b> platforms'
        f'</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# 8. PAGE: DASHBOARD
# ─────────────────────────────────────────────
def page_dashboard():
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Overview of the Google Photos photo-retrieval research corpus</div>', unsafe_allow_html=True)
    google_accent_bar()

    # ── Metrics row ──
    colors = GOOGLE_COLORS
    metrics = [
        (len(REVIEWS), "Public Reviews", colors[0]),
        (len(SURVEY), "Survey Responses", colors[1]),
        (len(set(r.get("platform") for r in REVIEWS)), "Platforms", colors[2]),
        (len(compute_opportunity_areas()), "Opportunity Areas", colors[3]),
    ]
    cols = st.columns(4, gap="medium")
    for i, (num, label, color) in enumerate(metrics):
        with cols[i]:
            st.markdown(
                f'<div class="g-card">'
                f'<div class="g-num" style="color:{color};">{num}</div>'
                f'<div class="g-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Reviews by Platform ──
    st.markdown('<div class="section-hdr">Reviews by Platform</div>', unsafe_allow_html=True)
    plat_counts = Counter(r.get("platform", "Unknown") for r in REVIEWS)
    plat_colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#8E24AA", "#00ACC1", "#FF7043"]
    for idx, (plat, cnt) in enumerate(plat_counts.most_common()):
        pct = cnt / len(REVIEWS) * 100
        bar_color = plat_colors[idx % len(plat_colors)]
        st.markdown(f"""
        <div class="plat-card">
            <div style="flex:1;">
                <div class="plat-name">{plat}</div>
                <div class="plat-bar"><div class="plat-bar-fill" style="width:{pct}%;background:{bar_color};"></div></div>
            </div>
            <div class="plat-count">{cnt}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Affinity Mapping ──
    st.markdown('<div class="section-hdr">Affinity Mapping</div>', unsafe_allow_html=True)
    with st.expander("View Thematic Coding Methodology"):
        st.markdown("""
**How themes were identified:**

Each review was manually read and tagged with 1–3 themes from a taxonomy that emerged from the data itself. The taxonomy was developed through affinity mapping: grouping similar complaints, requests, and descriptions into clusters, then naming each cluster.

**Theme taxonomy (8 retrieval-focused themes):**

- **vague_memory_retrieval** — User remembers visual/emotional context but can't formulate the right search query
- **search_accuracy** — Search returns wrong, incomplete, or too many results
- **ai_search_regression** — Gemini/Ask Photos making search worse, slower, or less reliable
- **face_recognition** — Face grouping errors, misidentification, poor recognition edge cases
- **temporal_navigation** — Can't navigate by time, wrong timestamps, no date-range filtering
- **screenshot_document_search** — Can't find screenshots, documents, receipts, medical photos
- **location_search** — Location-based search gaps, missing GPS, no indoor location inference
- **organization_friction** — Albums, folders, archiving, tagging, manual effort

**Coding rules:** Each review gets 1–3 themes. Sentiment is tagged as positive/negative/mixed/neutral. User segment is inferred from context.
        """)

    # ── Opportunity Areas ──
    st.markdown('<div class="section-hdr">Opportunity Areas Ranked by Impact</div>', unsafe_allow_html=True)
    for area in compute_opportunity_areas():
        plat_str = ", ".join(f"{p}: {c}" for p, c in sorted(area["platforms"].items(), key=lambda x: -x[1]))
        st.markdown(f"""
        <div class="opp-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <h4>{area['label']}</h4>
                <span class="score">{area['impact']}/10</span>
            </div>
            <div style="color:#5F6368;font-size:0.85rem;margin-bottom:8px;line-height:1.5;">{area['description']}</div>
            <div style="color:#9AA0A6;font-size:0.75rem;">Evidence: {area['evidence_count']} reviews · {plat_str}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(area["impact"] / 10)


# ─────────────────────────────────────────────
# 9. PAGE: ASK INSIGHTS — PUBLIC REVIEWS
# ─────────────────────────────────────────────
def page_public_reviews():
    st.markdown('<div class="page-title">Ask Insights from Public Reviews</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Search the review corpus with any question — TF-IDF retrieval + AI synthesis</div>', unsafe_allow_html=True)
    google_accent_bar()

    with st.expander("💡 Sample questions to try"):
        st.markdown("""
- What kinds of old photos do users struggle to retrieve?
- What information do people actually remember about a photo vs what they've forgotten?
- How do users formulate searches when their memory is incomplete?
- What are the biggest complaints about the Ask Photos / Gemini AI search?
- How does face recognition fail for family organizers?
- What types of 'functional' photos (documents, receipts, medical) are hardest to find?
- Where does location-based search break down?
- How do users feel about the trade-off between AI search and classic keyword search?
        """)

    query = st.text_input("Your question:", placeholder="e.g. What kinds of photos are hardest to find?")
    search_btn = st.button("Search & Synthesize", type="primary")

    if search_btn and query:
        results = review_engine.search(query, top_k=15)
        if not results:
            st.warning("No matching reviews found. Try different keywords.")
            return

        api_key = get_api_key()
        if api_key:
            evidence = "\n\n".join(
                f"[Review {r['id']} | {r['platform']} | {r['sentiment']}]: \"{r['text']}\""
                for r in results
            )
            user_msg = f"QUESTION: {query}\n\nREVIEWS:\n{evidence}"
            with st.spinner("Synthesizing AI answer..."):
                answer = call_groq(REVIEW_SYSTEM_PROMPT, user_msg, api_key)
            if answer.startswith("__ERROR__"):
                st.error(f"LLM error: {answer}")
            else:
                st.markdown(
                    f'<div class="ai-answer"><b>AI-Synthesized Answer</b><br><br>{answer}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Add your Groq API key in Streamlit Cloud Secrets (`GROQ_API_KEY`) to enable AI synthesis.")

        st.markdown(f'<div class="section-hdr">Source Reviews ({len(results)} matches)</div>', unsafe_allow_html=True)
        for r in results:
            render_review_card(r)

        theme_dist = Counter()
        for r in results:
            for t in r.get("themes", []):
                theme_dist[t] += 1
        if theme_dist:
            st.markdown('<div class="section-hdr">Theme Distribution in Results</div>', unsafe_allow_html=True)
            for t, c in theme_dist.most_common():
                label = THEME_LABELS.get(t, t)
                st.markdown(f"**{label}** — {c} reviews")
                st.progress(c / len(results))


# ─────────────────────────────────────────────
# 10. PAGE: ASK INSIGHTS — USER SURVEY
# ─────────────────────────────────────────────
def page_user_survey():
    st.markdown('<div class="page-title">Ask Insights from User Survey</div>', unsafe_allow_html=True)
    google_accent_bar()

    if not SURVEY:
        st.info(
            "📂 **No survey data loaded yet.** Upload your survey data as `data/survey.json` "
            "and redeploy. The survey page will light up with search and AI synthesis over "
            "your primary research data."
        )
        st.markdown("---")
        st.markdown("### Expected format for `survey.json`")
        st.code("""{
  "id": 1,
  "demographics": { "gender": "Male", "age_group": "23-25", ... },
  "usage_behavior": { ... },
  "barriers_ratings": { "barrier_name": 3.0 },
  "open_ended_field": "User's verbatim response",
  "searchable_text": "All text fields concatenated for TF-IDF search"
}""", language="json")
        return

    st.markdown(f'<div class="page-subtitle">{len(SURVEY)} survey responses loaded</div>', unsafe_allow_html=True)

    query = st.text_input("Your question:", placeholder="e.g. What barriers do users face when retrieving old photos?")
    search_btn = st.button("Search & Synthesize", type="primary")

    if search_btn and query and survey_engine:
        results = survey_engine.search(query, top_k=15)
        if not results:
            st.warning("No matching survey responses found.")
            return

        api_key = get_api_key()
        if api_key:
            evidence = "\n\n".join(
                f"[Respondent {r.get('id','')}]: {r.get('searchable_text','')[:500]}"
                for r in results
            )
            user_msg = f"QUESTION: {query}\n\nSURVEY DATA:\n{evidence}"
            with st.spinner("Synthesizing AI answer..."):
                answer = call_groq(SURVEY_SYSTEM_PROMPT, user_msg, api_key)
            if answer.startswith("__ERROR__"):
                st.error(f"LLM error: {answer}")
            else:
                st.markdown(
                    f'<div class="ai-answer"><b>AI-Synthesized Answer</b><br><br>{answer}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Add your Groq API key in Streamlit Cloud Secrets to enable AI synthesis.")

        st.markdown(f'<div class="section-hdr">Matching Responses ({len(results)})</div>', unsafe_allow_html=True)
        for r in results:
            st.markdown(
                f"""<div class="review-card">
                    <div style="color:#4285F4;font-weight:600;font-size:0.85rem;">Respondent {r.get('id','')}</div>
                    <div class="review-text">{r.get('searchable_text','')[:400]}...</div>
                </div>""",
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────
# 11. PAGE: REVIEW EXPLORER
# ─────────────────────────────────────────────
def page_explorer():
    st.markdown('<div class="page-title">Review Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Filter and browse the full review corpus</div>', unsafe_allow_html=True)
    google_accent_bar()

    c1, c2, c3, c4 = st.columns(4)
    platforms = sorted(set(r.get("platform", "Unknown") for r in REVIEWS))
    all_themes = sorted(set(t for r in REVIEWS for t in r.get("themes", [])))
    sentiments = sorted(set(r.get("sentiment", "unknown") for r in REVIEWS))
    segments = sorted(set(r.get("user_segment", "unknown") for r in REVIEWS))

    with c1:
        sel_platforms = st.multiselect("Platform", platforms, default=platforms)
    with c2:
        sel_themes = st.multiselect("Theme", all_themes, default=all_themes)
    with c3:
        sel_sentiments = st.multiselect("Sentiment", sentiments, default=sentiments)
    with c4:
        sel_segments = st.multiselect("User Segment", segments, default=segments)

    filtered = [
        r for r in REVIEWS
        if r.get("platform") in sel_platforms
        and r.get("sentiment") in sel_sentiments
        and r.get("user_segment") in sel_segments
        and any(t in sel_themes for t in r.get("themes", []))
    ]

    st.markdown(f"**Showing {len(filtered)}** of {len(REVIEWS)} reviews")
    st.markdown("---")

    for r in filtered:
        render_review_card(r)


# ─────────────────────────────────────────────
# 12. PAGE: COMPARISON MATRIX
# ─────────────────────────────────────────────
def page_comparison():
    st.markdown('<div class="page-title">Comparison Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Impact vs Evidence Volume for each opportunity area</div>', unsafe_allow_html=True)
    google_accent_bar()

    try:
        import altair as alt
        import pandas as pd
    except ImportError:
        st.error("Install altair and pandas: `pip install altair pandas`")
        return

    areas = compute_opportunity_areas()
    if not areas:
        st.warning("No opportunity areas computed.")
        return

    df = pd.DataFrame(areas)

    chart = (
        alt.Chart(df)
        .mark_circle(size=200, opacity=0.85)
        .encode(
            x=alt.X("evidence_count:Q", title="Evidence Volume (# reviews)", scale=alt.Scale(zero=True)),
            y=alt.Y("impact:Q", title="Impact Score (0–10)", scale=alt.Scale(domain=[0, 10.5])),
            color=alt.Color(
                "label:N", title="Opportunity Area",
                scale=alt.Scale(range=["#4285F4", "#EA4335", "#34A853", "#FBBC05", "#8E24AA", "#00ACC1", "#FF7043", "#78909C"]),
            ),
            tooltip=["label:N", "impact:Q", "evidence_count:Q", "description:N"],
        )
        .properties(width=700, height=450)
        .configure_axis(labelFontSize=12, titleFontSize=13)
        .configure_legend(labelFontSize=11, titleFontSize=12)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown('<div class="section-hdr">Summary Table</div>', unsafe_allow_html=True)
    summary_df = df[["label", "impact", "evidence_count"]].rename(
        columns={"label": "Opportunity Area", "impact": "Impact Score*", "evidence_count": "Evidence Count"}
    )
    st.dataframe(summary_df.sort_values("Impact Score*", ascending=False), use_container_width=True, hide_index=True)
    st.markdown(
        '<p style="color:#9AA0A6;font-size:0.75rem;margin-top:4px;">'
        '*Impact Score = (review count for this theme ÷ highest review count across all themes) × 10. '
        'It is a proxy for how widespread the problem is based on evidence volume, not a measure of severity or business impact.'
        '</p>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 13. PAGE: FOCUSED REVIEWS (KPI TREE)
# ─────────────────────────────────────────────
KPI_NODES = {
    "attempt_fuzzy_retrieval": {
        "label": "% Who Attempt Fuzzy Retrieval",
        "metric": "Awareness & willingness to search",
        "description": "Do users even attempt a search when they have a vague, incomplete memory of a photo? Many users have learned that search won't understand what they're looking for, so they default to scrolling or asking friends. This node captures abandonment before a search is even tried.",
        "color": "#4285F4",
    },
    "query_formation": {
        "label": "Query Formation",
        "metric": "72% — moderate friction",
        "description": "Can users translate their episodic memory into a text query? Users remember scenes, emotions, colors, and context — but the search requires keywords. The gap between how humans remember and how they must express that memory is the core friction here.",
        "color": "#FBBC05",
    },
    "result_relevance": {
        "label": "Result Relevance",
        "metric": "45% — BOTTLENECK",
        "description": "Are the search results actually relevant to what the user is looking for? This is the biggest drop-off in the funnel. Search returns too many results, wrong results, or misses the target entirely. Adjectives are ignored, context is lost, and AI search regressions have worsened this.",
        "color": "#EA4335",
    },
    "target_found": {
        "label": "Target Found",
        "metric": "60% — significant drop",
        "description": "Even when results are broadly relevant, can the user identify THE specific photo they were looking for? A search for 'beach' might return 200 beach photos — the user must visually scan tiny thumbnails to find the one. No sub-filtering, no result sorting, no refine-within-results.",
        "color": "#FF7043",
    },
    "confirmed": {
        "label": "Confirmed",
        "metric": "90% — healthy",
        "description": "Once a user thinks they found the photo, are they confident it's the right one? This step is mostly healthy, but fails for similar-looking documents, repeated visits to the same location, and photos where metadata (date, location) is needed for verification but hidden behind taps.",
        "color": "#34A853",
    },
}

KPI_FUNNEL_ORDER = [
    "attempt_fuzzy_retrieval",
    "query_formation",
    "result_relevance",
    "target_found",
    "confirmed",
]

def page_kpi_tree():
    st.markdown('<div class="page-title">Focused Reviews (KPI Tree)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">User evidence mapped to each stage of the retrieval success funnel</div>', unsafe_allow_html=True)
    google_accent_bar()

    # ── Funnel visualization ──
    st.markdown('<div class="section-hdr">Retrieval Success Funnel</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#FFFFFF;border-radius:12px;padding:24px;box-shadow:0 1px 2px rgba(60,64,67,0.3);margin-bottom:28px;">
        <div style="text-align:center;color:#5F6368;font-size:0.82rem;margin-bottom:8px;">
            Success Rate per Session = Query Formation × Result Relevance × Target Found × Confirmed
        </div>
        <div style="text-align:center;color:#202124;font-size:1.1rem;font-weight:700;margin-bottom:20px;">
            0.72 × 0.45 × 0.60 × 0.90 ≈ <span style="color:#EA4335;">17.5% success rate</span>
        </div>
        <div style="display:flex;gap:6px;align-items:stretch;">
            <div style="flex:1;background:#E8F0FE;border-radius:8px;padding:14px 8px;text-align:center;border-top:3px solid #4285F4;">
                <div style="font-size:0.65rem;color:#5F6368;text-transform:uppercase;letter-spacing:0.05em;">Attempt</div>
                <div style="font-size:0.82rem;font-weight:700;color:#4285F4;margin-top:2px;">Fuzzy Retrieval</div>
            </div>
            <div style="display:flex;align-items:center;color:#DADCE0;font-size:1.2rem;">›</div>
            <div style="flex:1;background:#FEF7E0;border-radius:8px;padding:14px 8px;text-align:center;border-top:3px solid #FBBC05;">
                <div style="font-size:0.65rem;color:#5F6368;text-transform:uppercase;letter-spacing:0.05em;">Query</div>
                <div style="font-size:0.82rem;font-weight:700;color:#FBBC05;margin-top:2px;">72%</div>
            </div>
            <div style="display:flex;align-items:center;color:#DADCE0;font-size:1.2rem;">›</div>
            <div style="flex:1;background:#FCE8E6;border-radius:8px;padding:14px 8px;text-align:center;border-top:3px solid #EA4335;">
                <div style="font-size:0.65rem;color:#5F6368;text-transform:uppercase;letter-spacing:0.05em;">Relevance</div>
                <div style="font-size:0.82rem;font-weight:700;color:#EA4335;margin-top:2px;">45% ⚠</div>
            </div>
            <div style="display:flex;align-items:center;color:#DADCE0;font-size:1.2rem;">›</div>
            <div style="flex:1;background:#FBE9E7;border-radius:8px;padding:14px 8px;text-align:center;border-top:3px solid #FF7043;">
                <div style="font-size:0.65rem;color:#5F6368;text-transform:uppercase;letter-spacing:0.05em;">Found</div>
                <div style="font-size:0.82rem;font-weight:700;color:#FF7043;margin-top:2px;">60%</div>
            </div>
            <div style="display:flex;align-items:center;color:#DADCE0;font-size:1.2rem;">›</div>
            <div style="flex:1;background:#E6F4EA;border-radius:8px;padding:14px 8px;text-align:center;border-top:3px solid #34A853;">
                <div style="font-size:0.65rem;color:#5F6368;text-transform:uppercase;letter-spacing:0.05em;">Confirmed</div>
                <div style="font-size:0.82rem;font-weight:700;color:#34A853;margin-top:2px;">90% ✓</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Node selector ──
    st.markdown('<div class="section-hdr">Explore by Funnel Stage</div>', unsafe_allow_html=True)

    selected_node = st.selectbox(
        "Select a funnel stage:",
        KPI_FUNNEL_ORDER,
        format_func=lambda x: f"{KPI_NODES[x]['label']} ({KPI_NODES[x]['metric']})",
    )

    node_info = KPI_NODES[selected_node]

    # ── Node header card ──
    node_reviews = [r for r in REVIEWS if selected_node in r.get("kpi_node", [])]
    neg_count = sum(1 for r in node_reviews if r.get("sentiment") == "negative")
    pos_count = sum(1 for r in node_reviews if r.get("sentiment") == "positive")
    mix_count = len(node_reviews) - neg_count - pos_count

    st.markdown(f"""
    <div style="background:#FFFFFF;border-radius:12px;padding:24px;
                border-left:5px solid {node_info['color']};margin-bottom:24px;
                box-shadow:0 1px 2px rgba(60,64,67,0.3);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <h3 style="margin:0;color:#202124;font-size:1.2rem;">{node_info['label']}</h3>
                <span style="color:{node_info['color']};font-weight:600;font-size:0.88rem;">{node_info['metric']}</span>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2.2rem;font-weight:700;color:{node_info['color']};line-height:1;">{len(node_reviews)}</div>
                <div style="font-size:0.75rem;color:#5F6368;">reviews</div>
            </div>
        </div>
        <p style="color:#5F6368;font-size:0.88rem;margin-top:14px;line-height:1.6;">{node_info['description']}</p>
        <div style="margin-top:14px;display:flex;gap:20px;">
            <span style="color:#EA4335;font-size:0.8rem;font-weight:500;">● {neg_count} negative</span>
            <span style="color:#34A853;font-size:0.8rem;font-weight:500;">● {pos_count} positive</span>
            <span style="color:#F9AB00;font-size:0.8rem;font-weight:500;">● {mix_count} mixed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Platform breakdown for this node — capped at 4 cols ──
    plat_counts = Counter(r.get("platform", "Unknown") for r in node_reviews)
    if plat_counts:
        top_plats = plat_counts.most_common(4)
        cols = st.columns(len(top_plats), gap="medium")
        plat_colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
        for i, (plat, cnt) in enumerate(top_plats):
            with cols[i]:
                st.markdown(
                    f'<div class="g-card">'
                    f'<div class="g-num" style="color:{plat_colors[i % 4]};">{cnt}</div>'
                    f'<div class="g-label">{plat}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── AI synthesis for this node ──
    st.markdown("---")
    api_key = get_api_key()
    if api_key:
        synth_btn = st.button(f"Synthesize insights for: {node_info['label']}", type="primary")
        if synth_btn:
            evidence = "\n\n".join(
                f"[Review {r['id']} | {r['platform']} | {r['sentiment']}]: \"{r['text']}\""
                for r in node_reviews[:20]
            )
            kpi_prompt = f"""You are a senior user researcher analyzing Google Photos feedback mapped to a specific stage of the retrieval funnel.

The funnel stage is: **{node_info['label']}** — {node_info['description']}

Answer grounded ONLY in the provided reviews. Do NOT number sections.

Start with a 2-3 sentence synthesis of what's happening at this funnel stage.

Then **Key Patterns** — the 3-4 most prominent failure modes at this stage with evidence.

Then **Who's Most Affected** — which user types suffer most at this stage.

Then **Opportunity** — what specific product change would move this metric, grounded in what users say they need.

Quote specific reviews as evidence."""

            user_msg = f"FUNNEL STAGE: {node_info['label']}\n\nREVIEWS:\n{evidence}"
            with st.spinner("Synthesizing insights..."):
                answer = call_groq(kpi_prompt, user_msg, api_key)
            if answer.startswith("__ERROR__"):
                st.error(f"LLM error: {answer}")
            else:
                st.markdown(
                    f'<div class="ai-answer"><b>AI Synthesis — {node_info["label"]}</b><br><br>{answer}</div>',
                    unsafe_allow_html=True,
                )

    # ── Reviews list ──
    st.markdown(
        f'<div class="section-hdr">All Reviews — {node_info["label"]} ({len(node_reviews)})</div>',
        unsafe_allow_html=True,
    )

    sent_filter = st.multiselect(
        "Filter by sentiment:",
        ["negative", "positive", "mixed", "neutral"],
        default=["negative", "positive", "mixed", "neutral"],
        key="kpi_sent_filter",
    )
    filtered = [r for r in node_reviews if r.get("sentiment") in sent_filter]
    for r in filtered:
        render_review_card(r)


# ─────────────────────────────────────────────
# 14. ROUTER
# ─────────────────────────────────────────────
if st.session_state["page"] == "dashboard":
    page_dashboard()
elif st.session_state["page"] == "kpi_tree":
    page_kpi_tree()
elif st.session_state["page"] == "public_reviews":
    page_public_reviews()
elif st.session_state["page"] == "user_survey":
    page_user_survey()
elif st.session_state["page"] == "explorer":
    page_explorer()
elif st.session_state["page"] == "comparison":
    page_comparison()
