# Role 2 — ProcessUserRequest

## Responsibility

Coordinate the Runtime inference pipeline by invoking the appropriate
components in the correct order and ensuring that each stage receives
the information required to fulfill its responsibility.

---

## It should guarantee

- Every pipeline stage is executed in the expected order.
- The output of one stage becomes the validated input of the next stage.
- The inference pipeline stops whenever a component cannot satisfy its contract.
- Infrastructure failures are propagated using the Runtime error strategy.
- Business components remain isolated from each other.

---

## It should never

- Detect capabilities.
- Select knowledge.
- Compile prompts.
- Communicate directly with an LLM provider.
- Execute business logic belonging to another component.
- Modify the output produced by another component except for orchestration purposes.

---

## It receives

- A valid Runtime inference request.

---

## It returns
- ProcessSuccess or RuntimeFailure, according to the Output Contract.

---

## Output Contract

ProcessUserRequest returns exactly one of:

- ProcessSuccess
  - represents a successful Runtime execution
  - contains the Runtime response

- RuntimeFailure
  - represents a failed Runtime execution
  - contains at least:
    - a machine-readable error code
    - a human-readable error message

Success and failure are mutually exclusive outcomes.

A Runtime failure must never be represented as a successful
empty response.

---

## Error Contract

Runtime errors are failures that occur after a valid RuntimeRequest
has entered the application pipeline.

Each Runtime component is responsible for signaling when it cannot
satisfy its own contract.

A Runtime failure must stop pipeline execution and must never be
represented as a successful empty response.

ProcessUserRequest is responsible for returning either:
- a successful Runtime response
- a structured Runtime failure

A structured Runtime failure must provide at least:
- a machine-readable error code
- a human-readable error message

Runtime failures must preserve the semantic meaning of the original
component failure.

---

## Dependencies

- Capability Detector
- Knowledge Selector
- Prompt Compiler
- LLM Adapter

---

## It must not know

- Provider implementation details.
- Knowledge retrieval implementation.
- Prompt compilation rules.
- Vector search algorithms.