# 📦 KLB Assignment - Django + Telegram Integration

This project is a full-stack Django application built as part of the KLB internship assignment. It includes:

- 🔐 JWT Authentication using `SimpleJWT`
- 📧 Background email sending using `Celery + Redis`
- 🤖 Telegram bot integration using `python-telegram-bot`
- 🧾 Clean RESTful API structure using Django REST Framework
- ⚙️ Production-ready setup with `.env` support

---

## 📁 Features

### ✅ Core Features

- User Registration & Login (`/api/register/`, `/api/token/`)
- Protected profile API with JWT authentication
- Celery background task to send welcome email
- Telegram bot that:
  - Responds to `/start`
  - Sends Telegram user data to Django via `POST /api/telegram/register/`
- Stores Telegram users in DB (create or update)

---

## 🔧 Project Setup

### 1. Clone the Repo

```bash
git clone https://github.com/jitendra-ky/klb_assignment
cd klb_assignment
````

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/macOS
.venv\Scripts\activate     # For Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Setup `.env`

Create a `.env` file in the root:

```env
TELEGRAM_BOT_TOKEN=your-token-here
```

---

## ⚙️ Run Services

### 🟢 Run Django App

```bash
python manage.py migrate
python manage.py runserver
```

### 🟢 Run Celery Worker

```bash
celery -A klb_assignment worker --loglevel=info
```

### 🤖 Run Telegram Bot

```bash
python telegram_bot/bot.py
```

---

## 🚀 API Endpoints

| Method | Endpoint                  | Description                                    |
| ------ | ------------------------- | ---------------------------------------------- |
| POST   | `/api/register/`          | (public) Register a new user                   |
| GET    | `/api/profile/`           | (protected) View user profile (JWT required)   |
| POST   | `/api/token/`             | Get JWT tokens (access + refresh)              |
| POST   | `/api/token/refresh/`     | Refresh access token                           |
| POST   | `/api/telegram/register/` | Save/update Telegram user info (called by bot) |

---

## 🧪 Testing With Curl
| make sure django server is running `python manage.py runserver`

### ✅ 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"jitendra","email":"jitendra@example.com","password":"123456"}'
```

---

### ✅ 2. Get Access & Refresh Tokens (Login)

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"jitendra","password":"123456"}'
```

📌 Copy the `"access"` token from the response.

---

### ✅ 3. Use Access Token to Access Protected Profile API

Replace `YOUR_ACCESS_TOKEN_HERE` with the actual token you copied 👇

```bash
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

### ✅ 4. Refresh Your Access Token Using the Refresh Token

Replace `YOUR_REFRESH_TOKEN_HERE` with the actual token you copied 👇

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"YOUR_REFRESH_TOKEN_HERE"}'
```


---

## 📦 Tech Stack

* Django 4.x
* Django REST Framework
* SimpleJWT
* Celery
* Redis
* python-telegram-bot v20+
* httpx (for async bot requests)

---

## ✅ Deployment-Ready Setup

* Environment variables managed via `.env`
* Static files with `collectstatic`
* PostgreSQL or SQLite support
* Gunicorn or Uvicorn compatible
* Telegram bot runs separately from web server