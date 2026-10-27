<div align="center">

# 🎓 SnapClass
### Next-Gen AI-Powered Classroom Attendance System

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database%20%26%20Auth-3ECF8E.svg)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<br/>

**SnapClass** revolutionizes the traditional roll-call process by combining high-speed **Computer Vision Face Detection** and **Voice Biometric Embeddings**. With support for instant multi-student classroom scanning, QR-driven enrollment, and cross-platform synchronization, SnapClass turns 10 minutes of manual attendance into a few seconds.

</div>

---

## 🌟 Key Features

### 👨‍🏫 Teacher Portal
- **Dashboard & Course Management:** Create subjects, manage sections, and inspect student rosters in real-time.
- **📸 Multi-Face Photo Attendance:** Capture a single room photo; the AI pipeline extracts all facial embeddings, classifies students, and logs attendance records with confidence scores.
- **🎙️ Sequential Voice Roll-Call:** Record classroom audio to match students' spoken verification against enrolled voice embeddings.
- **🔗 Instant Share Links & QR Codes:** Dynamically generate course join links and scan-to-join QR codes for rapid student onboarding.
- **📊 Export & Analytics:** Review historic logs, calculate attendance rates, and download reports.

### 🧑‍🎓 Student Portal
- **FaceID & Voice Registration:** One-time biometric enrollment for facial and voice signatures.
- **Quick Join:** Click a teacher's share link or scan a QR code to auto-enroll into a subject.
- **Personal Attendance Insights:** View attendance percentages and historical logs across all registered courses.

### 🌐 Modern Landing Page (`SNAPCLASS-FRONTEND`)
- Responsive marketing landing page built with **Flask**, showcasing the teacher/student workflows, features, and tech stack.
- Production-ready for deployment on **Vercel** with `vercel.json` and `gunicorn`.

---

## 🏗️ Architecture & Project Structure

```text
snapclass/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies for the core app
├── README.md                   # Project documentation
│
├── .streamlit/
│   ├── config.toml             # Streamlit theme and server configuration
│   └── secrets.toml            # Supabase credentials (SUPABASE_URL, SUPABASE_KEY)
│
├── src/
│   ├── components/             # Reusable UI dialogs and widgets
│   │   ├── dialog_add_photo.py          # Camera snapshot modal for training data
│   │   ├── dialog_attendance_results.py # Attendance summary and confirmation modal
│   │   ├── dialog_auto_enroll.py        # Query param instant enrollment modal
│   │   ├── dialog_create_subject.py     # Create course dialog
│   │   ├── dialog_enroll.py             # Student course enrollment dialog
│   │   ├── dialog_share_subject.py      # QR code & dynamic join link generator
│   │   ├── dialog_voice_attendance.py   # Voice biometric recording dialog
│   │   ├── header.py                    # Header banners
│   │   ├── footer.py                    # Footer branding
│   │   └── subject_card.py              # Subject overview cards with badges
│   │
│   ├── database/               # Database integration layer
│   │   ├── config.py           # Supabase client initialization (resilient config)
│   │   └── db.py               # Database queries (CRUD for teachers, students, subjects, logs)
│   │
│   ├── pipelines/              # AI Biometric Pipelines
│   │   ├── face_pipeline.py    # Face embedding extraction (dlib/face_recognition), KNN classifier
│   │   └── voice_pipeline.py   # Voice embedding extraction (resemblyzer, librosa)
│   │
│   ├── screens/                # Primary portal views
│   │   ├── home_screen.py      # Portal selector (Student vs. Teacher)
│   │   ├── teacher_screen.py   # Teacher authentication, course management, & attendance flows
│   │   └── student_screen.py   # Student FaceID login, registration, & dashboard
│   │
│   └── ui/
│       └── base_layout.py      # Global CSS design system (pill cards, animations, responsive modals)
│
└── SNAPCLASS-FRONTEND/         # Standalone Flask Landing Page
    ├── app.py                  # Flask server entry point
    ├── requirements.txt        # Flask & Gunicorn dependencies
    ├── vercel.json             # Vercel serverless deployment config
    ├── static/                 # CSS styles, images, and JavaScript
    └── templates/              # HTML5 landing page templates
```

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Frontend Frameworks** | [Streamlit](https://streamlit.io/) (Core App), [Flask](https://flask.palletsprojects.com/) (Landing Site) |
| **Styling & Design** | Modern CSS Design System, Google Fonts (*Climate Crisis*, *Outfit*), Glassmorphism |
| **Database & Auth** | [Supabase](https://supabase.com/) (PostgreSQL), Bcrypt |
| **Computer Vision** | `dlib`, `face_recognition_models`, `scikit-learn`, `Pillow`, `NumPy` |
| **Audio Processing** | `resemblyzer`, `librosa`, `webrtcvad` |
| **QR Code Generation** | `segno` |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10 to 3.13** installed.
- (macOS users) `cmake` and `dlib` prerequisites:
  ```bash
  brew install cmake
  ```

### 2. Clone the Repository
```bash
git clone https://github.com/Nirbhay404/Snap-Class-AI-Attendance-application-.git
cd Snap-Class-AI-Attendance-application-
```

### 3. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Supabase Credentials
Create a `.streamlit/secrets.toml` file in the root directory (the app refuses to start without credentials; see [SECURITY_SETUP.md](SECURITY_SETUP.md) for how to lock down the database):
```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-secret-key"   # sb_secret_... (never the publishable/anon key)

# Optional: explicitly set base URL for generated share links
# APP_URL = "https://your-domain.streamlit.app"
```

---

## 💻 Running the Application

### Core AI Attendance App (Streamlit)
To start the attendance portal:
```bash
streamlit run app.py
```
Open your browser and navigate to:
```text
http://localhost:8501
```

### Marketing Landing Page (Flask)
To run the companion marketing landing page:
```bash
python SNAPCLASS-FRONTEND/app.py
```
Open your browser and navigate to:
```text
http://localhost:5002
```

---

## 🌐 Deployment

### Deploying the Streamlit App (Streamlit Community Cloud)
1. Fork or push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository:
   - **Repository:** `YourUsername/Snap-Class-AI-Attendance-application-`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Add your secrets under **App Settings → Secrets**:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-secret-key"
   ```
5. Deploy!

### Deploying the Landing Page (Vercel)
1. Install the Vercel CLI or import `SNAPCLASS-FRONTEND` via GitHub on [Vercel](https://vercel.com).
2. Root directory: set to `SNAPCLASS-FRONTEND`.
3. Vercel will automatically detect `vercel.json` and deploy the Python serverless function.

---

## 🔒 Security & Privacy
- **Biometric Protection:** Raw video streams and audio are processed locally in-memory; only numerical 128-dimensional facial vectors and audio embeddings are securely stored in Supabase.
- **Password Hashing:** Passwords are salted and hashed using `bcrypt` prior to storage.

---

## 👨‍💻 Author

Created with ❤️ by **Nirbhay Kumar**
- GitHub: [@Nirbhay404](https://github.com/Nirbhay404)
