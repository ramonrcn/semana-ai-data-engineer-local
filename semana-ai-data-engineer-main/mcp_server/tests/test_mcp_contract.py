from mcp_server.orchestrator import run_task


def run_tests():
    print("\n--- test_business_analysis_exploration ---")
    result = run_task("business_analysis")
    assert result["status"] == "success"
    assert "COUNTS" in result["result"]
    print("✅ Passed")

    print("\n--- test_business_analysis_executive ---")
    result = run_task(
        "business_analysis",
        intent="metrics=average_order_value"
    )
    assert result["status"] == "success"
    assert "EXECUTIVE SUMMARY" in result["result"]
    print("✅ Passed")

    print("\n--- test_analyze_reviews ---")
    result = run_task("analyze_reviews")
    assert result["status"] == "success"
    assert "REVIEW STRUCTURE" in result["result"]
    print("✅ Passed")

    print("\n--- test_normalization_metrics_goes_executive ---")
    result = run_task(
        "business_analysis",
        intent="metrics=average_order_value"
    )
    assert "EXECUTIVE SUMMARY" in result["result"]
    print("✅ Passed")

    print("\n--- test_business_analysis_output_quality ---")
    test_business_analysis_output_quality()
    print("✅ Passed")

    print("\n--- test_invalid_output_rejected ---")
    test_invalid_output_rejected()
    print("✅ Passed")

def test_business_analysis_output_quality():
    result = run_task("business_analysis", intent="metrics summary")

    output = result["result"]

    assert "EXECUTIVE SUMMARY" in output
    assert "Average" in output or "Value" in output
    assert len(output) > 100  # avoid empty/vague outputs

def test_invalid_output_rejected():
    from mcp_server.contracts import TaskResponse

    try:
        TaskResponse(
            status="success",
            task="business_analysis",
            result="EXECUTIVE SUMMARY\nnothing useful here",
            trace_id="test"
        )
    except Exception:
        print("✅ validation working")
        return

    raise AssertionError("Validation did not trigger")

if __name__ == "__main__":
    run_tests()