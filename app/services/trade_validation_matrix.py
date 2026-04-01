from typing import Callable, Dict, Any, List

def run_trade_validation_matrix(evaluator: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    test_cases = [
        {
            "id": "case_good",
            "payload": {
                "company_age_years": 10,
                "sector_match": True,
                "has_cis": True,
                "has_product_spec": True,
                "has_coa": True,
                "payment_terms": "LC",
                "monthly_quantity_mt": 2000,
                "offer_price": 1200,
                "benchmark_price": 1250
            },
            "expected": "PROCEED"
        },
        {
            "id": "case_fraud",
            "payload": {
                "company_age_years": 1,
                "sector_match": False,
                "has_cis": False,
                "has_product_spec": False,
                "has_coa": False,
                "payment_terms": "TT",
                "monthly_quantity_mt": 20000,
                "offer_price": 800,
                "benchmark_price": 1300
            },
            "expected": "REJECT"
        }
    ]

    results: List[Dict[str, Any]] = []
    passed = 0

    for case in test_cases:
        out = evaluator(case["payload"])
        decision = out["decision"]["action"]
        ok = decision == case["expected"]

        if ok:
            passed += 1

        results.append({
            "case_id": case["id"],
            "label": case["expected"],
            "actual": out,
            "comparison": {
                "all_passed": ok
            }
        })

    total = len(test_cases)
    failed = total - passed
    rate = round((passed / total) * 100, 2)

    return {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": failed,
        "pass_rate": rate,
        "results": results
    }
