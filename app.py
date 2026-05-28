import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json
import os
import time
import hashlib
from datetime import datetime, date

# =====================================================
# 📋 PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Smart Study System",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# 🎨 STYLING
# =====================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

h1, h2 {
    color: #667eea;
    text-align: center;
}

.stTabs [data-baseweb="tab-list"] button {
    font-size: 18px;
}

.timer-display {
    text-align: center;
    font-size: 64px;
    font-weight: bold;
    padding: 20px;
    background: #f0f4ff;
    border-radius: 20px;
    margin: 20px 0;
}

.card-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.success-box {
    background: #d4edda;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.error-box {
    background: #f8d7da;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 40px;
    background: white;
    border-radius: 20px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 👤 AUTHENTICATION SYSTEM
# =====================================================
USERS_FILE = "users.json"

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load user credentials"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_users(users):
    """Save user credentials"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Register new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = hash_password(password)
    save_users(users)
    return True, "Registration successful!"

def authenticate_user(username, password):
    """Authenticate user"""
    users = load_users()
    if username not in users:
        return False, "Username not found"
    if users[username] != hash_password(password):
        return False, "Incorrect password"
    return True, "Login successful!"

def get_user_data_path(username, file_type):
    """Get user-specific file path"""
    user_folder = f"user_data/{username}"
    os.makedirs(user_folder, exist_ok=True)
    
    if file_type == "db":
        return f"{user_folder}/tasks.db"
    elif file_type == "study":
        return f"{user_folder}/study_data.json"
    elif file_type == "progress":
        return f"{user_folder}/progress.json"
    
    return user_folder

# =====================================================
# 🔐 SESSION STATE FOR LOGIN
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# =====================================================
# 📝 LOGIN PAGE
# =====================================================
if not st.session_state.logged_in:
    st.title("🔐 Smart Study System - Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        # Tab for Login/Register
        tab1, tab2 = st.tabs(["🔓 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Welcome Back!")
            
            login_username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                if not login_username or not login_password:
                    st.error("❌ Please enter both username and password")
                else:
                    success, message = authenticate_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        with tab2:
            st.subheader("Create New Account")
            
            reg_username = st.text_input("Choose Username", key="reg_username", placeholder="Create a username")
            reg_password = st.text_input("Choose Password", type="password", key="reg_password", placeholder="Create a password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
            
            if st.button("📝 Register", use_container_width=True, key="register_btn"):
                if not reg_username or not reg_password or not reg_confirm:
                    st.error("❌ Please fill all fields")
                elif reg_password != reg_confirm:
                    st.error("❌ Passwords do not match")
                elif len(reg_password) < 4:
                    st.error("❌ Password must be at least 4 characters")
                else:
                    success, message = register_user(reg_username, reg_password)
                    if success:
                        st.success(f"✅ {message} You can now login!")
                    else:
                        st.error(f"❌ {message}")
        
        st.markdown("---")
        st.info("💡 Your data will be saved securely and only accessible with your login credentials.")

else:
    # =====================================================
    # 💾 DATABASE FUNCTIONS (USER-SPECIFIC)
    # =====================================================
    username = st.session_state.username
    db_path = get_user_data_path(username, "db")
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT, status TEXT, due_date DATE)')
        conn.commit()

    def add_data(task, status, due_date):
        c.execute('INSERT INTO taskstable(task, status, due_date) VALUES (?, ?, ?)', (task, status, due_date))
        conn.commit()

    def view_all_data():
        c.execute('SELECT * FROM taskstable')
        return c.fetchall()

    def view_unique_task():
        c.execute('SELECT DISTINCT task FROM taskstable')
        return c.fetchall()

    def get_task(task):
        c.execute('SELECT * FROM taskstable WHERE task=?', (task,))
        return c.fetchall()

    def edit_task(new_task, new_status, new_due_date, old_task):
        c.execute('UPDATE taskstable SET task=?, status=?, due_date=? WHERE task=?',
                  (new_task, new_status, new_due_date, old_task))
        conn.commit()

    def delete_data(task):
        c.execute('DELETE FROM taskstable WHERE task=?', (task,))
        conn.commit()

    # =====================================================
    # 📁 DATA FILES (USER-SPECIFIC)
    # =====================================================
    study_data_path = get_user_data_path(username, "study")
    progress_path = get_user_data_path(username, "progress")

    def load_study_data():
        if os.path.exists(study_data_path):
            try:
                with open(study_data_path, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"records": {}, "streak": {}, "last_date": None}

    def save_study_data(data):
        with open(study_data_path, "w") as f:
            json.dump(data, f)

    def load_progress():
        if os.path.exists(progress_path):
            try:
                with open(progress_path, "r") as f:
                    return json.load(f)
            except:
                pass
        return None

    def save_progress():
        try:
            data = {
                "flash_index": st.session_state.get("flash_index", 0),
                "mcq_index": st.session_state.get("mcq_index", 0),
                "learning_mode": st.session_state.get("learning_mode", "flashcards"),
                "learning_subject": st.session_state.get("learning_subject", "Biology")
            }
            with open(progress_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            st.error(f"Save failed: {e}")

    # =====================================================
    # 📇 FLASHCARDS & MCQ DATA
    # =====================================================
    FLASHCARDS = {
        "Biology": [
            {"q": "What is ATP?", "a": "Energy currency of cells"},
            {"q": "What is DNA?", "a": "Genetic material"},
            {"q": "What is osmosis?", "a": "Movement of water through membrane"},
        ],
        "Chemistry": [
            {"q": "What is ionic bond?", "a": "Transfer of electrons"},
            {"q": "What is covalent bond?", "a": "Sharing electrons"},
            {"q": "What is an atom?", "a": "Smallest unit of element"},
        ],
        "Physics": [
            {"q": "What is force unit?", "a": "Newton"},
            {"q": "Formula for speed?", "a": "Distance ÷ Time"},
            {"q": "What is energy?", "a": "Ability to do work"},
        ],
        "Math": [
            {"q": "Derivative of x²?", "a": "2x"},
            {"q": "Area of square?", "a": "side²"},
            {"q": "What is π?", "a": "3.14159"},
        ],
        "English": [
            {"q": "What is a noun?", "a": "Person, place or thing"},
            {"q": "What is a verb?", "a": "Action word"},
            {"q": "What is an adjective?", "a": "Describes noun"},
        ],
        "Geography": [
            {"q": "Capital of Malaysia?", "a": "Kuala Lumpur"},
            {"q": "Largest ocean?", "a": "Pacific Ocean"},
            {"q": "Continent of Malaysia?", "a": "Asia"},
        ]
    }

    MCQ_BANK = {
        "Biology": [
            {
                "q": "Why do mitochondria have folded membranes?",
                "options": ["More ATP production", "Less respiration", "Store water", "Protect DNA"],
                "a": "More ATP production"
            },
            {
                "q": "Enzyme specificity means?",
                "options": ["Random reaction", "Shape match", "No function", "Cell destruction"],
                "a": "Shape match"
            },
            {
                "q": "Osmosis involves movement of?",
                "options": ["Protein", "Water", "Salt", "DNA"],
                "a": "Water"
            }
        ],
        "Chemistry": [
            {
                "q": "NaCl forms through?",
                "options": ["Electron transfer", "Electron sharing", "Hydrogen bonding", "Magnetism"],
                "a": "Electron transfer"
            },
            {
                "q": "Bond energy depends on?",
                "options": ["Color", "Attraction strength", "Mass only", "Temperature only"],
                "a": "Attraction strength"
            },
            {
                "q": "Covalent bond means?",
                "options": ["Sharing electrons", "Transfer electrons", "No electrons", "Heat transfer"],
                "a": "Sharing electrons"
            }
        ],
        "Physics": [
            {
                "q": "Why does friction produce heat?",
                "options": ["Energy conversion", "Gravity", "Light reflection", "Air pressure"],
                "a": "Energy conversion"
            },
            {
                "q": "Objects fall because of?",
                "options": ["Wind", "Gravity", "Friction", "Temperature"],
                "a": "Gravity"
            },
            {
                "q": "SI unit of force?",
                "options": ["Newton", "Joule", "Pascal", "Watt"],
                "a": "Newton"
            }
        ],
        "Math": [
            {
                "q": "Derivative represents?",
                "options": ["Slope", "Area", "Volume", "Mass"],
                "a": "Slope"
            },
            {
                "q": "Integral represents?",
                "options": ["Area under curve", "Slope", "Distance only", "Temperature"],
                "a": "Area under curve"
            },
            {
                "q": "What is 5²?",
                "options": ["10", "15", "20", "25"],
                "a": "25"
            }
        ],
        "English": [
            {
                "q": "A thesis statement is?",
                "options": ["Main argument", "Random word", "A verb", "Punctuation"],
                "a": "Main argument"
            },
            {
                "q": "Metaphor is a?",
                "options": ["Comparison", "Question", "Verb", "Noun"],
                "a": "Comparison"
            },
            {
                "q": "Adjective describes a?",
                "options": ["Noun", "Verb", "Sentence", "Paragraph"],
                "a": "Noun"
            }
        ],
        "Geography": [
            {
                "q": "Earthquakes caused by?",
                "options": ["Plate movement", "Rain", "Wind", "Moonlight"],
                "a": "Plate movement"
            },
            {
                "q": "Equator is hotter because?",
                "options": ["Direct sunlight", "Wind", "Rain", "Clouds"],
                "a": "Direct sunlight"
            },
            {
                "q": "Largest ocean?",
                "options": ["Indian", "Atlantic", "Pacific", "Arctic"],
                "a": "Pacific"
            }
        ]
    }

    # =====================================================
    # 🧠 SESSION STATE INITIALIZATION
    # =====================================================
    defaults = {
        "page": "Home",
        "running": False,
        "time_left": 0,
        "total_time": 0,
        "timer_mode": "Focus",
        "pomodoro": False,
        "timer_subject": None,
        "flash_index": 0,
        "mcq_index": 0,
        "learning_mode": "flashcards",
        "learning_subject": "Biology"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Load saved progress
    saved_progress = load_progress()
    if saved_progress:
        st.session_state.flash_index = saved_progress.get("flash_index", 0)
        st.session_state.mcq_index = saved_progress.get("mcq_index", 0)
        st.session_state.learning_mode = saved_progress.get("learning_mode", "flashcards")
        st.session_state.learning_subject = saved_progress.get("learning_subject", "Biology")

    # =====================================================
    # 📊 SIDEBAR NAVIGATION & LOGOUT
    # =====================================================
    st.sidebar.title(f"📚 {username}'s Study System")
    
    # User info
    st.sidebar.markdown(f"**👤 Logged in as:** `{username}`")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Page:",
        ["📝 Tasks", "⏱️ Timer", "🧠 Learning"]
    )
    st.session_state.page = page

    # =====================================================
    # 📝 TASKS PAGE
    # =====================================================
    if page == "📝 Tasks":
        st.title("📝 Task Management")
        
        create_table()
        
        task_menu = st.sidebar.selectbox("Task Menu", ["Add", "View", "Edit", "Delete"])
        
        if task_menu == "Add":
            st.subheader("Add a New Task")
            
            col1, col2 = st.columns(2)
            
            with col1:
                task = st.text_area("Task Description", height=100)
            
            with col2:
                status = st.selectbox("Status", ["To Do", "In Progress", "Complete"])
                due_date = st.date_input("Due Date")
            
            if st.button("➕ Add Task", key="add_btn"):
                if task.strip() == "":
                    st.error("❌ Task cannot be empty!")
                else:
                    add_data(task, status, due_date)
                    st.success(f"✅ Successfully added task: {task}")
        
        elif task_menu == "View":
            st.subheader("View All Tasks")
            
            result = view_all_data()
            
            if result:
                df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
                st.dataframe(df, use_container_width=True)
                
                with st.expander("📊 Task Status Summary"):
                    status_counts = df['Status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'Count']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.dataframe(status_counts, use_container_width=True)
                    
                    with col2:
                        fig = px.pie(status_counts, names='Status', values='Count', title='Task Distribution')
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ No tasks yet. Add one to get started!")
        
        elif task_menu == "Edit":
            st.subheader("Edit Your Tasks")
            
            list_of_tasks = [i[0] for i in view_unique_task()]
            
            if list_of_tasks:
                selected_task = st.selectbox("Select Task to Edit", list_of_tasks)
                selected_result = get_task(selected_task)
                
                if selected_result:
                    task = selected_result[0][0]
                    status = selected_result[0][1]
                    due_date = selected_result[0][2]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_task = st.text_area("Task Description", task, height=100)
                    
                    with col2:
                        new_status = st.selectbox(
                            "Status",
                            ["To Do", "In Progress", "Complete"],
                            index=["To Do", "In Progress", "Complete"].index(status)
                        )
                        new_due_date = st.date_input("Due Date", due_date)
                    
                    if st.button("💾 Update Task"):
                        edit_task(new_task, new_status, new_due_date, task)
                        st.success(f"✅ Updated: {task} → {new_task}")
            else:
                st.info("ℹ️ No tasks to edit yet!")
        
        elif task_menu == "Delete":
            st.subheader("Delete a Task")
            
            list_of_tasks = [i[0] for i in view_unique_task()]
            
            if list_of_tasks:
                selected_task = st.selectbox("Select Task to Delete", list_of_tasks)
                st.warning(f"⚠️ Are you sure you want to delete '{selected_task}'?")
                
                if st.button("🗑️ Delete Task"):
                    delete_data(selected_task)
                    st.success(f"✅ Task '{selected_task}' has been deleted!")
            else:
                st.info("ℹ️ No tasks to delete yet!")

    # =====================================================
    # ⏱️ TIMER PAGE
    # =====================================================
    elif page == "⏱️ Timer":
        st.title("⏱️ Smart Study Timer")
        
        study_data = load_study_data()
        today = str(date.today())
        
        if study_data["last_date"] != today:
            study_data["streak"] = {today: 0}
            study_data["last_date"] = today
            save_study_data(study_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📅 Today's Sessions", study_data["streak"].get(today, 0))
        
        with col2:
            total_minutes = sum(
                sum(s.get("duration", 0) for s in sessions) 
                for sessions in study_data["records"].values()
            ) // 60
            st.metric("⏰ Total Minutes", total_minutes)
        
        with col3:
            st.metric("📚 Subjects Studied", len(study_data["records"]))
        
        st.markdown("---")
        
        subjects = ["Math", "Chemistry", "Physics", "Biology", "English", "Computer Science"]
        
        col_subj, col_min, col_break = st.columns(3)
        
        with col_subj:
            subject = st.selectbox("📖 Select Subject", subjects)
        
        with col_min:
            minutes = st.number_input("⏳ Focus Time (minutes)", min_value=1, max_value=180, value=25)
        
        with col_break:
            break_min = st.number_input("☕ Break Time (minutes)", min_value=1, max_value=60, value=5)
        
        pomodoro = st.toggle("🍅 Enable Pomodoro Mode")
        st.session_state.pomodoro = pomodoro
        
        # Timer Display
        timer_placeholder = st.empty()
        
        col_start, col_pause, col_stop = st.columns(3)
        
        with col_start:
            if st.button("▶ Start Timer"):
                st.session_state.running = True
                st.session_state.timer_subject = subject
                
                if st.session_state.time_left == 0:
                    st.session_state.timer_mode = "Focus"
                    st.session_state.time_left = minutes * 60
                    st.session_state.total_time = minutes * 60
        
        with col_pause:
            if st.button("⏸ Pause"):
                st.session_state.running = False
        
        with col_stop:
            if st.button("⏹ Stop"):
                if st.session_state.total_time > 0 and st.session_state.timer_subject:
                    elapsed = st.session_state.total_time - st.session_state.time_left
                    
                    if elapsed > 0:
                        study_data["records"].setdefault(st.session_state.timer_subject, [])
                        study_data["records"][st.session_state.timer_subject].append({
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "duration": elapsed
                        })
                        study_data["streak"][today] = study_data["streak"].get(today, 0) + 1
                        save_study_data(study_data)
                        
                        st.success(f"✅ Session saved! ({elapsed//60}m {elapsed%60}s)")
                
                st.session_state.running = False
                st.session_state.time_left = 0
        
        # Display Timer
        if st.session_state.running:
            while st.session_state.running and st.session_state.time_left > 0:
                mins, secs = divmod(st.session_state.time_left, 60)
                
                with timer_placeholder.container():
                    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", 
                               unsafe_allow_html=True)
                
                time.sleep(1)
                st.session_state.time_left -= 1
                st.rerun()
        else:
            mins, secs = divmod(st.session_state.time_left if st.session_state.time_left > 0 else 0, 60)
            with timer_placeholder.container():
                st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", 
                           unsafe_allow_html=True)
        
        # Study History
        with st.expander("📊 Study History"):
            if study_data["records"]:
                history_data = []
                for subj, sessions in study_data["records"].items():
                    total_secs = sum(s.get("duration", 0) for s in sessions)
                    history_data.append({
                        "Subject": subj,
                        "Sessions": len(sessions),
                        "Total Time": f"{total_secs//60}m {total_secs%60}s"
                    })
                
                hist_df = pd.DataFrame(history_data)
                st.dataframe(hist_df, use_container_width=True)
            else:
                st.info("ℹ️ No study sessions yet!")

    # =====================================================
    # 🧠 LEARNING PAGE
    # =====================================================
    elif page == "🧠 Learning":
        st.title("🧠 Smart Learning Center")
        
        # Learning subject selector
        learning_subject = st.selectbox(
            "Choose Subject",
            list(FLASHCARDS.keys()),
            index=list(FLASHCARDS.keys()).index(st.session_state.learning_subject)
        )
        
        if learning_subject != st.session_state.learning_subject:
            st.session_state.learning_subject = learning_subject
            st.session_state.flash_index = 0
            st.session_state.mcq_index = 0
            st.session_state.learning_mode = "flashcards"
        
        # Mode selector
        learning_mode = st.radio(
            "Choose Mode",
            ["📇 Flashcards", "🧪 MCQ Test"],
            horizontal=True
        )
        
        if learning_mode == "📇 Flashcards":
            st.session_state.learning_mode = "flashcards"
        else:
            st.session_state.learning_mode = "mcq"
        
        # =====================================================
        # FLASHCARDS MODE
        # =====================================================
        if st.session_state.learning_mode == "flashcards":
            st.subheader("📇 Flashcards Revision")
            
            cards = FLASHCARDS[learning_subject]
            
            if st.session_state.flash_index >= len(cards):
                st.success("🎉 Flashcards Completed! Great job!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Restart Flashcards"):
                        st.session_state.flash_index = 0
                        save_progress()
                with col2:
                    if st.button("📝 Go To MCQ Test"):
                        st.session_state.learning_mode = "mcq"
                        save_progress()
            else:
                card = cards[st.session_state.flash_index]
                
                # Progress
                st.progress(
                    (st.session_state.flash_index + 1) / len(cards),
                    text=f"Card {st.session_state.flash_index + 1} of {len(cards)}"
                )
                
                # Question
                st.markdown("### ❓ Question")
                st.write(f"**{card['q']}**")
                
                # Answer
                col_ans = st.columns(1)[0]
                with col_ans:
                    st.markdown(f"### ✅ Answer")
                    st.success(f"**{card['a']}**")
                
                # Navigation
                col_prev, col_next = st.columns(2)
                
                with col_prev:
                    if st.button("⬅️ Previous Card"):
                        if st.session_state.flash_index > 0:
                            st.session_state.flash_index -= 1
                            save_progress()
                            st.rerun()
                
                with col_next:
                    if st.button("Next Card ➡️"):
                        st.session_state.flash_index += 1
                        save_progress()
                        st.rerun()
        
        # =====================================================
        # MCQ MODE
        # =====================================================
        else:
            st.subheader("🧪 Hard MCQ Test")
            
            mcqs = MCQ_BANK[learning_subject]
            
            if st.session_state.mcq_index >= len(mcqs):
                st.success("🎉 MCQ Test Completed! Excellent work!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Restart MCQ"):
                        st.session_state.mcq_index = 0
                        save_progress()
                        st.rerun()
                with col2:
                    if st.button("📇 Go To Flashcards"):
                        st.session_state.learning_mode = "flashcards"
                        save_progress()
            else:
                q = mcqs[st.session_state.mcq_index]
                
                # Progress
                st.progress(
                    (st.session_state.mcq_index + 1) / len(mcqs),
                    text=f"Question {st.session_state.mcq_index + 1} of {len(mcqs)}"
                )
                
                # Question
                st.markdown("### ❓ Question")
                st.write(f"**{q['q']}**")
                
                # Options
                choice = st.radio(
                    "Select your answer:",
                    q['options'],
                    key=f"mcq_{st.session_state.mcq_index}",
                    index=None
                )
                
                # Submit
                col_submit, col_empty = st.columns([1, 3])
                with col_submit:
                    if st.button("Submit Answer"):
                        if choice is None:
                            st.warning("⚠️ Please select an answer!")
                        elif choice == q['a']:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Wrong! Correct Answer: {q['a']}")
                
                # Navigation
                col_prev, col_next = st.columns(2)
                
                with col_prev:
                    if st.button("⬅️ Previous Question"):
                        if st.session_state.mcq_index > 0:
                            st.session_state.mcq_index -= 1
                            save_progress()
                            st.rerun()
                
                with col_next:
                    if st.button("Next Question ➡️"):
                        st.session_state.mcq_index += 1
                        save_progress()
                        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("📚 Smart Study System v2.0\nMulti-user with personalized history!")
