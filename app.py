import time
import streamlit as st

st.set_page_config(page_title="StretchPractice", page_icon="🧘", layout="centered")

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
# Structure: AREAS -> list of routine dicts -> list of exercise dicts
AREAS = {
    "Hips": {
        "emoji": "🧘",
        "routines": [
            {
                "name": "Hips 1",
                "minutes": 5,
                "desc": "A series of stretches designed to increase flexibility in the hips, "
                        "including your hip flexors & extensors, abductors & adductors, and hip rotators.",
                "exercises": [
                    {"name": "Lunge", "seconds": 60},
                    {"name": "Reverse Lunge", "seconds": 60},
                    {"name": "Butterfly", "seconds": 30},
                    {"name": "Lying Figure Four", "seconds": 60},
                    {"name": "Quad Stretch", "seconds": 60},
                    {"name": "Spinal Twist", "seconds": 60},
                ],
            },
            {
                "name": "Hips 2",
                "minutes": 10,
                "desc": "A deeper hip-opening flow for tight runners and cyclists.",
                "exercises": [
                    {"name": "Lizard Pose", "seconds": 60},
                    {"name": "Pigeon Pose", "seconds": 60},
                    {"name": "Frog Stretch", "seconds": 60},
                    {"name": "Deep Squat Hold", "seconds": 60},
                    {"name": "Seated Forward Fold", "seconds": 60},
                ],
            },
            {
                "name": "Hips 3",
                "minutes": 15,
                "desc": "Extended hip mobility routine combining strength and flexibility.",
                "exercises": [
                    {"name": "Cossack Squat", "seconds": 60},
                    {"name": "Half Kneeling Hip Flexor Stretch", "seconds": 60},
                    {"name": "Butterfly", "seconds": 45},
                    {"name": "Figure Four Stretch", "seconds": 60},
                    {"name": "Wide Leg Forward Fold", "seconds": 60},
                ],
            },
        ],
    },
    "Lower Back": {
        "emoji": "🦴",
        "routines": [
            {
                "name": "Lower Back 1",
                "minutes": 5,
                "desc": "Gentle stretches to relieve tension in the lower back.",
                "exercises": [
                    {"name": "Cat-Cow", "seconds": 45},
                    {"name": "Child's Pose", "seconds": 60},
                    {"name": "Knee to Chest", "seconds": 45},
                    {"name": "Seated Spinal Twist", "seconds": 45},
                ],
            },
        ],
    },
    "Neck": {
        "emoji": "🙆",
        "routines": [
            {
                "name": "Neck 1",
                "minutes": 5,
                "desc": "Simple neck mobility stretches for desk-related tension.",
                "exercises": [
                    {"name": "Neck Tilt", "seconds": 30},
                    {"name": "Neck Rotation", "seconds": 30},
                    {"name": "Chin Tuck", "seconds": 30},
                    {"name": "Upper Trap Stretch", "seconds": 30},
                ],
            },
        ],
    },
    "Shoulders": {
        "emoji": "💪",
        "routines": [
            {
                "name": "Shoulders 1",
                "minutes": 5,
                "desc": "Loosen up tight shoulders after training or long desk hours.",
                "exercises": [
                    {"name": "Cross-Body Shoulder Stretch", "seconds": 45},
                    {"name": "Overhead Triceps Stretch", "seconds": 45},
                    {"name": "Doorway Chest Stretch", "seconds": 45},
                    {"name": "Shoulder Rolls", "seconds": 30},
                ],
            },
        ],
    },
    "Splits": {
        "emoji": "🤸",
        "routines": [
            {
                "name": "Splits 1",
                "minutes": 10,
                "desc": "Progressive stretches building toward full splits.",
                "exercises": [
                    {"name": "Low Lunge", "seconds": 60},
                    {"name": "Half Split", "seconds": 60},
                    {"name": "Frog Stretch", "seconds": 60},
                    {"name": "Side Split Hold", "seconds": 60},
                ],
            },
        ],
    },
    "Hamstrings": {
        "emoji": "🏃",
        "routines": [
            {
                "name": "Hamstrings 1",
                "minutes": 5,
                "desc": "Great post-run or post-ride hamstring release.",
                "exercises": [
                    {"name": "Standing Forward Fold", "seconds": 45},
                    {"name": "Seated Hamstring Stretch", "seconds": 45},
                    {"name": "Reclined Hamstring Stretch", "seconds": 45},
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# STYLE (dark theme, rounded cards - similar vibe to the reference app)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: white; }
    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        padding: 0.9em;
        background-color: #1c1c1e;
        color: white;
        border: 1px solid #2c2c2e;
        font-weight: 600;
        text-align: left;
    }
    div.stButton > button:hover { background-color: #2c2c2e; border-color: #444; }
    .start-btn button {
        background-color: #2f8fe0 !important;
        text-align: center !important;
        font-size: 1.1em !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
defaults = {
    "page": "home",
    "area": None,
    "routine_idx": None,
    "durations": {},  # per-routine overrides: {(area, routine_name): [seconds,...]}
    "playing_idx": 0,
}
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


# ---------------------------------------------------------------------------
# PAGE: HOME (browse by area)
# ---------------------------------------------------------------------------
def page_home():
    st.title("🧘 StretchPractice")
    st.caption("A practice clone — browse by area, pick a routine, start stretching.")
    st.text_input("🔍 Search for a routine", key="search", label_visibility="visible")

    st.subheader("BROWSE BY AREA")
    areas = list(AREAS.keys())
    cols = st.columns(3)
    for i, area in enumerate(areas):
        with cols[i % 3]:
            if st.button(f"{AREAS[area]['emoji']}\n\n**{area}**", key=f"area_{area}"):
                go("area", area=area)
                st.rerun()


# ---------------------------------------------------------------------------
# PAGE: AREA (list of routines, e.g. "Hips 1..6")
# ---------------------------------------------------------------------------
def page_area():
    area = st.session_state.area
    if st.button("← Back"):
        go("home")
        st.rerun()
    st.title(area)
    st.subheader("FLEXIBILITY")
    for i, routine in enumerate(AREAS[area]["routines"]):
        label = f"**{routine['name']}**\n\n{routine['minutes']} minutes"
        if st.button(label, key=f"routine_{i}"):
            go("routine", routine_idx=i)
            st.rerun()


# ---------------------------------------------------------------------------
# PAGE: ROUTINE DETAIL (exercise list w/ adjustable durations + Start)
# ---------------------------------------------------------------------------
def page_routine():
    routine = get_routine()
    durations = get_durations(routine)

    if st.button("← Back"):
        go("area")
        st.rerun()

    st.title(routine["name"])
    total_min = sum(durations) // 60
    st.caption(f"{total_min} MINUTES")
    st.write(routine["desc"])
    st.divider()

    for i, ex in enumerate(routine["exercises"]):
        c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
        c1.markdown(f"**{ex['name']}**")
        if c2.button("−", key=f"minus_{i}"):
            durations[i] = max(5, durations[i] - 5)
            st.rerun()
        mins, secs = divmod(durations[i], 60)
        c3.markdown(f"<div style='text-align:center;padding-top:6px'>{mins}:{secs:02d}</div>", unsafe_allow_html=True)
        if c4.button("+", key=f"plus_{i}"):
            durations[i] += 5
            st.rerun()

    st.divider()
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("▶ START", key="start_btn"):
        go("play", playing_idx=0)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# PAGE: PLAY (countdown timer through the exercise list)
# ---------------------------------------------------------------------------
def page_play():
    routine = get_routine()
    durations = get_durations(routine)
    exercises = routine["exercises"]
    idx = st.session_state.playing_idx

    if idx >= len(exercises):
        st.title("🎉 Done!")
        st.success(f"You finished {routine['name']}.")
        if st.button("Back to routine"):
            go("routine")
            st.rerun()
        return

    ex = exercises[idx]
    seconds = durations[idx]

    st.title(ex["name"])
    st.caption(f"Exercise {idx + 1} of {len(exercises)}")

    top1, top2 = st.columns(2)
    if top1.button("⏭ Skip"):
        st.session_state.playing_idx += 1
        st.rerun()
    if top2.button("⏹ Stop"):
        go("routine")
        st.rerun()

    placeholder = st.empty()
    progress = st.progress(0)
    for remaining in range(seconds, 0, -1):
        placeholder.markdown(
            f"<h1 style='text-align:center;font-size:4em'>{remaining}</h1>",
            unsafe_allow_html=True,
        )
        progress.progress(int((seconds - remaining + 1) / seconds * 100))
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
