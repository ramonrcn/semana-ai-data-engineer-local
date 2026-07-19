# PromptCompiler Specification

## 0. Design Philosophy
    The PromptCompiler is responsible only for composing prompts.

    It never performs retrieval.
    It never selects knowledge.
    It never modifies the objective.
    It only transforms RuntimeContext into a deterministic prompt.

## 1. Purpose
    The PromptCompiler is responsible for transforming a fully prepared RuntimeContext into a deterministic prompt ready to be consumed by a Large Language Model (LLM).

    It acts as the final composition stage of the runtime pipeline, ensuring that all required context is assembled into a consistent and predictable prompt while preserving the integrity of the provided RuntimeContext.

## 2. Component Contract
    The PromptCompiler receives a fully prepared RuntimeContext.
    It assumes capability detection has already completed.
    It assumes knowledge selection has already completed.
    It guarantees a deterministic prompt suitable for an LLM.

## 3. Responsibilities
    Produce a deterministic prompt from the provided RuntimeContext.
    Preserve all selected knowledge in the final prompt.
    Preserve the order of the knowledge returned by KnowledgeSelector.
    Preserve the order of every context element provided by RuntimeContext.
    
## 4. Non Responsibilities
    Never perform capability detection.
    Never retrieve knowledge.
    Never modify RuntimeContext.
    Never summarize knowledge.
    Never call LLMs.
    Never execute tools.

## 5. Inputs
    RuntimeContext containing:
        - Objective
        - Capability
        - Selected knowledge
        - EnvironmentTools

## 6. Outputs
    The PromptCompiler always returns:
        - A non-empty UTF-8 encoded prompt.
        - A deterministic prompt.
        - A prompt containing every required section.
        - The prompt contains every required section defined by Prompt Structure.

## 7. Prompt Structure
    Section ordering is defined exclusively by PromptCompiler.
    Optional sections are ommited when not present in RuntimeContext.
    Required sections are always present.
    Every section has a unique purpose.
    Sections never repeat.
    Sections are well-delimited.

    Structure follows this order:
        1 - System prompt.
        2 - Execution rules.
        3 - Objective.
        4 - Selected knowledge.
    Conversation history is intentionally omitted until RuntimeContext supports conversational context.

### 7.1 Prompt Sections
    System Prompt
        Defines the LLM behavior.
    Execution Rules
        Defines mandatory runtime constraints.
    Objective
        Defines the current user objective.
    Reference Knowledge
        Contains retrieved documents preserving KnowledgeSelector ordering.

## 8. Invariants
    Equivalent RuntimeContext always produces equivalent prompts.
    Prompt compilation has no side-effects.
    RuntimeContext is never mutated.
    Output is always a valid UTF-8 prompt.
    Section ordering is deterministic.
    No information is silently discarded.

## 9. Acceptance Criteria
    A PromptCompiler implementation is considered valid if it satisfies all of the following conditions:
        - Produces a deterministic prompt for equivalent RuntimeContext inputs.
        - Never mutates the provided RuntimeContext.
        - Preserves all selected knowledge.
        - Includes every required prompt section.
        - Omits optional sections when they contain no content.
        - Produces a non-empty UTF-8 encoded prompt.
        - Produces no side effects during compilation.
        - Never performs responsibilities owned by other runtime components.

## 10. Edge Cases
    The PromptCompiler must define deterministic behavior for at least the following situations:
        - RuntimeContext contains no selected knowledge.
        - RuntimeContext contains an empty conversation.
        - Objective is empty or missing.
        - Duplicate knowledge entries are present.
        - Optional sections contain no content.
        - Extremely large knowledge contexts.
        - Invalid or malformed RuntimeContext.

## 11. Future Extensions
    This specification intentionally allows future enhancements without changing the component responsibilities, including:
        - Support for multiple prompt formats.
        - Configurable prompt templates.
        - Multiple prompt composition strategies.
        - Prompt optimization stages.
        - Prompt validation before delivery.
        - Prompt instrumentation for evaluation and observability.

## 12. Out of Scope
    The PromptCompiler is explicitly not responsible for:
        - Knowledge retrieval
        - Capability detection
        - Context ranking
        - Token optimization
        - Prompt evaluation
        - LLM communication
        - Tool execution