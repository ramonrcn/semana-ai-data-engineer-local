# Role 1 — Request Gateway

## The Request Gateway is responsible for:
 - accepting inference requests from external clients and translating them into the Runtime's internal request representation.
 - if something goes wrong before a valid RuntimeRequest can be produced, the Gateway must stop processing and surface an explicit Gateway error.

## It should grant:
 - that the solicitation is never sent being empty or null

## The Request Gateway should Never:
 - know details from a provider
 - select knowledge
 - detect capabilities
 - execute inferences
 - apply Runtime business rules

## Error Contract

The Request Gateway owns failures that occur before a valid
RuntimeRequest can be produced.

Gateway errors include:
- malformed external input
- failure to translate the external request
- unavailable required request data
- empty or null objective

A Gateway failure must stop request processing.
An invalid request must never reach ProcessUserRequest.

Gateway failures must be represented as explicit Gateway errors
rather than successful empty requests.
