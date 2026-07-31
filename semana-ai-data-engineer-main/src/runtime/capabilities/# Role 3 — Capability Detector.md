# Role 3 — Capability Detector

## Responsibility

Identify the Runtime capability that best matches the user's inference objective.

---

## It should guarantee

- Exactly one Capability is returned for every supported request.
- The selected Capability is the best deterministic match.
- Unsupported objectives are explicitly rejected.
- Ambiguous matches are never propagated downstream.
- A Runtime Capability is never considered valid without an associated Knowledge Base.

---

## It should never

- Retrieve knowledge.
- Rank documents.
- Compile prompts.
- Execute inference.
- Communicate with LLM providers.
- Make business decisions outside capability classification.

---

## It receives

- A validated Runtime inference request.

---

## It returns

- One Runtime Capability.

or

- UnsupportedCapabilityError

or

- AmbiguousCapabilityError