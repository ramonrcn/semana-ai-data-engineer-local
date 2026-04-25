from mcp_server.orchestrator import run_task
from mcp_server.tests.test_mcp_contract import run_tests as run_contract_tests


def assert_success(result):
    assert result["status"] == "success"
    assert "result" in result


def assert_error(result):
    assert result["status"] == "error"


def run_tests():

    print("\n=== 1. BASIC TASK EXECUTION ===")

    result = run_task("ping")
    assert_success(result)
    print("✅ ping")

    result = run_task("get_models")
    assert_success(result)
    print("✅ get_models")

    result = run_task("business_analysis")
    assert_success(result)
    assert "COUNTS" in result["result"]
    print("✅ business_analysis (exploration)")

    result = run_task("analyze_reviews")
    assert_success(result)
    assert "REVIEW STRUCTURE" in result["result"]
    print("✅ analyze_reviews")


    print("\n=== 2. EXECUTIVE MODE DETECTION ===")

    result = run_task(
        "business_analysis",
        intent="metrics=average_order_value"
    )
    assert_success(result)
    assert "EXECUTIVE SUMMARY" in result["result"]
    print("✅ executive mode via intent")


    print("\n=== 3. CONTINUE-STYLE BROKEN INPUTS ===")

    # kwargs as string (classic Continue bug)
    result = run_task(
        "business_analysis",
        kwargs="metrics=average_order_value"
    )
    assert_success(result)
    assert "EXECUTIVE SUMMARY" in result["result"]
    print("✅ kwargs as string handled")

    # nested kwargs (real log case)
    result = run_task(
        "business_analysis",
        kwargs={"intent": "metrics summary"}
    )
    assert_success(result)
    assert "EXECUTIVE SUMMARY" in result["result"]
    print("✅ nested kwargs handled")

    # empty kwargs
    result = run_task(
        "business_analysis",
        kwargs=""
    )
    assert_success(result)
    assert "COUNTS" in result["result"]
    print("✅ empty kwargs fallback")


    print("\n=== 4. TASK ALIASING ===")

    result = run_task("models")
    assert_success(result)
    print("✅ alias: models → get_models")

    result = run_task("database")
    assert_success(result)
    print("✅ alias: database → business_analysis")

    result = run_task("reviews")
    assert_success(result)
    print("✅ alias: reviews → analyze_reviews")


    print("\n=== 5. INVALID TASK HANDLING ===")

    result = run_task("non_existent_task")
    assert_error(result)
    print("✅ invalid task handled")


    print("\n=== 6. FORMAT VALIDATION ===")

    result = run_task("business_analysis")
    text = result["result"]

    assert "📊" in text
    assert "CUSTOMERS" in text.upper()
    print("✅ formatting looks correct")


    print("\n=== 7. HARD EDGE CASES ===")

    # garbage input
    result = run_task("business_analysis", kwargs=123)
    assert_success(result)
    print("✅ numeric kwargs handled")

    result = run_task("business_analysis", intent=None)
    assert_success(result)
    print("✅ None intent handled")

    print("\n=== 8. CONTRACT TESTS ===")
    run_contract_tests()
    print("✅ Invalid output rejected")

    print("\n🔥 ALL TESTS PASSED 🔥")


if __name__ == "__main__":
    run_tests()