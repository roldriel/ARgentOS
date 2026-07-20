# ARgentOS

ARgentOS is a state-based agent orchestration protocol governed by the `.agents/` directory.

## Protocol

The full protocol entry point is [`AGENTS.md`](AGENTS.md).

## Testing the protocol

To validate the `.agents/` workflow, a Flask ABM-style microservice with endpoints, validations, persistence, and tests is used as a model. This microservice is only a test model and may not be available depending on the tests executed at any given time.

## Quick start

Read [`AGENTS.md`](AGENTS.md) to learn how to use the protocol.

## Implementation plans

All implementation plans generated for this project by agents (or otherwise) must be placed in the `plans/` directory at the repository root.
