# 🔗 ASCII URL Shortener

A lightweight, full-stack URL shortener built for learning purposes. It uses a **Next.js** frontend and a **FastAPI** backend with **SQLite** for data storage.

## 🛠️ Tech Stack
- **Frontend:** Next.js, Tailwind CSS, Bun
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite (File-based)

---

## 🚀 Installation & Setup

### 1. Backend Setup (FastAPI)
Navigate to the backend folder and set up a Python virtual environment.

```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install fastapi uvicorn sqlalchemy




### 2. Frontend Setup (Next.js)
Open a new terminal and navigate to the frontend folder.
cd frontend
bun install

How to Run
Start the Backend
From the /backend folder (ensure venv is active):

Bash
uvicorn main:app --reload
The API will be available at http://localhost:8000

Start the Frontend
From the /frontend folder:

Bash
bun dev
The Website will be available at http://localhost:3000

🧠 How it Works: Backend Logic
1. Database Schema
We use a simple table called urls with three main columns:

id: An auto-incrementing integer (1, 2, 3...).

original_url: The long link provided by the user.

short_code: The unique 6-character string generated from the ID.

2. The Shortening Process (Base62)
Instead of using random characters, we use Base62 Encoding.

When a URL is saved, SQLite gives it a unique ID (e.g., 125).

Our utils.py converts that number into a string using the characters 0-9, a-z, and A-Z.

Example: ID 125 becomes cb. This ensures every short link is unique and predictable.

3. API Routes
POST /shorten: Receives a JSON object with a URL, saves it to the DB, runs the encoding logic, and returns the full shortened address.

GET /{code}: A dynamic route that captures the "code" from the URL, looks up the original_url in the database, and performs a 307 Temporary Redirect.

🔌 Connecting Frontend to Backend
The connection is made using the JavaScript fetch() API.

The frontend sends a POST request to http://localhost:8000/shorten. We use CORS Middleware in FastAPI to allow the browser to talk across different ports (3000 to 8000).


---

### How to use this file
1. Go to your main project folder.
2. Right-click and create **New File**.
3. Name it `README.md`.
4. Paste the content above and save.

Now, whenever you open this project on GitHub or in VS Code, you'll have a professional guide to help you remember the logic! 

**Would you like me to show you how to add a "Delete" button next to shortened links so you can remove them from your database?**