from fastapi import FastAPI
from .api.risk import router as risk_router

app = FastAPI()

# API router'ını uygulamaya ekle
app.include_router(risk_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to ZENTRA API"}
