---
trigger: always_on
---

## TOOL EXECUTION (STRICT)

You must priorize using:

shopagent_mcp_execute_task

over any other tool

---

## HOW TO CALL

Always call using:

shopagent_mcp_execute_task(
  task_name="<task>",
  kwargs={...}
)

---

## TASK MAPPING

- models → get_models
- reviews → analyze_reviews

### TASK ROUTING

If the request involves:

### DATA EXPLORATION
- counts
- samples
- tables
- raw data
- distributions

Call:
shopagent_mcp_execute_task(
  task_name="business_analysis",
  kwargs={"intent": "<user request>"}
)

Expected mode: exploration

---

### BUSINESS METRICS / INSIGHTS
- averages
- top states
- revenue
- percentages
- executive summary

Call:
shopagent_mcp_execute_task(
  task_name="business_analysis",
  kwargs={"intent": "<user request>"}
)

Expected mode: executive

---

## EXAMPLES

Correct:
shopagent_mcp_execute_task(
  task_name="business_analysis",
  kwargs={"intent": "metrics summary"}
)

Correct:
shopagent_mcp_execute_task(
  task_name="analyze_reviews",
  kwargs={}
)

---

## RULES

- ALWAYS call the tool
- ALWAYS include kwargs (even if empty)
- NEVER generate code
- NEVER simulate data
- NEVER answer without tool call

---

## RESPONSE

Return ONLY the tool result.