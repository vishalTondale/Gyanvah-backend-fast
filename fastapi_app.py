from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uvicorn

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

app = FastAPI(
    title="GyanVah API",
    description="Educational platform API - सिद्धिर्भवति कर्मजा (Success comes from action)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
}

DB = os.getenv("SNOWFLAKE_DATABASE", "GYANVAH")
SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

# Pydantic models for request/response
class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class Course(BaseModel):
    COURSE_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    CATEGORY: Optional[str]
    COURSE_LINK: Optional[str]

class Book(BaseModel):
    BOOK_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    IS_PAID: Optional[int]
    PDF_LINK: Optional[str]

class Project(BaseModel):
    PROJECT_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    DIFFICULTY: Optional[str]
    GITHUB_LINK: Optional[str]

class Note(BaseModel):
    NOTE_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    SUBJECT: Optional[str]
    PDF_LINK: Optional[str]

class Video(BaseModel):
    VIDEO_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    CATEGORY: Optional[str]
    VIDEO_LINK: Optional[str]

class Cheatsheet(BaseModel):
    CHEATSHEET_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]
    PDF_LINK: Optional[str]

class LearningPath(BaseModel):
    PATH_ID: Optional[int]
    TITLE: str
    DESCRIPTION: Optional[str]

class PythonCourseEpisode(BaseModel):
    EPISODE_ID: Optional[int]
    EPISODE_NUMBER: int
    TITLE: str
    DESCRIPTION: Optional[str]
    YOUTUBE_URL: Optional[str]
    NOTES_URL: Optional[str]
    IS_PUBLISHED: Optional[bool]

class NetworkingEssentialsEpisode(BaseModel):
    ID: Optional[int]
    EPISODE_NUMBER: int
    TITLE: str
    DESCRIPTION: Optional[str]
    YOUTUBE_URL: Optional[str]
    NOTES_URL: Optional[str]
    IS_PUBLISHED: Optional[bool]

class GenAiCourseEpisode(BaseModel):
    ID: Optional[int]
    EPISODE_NUMBER: int
    TITLE: str
    DESCRIPTION: Optional[str]
    YOUTUBE_URL: Optional[str]
    NOTES_URL: Optional[str]
    IS_PUBLISHED: Optional[bool]

# Database connection functions
def get_connection():
    """Get Snowflake database connection"""
    try:
        return snowflake.connector.connect(**DB_CONFIG)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

def query(table: str, order_by: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query all records from a table"""
    conn = get_connection()
    try:
        q = f"SELECT * FROM {DB}.{SCHEMA}.{table}"
        if order_by:
            q += f" ORDER BY {order_by}"
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(q)
        return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        conn.close()

def run_sql(sql: str) -> List[Dict[str, Any]]:
    """Execute a custom SQL query"""
    conn = get_connection()
    
    try:
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL execution failed: {str(e)}")
    finally:
        conn.close()

def insert_sql(sql: str):
    """Execute an INSERT SQL statement"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insert failed: {str(e)}")
    finally:
        conn.close()

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to GyanVah API",
        "tagline": "सिद्धिर्भवति कर्मजा — Success comes from action",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/stats")
async def get_stats():
    """Get platform statistics"""
    try:
        courses = query("COURSES")
        books = query("BOOKS")
        projects = query("PROJECTS")
        notes = query("NOTES")
        videos = query("VIDEOS")
        cheatsheets = query("CHEATSHEETS")

        return {
            "courses": len(courses),
            "books": len(books),
            "projects": len(projects),
            "notes": len(notes),
            "videos": len(videos),
            "cheatsheets": len(cheatsheets)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses", response_model=List[Course])
async def get_courses(category: Optional[str] = None):
    """Get all courses, optionally filtered by category"""
    try:
        courses = query("COURSES")
        if category and category != "All":
            courses = [c for c in courses if c.get("CATEGORY") == category]
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses/categories")
async def get_course_categories():
    """Get unique course categories"""
    try:
        courses = query("COURSES")
        categories = sorted(set(c.get("CATEGORY", "General") for c in courses))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books", response_model=List[Book])
async def get_books(
    filter_type: Optional[str] = Query(None, alias="filter"),
    search: Optional[str] = None
):
    """Get all books, optionally filtered by type or search term"""
    try:
        books = query("BOOKS")

        if filter_type == "Free":
            books = [b for b in books if b.get("IS_PAID", 0) == 0]
        elif filter_type == "Paid":
            books = [b for b in books if b.get("IS_PAID", 0) == 1]

        if search:
            search_lower = search.lower()
            books = [b for b in books if
                    search_lower in b.get("TITLE", "").lower() or
                    search_lower in b.get("DESCRIPTION", "").lower()]

        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects", response_model=List[Project])
async def get_projects(difficulty: Optional[str] = None):
    """Get all projects, optionally filtered by difficulty"""
    try:
        projects = query("PROJECTS")
        if difficulty and difficulty != "All":
            projects = [p for p in projects if p.get("DIFFICULTY") == difficulty]
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/difficulties")
async def get_project_difficulties():
    """Get unique project difficulties"""
    try:
        projects = query("PROJECTS")
        difficulties = sorted(set(p.get("DIFFICULTY", "General") for p in projects))
        return {"difficulties": difficulties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes", response_model=List[Note])
async def get_notes(
    subject: Optional[str] = None,
    search: Optional[str] = None
):
    """Get all notes, optionally filtered by subject or search term"""
    try:
        notes = query("NOTES")

        if subject and subject != "All":
            notes = [n for n in notes if n.get("SUBJECT") == subject]

        if search:
            search_lower = search.lower()
            notes = [n for n in notes if
                    search_lower in n.get("TITLE", "").lower() or
                    search_lower in n.get("DESCRIPTION", "").lower()]

        return notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/subjects")
async def get_note_subjects():
    """Get unique note subjects"""
    try:
        notes = query("NOTES")
        subjects = sorted(set(n.get("SUBJECT", "General") for n in notes))
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cheatsheets", response_model=List[Cheatsheet])
async def get_cheatsheets():
    """Get all cheatsheets"""
    try:
        return query("CHEATSHEETS")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos", response_model=List[Video])
async def get_videos(category: Optional[str] = None):
    """Get all videos, optionally filtered by category"""
    try:
        videos = query("VIDEOS")
        if category and category != "All":
            videos = [v for v in videos if v.get("CATEGORY") == category]
        return videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/categories")
async def get_video_categories():
    """Get unique video categories"""
    try:
        videos = query("VIDEOS")
        categories = sorted(set(v.get("CATEGORY", "General") for v in videos))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning-paths", response_model=List[LearningPath])
async def get_learning_paths():
    """Get all learning paths"""
    try:
        return query("LEARNING_PATHS")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning-paths/{path_id}")
async def get_learning_path_details(path_id: int):
    """Get details of a specific learning path including its courses"""
    try:
        paths = query("LEARNING_PATHS")
        path = next((p for p in paths if p["PATH_ID"] == path_id), None)

        if not path:
            raise HTTPException(status_code=404, detail="Learning path not found")

        # Get courses in this path
        courses = run_sql(f"SELECT c.* FROM {DB}.{SCHEMA}.COURSES c JOIN {DB}.{SCHEMA}.PATH_COURSES pc ON c.COURSE_ID=pc.COURSE_ID WHERE pc.PATH_ID={path_id}")

        return {
            "path": path,
            "courses": courses,
            "course_count": len(courses)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/python-course", response_model=List[PythonCourseEpisode])
async def get_python_course():
    """Get all published Python course episodes"""
    try:
        episodes = query("PYTHON_COURSE_VIDEOS", "EPISODE_NUMBER")
        published = [e for e in episodes if e.get("IS_PUBLISHED", True)]
        # Map ID to EPISODE_ID for Pydantic validation
        for episode in published:
            if "ID" in episode and "EPISODE_ID" not in episode:
                episode["EPISODE_ID"] = episode["ID"]
        return published
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/networking-essentials", response_model=List[NetworkingEssentialsEpisode])
async def get_networking_essentials():
    """Get all published Networking Essentials course episodes"""
    try:
        episodes = query("NETWORKING_ESSENTIALS_VIDEOS", "EPISODE_NUMBER")
        published = [e for e in episodes if e.get("IS_PUBLISHED", True)]
        return published
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/genai-course", response_model=List[GenAiCourseEpisode])
async def get_genai_course():
    """Get all published GenAI course episodes"""
    try:
        episodes = query("GENAI_COURSE_VIDEOS", "EPISODE_NUMBER")
        published = [e for e in episodes if e.get("IS_PUBLISHED", True)]
        return published
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
async def submit_contact_form(contact: ContactForm):
    """Submit a contact form"""
    try:
        # Validate input
        if not contact.name or not contact.email or not contact.subject or not contact.message:
            raise HTTPException(status_code=400, detail="All fields are required")

        # Insert into database
        insert_sql(f"""INSERT INTO {DB}.{SCHEMA}.CONTACTS (NAME, EMAIL, SUBJECT, MESSAGE)
                      VALUES ('{contact.name.replace("'", "''")}',
                              '{contact.email.replace("'", "''")}',
                              '{contact.subject.replace("'", "''")}',
                              '{contact.message.replace("'", "''")}')""")

        return {"message": "Message sent successfully! We'll get back to you soon."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/about")
async def get_about_info():
    """Get information about GyanVah"""
    return {
        "title": "About GyanVah",
        "tagline": "Empowering minds, building futures",
        "description": "Gyanvah empowers students and fresh graduates by providing real-world internship experience and mentorship in various domains. We believe in success through action and learning.",
        "mission": "To make learning accessible, practical, and affordable, helping learners upskill and apply knowledge in the real world.",
        "vision": "To build a global community of skilled learners and professionals who grow through knowledge, projects, and collaboration.",
        "offers": [
            {"icon": "🚀", "title": "Real Project Internships", "description": "Hands-on experience with real-world projects."},
            {"icon": "💼", "title": "Freelancing Experts", "description": "Hire top freelancers for real-world projects."},
            {"icon": "🎓", "title": "Learning Courses", "description": "Curated courses for development, data science & more."},
            {"icon": "📝", "title": "Handwritten & Digital Notes", "description": "High-quality notes for quick learning."},
            {"icon": "🔧", "title": "Projects & Practice", "description": "Build your portfolio with guided projects."}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)