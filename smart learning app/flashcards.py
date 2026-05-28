import streamlit as st
import json
import os

# =====================================================
# 💾 SAVE SYSTEM
# =====================================================

SAVE_FILE = "progress.json"

def save_data():
    try:
        data = {
            "flash_index": st.session_state.flash_index,
            "mcq_index": st.session_state.mcq_index,
            "mode": st.session_state.mode,
            "subject": st.session_state.subject
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        st.error(f"Save failed: {e}")

def load_data():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return None

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
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.block-container {
    background-color: rgba(255,255,255,0.94);
    padding: 2rem;
    border-radius: 16px;
}

h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: black !important;
}

div.stButton > button {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
    border: 1px solid #ccc;
    font-weight: bold;
}

.stRadio label {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 📇 FLASHCARDS
# =====================================================

flashcards = {

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

# =====================================================
# 🧪 HARD MCQ
# =====================================================

mcq_bank = {

    "Biology": [
        {
            "q": "Why do mitochondria have folded membranes?",
            "options": [
                "More ATP production",
                "Less respiration",
                "Store water",
                "Protect DNA"
            ],
            "a": "More ATP production"
        },
        {
            "q": "Enzyme specificity means?",
            "options": [
                "Random reaction",
                "Shape match",
                "No function",
                "Cell destruction"
            ],
            "a": "Shape match"
        },
        {
            "q": "Osmosis involves movement of?",
            "options": [
                "Protein",
                "Water",
                "Salt",
                "DNA"
            ],
            "a": "Water"
        }
    ],

    "Chemistry": [
        {
            "q": "NaCl forms through?",
            "options": [
                "Electron transfer",
                "Electron sharing",
                "Hydrogen bonding",
                "Magnetism"
            ],
            "a": "Electron transfer"
        },
        {
            "q": "Bond energy depends on?",
            "options": [
                "Color",
                "Attraction strength",
                "Mass only",
                "Temperature only"
            ],
            "a": "Attraction strength"
        },
        {
            "q": "Covalent bond means?",
            "options": [
                "Sharing electrons",
                "Transfer electrons",
                "No electrons",
                "Heat transfer"
            ],
            "a": "Sharing electrons"
        }
    ],

    "Physics": [
        {
            "q": "Why does friction produce heat?",
            "options": [
                "Energy conversion",
                "Gravity",
                "Light reflection",
                "Air pressure"
            ],
            "a": "Energy conversion"
        },
        {
            "q": "Objects fall because of?",
            "options": [
                "Wind",
                "Gravity",
                "Friction",
                "Temperature"
            ],
            "a": "Gravity"
        },
        {
            "q": "SI unit of force?",
            "options": [
                "Newton",
                "Joule",
                "Pascal",
                "Watt"
            ],
            "a": "Newton"
        }
    ],

    "Math": [
        {
            "q": "Derivative represents?",
            "options": [
                "Slope",
                "Area",
                "Volume",
                "Mass"
            ],
            "a": "Slope"
        },
        {
            "q": "Integral represents?",
            "options": [
                "Area under curve",
                "Slope",
                "Distance only",
                "Temperature"
            ],
            "a": "Area under curve"
        },
        {
            "q": "What is 5²?",
            "options": [
                "10",
                "15",
                "20",
                "25"
            ],
            "a": "25"
        }
    ],

    "English": [
        {
            "q": "A thesis statement is?",
            "options": [
                "Main argument",
                "Random word",
                "A verb",
                "Punctuation"
            ],
            "a": "Main argument"
        },
        {
            "q": "Metaphor is a?",
            "options": [
                "Comparison",
                "Question",
                "Verb",
                "Noun"
            ],
            "a": "Comparison"
        },
        {
            "q": "Adjective describes a?",
            "options": [
                "Noun",
                "Verb",
                "Sentence",
                "Paragraph"
            ],
            "a": "Noun"
        }
    ],

    "Geography": [
        {
            "q": "Earthquakes caused by?",
            "options": [
                "Plate movement",
                "Rain",
                "Wind",
                "Moonlight"
            ],
            "a": "Plate movement"
        },
        {
            "q": "Equator is hotter because?",
            "options": [
                "Direct sunlight",
                "Wind",
                "Rain",
                "Clouds"
            ],
            "a": "Direct sunlight"
        },
        {
            "q": "Largest ocean?",
            "options": [
                "Indian",
                "Atlantic",
                "Pacific",
                "Arctic"
            ],
            "a": "Pacific"
        }
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

# =====================================================
# 📂 LOAD SAVE
# =====================================================

saved = load_data()

if saved:
    st.session_state.flash_index = saved.get("flash_index", 0)
    st.session_state.mcq_index = saved.get("mcq_index", 0)
    st.session_state.mode = saved.get("mode", "flashcards")
    st.session_state.subject = saved.get("subject", "Biology")

# =====================================================
# 🧠 TITLE
# =====================================================

st.title("🧠 SmartLearners")

subject = st.selectbox(
    "Choose Subject",
    list(flashcards.keys())
)

# =====================================================
# 🔄 RESET WHEN SUBJECT CHANGES
# =====================================================

if subject != st.session_state.subject:
    st.session_state.subject = subject
    st.session_state.flash_index = 0
    st.session_state.mcq_index = 0
    st.session_state.mode = "flashcards"

# =====================================================
# 🎛️ MODE SELECTOR
# =====================================================

mode = st.radio(
    "Choose Mode",
    ["📇 Flashcards", "🧪 MCQ Test"],
    horizontal=True
)

if mode == "📇 Flashcards":
    st.session_state.mode = "flashcards"
else:
    st.session_state.mode = "mcq"

# =====================================================
# 📇 FLASHCARDS MODE
# =====================================================

if st.session_state.mode == "flashcards":

    cards = flashcards[subject]

    if st.session_state.flash_index >= len(cards):
        st.success("🎉 Flashcards Completed!")

        if st.button("Go To MCQ Test"):
            st.session_state.mode = "mcq"

    else:

        card = cards[st.session_state.flash_index]

        st.subheader("📇 Flashcards Revision")

        st.write(
            f"Card {st.session_state.flash_index + 1} / {len(cards)}"
        )

        st.write("### Question")
        st.write(card["q"])

        st.success(card["a"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Previous"):
                if st.session_state.flash_index > 0:
                    st.session_state.flash_index -= 1
                    save_data()

        with col2:
            if st.button("Next ➡"):
                st.session_state.flash_index += 1
                save_data()

# =====================================================
# 🧪 MCQ MODE
# =====================================================

else:

    mcqs = mcq_bank[subject]

    if st.session_state.mcq_index >= len(mcqs):

        st.success("🎉 MCQ Completed!")

        if st.button("Restart MCQ"):
            st.session_state.mcq_index = 0
            save_data()

    else:

        q = mcqs[st.session_state.mcq_index]

        st.subheader("🧪 Hard MCQ Test")

        st.write(
            f"Question {st.session_state.mcq_index + 1} / {len(mcqs)}"
        )

        choice = st.radio(
            q["q"],
            q["options"],
            key=f"mcq_{st.session_state.mcq_index}"
        )

        if st.button("Submit Answer"):

            if choice == q["a"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Correct Answer: {q['a']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Previous MCQ"):
                if st.session_state.mcq_index > 0:
                    st.session_state.mcq_index -= 1
                    save_data()

        with col2:
            if st.button("Next MCQ ➡"):
                st.session_state.mcq_index += 1
                save_data()

# =====================================================
# 💾 AUTO SAVE
# =====================================================

save_data()
