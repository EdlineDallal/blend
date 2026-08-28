import time
import streamlit as st

st.set_page_config(page_title="StretchPractice", page_icon="🧘", layout="centered", initial_sidebar_state="collapsed")

# ---------------------------------------------------------------------------
# DATA  (from user-provided screenshots — Lower Back category)
# ---------------------------------------------------------------------------
# Each exercise: name, seconds, emoji, bg color (matched to screenshot icon colors)
AREAS = {
    "Lower Back": {
        "emoji": "🧎",
        "color": "#3E9B7A",
        "routines": [
            {
                "name": "Lower Back 1",
                "minutes": 5,
                "level": "Beginner",
                "desc": "A series of stretches designed to increase flexibility in the lower back.",
                "exercises": [
                    {"name": "Cat Cow",          "seconds": 30, "pose": "cat_cow",       "color": "#8C3B4A"},
                    {"name": "Downward Dog",      "seconds": 30, "pose": "downward_dog",  "color": "#3E9B7A"},
                    {"name": "Lunge",             "seconds": 45, "pose": "lunge",         "color": "#C7D66B"},
                    {"name": "Reverse Lunge",     "seconds": 45, "pose": "reverse_lunge", "color": "#1F5C4B"},
                    {"name": "Butterfly",         "seconds": 30, "pose": "butterfly",     "color": "#E8B4C8"},
                    {"name": "Knees-to-chest",    "seconds": 30, "pose": "knees_chest",   "color": "#E0B84A"},
                    {"name": "Spinal Twist",      "seconds": 45, "pose": "spinal_twist",  "color": "#5A5FA8"},
                    {"name": "Lying Figure Four", "seconds": 45, "pose": "figure_four",   "color": "#D4772E"},
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# ORIGINAL HAND-DRAWN STICK-FIGURE ICONS (inline SVG, simple flat style)
# Drawn from scratch — not copied from any reference app.
# Each is a minimal white-stroke figure on a transparent 100x100 canvas.
# ---------------------------------------------------------------------------
POSE_SVGS = {
    "cat_cow": """
        <circle cx="30" cy="35" r="7"/>
        <path d="M30 42 Q50 30 75 42" fill="none"/>
        <path d="M75 42 L82 60" fill="none"/>
        <path d="M30 42 L25 60" fill="none"/>
        <path d="M40 55 L38 78" fill="none"/>
        <path d="M65 55 L67 78" fill="none"/>
    """,
    "downward_dog": """
        <circle cx="78" cy="60" r="7"/>
        <path d="M78 65 L35 30" fill="none"/>
        <path d="M35 30 L20 55" fill="none"/>
        <path d="M35 30 L48 50" fill="none"/>
        <path d="M78 65 L60 78" fill="none"/>
        <path d="M78 65 L88 80" fill="none"/>
    """,
    "lunge": """
        <circle cx="45" cy="20" r="7"/>
        <path d="M45 27 L48 55" fill="none"/>
        <path d="M48 55 L30 80" fill="none"/>
        <path d="M48 55 L72 62" fill="none"/>
        <path d="M45 30 L25 20" fill="none"/>
        <path d="M45 35 L68 25" fill="none"/>
    """,
    "reverse_lunge": """
        <circle cx="42" cy="22" r="7"/>
        <path d="M42 29 L45 55" fill="none"/>
        <path d="M45 55 L70 45" fill="none"/>
        <path d="M45 55 L35 82" fill="none"/>
        <path d="M42 32 L60 20" fill="none"/>
        <path d="M42 38 L22 45" fill="none"/>
    """,
    "butterfly": """
        <circle cx="50" cy="22" r="7"/>
        <path d="M50 29 L50 55" fill="none"/>
        <path d="M50 55 L30 70" fill="none"/>
        <path d="M50 55 L70 70" fill="none"/>
        <path d="M30 70 L50 75" fill="none"/>
        <path d="M70 70 L50 75" fill="none"/>
        <path d="M50 35 L30 45" fill="none"/>
        <path d="M50 35 L70 45" fill="none"/>
    """,
    "knees_chest": """
        <circle cx="25" cy="55" r="7"/>
        <path d="M25 62 L55 70" fill="none"/>
        <path d="M55 70 L55 45" fill="none"/>
        <path d="M55 45 L40 30" fill="none"/>
        <path d="M55 45 L40 55" fill="none"/>
        <path d="M25 60 L35 75" fill="none"/>
    """,
    "spinal_twist": """
        <circle cx="35" cy="30" r="7"/>
        <path d="M35 37 L45 65" fill="none"/>
        <path d="M45 65 L25 78" fill="none"/>
        <path d="M45 65 L68 78" fill="none"/>
        <path d="M38 45 L70 35" fill="none"/>
        <path d="M38 45 L18 55" fill="none"/>
    """,
    "figure_four": """
        <circle cx="20" cy="45" r="7"/>
        <path d="M20 52 L50 55" fill="none"/>
        <path d="M50 55 L75 45" fill="none"/>
        <path d="M50 55 L70 68" fill="none"/>
        <path d="M70 68 L55 72" fill="none"/>
        <path d="M20 50 L15 68" fill="none"/>
    """,
}


def pose_icon(pose_key, color, size=54):
    body = POSE_SVGS.get(pose_key, "")
    return f"""
    <div class="icon-circle" style="background:{color}">
      <svg width="{int(size*0.62)}" height="{int(size*0.62)}" viewBox="0 0 100 100"
           stroke="white" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="white">
        {body}
      </svg>
    </div>
    """

# ---------------------------------------------------------------------------
# STYLE
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 560px; }

    div.stButton > button {
        width: 100%;
        border-radius: 16px;
        padding: 0.9em 1em;
        background-color: #17171A;
        color: white;
        border: 1px solid #262629;
        font-weight: 600;
        text-align: left;
        transition: 0.15s;
    }
    div.stButton > button:hover { background-color: #212124; border-color: #3a3a3d; }

    .start-btn button {
        background: linear-gradient(135deg, #3E8FE0, #2F6FE0) !important;
        text-align: center !important;
        font-size: 1.15em !important;
        border: none !important;
        letter-spacing: 0.5px;
    }

    .pill {
        display: inline-block;
        background-color: #1c1c1e;
        color: #aaaaaa;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: 700;
        letter-spacing: 1px;
        margin-right: 6px;
    }

    .icon-circle {
        width: 54px; height: 54px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 26px; flex-shrink: 0;
    }

    .area-card {
        border-radius: 16px; border: 1px solid #262629; padding: 18px 14px;
        text-align: center; background-color: #111113;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
defaults = {"page": "home", "area": None, "routine_idx": None, "durations": {}, "playing_idx": 0, "paused": False}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v


def get_routine():
    area = st.session_state.area
    idx = st.session_state.routine_idx
    return AREAS[area]["routines"][idx]


def get_durations(routine):
    key = (st.session_state.area, routine["name"])
    if key not in st.session_state.durations:
        st.session_state.durations[key] = [e["seconds"] for e in routine["exercises"]]
    return st.session_state.durations[key]


def fmt(sec):
    m, s = divmod(sec, 60)
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# PAGE: HOME
# ---------------------------------------------------------------------------
def page_home():
    st.markdown("### 🧘 StretchPractice")
    st.text_input("🔍", placeholder="Search for a routine", label_visibility="collapsed")
    st.markdown("<div style='color:#888;font-weight:700;letter-spacing:1px;margin:18px 0 10px;'>BROWSE BY AREA</div>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, area in enumerate(AREAS):
        with cols[i % 3]:
            st.markdown(
                f"""<div class="area-card">
                    <div style="font-size:2em;">{AREAS[area]['emoji']}</div>
                    <div style="font-weight:700;margin-top:6px;">{area}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button("Open", key=f"area_{area}"):
                go("area", area=area)
                st.rerun()

    st.caption("More areas (Hips, Neck, Shoulders...) coming as you send more screenshots 👀")


# ---------------------------------------------------------------------------
# PAGE: AREA — list routines
# ---------------------------------------------------------------------------
def page_area():
    area = st.session_state.area
    if st.button("← Back", key="back_area"):
        go("home")
        st.rerun()
    st.markdown(f"## {AREAS[area]['emoji']} {area}")
    st.markdown("<div style='color:#888;font-weight:700;letter-spacing:1px;margin:14px 0 10px;'>FLEXIBILITY</div>", unsafe_allow_html=True)

    for i, routine in enumerate(AREAS[area]["routines"]):
        if st.button(f"**{routine['name']}**  \n{routine['minutes']} minutes · {routine['level']}", key=f"routine_{i}"):
            go("routine", routine_idx=i)
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE: ROUTINE DETAIL
# ---------------------------------------------------------------------------
def page_routine():
    routine = get_routine()
    durations = get_durations(routine)

    if st.button("← Back", key="back_routine"):
        go("area")
        st.rerun()

    st.markdown(f"## {routine['name']}")
    total_min = sum(durations) // 60
    st.markdown(f"<span class='pill'>{total_min} MINUTES</span><span class='pill'>{routine['level'].upper()}</span>", unsafe_allow_html=True)
    st.write("")
    st.write(routine["desc"])
    st.write("")

    for i, ex in enumerate(routine["exercises"]):
        c1, c2, c3, c4, c5 = st.columns([1, 4, 1, 1.3, 1])
        c1.markdown(pose_icon(ex["pose"], ex["color"]), unsafe_allow_html=True)
        c2.markdown(f"<div style='padding-top:14px;font-weight:600'>{ex['name']}</div>", unsafe_allow_html=True)
        if c3.button("−", key=f"minus_{i}"):
            durations[i] = max(5, durations[i] - 5)
            st.rerun()
        c4.markdown(f"<div style='text-align:center;padding-top:14px;color:#ccc'>{fmt(durations[i])}</div>", unsafe_allow_html=True)
        if c5.button("+", key=f"plus_{i}"):
            durations[i] += 5
            st.rerun()

    st.write("")
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("▶  START", key="start_btn"):
        go("play", playing_idx=0, paused=False)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# PAGE: PLAY — animated countdown with progress ring
# ---------------------------------------------------------------------------
def ring_svg(pct, color, big_text, sub_text):
    circumference = 2 * 3.14159 * 90
    offset = circumference * (1 - pct)
    return f"""
    <div style="display:flex;justify-content:center;margin:20px 0;">
      <svg width="240" height="240" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="90" stroke="#1c1c1e" stroke-width="12" fill="none"/>
        <circle cx="100" cy="100" r="90" stroke="{color}" stroke-width="12" fill="none"
          stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
          transform="rotate(-90 100 100)" style="transition: stroke-dashoffset 1s linear;"/>
        <text x="100" y="95" text-anchor="middle" fill="white" font-size="42" font-weight="700">{big_text}</text>
        <text x="100" y="125" text-anchor="middle" fill="#999" font-size="13">{sub_text}</text>
      </svg>
    </div>
    """


def page_play():
    routine = get_routine()
    durations = get_durations(routine)
    exercises = routine["exercises"]
    idx = st.session_state.playing_idx

    if idx >= len(exercises):
        st.balloons()
        st.markdown("## 🎉 Done!")
        st.success(f"You finished **{routine['name']}**.")
        if st.button("Back to routine"):
            go("routine")
            st.rerun()
        return

    ex = exercises[idx]
    seconds = durations[idx]
    next_name = exercises[idx + 1]["name"] if idx + 1 < len(exercises) else "Finish"

    top1, top2, top3 = st.columns([1, 1, 1])
    if top1.button("⏹ Stop"):
        go("routine")
        st.rerun()
    top2.markdown(f"<div style='text-align:center;color:#999;padding-top:8px;'>{idx+1} / {len(exercises)}</div>", unsafe_allow_html=True)
    if top3.button("⏭ Skip"):
        st.session_state.playing_idx += 1
        st.rerun()

    st.markdown(
        f"<div style='display:flex;justify-content:center;transform:scale(1.6);margin:18px 0 10px;'>{pose_icon(ex['pose'], ex['color'])}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<h1 style='text-align:center;font-size:1.8em;margin-top:4px'>{ex['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;color:#777'>Up next: {next_name}</div>", unsafe_allow_html=True)

    placeholder = st.empty()
    for remaining in range(seconds, 0, -1):
        pct = 1 - (remaining - 1) / seconds
        placeholder.markdown(ring_svg(pct, ex["color"], remaining, "seconds"), unsafe_allow_html=True)
        time.sleep(1)

    st.session_state.playing_idx += 1
    st.rerun()


# ---------------------------------------------------------------------------
# ROUTER
# ---------------------------------------------------------------------------
page = st.session_state.page
if page == "home":
    page_home()
elif page == "area":
    page_area()
elif page == "routine":
    page_routine()
elif page == "play":
    page_play()
