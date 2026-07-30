# Role 1 — Request Gateway

## The Request Gateway is responsible for:
 - accepting inference requests from external clients and translating them into the Runtime's internal request representation.
 - if somehting goes wrong, it should send to Runtime a error message

## It should grant:
 - that the solicitation is never sent being empty or null

## The Request Gateway should Never:
 - know details from a provider
 - select knowledge
 - detect capabilities
 - execute inferences
 - apply Runtime business rules

## TODO: Define the Runtime error propagation strategy for invalid input and infrastructure failures.
-------
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

- A successful Runtime inference response.

or

- A structured Runtime error.

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