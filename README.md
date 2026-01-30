# 🏥 Mini Hospital Management System (HMS)

A backend-focused **Mini Hospital Management System** built using **Django**, featuring **role-based authentication**, **appointment booking**, **Google Calendar integration**, and a clean modular architecture.

This project is designed to demonstrate **real-world backend engineering practices**, not just CRUD operations.

---

## 🚀 Features

### 👨‍⚕️ Doctor
- Secure login & signup
- Create availability slots
- View own availability
- Google Calendar sync for appointments

### 🧑‍🤝‍🧑 Patient
- Secure login & signup
- View available doctor slots
- Book appointments
- Automatic slot blocking after booking
- Google Calendar event creation

### 🔐 Authentication
- Custom User model
- Role-based access (Doctor / Patient)
- Dashboard redirection based on role

### 📅 Google Calendar Integration
- OAuth 2.0 authentication
- Stores access & refresh tokens per user
- Automatically creates calendar events on booking

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (development)
- **Authentication:** Django Auth + Custom User Model
- **APIs:** Google Calendar API (OAuth 2.0)
- **Version Control:** Git & GitHub
- **Frontend:** Minimal HTML (backend-focused)

---

## 📂 Project Structure
mini_hms/
│
├── config/ # Project settings & URLs
├── users/ # Custom user model & auth logic
├── doctors/ # Doctor dashboard & availability
├── bookings/ # Appointment booking logic
├── templates/ # HTML templates
├── manage.py
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mini-hms-django.git
cd mini-hms-django

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install django google-auth google-auth-oauthlib google-api-python-client

4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver

🔑 Google Calendar Setup

Go to Google Cloud Console

Create a project

Enable Google Calendar API

Create OAuth 2.0 Client (Web Application)

Add redirect URI:

http://127.0.0.1:8000/google/callback/


Add credentials in settings.py:

GOOGLE_CLIENT_ID = "your_client_id"
GOOGLE_CLIENT_SECRET = "your_client_secret"

🧪 How It Works (Flow)

Doctor logs in → creates availability

Patient logs in → views available slots

Patient books slot → slot locked atomically

Appointment added to:

Patient’s Google Calendar

Doctor’s Google Calendar

🔒 Security Notes

Secrets are excluded using .gitignore

OAuth tokens stored securely per user

Transactions prevent double-booking

Role-based access enforced at view level

📌 Future Improvements

Email notifications (Serverless / Lambda)

Admin analytics dashboard

Deployment on Render / Railway

PostgreSQL for production

Frontend UI with React
