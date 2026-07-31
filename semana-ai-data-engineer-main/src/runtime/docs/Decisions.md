ADR-001

Capability Resolution Strategy

Decision

A Runtime inference request MUST resolve to exactly one Capability.

Rationale

The Runtime favors deterministic execution over capability composition.

Consequences

- CapabilityDetector returns exactly one Capability.
- Multiple matches are treated as an ambiguity error.
- No matches are treated as an unsupported request.
- Downstream components never need to decide which capability to use.