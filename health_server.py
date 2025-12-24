from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

def run_health_server():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="warning"
    )
