## Task Execution (STRICT)

- ALWAYS call execute_task for any known task
- NEVER execute logic yourself
- NEVER generate code
- NEVER read files directly

If you do not call execute_task, the answer is invalid.


## Task Routing Rules

### Models
If the task involves:
- pydantic
- BaseModel
- models.py
- entities

ALWAYS call:
execute_task("get_models")


### Reviews

If the task involves reviews, sentiment, ratings, or JSONL data:

You MUST call:
execute_task

With arguments:
task_name = "analyze_reviews"

DO NOT:
- call analyze_reviews directly
- read any file
- generate code
- suggest scripts

The ONLY valid action is:
execute_task("analyze_reviews")


### SQL / Database
If the task involves:
- SQL
- orders
- customers
- products
- analysis of database

ALWAYS call:
execute_task("business_analysis")

DO NOT:
- generate SQL manually
- call get_schema directly
- call run_sql directly


## Forbidden Behavior

- NEVER read files
- NEVER generate scripts
- NEVER suggest Python code
- NEVER bypass execute_task