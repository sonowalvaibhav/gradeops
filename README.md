# GradeOps · AI-Powered Examination Grading & Academic Integrity System

> **Human-in-the-Loop exam grading powered by Vision-Language Models, Agentic LLMs, and a high-throughput TA review dashboard.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas_or_Local-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)
[![Gemini](https://img.shields.io/badge/Google_Gemini-3.6_Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

### Project Team

* **Himanshu Kumar** — 230122020
* **Akhil Lavudya** — 230122026
* **Vaibhav Sonowal** — 230122062

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Sample Exam Testing](#sample-exam-testing)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Roles & Permissions](#roles--permissions)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Manual grading of handwritten exams is slow, inconsistent, and prone to fatigue-induced bias. **GradeOps** solves this with a three-stage pipeline:

1. **Extract** — Multimodal Vision models (Google Gemini Vision) transcribe handwritten student answers, formulas, and diagrams directly from exam images.
2. **Grade** — An Agentic LLM evaluates each answer question-by-question against instructor-defined JSON rubrics, awarding partial credit with structured textual justifications.
3. **Review** — A high-throughput dashboard surfaces AI-proposed grades to TAs, who can approve or override with keyboard shortcuts before committing to the database.

The result: consistent, auditable grades at scale — with a human always in the loop.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GradeOps Platform                        │
│                                                                 │
│  ┌──────────────┐    REST/JSON    ┌──────────────────────────┐  │
│  │  React (Vite)│◄──────────────►│    FastAPI Backend        │  │
│  │  Frontend    │                │                          │  │
│  │              │                │  ┌────────────────────┐  │  │
│  │  Instructor  │                │  │  Grading Agent     │  │  │
│  │  Dashboard   │                │  │  (LangChain)       │  │  │
│  │              │                │  └────────┬───────────┘  │  │
│  │  TA Review   │                │           │              │  │
│  │  Dashboard   │                │  ┌────────▼───────────┐  │  │
│  └──────────────┘                │  │  Gemini 3.6 Flash  │  │  │
│                                  │  │  (OCR + Grading)   │  │  │
│                                  │  └────────────────────┘  │  │
│                                  │           │              │  │
│                                  │  ┌────────▼───────────┐  │  │
│                                  │  │   MongoDB / Local   │  │  │
│                                  │  │   (Grades Roster)  │  │  │
│                                  │  └────────────────────┘  │  │
│                                  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Features

### 🧠 Agentic Multi-Question Grading
Decomposes exam submissions question-by-question, evaluates answers against strict JSON rubrics, and awards partial credit with justifications — all in a single pipeline execution.

### 👁️ Vision-Language OCR
Google Gemini Vision extracts and transcribes handwritten answers, equations, and math notation from photos/scans.

### 🕵️ Logic-Based Plagiarism Detection
Compares two submissions for shared *anomalous logic structures* and identical erroneous reasoning patterns that indicate copying.

### ✏️ Human-in-the-Loop (HITL) Review Dashboard
A side-by-side view of the student answer image, extracted OCR text, and the AI-proposed breakdown. TAs can approve, override score, or edit feedback before committing to the database — with full keyboard shortcut support for high-throughput grading.

### 🗄️ Resilient Class Roster
Stores finalized grades, structured feedback, and student IDs. Supports **MongoDB Atlas**, local MongoDB instances, and a built-in **Local JSON Database** (`grades_db.json`) fallback that works out of the box with zero external database installation.

### 🔐 Role-Based Access Control (RBAC)

| Role | Capabilities |
| ---- | ------------ |
| **Instructor** | Upload exams, customize JSON rubrics, view/delete roster records, run plagiarism analysis |
| **Teaching Assistant** | Access grading review queue, approve/override AI grades with keyboard shortcuts |

---

## Tech Stack

| Layer | Technology |
| ----- | ---------- |
| **Frontend** | React 19 (Vite), Axios, Custom Dark-Mode Glassmorphism CSS |
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Database** | MongoDB Atlas / Local MongoDB / Auto Local Storage Fallback (`grades_db.json`) |
| **AI / Vision** | Google Gemini (`gemini-3.6-flash` via `google-genai` SDK) |
| **Agentic Orchestration** | LangChain (`langchain-google-genai` with Structured Pydantic Outputs) |

---

## Project Structure

```
GRADEOPS/
├── backend/
│   ├── main.py              # FastAPI entry point, CORS, routes & database handlers
│   ├── agentic_grader.py    # LangChain agent orchestration & multi-question grading logic
│   ├── plagiarism_agent.py  # Plagiarism detection agent for semantic anomaly tracking
│   ├── vision_engine.py     # Gemini Vision multimodal image-to-text OCR wrapper
│   ├── database.py          # MongoDB standalone connection utility
│   ├── requirements.txt     # Python ecosystem dependencies (FastAPI, LangChain, etc.)
│   ├── rubric.json          # Evaluation rubric schema & default criteria
│   ├── grades_db.json       # Auto-generated local storage database fallback
│   └── .env                 # Environment secrets (GEMINI_API_KEY, MONGODB_URI)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Core UI with tab navigation, keyboard shortcuts & grading workflows
│   │   ├── App.css          # Dark-mode glassmorphism styling
│   │   └── main.jsx         # Vite entry script
│   ├── package.json         # Frontend package manifest
│   └── vite.config.js       # Vite configuration
│
├── sample_exams/            # Ready-to-use sample student exam scans for testing
│   ├── student1_alex_johnson.jpg  # Full score (10/10) sample exam
│   └── student2_maya_patel.jpg    # Partial credit (7/10) sample exam
│
├── .gitignore
├── LICENSE                  # MIT License
└── README.md
```

---

## Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher & npm
- **Google Gemini API Key** ([Get one from Google AI Studio](https://aistudio.google.com/app/apikey) or [Google Cloud Console](https://console.cloud.google.com/apis/credentials))
- *(Optional)* **MongoDB Atlas** account (or local MongoDB). If not configured, GradeOps automatically uses its built-in local database.

---

## Local Setup

### 1. Clone & Navigate

```bash
git clone https://github.com/sonowalvaibhav/gradeops.git
cd gradeops
```

### 2. Backend Setup (FastAPI)

```powershell
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate        # Windows (PowerShell)
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (create .env file)
# Add your GEMINI_API_KEY inside backend/.env

# Start the backend server
uvicorn main:app --reload --port 8000
```

- **Backend URL:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

### 3. Frontend Setup (React + Vite)

Open a **new terminal window**:

```powershell
# Navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start Vite development server
npm run dev
```

- **Frontend Application:** `http://localhost:5173`

---

## Sample Exam Testing

Ready-to-use exam images are located in the [`sample_exams/`](sample_exams/) folder:

1. Open `http://localhost:5173` in your browser.
2. Select **Instructor** mode.
3. In **Session Context & Batch Assets**:
   - Enter Student ID: `Alex Johnson`
   - Click **Browse** and select `sample_exams/student1_alex_johnson.jpg`.
4. Click **Run Pipeline** to view OCR extraction and automated question grading!
5. In the TA review card, press <kbd>Enter</kbd> to **Approve** and save the grade to the Class Roster.

---

## Environment Variables

Configure your `backend/.env` file with the following keys:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration (Optional - falls back to local JSON storage if offline)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=gradeops
```

> ⚠️ **Security Notice:** Never commit `.env` containing live secrets. It is already included in `.gitignore`.

---

## API Reference

Interactive OpenAPI documentation is available at `/docs` (Swagger UI) when the backend is running.

| Method | Endpoint | Description | Role |
| ------ | -------- | ----------- | ---- |
| `POST` | `/api/extract` | Upload exam image and perform Gemini Vision OCR | All |
| `POST` | `/api/grade` | Run Agentic Grader against custom rubric JSON | All |
| `POST` | `/api/check-plagiarism` | Compare two answers for shared logic anomalies | Instructor |
| `POST` | `/api/save-grade` | Save finalized student grade & feedback to database | TA / Instructor |
| `GET` | `/api/grades` | Fetch all saved grades for Class Roster | Instructor |
| `DELETE` | `/api/grades/{id}` | Delete a grade entry from the Class Roster | Instructor |

---

## Keyboard Shortcuts

The review dashboard is optimized for rapid grading throughput:

| Key | Action |
| --- | ------ |
| <kbd>Enter</kbd> | Approve AI-proposed grade and save to database |
| <kbd>Space</kbd> | Open manual score & feedback override panel |
| <kbd>Esc</kbd> | Cancel override and return to inspection card |

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
