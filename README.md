# Interview Question Generator

A full-stack AI-powered web app that generates 3 tailored interview questions
for any job title in seconds.

**Live demo:** YOUR_LIVE_URL  
**Built by:** YOUR_NAME

---

## What it does

You type a job title — "Customer Success Manager", "DevOps Engineer", "Nurse" —
and the app returns 3 thoughtful, role-specific interview questions:
one behavioral, one situational, one competency-based.

No generic questions. Every result is specific to the role.

---

## Why I built it this way

This was a 30-minute assignment. I chose to treat it like a production system
because that is how I build. Here are the decisions that matter:

**Three layers of input validation**  
Bad input never reaches the AI. The serializer catches blank and oversized input.
The validator catches gibberish and non-job words. The AI prompt catches anything
subtle that slips through. Each layer has one job.

**Provider fallback**  
If Groq goes down, the app automatically switches to Gemini. If both are down,
the user gets a clear error message — not a crash. The founder never gets a
call saying "the app is broken" because one API had an outage.

**Circuit breaker**  
If a provider fails repeatedly, the app stops calling it temporarily and
switches to the backup. This prevents wasting API quota on a provider that
is already down.

**Rate limiting**  
20 requests per IP per minute. Prevents a single bad actor from burning the
entire free API quota in minutes.

**Caching**  
The same job title submitted twice returns the cached result instantly.
No API call needed. This saves cost and makes the app faster for common roles.

**Prompt injection protection**  
User input is sandwiched between instructions. Someone typing
"ignore previous instructions" into the job title field has no effect.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Django + Django REST Framework |
| AI Provider (primary) | Groq — Llama 3.1 8B |
| AI Provider (fallback) | Google Gemini 2.0 Flash |
| Hosting (frontend) | Vercel |
| Hosting (backend) | YOUR_BACKEND_HOST |
| Containerisation | Docker + Docker Compose |

---

## How I used AI

I used Claude as a thinking partner throughout this build — not to write code
for me, but to pressure-test decisions. I would describe a problem, explain
my approach, and ask what could go wrong. The circuit breaker, the three-layer
validation, and the rate limiting all came from that process.

The prompt engineering was mine. I iterated on the AI prompt until it produced
consistent JSON output with role-specific questions and handled edge cases
like shorthand input ("PM" → "Product Manager") reliably.

---

## Project structure

```
backend/
  questions/
    ai_service.py     — AI calls, retry, circuit breaker, fallback, cache
    validators.py     — local input validation before any API call
    serializers.py    — DRF serializer, first line of defence
    views.py          — thin coordinator, rate limiting
    constants.py      — blocklists, allowlists, shared limits
    exceptions.py     — custom exceptions for clean error handling
    urls.py           — question app routing
  config/
    settings.py       — Django settings, cache config, logging
    urls.py           — root URL routing
  Dockerfile          — production container definition
  requirements.txt    — Python dependencies

frontend/
  src/
    App.jsx           — UI, state management, form handling
    api.js            — single file that knows the backend URL
    App.css           — all styles

docker-compose.yml    — runs backend locally with one command
```

---

## Running with Docker (recommended)

```bash
# 1. Clone the repo
git clone YOUR_REPO_URL
cd YOUR_REPO_NAME

# 2. Set up environment variables
cp backend/.env.example backend/.env
# Open backend/.env and fill in:
#   AI_API_KEY=your_key_here
#   AI_PROVIDER=groq
#   DJANGO_SECRET_KEY=any_random_string
#   DEBUG=False

# 3. Start the backend
docker compose up --build
```

Backend runs at `http://localhost:8000`  
Health check: `http://localhost:8000/api/health/`  
Docker automatically restarts the container if health checks fail.

---

## Running locally without Docker

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# create backend/.env with the variables above
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Yes | Any long random string |
| `AI_API_KEY` | Yes | Your Groq or Gemini API key |
| `AI_PROVIDER` | Yes | `groq` or `gemini` |
| `DEBUG` | No | `False` in production |
| `ALLOWED_HOSTS` | No | Your backend domain |

---

## If I had more time

I would add an `/api/health/` endpoint that exposes circuit breaker state
per provider — which provider is serving requests, cache hit rate, and how
many requests were rate limited. Right now that information lives only in
logs. A founder should be able to see system health without reading logs.
