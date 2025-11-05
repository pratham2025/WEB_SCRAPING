# 📢 GETNOTIFY — Real-time Educational Notifications Platform

🚀 **Instant Exam Alerts, Smart Scraping, and Beautiful UI for Students Across India**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)  
![Supabase](https://img.shields.io/badge/Supabase-Cloud%20Database-3ECF8E)  
![HTML5](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)  
![Python](https://img.shields.io/badge/Python-3.10+-yellow)  
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED)

---

## 🔎 Overview
**GETNOTIFY** is a next-generation platform that delivers **real-time educational notifications** from official sources such as **NTA, CBSE, NEET, JEE, UPSC, ISRO, and more**.  
It combines a **FastAPI backend**, **Supabase database**, and a **modern glass-inspired web UI** to help students stay updated with the latest exam news, results, admit cards, and syllabus updates.

---

## 🧠 Core Features
- ⚡ **Real-time Web Scraping** using FastAPI microservices
- 🧩 **Dynamic Frontend** (modular HTML injection: header/footer/components)
- 🗂️ **Beautiful Notice Board UI** with animations & pinned notices
- 🔔 **Google Login Integration** via Google Identity Services
- 🗄️ **Supabase Cloud Storage** for announcements and user data
- 📈 **Responsive Design** optimized for desktop and mobile
- 🧠 **Smart Sorting & Filtering** (latest first, categorized by source)
- 🧰 **Modular Code Structure** (common.js, app.js, home.js)

---

## 🏗️ Architecture

```
Frontend (HTML + JS + CSS)
   ├── Dynamic UI (home.html, index.html, syllabus.html)
   ├── Header/Footer Injection (common.js)
   └── Notice Board Animations (home.js)

Backend (FastAPI)
   ├── /sources              → List of all educational boards
   ├── /announcements/{src}  → Announcements by source
   └── /latest-news          → Latest news for homepage

Database (Supabase / PostgreSQL)
   ├── Sources Table
   └── Announcements Table
```

---

## 🧩 Project Structure
```
GETNOTIFY/
│
├── frontend/
│   ├── index.html              # Notifications page
│   ├── home.html               # Homepage with notice board
│   ├── syllabus.html           # Coming soon section
│   ├── styles.css              # Full responsive styling
│   ├── common.js               # Header/Footer injection
│   ├── app.js                  # Source + announcement logic
│   ├── home.js                 # Notice board logic
│   └── _header.html / _footer.html
│
├── backend/
│   ├── scraper_api.py          # FastAPI microservice
│   ├── utils/                  # Scraping + formatting utilities
│   └── requirements.txt
│
├── secrets.js                  # Supabase anon key
└── README.md                   # Documentation
```

---

## 💡 Frontend Highlights
- 🌟 **Home Page**: Animated hero, feature cards, and notice board
- 📰 **Latest News Board**: Pinned paper-style cards with NEW badge & animations
- 📱 **Responsive Design**: Works beautifully on mobile and desktop
- 💬 **Notifications**: Dynamic alerts for API errors/success
- ⚙️ **Header & Footer Injection**: Consistent layout across pages

---

## ⚙️ Backend Highlights
- 🧠 **FastAPI REST Endpoints** for announcements and sources
- 🌐 **Supabase Integration** for data storage and retrieval
- 🪶 **CORS Enabled** for frontend communication
- 🕵️ **Reversed Order Logic** ensures newest announcements show first
- 🧩 **JSON Response Format**: clean data for easy parsing by frontend

---

## 🧾 API Endpoints
| Endpoint | Description |
|-----------|-------------|
| `/sources` | Returns all available exam boards |
| `/announcements/{source}` | Returns announcements by source |
| `/latest-news` | Returns latest educational updates |

**Example Response:**
```json
{
  "news": [
    {
      "headline": "JEE Main 2025 Registration Begins",
      "article_link": "https://jeemain.nta.ac.in",
      "article_date": "2025-11-05"
    }
  ]
}
```

---

## 🖥️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/pratham2025/GETNOTIFY.git
cd GETNOTIFY
```

### 2️⃣ Setup Python Environment
```bash
pip install -r requirements.txt
```

### 3️⃣ Run FastAPI Backend
```bash
uvicorn scraper_api:app --reload --host 127.0.0.1 --port 8000
```

### 4️⃣ Launch Frontend
Simply open `frontend/home.html` or `frontend/index.html` in your browser.

---

## 🧰 Optional: Docker Setup
```bash
docker build -t getnotify .
docker run -p 8000:8000 --network host getnotify
```

---

## 🧩 Supabase Configuration
```javascript
// secrets.js
window.SUPABASE = {
  url: "https://your-project-id.supabase.co",
  anonKey: "YOUR_ANON_KEY"
}
```
Use the **Anon Public Key** only (never expose service key).

---

## 📱 Future Enhancements
- 🤖 AI-based summarization of announcements
- 📅 Personalized dashboard for followed sources
- 📤 Email & push notifications for updates
- 🌗 Dark mode toggle with persistent preference
- 📊 Analytics dashboard (top sources, most active boards)

---

## 🧑‍💻 Author
**Developed by:** [Pratham Patil (Bosco)](https://github.com/pratham2025)  
**Role:** Full Stack Developer & Data Engineer  
**Project:** Educational Notification & Scraping System  
**Tech Stack:** FastAPI · Supabase · HTML/CSS/JS · Docker · PostgreSQL

---

## 📜 License
This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

### ⭐ Star this repo if you like the project!
> "Stay informed, stay ahead — with GETNOTIFY!"