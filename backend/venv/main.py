from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import our logic function from the other file
from utils import encode_base62

# --- DATABASE CONFIG ---
DB_URL = "sqlite:///./shortener.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define how our "urls" table looks in SQLite
class URLModel(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String)
    short_code = Column(String, unique=True)

# Create the database file and table
Base.metadata.create_all(bind=engine)

# --- APP CONFIG ---
app = FastAPI()

# IMPORTANT: This allows your Next.js (port 3000) to talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.post("/shorten")
async def shorten_url(request: Request):
    # 1. Get the long URL from the frontend request
    data = await request.json()
    long_url = data.get("url")
    
    db = SessionLocal()
    
    # 2. Save the long URL first to generate a unique ID
    new_entry = URLModel(original_url=long_url)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry) # This gives us access to the new ID
    
    # 3. Use the ID to create the short code
    code = encode_base62(new_entry.id)
    
    # 4. Update the record with its new short code
    new_entry.short_code = code
    db.commit()
    db.close()
    
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect_to_url(code: str):
    db = SessionLocal()
    # Find the record that matches the short code
    url_record = db.query(URLModel).filter(URLModel.short_code == code).first()
    db.close()
    
    if url_record:
        # Send the user to the original long URL
        return RedirectResponse(url=url_record.original_url)
    
    raise HTTPException(status_code=404, detail="Short link not found")