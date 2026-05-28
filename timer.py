import streamlit as st
import time
import json
import os
from datetime import datetime, date

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Smart Study Pro Timer",
    page_icon="📚",
    layout="centered"
)

# ----------------------------
# STYLING
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #eef2ff, #dbeafe);
    color: #111827;
}

h1, h2, h3 {
    color: #1e3a8a;
    text-align: center;
}

.stButton>button {
    width: 100%;
    border-radius: 15px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
    border: none;
    background-color: #2563eb;
    color: white;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    transform: scale(1.03);
}

.timer-box {
    text-align: center;
    padding: 20px;
    border-radius: 20px;
    background: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-top: 20px;
    margin-bottom: 20px;
}

.history-box {
    background: white;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# DATA FILE
# ----------------------------
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass

    return {
        "records": {},
        "streak": {},
        "last_date": None
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ----------------------------
# SESSION STATE
# ----------------------------
defaults = {
    "running": False,
    "time_left": 0,
    "total_time": 0,
    "mode": "Focus",
    "pomodoro": False,
    "subject": None,
    "session_done": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------------------------
# STREAK UPDATE
# ----------------------------
today = str(date.today())

if data["last_date"] != today:
    data["streak"][today] = 0
    data["last_date"] = today
    save_data(data)

# ----------------------------
# TITLE
# ----------------------------
st.title("📚 Smart Study Pro Timer")
st.caption("Stay focused. Study smarter. ✨")

# ----------------------------
# SETTINGS
# ----------------------------
subjects = [
    "Math",
    "Chemistry",
    "Physics",
    "Biology",
    "English",
    "Computer Science"
]

subject = st.selectbox("📖 Choose Subject", subjects)

minutes = st.number_input(
    "⏳ Focus Minutes",
    min_value=1,
    max_value=180,
    value=25
)

break_min = st.number_input(
    "☕ Break Minutes",
    min_value=1,
    max_value=60,
    value=5
)

pomodoro = st.toggle("🍅 Enable Pomodoro Mode")

st.session_state.pomodoro = pomodoro

# ----------------------------
# BUTTONS
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Start"):

        st.session_state.running = True
        st.session_state.subject = subject
        st.session_state.session_done = False

        if st.session_state.time_left == 0:
            st.session_state.mode = "Focus"
            st.session_state.time_left = minutes * 60
            st.session_state.total_time = minutes * 60

with col2:
    if st.button("⏸ Pause"):
        st.session_state.running = False

with col3:
    if st.button("⏹ Stop"):

        # Save partial progress
        if (
            st.session_state.total_time > 0
            and st.session_state.subject
        ):

            elapsed = (
                st.session_state.total_time
                - st.session_state.time_left
            )

            if elapsed > 0:
                data["records"].setdefault(
                    st.session_state.subject,
                    []
                )

                data["records"][
                    st.session_state.subject
                ].append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "duration": elapsed
                })

                data["streak"][today] = (
                    data["streak"].get(today, 0) + 1
                )

                save_data(data)

        # Reset everything
        st.session_state.running = False
        st.session_state.time_left = 0
        st.session_state.total_time = 0
        st.session_state.mode = "Focus"
        st.session_state.subject = None
        st.session_state.session_done = False

# ----------------------------
# TIMER DISPLAY
# ----------------------------
if st.session_state.total_time > 0:
    progress = 1 - (
        st.session_state.time_left
        / st.session_state.total_time
    )

    progress = max(0.0, min(progress, 1.0))

    st.progress(progress)

else:
    st.progress(0)

mins = st.session_state.time_left // 60
secs = st.session_state.time_left % 60

st.markdown(f"""
<div class="timer-box">
    <h2>{st.session_state.mode} Session</h2>
    <h1>{mins:02d}:{secs:02d}</h1>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# TIMER LOGIC
# ----------------------------
if (
    st.session_state.running
    and st.session_state.time_left > 0
):

    time.sleep(1)

    st.session_state.time_left -= 1

    st.rerun()

# ----------------------------
# AUTO FINISH
# ----------------------------
if (
    st.session_state.time_left == 0
    and st.session_state.total_time > 0
    and not st.session_state.session_done
):

    st.session_state.session_done = True

    st.success("🔔 Session Complete!")

    subj = st.session_state.subject

    if subj:

        data["records"].setdefault(subj, [])

        data["records"][subj].append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "duration": st.session_state.total_time
        })

        data["streak"][today] = (
            data["streak"].get(today, 0) + 1
        )

        save_data(data)

    # Pomodoro Auto Switch
    if st.session_state.pomodoro:

        time.sleep(2)

        if st.session_state.mode == "Focus":

            st.session_state.mode = "Break"
            st.session_state.time_left = break_min * 60
            st.session_state.total_time = break_min * 60

        else:

            st.session_state.mode = "Focus"
            st.session_state.time_left = minutes * 60
            st.session_state.total_time = minutes * 60

        st.session_state.running = True
        st.session_state.session_done = False

        st.rerun()

    else:
        st.session_state.running = False

# ----------------------------
# HISTORY
# ----------------------------
st.subheader("📊 Study History")

if not data["records"]:
    st.info("No study sessions yet.")

for subj, sessions in data["records"].items():

    st.markdown(f"### 📘 {subj}")

    total = 0

    for s in sessions:

        mins_done = s["duration"] // 60
        secs_done = s["duration"] % 60

        st.markdown(f"""
        <div class="history-box">
            🕒 {s['time']} <br>
            ⏳ {mins_done} min {secs_done} sec
        </div>
        """, unsafe_allow_html=True)

        total += s["duration"]

    st.write(
        f"**Total Study Time:** "
        f"{total//60} min {total%60} sec"
    )

# ----------------------------
# STREAK
# ----------------------------
st.subheader("🔥 Today's Streak")

st.metric(
    label="Completed Sessions",
    value=data["streak"].get(today, 0)
    )