from fastapi import APIRouter
from .live_data import get_live_data, process_live_data

router = APIRouter()

# Risk ve stress hesaplama endpoint'i
@router.get("/calculate-risk")
def calculate_risk(amount: float = 100000, payment_delay_days: float = 5, customer_score: float = 75, exposure_ratio: float = 0.30):
    live_data = get_live_data()  # Canlı veriyi al
    processed_data = process_live_data(live_data)  # Veriyi işleyelim
    
    # Risk hesaplama
    # Örnek olarak basit bir risk hesaplama
    risk_score = amount * (processed_data["USD/TRY"] / 1000)  # Canlı veriye dayalı risk hesaplama

    # Sonuçları döndür
    return {
        "risk_score": risk_score,
        "processed_data": processed_data,
    }
