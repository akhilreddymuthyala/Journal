# 📖 Journal App

A full-stack personal journal web app built with **FastAPI**, **PostgreSQL**, and vanilla **HTML/CSS/JS**.

---

## 🛠 Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Frontend | HTML, CSS, JS     |
| Backend  | Python + FastAPI  |
| Database | PostgreSQL        |

---

## 📁 Project Structure

```
Journal/
├── backend/
│   ├── main.py          # API routes
│   ├── database.py      # DB connection
│   ├── requirements.txt # Dependencies
│   └── .env             # DB credentials (not committed)
├── frontend/
│   └── index.html       # UI
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/journal-app.git
cd journal-app
```

### 2. Set up PostgreSQL
```bash
psql -U postgres -c "CREATE DATABASE journaldb;"
```

### 3. Configure environment
Create `backend/.env`:
```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=journaldb
DB_USER=postgres
DB_PASSWORD=yourpassword
```

### 4. Install dependencies & run backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 5. Open the frontend
Open `frontend/index.html` in your browser.

---

## 🔗 API Endpoints

| Method | Endpoint          | Description       |
|--------|-------------------|-------------------|
| GET    | `/entries`        | Get all entries   |
| POST   | `/entries`        | Create new entry  |
| DELETE | `/entries/{id}`   | Delete an entry   |

API docs available at `http://127.0.0.1:8000/docs`

---

## ✨ Features

- Write and save journal entries
- Pick a mood for each entry
- Search through past entries
- Delete entries
- Data stored in PostgreSQL
