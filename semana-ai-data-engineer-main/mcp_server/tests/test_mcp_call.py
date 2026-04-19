from mcp_server.server import execute_task

# simulate what Continue would do

def run():
    print("\n--- TEST: business_analysis ---")
    result = execute_task(task_name="business_analysis")
    print(result)

    print("\n--- TEST: analyze_reviews ---")
    result = execute_task(task_name="analyze_reviews")
    print(result)

    print("\n--- TEST: get_models ---")
    result = execute_task(task_name="get_models")
    print(result)


if __name__ == "__main__":
    run()