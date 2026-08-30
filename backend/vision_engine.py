import os
import sys
from dotenv import load_dotenv
load_dotenv() # Load the hidden keys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from google import genai
from PIL import Image

class CloudVisionEngine:
    def __init__(self):
        self.model_id = "gemini-3.6-flash"
        print("[OK] Cloud Vision Engine Initialized (Model: gemini-3.6-flash).")

    def extract_text(self, image_path: str) -> str:
        print(f"[*] Sending '{image_path}' to Gemini for OCR...")
        
        try:
            # Gemini natively handles the raw image file, no Base64 required!
            img = Image.open(image_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find '{image_path}'.")

        prompt = "Extract and transcribe all the handwritten text and math formulas from this image exactly as written. Output only the transcribed text. Do not add any conversational filler."

        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_actual_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is not configured. Please set your key in backend/.env")

        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model=self.model_id,
                contents=[img, prompt]
            )
            return response.text
        except Exception as e:
            raise Exception(f"Vision API Error: {str(e)}")

# --- Test the Engine ---
if __name__ == "__main__":
    engine = CloudVisionEngine()
    
    # Make sure 'test_exam.png' is in the main GRADEOPS folder!
    result = engine.extract_text("test_exam.png") 
    
    print("\n" + "="*40)
    print("        EXTRACTION RESULT")
    print("="*40)
    print(result)