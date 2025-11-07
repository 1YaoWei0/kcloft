# Back End Guide

## Create the folder structure

```bash
kcloft-backend/
 ├─ app/
 │   ├─ main.py              # FastAPI entrypoint
 │   ├─ core/                # config, settings
 │   │   └─ config.py
 │   ├─ models/              # SQLAlchemy models
 │   │   └─ question.py
 │   ├─ schemas/             # Pydantic schemas
 │   │   └─ question.py
 │   ├─ crud/                # DB operations
 │   │   └─ question.py
 │   ├─ routers/             # API endpoints
 │   │   └─ question.py
 │   └─ database.py          # DB session and engine
 ├─ requirements.txt
 └─ .env                     # environment variables
```