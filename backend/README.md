# Portuguese Learning API

An LLM-assisted competency-based Portuguese (Brazilian) learning system. May add other languages in the future

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- uv (package manager)

## Setup

### 1. Install dependencies
```bash
uv sync
```

### 2. Configure environment

Create an env file

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/portuguese_learning
```

----------

### 3. Run database migrations

```
uv run alembic upgrade head
```

----------

### 4. Seed competency data

```
uv run python -m scripts.seed_competencies
```

----------

### 5. Start the API

```
uv run uvicorn app.main:app --reload
```

API will be available at:

```
http://localhost:8000
```