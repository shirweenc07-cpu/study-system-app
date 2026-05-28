# 🔐 Multi-User Login System Guide

## 🆕 What's New

Your Smart Study System now includes a **secure multi-user login system** that allows each user to have their own personalized study space with separate history!

---

## 🚀 Quick Start

### Running the App

```bash
streamlit run app.py
```

---

## 👤 Login Features

### 1️⃣ **Create Account (First Time)**
- Click the **"📝 Register"** tab
- Choose a **username** (can be any text)
- Enter a **password** (minimum 4 characters)
- Confirm your password
- Click **"📝 Register"**

### 2️⃣ **Login**
- Click the **"🔓 Login"** tab
- Enter your **username** and **password**
- Click **"🔓 Login"**

### 3️⃣ **Logout**
- In the sidebar, click **"🚪 Logout"**
- You'll be returned to the login page

---

## 📊 User-Specific Data

Each user's data is **completely separate and independent**:

```
user_data/
├── username1/
│   ├── tasks.db              # User 1's tasks
│   ├── study_data.json       # User 1's study sessions
│   └── progress.json         # User 1's learning progress
│
└── username2/
    ├── tasks.db              # User 2's tasks
    ├── study_data.json       # User 2's study sessions
    └── progress.json         # User 2's learning progress
```

### What's Saved Per User?

✅ **Tasks** - All task management data (add, edit, delete)  
✅ **Study History** - All timer sessions and streaks  
✅ **Learning Progress** - Flashcard & MCQ progress per subject  
✅ **Preferences** - Last studied subject and mode selection  

---

## 🔒 Security

- ✅ **Password Hashing** - Passwords are encrypted using SHA-256
- ✅ **Secure Storage** - Credentials stored in `users.json`
- ✅ **Data Privacy** - Each user can only access their own data
- ✅ **Session Management** - Auto-logout with page refresh

---

## 📁 File Structure

```
study-system-app/
├── app.py                    # Main app with login system
├── users.json               # User credentials (auto-created)
├── user_data/               # User-specific data folder
│   ├── alice/
│   └── bob/
├── requirements.txt
├── README_APP.md
└── QUICKSTART.md
```

---

## 🎯 Example Workflow

### User 1 (Alice)
1. Register with username: `alice`, password: `mypass123`
2. Add tasks, study math for 25 minutes
3. Complete flashcards
4. **Alice's data saved** in `user_data/alice/`

### User 2 (Bob)
1. Register with username: `bob`, password: `study2024`
2. Add different tasks, study physics
3. Bob **cannot see** Alice's tasks or study history
4. **Bob's data saved** in `user_data/bob/`

### Alice Returns
1. Login with: `alice` / `mypass123`
2. **All previous data restored** - tasks, study history, flashcard progress

---

## 🛡️ Important Notes

⚠️ **Backup Your Data** - Keep backups of the `user_data/` folder  
⚠️ **Don't Share Accounts** - Use unique usernames for each person  
⚠️ **Password Security** - Use strong passwords (more than 4 chars recommended)  
⚠️ **Clear Browser Cache** - If having login issues, clear cache  

---

## 🔑 Default Test Accounts

For testing purposes, you can create test accounts:

**Test Account 1**
- Username: `student1`
- Password: `test1234`

**Test Account 2**
- Username: `student2`
- Password: `pass5678`

---

## 🐛 Troubleshooting

### **"Username not found"**
→ Make sure you registered first or check spelling

### **"Incorrect password"**
→ Passwords are case-sensitive, check spelling

### **"Username already exists"**
→ Choose a different username when registering

### **Data not showing after login**
→ Log out and log back in, or refresh the page

### **Lost password**
→ Ask admin to check `users.json` or contact support

---

## 📈 Features Overview

| Feature | Available | User-Specific |
|---------|-----------|---|
| Tasks Management | ✅ | ✅ |
| Study Timer | ✅ | ✅ |
| Study History | ✅ | ✅ |
| Flashcards | ✅ | ✅ |
| MCQ Tests | ✅ | ✅ |
| Streaks Counter | ✅ | ✅ |
| Progress Tracking | ✅ | ✅ |

---

## 🚀 Next Steps

1. Run the app: `streamlit run app.py`
2. Register a new account
3. Start managing your study system!
4. Login as different users to see separate data

---

**Enjoy your personalized study experience!** 🎓✨
