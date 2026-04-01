from typing import Dict, Any, List

def evaluate_trade_deep(payload: Dict[str, Any]) -> Dict[str, Any]:
    company_age = payload.get("company_age_years", 0)
    sector_match = payload.get("sector_match", False)
    has_cis = payload.get("has_cis", False)
    has_spec = payload.get("has_product_spec", False)
    has_coa = payload.get("has_coa", False)
    payment_terms = payload.get("payment_terms", "")
    qty = payload.get("monthly_quantity_mt", 0)
    offer_price = payload.get("offer_price", 0)
    benchmark_price = payload.get("benchmark_price", 0)

    realism = 100
    fraud = 0
    execution = 100

    flags: List[str] = []
    missing: List[str] = []
    actions: List[str] = []

    # --- Company ---
    if company_age < 3:
        realism -= 15
        fraud += 15
        flags.append("young_company")

    if not sector_match:
        realism -= 20
        fraud += 20
        flags.append("sector_mismatch")

    # --- Docs ---
    if not has_cis:
        realism -= 10
        missing.append("CIS")
    if not has_spec:
        realism -= 10
        missing.append("Product Spec")
    if not has_coa:
        realism -= 10
        missing.append("COA")

    # --- Price anomaly ---
    if benchmark_price > 0:
        diff = (benchmark_price - offer_price) / benchmark_price
        if diff > 0.15:
            realism -= 25
            fraud += 25
            flags.append("price_anomaly")

    # --- Quantity ---
    if qty > 15000:
        execution -= 20
        flags.append("high_volume_claim")

    # --- Payment ---
    if "LC" not in payment_terms.upper():
        fraud += 20
        flags.append("weak_payment_terms")

    # --- Clamp ---
    realism = max(0, min(100, realism))
    fraud = max(0, min(100, fraud))
    execution = max(0, min(100, execution))

    # --- Decision ---
    if fraud >= 60:
        action = "REJECT"
        note = "Fraud risk too high"
    elif realism < 50:
        action = "REVIEW"
        note = "Low realism"
    else:
        action = "PROCEED"
        note = "Acceptable"

    # --- Actions ---
    if fraud >= 40:
        actions.extend([
            "Request past Bill of Lading",
            "Require SGS inspection",
            "Verify warehouse stock"
        ])

    return {
        "trade_realism_score": realism,
        "fraud_risk_score": fraud,
        "execution_viability_score": execution,
        "flags": flags,
        "missing_proofs": missing,
        "recommended_actions": actions,
        "decision": {
            "action": action,
            "note": note,
            "confidence": round(1 - (fraud / 100), 2)
        },
        "blocks": [
            {"name": "company", "score": realism},
            {"name": "documents", "score": 100 - len(missing)*10},
            {"name": "pricing", "score": realism},
            {"name": "execution", "score": execution}
        ]
    }
