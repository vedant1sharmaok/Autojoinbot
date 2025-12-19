from fastapi import FastAPI
from db import db

app = FastAPI()


@app.get("/health")
async def health_check():
    status = {
        "bot": "ok",
        "database": "unknown"
    }

    try:
        await db.command("ping")
        status["database"] = "ok"
    except Exception:
        status["database"] = "down"

    return status
