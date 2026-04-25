# Mini Hospital Management System (HMS) 

A streamlined hospital management web application designed for seamless doctor availability management and patient appointment bookings. This repository consists of a Django-powered robust backend with a Serverless Lambda Email Notification system hooked together natively via inter-service HTTP requests.

## 🚀 Key Features

* **Role-Based Authentication:** Clean session validations for dual profiles — `Doctor` and `Patient`.
* **Doctor Dashboard:** Manage dynamic temporal slots explicitly locked around the user's logged-in identity.
* **Patient Booking Engine:** Displays all un-occupied doctor time slots cleanly and instantly claims access upon booking confirmation securely eliminating race-condition possibilities via structural availability toggles.
* **Email Notification System:** Connects dynamically with an AWS Serverless Lambda environment running `serverless-offline`. Handled dynamically over Python and handles workflows like `SIGNUP_WELCOME` and `BOOKING_CONFIRMATION` automatically. 
* **Database Agnostic Base:** While wired sequentially inside Settings.py for `PostgreSQL`, an on-the-fly override defaults to `sqlite3` for local headless plug-and-play behavior preventing initial friction.
* **Fully Responsive Vanilla Design:** An immersive clean-plate dark theme aesthetics layout.

## 🛠 Tech Stack

- **Backend / Frontend Templates:** Django, Django ORM, HTML5
- **Design:** Modern CSS3 Vanilla
- **Severless Compute:** AWS Lambda framework running Python 3.9 natively offline via `serverless-offline`

## ⚙️ Quick Start

You will need Python 3.x and Node.js installed to run both services.

### 1. Launching the Email Notification Lambda (Service 1)
In a terminal, navigate inside the `email_service` directory:
```bash
cd email_service
npm install
npm run start


python -m venv venv
# Activate it (On Windows Native:)
.\venv\Scripts\activate

# Install dependencies
pip install django psycopg2 python-dotenv requests google-api-python-client google-auth-httplib2 google-auth-oauthlib django-widget-tweaks

# Establish database
python manage.py migrate

# Run app
python manage.py runserver

📅 Pending Integrations Note
Google Calendar API: Due strictly to GCP's robust OAuth2 credentials verification logic, automatic sync into individual desktop calendars remains a structural placeholder inside the .save() Booking models. To finalize: Drop your OAuth credentials inside the config, boot up google-auth-oauthlib, inject the dynamic session user variables across the execution, and build the dictionary payload exactly
