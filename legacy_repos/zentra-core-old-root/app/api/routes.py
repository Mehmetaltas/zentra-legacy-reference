from fastapi import APIRouter
from app.services.trade_deep_verification import evaluate_trade_deep
from app.services.trade_validation_matrix import run_trade_validation_matrix

router = APIRouter()

@router.get("/")
def root():
    return {"status": "ZENTRA CORE ACTIVE"}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/global/market")
def market():
    return {
        "market": {
            "usdtry": 30,
            "eurusd": 1.08,
            "gold": 2140,
            "oil": 89,
            "us10y": 4.4,
            "source": {"mode": "mixed"}
        },
        "pressure": {
            "level": "moderate",
            "reasons": ["fx_pressure"]
        }
    }

@router.get("/score")
def score():
    return {
        "final_risk_score": 66,
        "risk_band": "MID"
    }

@router.get("/stress")
def stress():
    return {
        "final_stress_score": 50,
        "stress_band": "MID"
    }

# TRADE ENGINE

@router.post("/trade/full-evaluate")
def trade_full(payload: dict):
    return evaluate_trade_deep(payload)

@router.get("/trade/validation-matrix")
def trade_matrix():
    return run_trade_validation_matrix(evaluate_trade_deep)
