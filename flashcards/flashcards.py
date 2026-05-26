import streamlit as st
import json
import os

# =====================================================
# 💾 SAVE SYSTEM
# =====================================================

SAVE_FILE = "progress.json"

def save_data():
    data = {
        "flash_index": st.session_state.flash_index,
        "mcq_index": st.session_state.mcq_index,
        "mode": st.session_state.mode,
        "subject": st.session_state.subject
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None

# =====================================================
# 🎨 STYLE
# =====================================================

st.markdown("""
<style>
.stApp {
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
* {
    color: black !important;
}
.block-container {
    background-color: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 12px;
}
div.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ccc;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 📇 FLASHCARDS (6 SUBJECTS)
# =====================================================

flashcards = {
    "Biology": [
        {"q": "What is ATP?", "a": "Energy currency of cells"},
        {"q": "What is DNA?", "a": "Genetic material"},
        {"q": "What is osmosis?", "a": "Water movement through membrane"},
    ],
    "Chemistry": [
        {"q": "What is ionic bond?", "a": "Transfer of electrons"},
        {"q": "What is covalent bond?", "a": "Sharing electrons"},
        {"q": "What is atom?", "a": "Smallest unit of element"},
    ],
    "Physics": [
        {"q": "Force unit?", "a": "Newton"},
        {"q": "Speed formula?", "a": "distance/time"},
        {"q": "Energy?", "a": "Ability to do work"},
    ],
    "Math": [
        {"q": "2 + 2?", "a": "4"},
        {"q": "Derivative of x²?", "a": "2x"},
        {"q": "Area of square?", "a": "side²"},
    ],
    "English": [
        {"q": "Noun?", "a": "Person/place/thing"},
        {"q": "Verb?", "a": "Action word"},
        {"q": "Adjective?", "a": "Describes noun"},
    ],
    "Geography": [
        {"q": "Capital of Malaysia?", "a": "Kuala Lumpur"},
        {"q": "Largest ocean?", "a": "Pacific"},
        {"q": "Continent of Malaysia?", "a": "Asia"},
    ]
}

# =====================================================
# 🧪 HARD MCQ (TEST MODE)
# =====================================================

mcq_bank = {
    "Biology": [
        {"q": "Why mitochondria have folds?", "options": ["More ATP", "Less DNA", "Faster transport", "Protection"], "a": "More ATP"},
        {"q": "Enzyme specificity means?", "options": ["Random reaction", "Shape match", "No function", "Break cells"], "a": "Shape match"},
    ],
    "Chemistry": [
        {"q": "Why is NaCl ionic?", "options": ["Electron transfer", "Sharing electrons", "No electrons", "Heat"], "a": "Electron transfer"},
        {"q": "Bond energy depends on?", "options": ["Attraction strength", "Color", "Size only", "Temperature"], "a": "Attraction strength"},
    ],
    "Physics": [
        {"q": "Why objects fall same rate?", "options": ["Gravity constant", "Mass difference", "Wind", "Friction"], "a": "Gravity constant"},
        {"q": "Friction produces heat because?", "options": ["Energy loss", "Mass gain", "Light", "Magnetism"], "a": "Energy loss"},
    ],
    "Math": [
        {"q": "Derivative shows?", "options": ["Slope", "Area", "Volume", "Distance"], "a": "Slope"},
        {"q": "Integral shows?", "options": ["Area under curve", "Slope", "Speed", "Force"], "a": "Area under curve"},
    ],
    "English": [
        {"q": "Thesis statement is?", "options": ["Main idea", "Random words", "Verb", "Grammar"], "a": "Main idea"},
        {"q": "Metaphor is?", "options": ["Comparison", "Definition", "Verb", "Noun"], "a": "Comparison"},
    ],
    "Geography": [
        {"q": "Earthquakes happen due to?", "options": ["Plate movement", "Rain", "Wind", "Heat"], "a": "Plate movement"},
        {"q": "Equator is hot because?", "options": ["Direct sunlight", "Cold air", "Distance", "Wind"], "a": "Direct sunlight"},
    ]
}

# =====================================================
# 🧠 SESSION STATE
# =====================================================

if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0
if "mcq_index" not in st.session_state:
    st.session_state.mcq_index = 0
if "mode" not in st.session_state:
    st.session_state.mode = "flashcards"
if "subject" not in st.session_state:
    st.session_state.subject = "Biology"

# LOAD SAVE FILE
saved = load_data()
if saved:
    st.session_state.flash_index = saved.get("flash_index", 0)
    st.session_state.mcq_index = saved.get("mcq_index", 0)
    st.session_state.mode = saved.get("mode", "flashcards")
    st.session_state.subject = saved.get("subject", "Biology")

# =====================================================
# TITLE & SUBJECT SELECTOR
# =====================================================

st.title("🧠 SmartLearners")
subject = st.selectbox("Choose Subject", list(flashcards.keys()), key="subject_select")

# RESET IF SUBJECT CHANGED
if subject != st.session_state.subject:
    st.session_state.subject = subject
    st.session_state.flash_index = 0
    st.session_state.mcq_index = 0

# =====================================================
# 🎛️ MODE SELECTOR
# =====================================================

mode_option = st.radio(
    "Select mode:",
    ["📇 Flashcards (Revision)", "🧪 MCQ (Test)"],
    index=0 if st.session_state.mode == "flashcards" else 1,
    horizontal=True,
    key="mode_select"
)
new_mode = "flashcards" if mode_option == "📇 Flashcards (Revision)" else "mcq"
if new_mode != st.session_state.mode:
    st.session_state.mode = new_mode

# =====================================================
# 🔧 CLAMP INDICES (allow sentinel value len() for completion)
# =====================================================

max_flash = len(flashcards[st.session_state.subject])
if st.session_state.flash_index < 0 or st.session_state.flash_index > max_flash:
    st.session_state.flash_index = 0

max_mcq = len(mcq_bank[st.session_state.subject])
if st.session_state.mcq_index < 0 or st.session_state.mcq_index > max_mcq:
    st.session_state.mcq_index = 0

# =====================================================
# 📇 FLASHCARDS MODE
# =====================================================

if st.session_state.mode == "flashcards":
    cards = flashcards[st.session_state.subject]

    if st.session_state.flash_index >= len(cards):
        st.info("🎉 You have completed all flashcards for this subject!")
        col1, col2 = st.columns(2)
        if col1.button("🔄 Restart Flashcards", key="restart_flash"):
            st.session_state.flash_index = 0
        if col2.button("🧪 Try MCQ Test", key="to_mcq_from_flash"):
            st.session_state.mode = "mcq"
    else:
        card = cards[st.session_state.flash_index]
        st.subheader("📇 Flashcards (Revision)")
        st.write(f"**Card {st.session_state.flash_index + 1} of {len(cards)}**")
        st.write(card["q"])
        st.success(card["a"])

        col1, col2 = st.columns(2)
        if col1.button("⬅ Previous", key="flash_prev"):
            if st.session_state.flash_index > 0:
                st.session_state.flash_index -= 1
        if col2.button("Next ➡", key="flash_next"):
            if st.session_state.flash_index + 1 < len(cards):
                st.session_state.flash_index += 1
            else:
                st.session_state.flash_index = len(cards)

# =====================================================
# 🧪 MCQ MODE
# =====================================================

else:  # mode == "mcq"
    mcqs = mcq_bank[st.session_state.subject]

    if st.session_state.mcq_index >= len(mcqs):
        st.success("🎉 You have completed all MCQs for this subject!")
        col1, col2 = st.columns(2)
        if col1.button("🔄 Restart MCQ", key="restart_mcq"):
            st.session_state.mcq_index = 0
        if col2.button("📇 Go to Flashcards", key="to_flash_from_mcq"):
            st.session_state.mode = "flashcards"
    else:
        q = mcqs[st.session_state.mcq_index]
        st.subheader("🧪 MCQ Test")
        st.write(f"**Question {st.session_state.mcq_index + 1} of {len(mcqs)}**")

        with st.form(key=f"mcq_form"):
            choice = st.radio(q["q"], q["options"], key="mcq_choice")
            submitted = st.form_submit_button("Submit")
            if submitted:
                if choice == q["a"]:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! Answer: {q['a']}")

        col1, col2 = st.columns(2)
        if col1.button("⬅ Previous MCQ", key="mcq_prev"):
            if st.session_state.mcq_index > 0:
                st.session_state.mcq_index -= 1
        if col2.button("Next MCQ ➡", key="mcq_next"):
            if st.session_state.mcq_index + 1 < len(mcqs):
                st.session_state.mcq_index += 1
            else:
                st.session_state.mcq_index = len(mcqs)

# =====================================================
# 💾 AUTO SAVE
# =====================================================

save_data()
