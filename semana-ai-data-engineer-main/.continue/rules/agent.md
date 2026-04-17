## Task Execution (CRITICAL)

- ALWAYS call execute_task

## Mapping

- models → execute_task("models")

## Behavior

- NEVER read files
- NEVER generate code
- NEVER use any other tool

If you do not call execute_task, the answer is invalid.