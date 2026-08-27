# GradeOps · AI-Powered Examination Grading & Academic Integrity System

> **Human-in-the-Loop exam grading powered by Vision-Language Models, Agentic LLMs, and a high-throughput TA review interface.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square\&logo=react\&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square\&logo=mongodb\&logoColor=white)](https://mongodb.com/atlas)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

### Project Team

* **Himanshu Kumar** — 230122020
* **Akhil Lavudya** — 230122026
* **Vaibhav Sonowal** — 230122062

---

## Contents

* [Project Introduction](#project-introduction)
* [System Architecture](#system-architecture)
* [Key Capabilities](#key-capabilities)
* [Technology Stack](#technology-stack)
* [Directory Structure](#directory-structure)
* [Requirements](#requirements)
* [Getting Started Locally](#getting-started-locally)
* [Configuration Variables](#configuration-variables)
* [API Endpoints](#api-endpoints)
* [User Roles & Access](#user-roles--access)
* [Review Shortcuts](#review-shortcuts)
* [Contribution Guide](#contribution-guide)
* [License](#license)

---

## Project Introduction

Evaluating handwritten examination papers manually can be slow, inconsistent, and influenced by grader fatigue. **GradeOps** addresses these limitations through a three-step AI-assisted workflow:

1. **Extract** — OCR and Vision models powered by Google Gemini 2.5 Flash convert handwritten student answers from bulk PDF scans into structured text.
2. **Evaluate** — An Agentic LLM assesses each response against instructor-defined JSON rubrics, assigns partial marks where appropriate, and produces structured reasoning for the awarded score.
3. **Review** — A high-throughput review interface presents AI-generated grades to TAs, allowing them to approve or modify results through quick keyboard interactions.

The result is a scalable and auditable evaluation workflow that improves grading consistency while keeping human reviewers involved in the final decision-making process.

---

## System Architecture

```text
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
│  └──────────────┘                │  │  Gemini 2.5 Flash  │  │
│                                  │  │  (OCR + Grading)   │  │
│                                  │  └────────────────────┘  │  │
│                                  │           │              │  │
│                                  │  ┌────────▼───────────┐  │  │
│                                  │  │   MongoDB Atlas     │  │
│                                  │  │   (Grades, Roster)  │  │
│                                  │  └────────────────────┘  │  │
│                                  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Capabilities

### 🧠 Autonomous Multi-Question Evaluation

GradeOps can process complete handwritten examination PDFs in batches. The LangChain-powered grading agent separates answer sheets into individual questions, evaluates responses using predefined JSON rubrics, assigns partial credit when applicable, and generates explanations for the assigned marks.

### 👁️ Handwritten Answer Extraction

Google Gemini 2.5 Flash is used to extract and transcribe handwritten responses from scanned examination papers. The system can work with varied handwriting styles, crossed-out responses, and multi-page answer sheets.

### 🕵️ Reasoning-Based Similarity Analysis

The plagiarism analysis system looks beyond direct text similarity. It also examines unusual similarities in reasoning patterns and logical structures, such as multiple students following an identical incorrect approach, which may indicate copied work.

### ✏️ Human-Supervised Review Workflow

The TA review interface presents the student's answer image alongside the AI-generated evaluation. Teaching assistants can quickly approve the suggested grade, manually modify the score, or edit feedback before saving the final result. Keyboard shortcuts help make the review process faster and more efficient.

### 🗄️ Centralized Grade Roster

MongoDB Atlas stores finalized grades, structured feedback, and student identifiers. The Instructor dashboard provides an up-to-date overview of the class roster and supports exporting grade data.

### 🔐 Access Control by Role

| Role                   | Capabilities                                                            |
| ---------------------- | ----------------------------------------------------------------------- |
| **Instructor**         | Upload exams, define rubrics, view full roster, run plagiarism analysis |
| **Teaching Assistant** | Access grading review queue, approve/override AI grades                 |

---

## Technology Stack

| Layer                     | Technology                                  |
| ------------------------- | ------------------------------------------- |
| **Frontend**              | React 18 (Vite), Axios, Custom CSS          |
| **Backend**               | Python 3.11+, FastAPI, Uvicorn              |
| **Database**              | MongoDB Atlas                               |
| **AI / Vision**           | Google Gemini 2.5 Flash                     |
| **Agentic Orchestration** | LangChain (Structured Outputs via Pydantic) |
| **OCR Models (alt.)**     | Hugging Face Nougat / Qwen-VL               |

---

## Directory Structure

```text
GRADEOPS/
├── backend/
│   ├── main.py              # FastAPI application entry point, routes, and CORS configuration
│   ├── agentic_grader.py    # LangChain orchestration and Gemini-based multi-question grading logic
│   ├── plagiarism_agent.py  # AI reasoning agent for identifying shared semantic logic anomalies
│   ├── vision_engine.py     # Gemini Vision wrapper for multimodal image-to-text extraction
│   ├── database.py          # MongoDB Atlas connection and database initialization
│   ├── requirements.txt     # Backend dependencies including FastAPI, LangChain, and related packages
│   └── rubric.json          # Local backup for validating the grading criteria schema
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI containing dashboard tabs and keyboard shortcut handling
│   │   ├── App.css          # Custom dark-mode glassmorphism styling and interface design
│   │   └── main.jsx         # Vite entry point responsible for mounting the React application
│   ├── package.json         # Node.js dependency and project configuration manifest
│   └── vite.config.js       # Vite development server configuration
│
├── .gitignore               # Rules preventing virtual environments and secret files from being committed
├── LICENSE                  # MIT open-source license documentation
└── README.md                # Project overview and technical setup documentation
```

---

## Requirements

Before setting up the project, ensure that the following tools and services are available:

* **Python** 3.11 or later
* **Node.js** 18 or later
* A **MongoDB Atlas** account (the free tier is sufficient)
* A **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

---

## Getting Started Locally

### 1. Download the Repository

```bash
git clone https://github.com/sonowalvaibhav/gradeops.git
cd gradeops
```

### 2. Configure the Backend

```bash
# Move into the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install the required packages
pip install -r requirements.txt

# Create your environment configuration file
cp .env.example .env

# Start the FastAPI development server
uvicorn main:app --reload --port 8000
```

The backend API will run at `http://localhost:8000`.

Interactive API documentation is available at `http://localhost:8000/docs`.

### 3. Configure the Frontend

Open another terminal and run:

```bash
# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start the Vite development server
npm run dev
```

The frontend application will be available at `http://localhost:5173`.

---

## Configuration Variables

Inside the `backend/` directory, create a `.env` file based on `.env.example`:

```env
# AI
GEMINI_API_KEY=your_google_gemini_api_key_here

# Database
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/gradeops
MONGODB_DB_NAME=gradeops

# Auth
SECRET_KEY=your_jwt_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=480

# App
ENVIRONMENT=development        # development | production
ALLOWED_ORIGINS=http://localhost:5173
```

> ⚠️ **Do not commit your `.env` file to the repository.** It is already included in `.gitignore`.

---

## API Endpoints

When the backend server is running, complete interactive API documentation is available through `/docs` using Swagger UI and through `/redoc`.

| Method  | Endpoint                     | Description                              | Role       |
| ------- | ---------------------------- | ---------------------------------------- | ---------- |
| `POST`  | `/api/exams/upload`          | Upload scanned examination PDFs in bulk  | Instructor |
| `POST`  | `/api/rubrics`               | Create or modify a grading rubric        | Instructor |
| `POST`  | `/api/grading/run`           | Start the complete AI grading workflow   | Instructor |
| `GET`   | `/api/grading/queue`         | Retrieve papers waiting for TA review    | TA         |
| `PATCH` | `/api/grading/{id}/approve`  | Accept the AI-generated grade            | TA         |
| `PATCH` | `/api/grading/{id}/override` | Submit a manually modified grade         | TA         |
| `GET`   | `/api/roster`                | Retrieve the complete class grade roster | Instructor |
| `POST`  | `/api/plagiarism/scan`       | Run plagiarism analysis on submissions   | Instructor |

---

## User Roles & Access

GradeOps uses JWT-based authentication and provides two primary user roles:

* **`INSTRUCTOR`** — Has complete access to the system, including exam uploads, rubric management, roster access, plagiarism analysis, and grading workflow controls.
* **`TA`** — Has access to the human review queue, where AI-generated grades can be reviewed, approved, or manually overridden. TAs cannot access rubric configurations or the complete class roster.

---

## Review Shortcuts

The TA review interface supports keyboard shortcuts for a faster grading workflow:

| Key       | Action                                   |
| --------- | ---------------------------------------- |
| `Enter`   | Approve the suggested grade and continue |
| `Space`   | Open the manual score override panel     |
| `←` / `→` | Move between submissions                 |
| `Esc`     | Cancel the override and return to review |

---

## Contribution Guide

Contributions are welcome. To contribute to the project:

1. Fork the repository and create a new feature branch:

```bash
git checkout -b feat/your-feature
```

2. Make your changes while keeping commits focused and descriptive.
3. Verify that the backend passes the required checks:

```bash
ruff check .
mypy .
```

4. Create a pull request targeting the `main` branch and clearly explain the changes made.

For larger features or significant architectural changes, opening an issue first to discuss the proposed approach is recommended.

---

## License

This project is released under the **MIT License**. Refer to the [LICENSE](LICENSE) file for complete details.

---
