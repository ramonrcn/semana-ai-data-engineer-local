# Role 4 — Knowledge Selector

## Responsibility

Select the smallest sufficient knowledge set for the identified Capability.

---

## It should guarantee

- At least one Knowledge Document is selected.
- All selected knowledge belongs to the identified Capability.
- Returned knowledge is sufficient to execute the next pipeline stage.
- Documents are ranked according to the configured selection strategy.

---

## It should never

- Detect capabilities.
- Compile prompts.
- Modify knowledge content.
- Generate new knowledge.
- Execute inference.
- Access LLM providers.

---

## It receives

- One Runtime Capability.
- The user's inference objective.

---

## It returns

- A non-empty ordered collection of Knowledge Documents.