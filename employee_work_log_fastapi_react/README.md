# Employee Work Log Web Application

A simple web database application using a FastAPI backend and React frontend.

## Tech stack

- Backend: Python, FastAPI
- Frontend: React, Vite, HTML, CSS, JavaScript
- Database: SQLite
- ORM: SQLAlchemy
- Authentication: HTTP-only cookie session with hashed passwords
- Testing: Pytest

## Test accounts

Admin:
- Email: admin@example.com
- Password: admin123

Regular users:
- Example email: abbas@example.com
- Password: password123

## Run the backend

From the project root:

```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
Should hopefully be hosted in Render by then
```

Backend runs on:

```text
http://127.0.0.1:8000
```

## Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://127.0.0.1:5173
```

## Build frontend for deployment

```bash
cd frontend
npm install
npm run build
```

Then run the backend. FastAPI will serve the built React app from `frontend/dist`.

## API routes

- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me
- POST /api/auth/logout
- GET /api/worklogs
- POST /api/worklogs
- PUT /api/worklogs/{log_id}
- DELETE /api/worklogs/{log_id}
