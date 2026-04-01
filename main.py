from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

# API'nin route'larını ekleyin
app.include_router(api_router)

# Giriş mesajı (isteğe bağlı)
@app.get("/")
def read_root():
    return {"message": "ZENTRA API is running."}
