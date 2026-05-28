import streamlit as st
import time
import json
import os
from datetime import datetime, date

# ----------------------------
# FILE STORAGE
# ----------------------------
DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"records": {}, "streak": {}, "last_date": None}

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
    "subject": None
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
# UI
# ----------------------------
st.title("📚 Smart Study Pro Timer")

subjects = ["Math", "Chemistry", "Physics", "Biology", "English", "Computer Science"]
subject = st.selectbox("Subject", subjects)

minutes = st.number_input("Focus minutes", 1, 180, 25)
break_min = st.number_input("Break minutes", 1, 60, 5)

pomodoro = st.toggle("🍅 Pomodoro Mode")

st.session_state.pomodoro = pomodoro

# ----------------------------
# BUTTONS
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Start"):
        st.session_state.running = True
        st.session_state.subject = subject

        if st.session_state.time_left == 0:
            st.session_state.time_left = minutes * 60
            st.session_state.total_time = minutes * 60

with col2:
    if st.button("⏸ Pause"):
        st.session_state.running = False

with col3:
    if st.button("⏹ Stop"):

        # ✅ SAVE PARTIAL PROGRESS (FIXED PART)
        if st.session_state.total_time > 0 and st.session_state.subject:

            elapsed = st.session_state.total_time - st.session_state.time_left

            if elapsed > 0:
                data["records"].setdefault(st.session_state.subject, [])
                data["records"][st.session_state.subject].append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "duration": elapsed
                })

                data["streak"][today] = data["streak"].get(today, 0) + 1
                save_data(data)

        # reset session
        st.session_state.running = False
        st.session_state.time_left = 0
        st.session_state.total_time = 0
        st.session_state.mode = "Focus"
        st.session_state.subject = None

# ----------------------------
# TIMER DISPLAY
# ----------------------------
if st.session_state.total_time > 0:
    progress = 1 - (st.session_state.time_left / st.session_state.total_time)
    st.progress(progress)
else:
    st.progress(0)

mins = st.session_state.time_left // 60
secs = st.session_state.time_left % 60

st.markdown(f"## ⏳ {st.session_state.mode} - {mins:02d}:{secs:02d}")

# ----------------------------
# TIMER LOGIC
# ----------------------------
if st.session_state.running and st.session_state.time_left > 0:
    time.sleep(1)
    st.session_state.time_left -= 1
    st.rerun()

# ----------------------------
# AUTO FINISH + POMODORO
# ----------------------------
if st.session_state.time_left == 0 and st.session_state.total_time > 0:

    st.success("🔔 Session Complete!")

    subj = st.session_state.subject

    if subj:
        data["records"].setdefault(subj, [])
        data["records"][subj].append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "duration": st.session_state.total_time
        })

        data["streak"][today] = data["streak"].get(today, 0) + 1
        save_data(data)

    # 🍅 Pomodoro switch
    if st.session_state.pomodoro:
        if st.session_state.mode == "Focus":
            st.session_state.mode = "Break"
            st.session_state.time_left = break_min * 60
            st.session_state.total_time = break_min * 60
            st.session_state.running = True
        else:
            st.session_state.mode = "Focus"
            st.session_state.time_left = minutes * 60
            st.session_state.total_time = minutes * 60
            st.session_state.running = True
    else:
        st.session_state.running = False

# ----------------------------
# HISTORY
# ----------------------------
st.subheader("📊 Study History")

for subj, sessions in data["records"].items():
    st.markdown(f"### {subj}")

    total = 0

    for s in sessions:
        st.write(f"🕒 {s['time']} — {s['duration']} sec")
        total += s["duration"]

    st.write(f"**Total: {total//60} min {total%60} sec**")
    st.markdown("---")

# ----------------------------
# STREAK
# ----------------------------
st.subheader("🔥 Streak Today")
st.write(data["streak"].get(today, 0), "sessions")