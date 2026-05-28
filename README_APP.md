# 📚 Smart Study System - Unified App

A comprehensive Streamlit application that combines **Task Management**, **Study Timer**, and **Interactive Learning** tools in one place.

## 🚀 Features

### 📝 **Task Management**
- ✅ Add tasks with status and due dates
- 📊 View all tasks in a table format
- ✏️ Edit existing tasks
- 🗑️ Delete completed tasks
- 📈 Visual statistics with pie charts

### ⏱️ **Study Timer**
- ⏳ Customizable focus timer (1-180 minutes)
- ☕ Break timer (1-60 minutes)
- 🍅 Pomodoro technique support
- 📊 Study history and session tracking
- 🔥 Streak counter
- 📚 Subject-specific tracking

### 🧠 **Smart Learning**
- 📇 Interactive flashcards across multiple subjects
- 🧪 Hard MCQ tests with 4 options each
- 📚  6 subjects: Biology, Chemistry, Physics, Math, English, Geography
- 💾 Progress tracking and saving
- 🔄 Switchable between flashcards and MCQ modes

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone or navigate to the project:**
```bash
cd /workspaces/study-system-app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🎮 Running the App

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 📝 Tasks Page
1. **Add Task:** Enter task description, select status, and pick due date
2. **View Tasks:** See all tasks in a table with status distribution chart
3. **Edit Task:** Select and modify existing tasks
4. **Delete Task:** Remove completed or unwanted tasks

### ⏱️ Timer Page
1. Select a subject from the dropdown
2. Set focus time (default: 25 minutes)
3. Set break time (default: 5 minutes)
4. Toggle Pomodoro mode if desired
5. Click "▶ Start" to begin
6. Track your progress in the metrics display

### 🧠 Learning Page
1. **Select Subject:** Choose from 6 available subjects
2. **Choose Mode:**
   - 📇 **Flashcards:** Learn with interactive flashcards
   - 🧪 **MCQ Test:** Practice with multiple-choice questions
3. **Navigation:** Use Previous/Next buttons to navigate
4. **Progress:** Visual progress bar shows completion status

## 📊 Data Storage

- **Tasks:** SQLite database (`study_system.db`)
- **Study Records:** JSON file (`study_data.json`)
  - Study sessions
  - Time tracking
  - Subject-wise records
  - Daily streak
- **Learning Progress:** JSON file (`progress.json`)
  - Flashcard index
  - MCQ index
  - Current mode
  - Selected subject

## 🎯 Keyboard Shortcuts & Navigation

All navigation is done through:
- Sidebar menu for main pages (Tasks, Timer, Learning)
- In-page dropdowns and buttons for specific actions
- Radio buttons for mode selection

## 💡 Tips for Best Use

1. **Study Timer:** Use Pomodoro mode for optimal focus (25 min focus + 5 min break)
2. **Flashcards:** Review cards multiple times for better retention
3. **MCQ Tests:** After completing flashcards, test yourself with MCQ
4. **Task Management:** Set realistic due dates and track progress
5. **Subject Tracking:** Study different subjects to diversify learning

## 🔧 Configuration

All settings are stored automatically:
- Session states are preserved during use
- Progress is saved to JSON files
- Tasks are stored in the SQLite database

## 📝 File Structure

```
study-system-app/
├── app.py                    # Main unified app
├── requirements.txt          # Python dependencies
├── study_system.db          # SQLite database (auto-created)
├── study_data.json          # Study records (auto-created)
├── progress.json            # Learning progress (auto-created)
└── README.md                # This file
```

## 🐛 Troubleshooting

**Timer not running?**
- Make sure you've selected a subject and clicked "Start"
- Use "⏸ Pause" to pause and "▶ Start" to resume

**Progress not saving?**
- Check file permissions for the working directory
- Ensure JSON files aren't corrupted (manually reset by deleting them)

**Tasks not appearing?**
- Clear browser cache
- Restart the Streamlit app with `streamlit run app.py --logger.level=error`

## 🌟 Future Enhancements

- 📱 Mobile responsive design
- 🎨 Custom color themes
- 📤 Export study data
- 🤝 Multi-user support
- 🔊 Audio notifications
- 📈 Advanced analytics

## 📄 License

This project is open source and available for educational use.

## 👨‍💻 Author

Created as a comprehensive study management system combining essential learning tools.

---

**Happy Studying! 📚✨**
