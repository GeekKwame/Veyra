# Veyra — Career Learning & Mastery for All Professions

> **Discover → Learn → Practice → Build → Assess → Prove → Career-Ready**

Veyra is a free, career-agnostic learning platform that optimizes for **"What can this person actually DO?"** rather than "How many courses has this person watched?" It provides structured career discovery, deterministic prerequisite roadmaps, verified legally free learning resources, authentic cross-disciplinary project rubrics, and contextual AI mentoring.

---

## 🏛 Architecture Overview

Veyra uses a **Decoupled Architecture**:
- **Backend (`/backend`):** Python 3.12+ / Django 5 / Django REST Framework, Celery background workers, PostgreSQL 16 (`pgvector`), and Redis.
- **Frontend (`/frontend`):** Next.js 15 (React 19, TypeScript), accessible CSS Design Tokens (WCAG AA), and Server Components.
- **Admin Studio:** Native Django Admin for curriculum curators to manage careers, competencies, skills, prerequisite graphs, and free resource verification states.

---

## 🚀 Quickstart Guide

### 1. Backend Setup (Django)

```bash
cd backend

# Activate Python 3.12 virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies (already prepared in .venv)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed 4 diverse careers (Developer, Medical Coding, Bookkeeper, Electrician)
python manage.py loaddata apps/careers/fixtures/seed_careers.json

# Run test suite (8 core DAG & pacing tests)
pytest

# Start backend API server (runs at http://127.0.0.1:8000)
python manage.py runserver
```

### 2. Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Start local development server (runs at http://localhost:3000)
npm run dev
```

---

## 🔬 Core Algorithms Implemented

1. **Deterministic DAG Prerequisite Engine (`apps/careers/engine/dag.py`):**
   - Kahn's algorithm for cycle detection and topological sorting.
   - Dynamic resolution of multi-level milestone tiers.
   - Enforced validation rules preventing circular skill dependencies on database save.

2. **Adaptive Pacing Engine (`apps/roadmaps/engine/pacing.py`):**
   - Calculates projected completion dates based on remaining hours and weekly commitment.
   - Seamless schedule recalibration without modifying completed skill milestones.

3. **Reactive Downstream Unlocking (`apps/roadmaps/models.py`):**
   - When a skill transitions to `MASTERED`, downstream skills automatically evaluate prerequisite fulfillment and transition from `LOCKED` to `AVAILABLE`.

---

## 📁 Repository Structure

```
Veyra/
├── backend/                          # Django 5 Backend
│   ├── veyra_core/                   # Settings, URLs, Celery, WSGI/ASGI
│   ├── apps/
│   │   ├── accounts/                 # Custom User, Profile, Auth
│   │   ├── careers/                  # Career, Competencies, Skills, DAG engine
│   │   ├── roadmaps/                 # UserRoadmaps, Progress, Pacing engine
│   │   ├── projects/                 # Project briefs, Rubric schemas, Submissions
│   │   ├── assessments/              # Quizzes, questions, server-side grading
│   │   └── mentor/                   # Contextual AI Socratic Mentor service
│   ├── manage.py
│   └── requirements.txt
├── frontend/                         # Next.js 15 Frontend
│   ├── src/
│   │   ├── app/                      # App router layout & pages
│   │   └── styles/                   # Accessible CSS design tokens & utilities
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml                # PostgreSQL 16 (pgvector) & Redis 7
├── README.md
└── .gitignore
```
