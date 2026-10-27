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

🚀 **Live app:** [snapclass on Streamlit Cloud](https://nirbhay404-snap-class-ai-attendance-application--app-lpyli0.streamlit.app/) &nbsp;·&nbsp; 🌐 **Landing page:** [snap-class-landing-page](https://github.com/Nirbhay404/snap-class-landing-page)

</div>

---

## 🌟 Key Features

### 👨‍🏫 Teacher Portal
- **Account & Subjects:** Register and log in with a username and password, then create subjects (unique subject code, name, and section). Each subject card shows its enrolled-student and class counts.
- **📸 Multi-Face Photo Attendance:** Add classroom photos from the camera or by uploading several images; the AI pipeline finds every face, matches it to enrolled students, and shows a Present/Absent review before anything is saved.
- **🎙️ Voice Roll-Call:** Record classroom audio where students say "I am present"; each voice is matched against the enrolled voice profiles and reviewed before saving.
- **🔗 Instant Share Links & QR Codes:** Generate a course join link and a scan-to-join QR code for rapid student onboarding.
- **📊 Attendance Records:** See every saved session with its subject and a present/total summary.

### 🧑‍🎓 Student Portal
- **FaceID Login & Registration:** Log in by face. New students register once with their name, and can optionally add a voice sample for voice attendance.
- **Quick Join:** Click a teacher's share link or scan a QR code to enroll in a subject, or type a subject code manually. Students can also unenroll.
- **Personal Attendance Insights:** See every enrolled subject with the number of sessions held and the number attended.

### 🌐 Landing Page (`SNAPCLASS-FRONTEND`)
- Responsive marketing landing page built with **Flask**, showcasing the teacher/student workflows (with screenshots of this app), features, and tech stack.
- Deployable on **Vercel** with `vercel.json` and `gunicorn`.
- Also published as its own repository: [snap-class-landing-page](https://github.com/Nirbhay404/snap-class-landing-page).

---

## 🏗️ Architecture & Project Structure

```text
snapclass/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies for the core app
├── README.md                   # Project documentation
├── SECURITY_SETUP.md           # Steps to lock down the Supabase database (RLS, keys)
│
├── .devcontainer/              # Dev container / Codespaces setup (Python 3.11)
│
├── .streamlit/
│   ├── config.toml             # Streamlit theme and toolbar settings
│   └── secrets.toml            # Supabase credentials (git-ignored; never commit)
│
├── supabase/
│   └── enable_rls.sql          # Turns on Row Level Security for all tables
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
│   │   ├── config.py           # Supabase client setup; reads credentials from secrets or env vars only
│   │   └── db.py               # Database queries (CRUD for teachers, students, subjects, logs)
│   │
│   ├── pipelines/              # AI Biometric Pipelines
│   │   ├── face_pipeline.py    # Face embedding extraction (dlib), SVM classifier (scikit-learn SVC)
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
- **Python 3.11 to 3.13** installed (developed on 3.13).
- A [Supabase](https://supabase.com/) project with the tables `teachers`, `students`, `subjects`, `subject_students`, and `attendance_logs`.
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
The landing page has its own dependencies (Flask and Gunicorn), so install them first, then start it:
```bash
pip install -r SNAPCLASS-FRONTEND/requirements.txt
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
4. Add your secrets under **App Settings → Secrets** (the app will not start without them):
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-secret-key"
   ```
5. Deploy, then follow [SECURITY_SETUP.md](SECURITY_SETUP.md) to turn on Row Level Security.

### Deploying the Landing Page (Vercel)
1. Import this repository (or the standalone [snap-class-landing-page](https://github.com/Nirbhay404/snap-class-landing-page) repo) on [Vercel](https://vercel.com).
2. From this repository, set the root directory to `SNAPCLASS-FRONTEND`. The standalone repo deploys from its root.
3. Vercel will automatically detect `vercel.json` and deploy the Python serverless function.

---

## 🔒 Security & Privacy
- **Biometric Protection:** Photos and audio are processed in memory on the app server; only numerical face vectors (128 dimensions) and voice embeddings are stored in Supabase, never the images or recordings.
- **Password Hashing:** Teacher passwords are salted and hashed with `bcrypt` before storage and are never kept in the session.
- **No Secrets in the Repo:** The app reads `SUPABASE_URL` and `SUPABASE_KEY` only from Streamlit secrets or environment variables, and refuses to start without them. Use the Supabase **secret key**, never the publishable/anon key.
- **Row Level Security:** Enable it on every table with [`supabase/enable_rls.sql`](supabase/enable_rls.sql) so the public key cannot read or write your data. The full, ordered checklist is in [SECURITY_SETUP.md](SECURITY_SETUP.md).
- **Known Limitation:** FaceID login does not check that a live person is in front of the camera, so a photo of a registered student could be accepted.

---

## 👨‍💻 Author

Created with ❤️ by **Nirbhay Kumar**
- GitHub: [@Nirbhay404](https://github.com/Nirbhay404)
