import os
import sys
import shutil
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from bson import ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

# Import your AI engines
from vision_engine import CloudVisionEngine
from agentic_grader import AgenticGrader
from plagiarism_agent import PlagiarismDetector

app = FastAPI(title="GradeOps API")

# Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MONGODB & LOCAL DATABASE SETUP ---
GRADES_FILE = "grades_db.json"

def _load_local_grades():
    if not os.path.exists(GRADES_FILE):
        return []
    try:
        with open(GRADES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_local_grades(grades):
    with open(GRADES_FILE, "w", encoding="utf-8") as f:
        json.dump(grades, f, indent=2)

mongo_uri = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017/"
)
db_name = os.getenv("MONGODB_DB_NAME", "gradeops")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
    db = client[db_name]
    grades_collection = db.grades
    print(f"[OK] MongoDB configured (Target: {mongo_uri})")
except Exception as e:
    print(f"[INFO] Using local storage for grades: {e}")
    client = None
    grades_collection = None

def save_grade_record(grade_dict):
    # Try MongoDB first if configured
    if grades_collection is not None:
        try:
            res = grades_collection.insert_one(dict(grade_dict))
            return str(res.inserted_id)
        except Exception as e:
            print(f"[INFO] MongoDB offline ({e}). Saving to local database.")
    
    # Fallback to local JSON storage
    grades = _load_local_grades()
    grade_id = str(uuid.uuid4())[:8]
    grade_dict["_id"] = grade_id
    grades.append(grade_dict)
    _save_local_grades(grades)
    return grade_id

def get_all_grade_records():
    if grades_collection is not None:
        try:
            grades = list(grades_collection.find())
            for g in grades:
                g["_id"] = str(g["_id"])
            return grades
        except Exception as e:
            print(f"[INFO] MongoDB offline ({e}). Loading from local database.")
    return _load_local_grades()

def delete_grade_record(grade_id: str):
    if grades_collection is not None:
        try:
            if ObjectId.is_valid(grade_id):
                res = grades_collection.delete_one({"_id": ObjectId(grade_id)})
                if res.deleted_count > 0:
                    return True
            res = grades_collection.delete_one({"_id": grade_id})
            if res.deleted_count > 0:
                return True
        except Exception:
            pass
    
    grades = _load_local_grades()
    initial_len = len(grades)
    grades = [g for g in grades if str(g.get("_id")) != str(grade_id)]
    if len(grades) < initial_len:
        _save_local_grades(grades)
        return True
    return False

# --- INITIALIZE AI ENGINES ---
vision_ai = CloudVisionEngine()
grader_ai = AgenticGrader()
plagiarism_ai = PlagiarismDetector()

# --- DATA MODELS ---
class GradingRequest(BaseModel):
    student_answer: str
    rubric_data: str 

class PlagiarismRequest(BaseModel):
    student_1_answer: str
    student_2_answer: str

class SaveGradeRequest(BaseModel):
    student_id: str
    total_score: int
    feedback: str
    status: str


# ==========================================
#               API ENDPOINTS
# ==========================================

@app.get("/")
def read_root():
    return {"status": "GradeOps API Server is LIVE 🚀"}

@app.post("/api/extract")
async def extract_text(file: UploadFile = File(...)):
    """Receives an image, saves it temporarily, and runs OCR via Gemini Vision."""
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        extracted_text = vision_ai.extract_text(temp_file_path)
        os.remove(temp_file_path)
        
        return {"extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/grade")
async def grade_answer(request: GradingRequest):
    """Receives extracted text AND the custom rubric, runs the Langchain Grader."""
    try:
        # Overwrite the local rubric file with the TA's custom one from the UI
        with open("rubric.json", "w") as f:
            f.write(request.rubric_data)
            
        evaluation = grader_ai.grade_answer("rubric.json", request.student_answer)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-plagiarism")
async def check_plagiarism(request: PlagiarismRequest):
    """Compares two answers and returns the plagiarism report."""
    try:
        report = plagiarism_ai.analyze_papers(request.student_1_answer, request.student_2_answer)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-grade")
async def save_grade(request: SaveGradeRequest):
    """Saves the final grade to MongoDB or local storage."""
    try:
        grade_doc = request.dict() 
        save_grade_record(grade_doc)
        return {"message": "Grade permanently saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/grades")
async def get_all_grades():
    """Fetches all saved grades for the Class Roster."""
    try:
        return get_all_grade_records()
    except Exception as e:
        return []
    
@app.delete("/api/grades/{grade_id}")
async def delete_grade(grade_id: str):
    """Deletes a specific grade from the Class Roster."""
    try:
        success = delete_grade_record(grade_id)
        if not success:
            raise HTTPException(status_code=404, detail="Grade not found.")
        return {"message": "Grade deleted successfully!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))