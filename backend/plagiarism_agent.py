import os
import sys
from dotenv import load_dotenv

load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------------------------
# 1. THE DATA SCHEMA (What the dashboard will flag)
# ---------------------------------------------------------
class PlagiarismReport(BaseModel):
    is_suspicious: bool = Field(description="True if there is high evidence of copying, False otherwise")
    confidence_score: int = Field(description="Confidence percentage from 0 to 100")
    shared_anomalies: list[str] = Field(description="List of specific bizarre mistakes or unique logical leaps both students made")
    verdict_justification: str = Field(description="A short explanation for the professor detailing why this was flagged or cleared")

# ---------------------------------------------------------
# 2. THE DETECTOR AGENT
# ---------------------------------------------------------
class PlagiarismDetector:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an elite Academic Integrity Investigator.
            Your job is to compare two student handwritten exam answers and detect plagiarism.
            
            CRITICAL RULES:
            1. VERBATIM MATCH: If the written phrasing, formatting, or equations are word-for-word identical, FLAG IT with 99% confidence. Students do not write the exact same sentences by coincidence.
            2. SHARED MISTAKES: If both students share the exact same incorrect mathematical logic, it is undeniable proof of copying.
            3. NEVER assume an answer is "correct" just because they both wrote it. Treat identical short answers as highly suspicious."""),
            ("human", "Student 1 Answer:\n{student_1}\n\nStudent 2 Answer:\n{student_2}\n\nAnalyze for shared anomalies.")
        ])
        print("[OK] Plagiarism Agent Initialized.")

    def analyze_papers(self, student_1_answer: str, student_2_answer: str):
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_actual_gemini_api_key_here":
            raise ValueError("Invalid GEMINI_API_KEY in backend/.env. Please replace 'your_actual_gemini_api_key_here' with your real Gemini API key from https://aistudio.google.com/app/apikey")

        print("[*] Comparing Student 1 and Student 2 logic structures...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.0, 
            api_key=api_key
        )
        structured_llm = llm.with_structured_output(PlagiarismReport)
        detection_chain = self.prompt | structured_llm

        return detection_chain.invoke({
            "student_1": student_1_answer,
            "student_2": student_2_answer
        })

# ---------------------------------------------------------
# 3. TEST THE DETECTOR
# ---------------------------------------------------------
if __name__ == "__main__":
    detector = PlagiarismDetector()
    
    # Let's test a highly suspicious scenario where both made the same weird mistake
    mock_student_1 = "The derivative of x^2 is 2x. The derivative of 5x is 3. So final is 2x + 3."
    mock_student_2 = "By power rule we get 2x for the first part. For 5x it becomes 3 somehow. Answer = 2x + 3"
    
    report = detector.analyze_papers(mock_student_1, mock_student_2)
    
    print("\n" + "="*50)
    print("             ACADEMIC INTEGRITY REPORT")
    print("="*50)
    
    if report.is_suspicious:
        print("🚨 ALERT: SUSPICIOUS ACTIVITY DETECTED 🚨")
    else:
        print("✅ CLEAR: NO PLAGIARISM DETECTED")
        
    print(f"Confidence: {report.confidence_score}%\n")
    
    print("Shared Logical Anomalies:")
    if not report.shared_anomalies:
        print(" - None")
    for anomaly in report.shared_anomalies:
        print(f" 🚩 {anomaly}")
        
    print(f"\nJustification: {report.verdict_justification}")
    print("="*50)