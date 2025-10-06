# Pixel Exo Sketch
AI models were used in development - Copilot, Claude, Gemini Pro


# 🚀 Project Setup & Execution
Prerequisites

Python 3.8+
Node.js 16+
pip and npm installed

Installation & Running
1. Backend (FastAPI)
bash# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
Backend will be available at: http://localhost:8000

2. Frontend (Vue)
bash# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
Frontend will be available at: http://localhost:5173 (or the port shown in terminal) or the public version (local backend required) https://exo-laser-learner-ce4u.vercel.app/

Quick Start

Start backend first (terminal 1):

bash   cd backend && uvicorn main:app --reload

Start frontend (terminal 2):

bash   cd frontend && npm run dev

Open browser at http://localhost:5173


API Documentation
Once backend is running, access interactive API docs at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
