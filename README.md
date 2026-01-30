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

