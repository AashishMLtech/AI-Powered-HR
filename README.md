# AI HR Automation Platform

A compact, beginner-friendly implementation of the HR automation project described in `document.md`.

## What Is Included

- FastAPI backend with JWT login
- SQLAlchemy models for HR users, jobs, candidates, applications, screening results, and social assets
- Job creation, JD review, approve/reject/regenerate flow
- Mock AI services for JD rewriting, social captions, CV screening, GitHub scoring, and AI-resume advisory flag
- Public application endpoint with consent guard and magic-byte file validation
- Candidate dashboard APIs with weighted combined scoring
- Minimal Next.js frontend pages for login, dashboard, jobs, candidates, social assets, and public apply form

The AI layer is intentionally simple. Gemini is the primary LLM provider, Groq is the fallback provider, and the local mock behavior keeps development usable when API keys are not configured.

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy ..\.env.example .env
python ..\scripts\seed_hr_user.py
uvicorn app.main:app --reload
```

Default HR login:

- Email: `hr@example.com`
- Password: `password123`

API docs: `http://localhost:8000/docs`

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## Important API Routes

- `POST /api/v1/auth/login`
- `GET /api/v1/jobs`
- `POST /api/v1/jobs`
- `PATCH /api/v1/jobs/{job_id}/approve`
- `PATCH /api/v1/jobs/{job_id}/reject`
- `POST /api/v1/jobs/{job_id}/regenerate`
- `GET /api/v1/jobs/{job_id}/public`
- `GET /api/v1/jobs/{job_id}/social-assets`
- `POST /api/v1/applications`
- `GET /api/v1/jobs/{job_id}/candidates`
- `GET /api/v1/candidates/{candidate_id}/screening`
- `PATCH /api/v1/candidates/{candidate_id}/linkedin-check`

## Architecture Notes

- No endpoint automatically accepts or rejects candidates.
- Scores are advisory only.
- Candidate consent is checked before database writes.
- File validation checks file bytes, not only the extension.
- The mock AI client makes the app usable without paid API keys.

## What I Would Build Next

- Real Gemini/Groq/OpenAI adapters
- Alembic migrations for production schema changes
- Real background worker mode for long-running AI jobs
- PDF/DOCX text extraction
- Playwright end-to-end tests
