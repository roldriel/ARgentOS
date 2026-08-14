---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: taxonomy
domain: cross-cutting
version: "1.0.0"
---

# Protocol Taxonomy

Master dictionary of the ARgentOS protocol. It is the single source of truth that relates
domains, lifecycles, states, artifacts, workflows, harness policies, actors, roles and workers.

The `version` field in the front matter is the format version of this dictionary,
independent of the protocol version declared in `.agents/VERSION`.

Rules:

- Every entity carries a `domain` (`core`, `discovery`, `system`, `cross-cutting`).
- States are referenced as `<domain>:<state>` (e.g. `core:ANALYZING_TASK`).
- Harness IDs use the domain namespace: `HNN` (core), `DNN` (discovery), `SNN` (system).
  `H13-protocol-taxonomy` is the documented cross-cutting exception (kept in the core
  `H` namespace for historical reasons after the protocol was split into domains).
  `H08` is intentionally omitted, `H12` is free (former `H12` became `D01`), and
  `H14` is intentionally omitted (unassigned); none of them is reported as missing.
- Protocol files reference this dictionary through a YAML metadata block; they do not
  duplicate the relationships defined here.
- This dictionary is validated by the Orchestrator's judgment against harness
  policy `.agents/harness/policies/H13-protocol-taxonomy.md`.

```yaml
domains:
  core:
    root: .agents/orchestrators/core/
    harness_prefix: H
    orchestrator_role: orchestrator
  discovery:
    root: .agents/orchestrators/discovery/
    harness_prefix: D
    orchestrator_role: discovery_orchestrator
  system:
    root: .agents/orchestrators/system/
    harness_prefix: S
    orchestrator_role: argentos
  cross-cutting:
    root: .agents/
    harness_prefix: null

lifecycles:
  system:
    domain: system
    description: Bootstrap of the protocol runtime environment (ArgentOS System Agent).
  task:
    domain: core
    description: Task understanding (analysis, intent confirmation, specification).
  context:
    domain: core
    description: Context gathering and validation.
  planning:
    domain: core
    description: Execution planning.
  execution:
    domain: core
    description: Execution and verification.
  final:
    domain: core
    description: Terminal states.
  exception:
    domain: core
    description: Clarification and recovery states.
  discovery:
    domain: discovery
    description: Knowledge-base discovery run.

entities:

  # -------------------------------------------------------------------------
  # States — domain: core
  # -------------------------------------------------------------------------
  "core:SYSTEM_READY":
    kind: state
    domain: core
    lifecycle: system
    name: System Ready
    description: The System Agent verified protocol health; the Orchestrator may accept a task.
    previous:
      - system:ENVIRONMENT_READY
    next:
      - core:TASK_RECEIVED
    artifacts_input: []
    artifacts_output: []
    workflow: .agents/orchestrators/system/workflow/00-bootstrap.md
    harness:
      - S00-system-ready
    actor: system_agent
    profile: null

  "core:TASK_RECEIVED":
    kind: state
    domain: core
    lifecycle: task
    name: Task Received
    description: A user request has been received; not analyzed yet.
    previous:
      - core:SYSTEM_READY
      - core:NEEDS_CLARIFICATION
    next:
      - core:ANALYZING_TASK
    artifacts_input: []
    artifacts_output:
      - SESSION_LOG.md
      - SESSION_BRIEF.md
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:ANALYZING_TASK":
    kind: state
    domain: core
    lifecycle: task
    name: Analyzing Task
    description: Analyze the user request and identify what is required to define the task.
    previous:
      - core:TASK_RECEIVED
      - core:CONFIRMING_INTENT
    next:
      - core:BUILDING_TASK_SPECIFICATION
      - core:CONFIRMING_INTENT
      - core:NEEDS_CLARIFICATION
      - core:PLANNING
      - core:RECOVERY
    artifacts_input:
      - SESSION_BRIEF.md
    artifacts_output:
      - TASK_ANALYSIS.md
    workflow: .agents/orchestrators/core/workflow/00-analyze-task.md
    harness:
      - H00-task-analysis
    actor: orchestrator
    profile: task_analyst

  "core:CONFIRMING_INTENT":
    kind: state
    domain: core
    lifecycle: task
    name: Confirming Intent
    description: Reflect the interpreted intent back to the user for confirmation or correction.
    previous:
      - core:ANALYZING_TASK
    next:
      - core:BUILDING_TASK_SPECIFICATION
      - core:ANALYZING_TASK
      - core:NEEDS_CLARIFICATION
      - core:RECOVERY
    artifacts_input:
      - TASK_ANALYSIS.md
    artifacts_output:
      - INTENT_REFLECTION.md
    workflow: .agents/orchestrators/core/workflow/01-confirm-intent.md
    harness:
      - H11-intent-reflection
    actor: orchestrator
    profile: intent_reflector

  "core:BUILDING_TASK_SPECIFICATION":
    kind: state
    domain: core
    lifecycle: task
    name: Building Task Specification
    description: Transform the analyzed request into a structured task specification.
    previous:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
    next:
      - core:TASK_READY
      - core:NEEDS_CLARIFICATION
      - core:RECOVERY
    artifacts_input:
      - TASK_ANALYSIS.md
      - INTENT_REFLECTION.md
    artifacts_output:
      - TASK_SPECIFICATION.md
    workflow: .agents/orchestrators/core/workflow/02-build-task-specification.md
    harness:
      - H01-task-specification
    actor: orchestrator
    profile: task_specification_writer

  "core:NEEDS_CLARIFICATION":
    kind: state
    domain: core
    lifecycle: exception
    name: Needs Clarification
    description: Required information is missing or ambiguous; ask the user before continuing.
    previous:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
      - core:BUILDING_TASK_SPECIFICATION
      - core:GATHERING_CONTEXT
      - core:VALIDATING_CONTEXT
      - core:PLANNING
      - core:RECOVERY
    next:
      - core:TASK_RECEIVED
    artifacts_input: []
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:TASK_READY":
    kind: state
    domain: core
    lifecycle: context
    name: Task Ready
    description: The task has a validated specification and can begin context gathering.
    previous:
      - core:BUILDING_TASK_SPECIFICATION
    next:
      - core:GATHERING_CONTEXT
    artifacts_input:
      - TASK_SPECIFICATION.md
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:GATHERING_CONTEXT":
    kind: state
    domain: core
    lifecycle: context
    name: Gathering Context
    description: Collect the information required to understand the execution environment.
    previous:
      - core:TASK_READY
    next:
      - core:CONTEXT_GATHERED
      - core:NEEDS_CLARIFICATION
      - core:RECOVERY
    artifacts_input:
      - TASK_SPECIFICATION.md
      - KB_RECOMMENDATION.md
      - KNOWLEDGE_INDEX.md
    artifacts_output:
      - CONTEXT_ARTIFACT.md
    workflow: .agents/orchestrators/core/workflow/03-gather-context.md
    harness:
      - H02-context-artifact
    actor: orchestrator
    profile: context_gatherer

  "core:CONTEXT_GATHERED":
    kind: state
    domain: core
    lifecycle: context
    name: Context Gathered
    description: The required context has been collected and is ready for evaluation.
    previous:
      - core:GATHERING_CONTEXT
    next:
      - core:VALIDATING_CONTEXT
    artifacts_input:
      - CONTEXT_ARTIFACT.md
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:VALIDATING_CONTEXT":
    kind: state
    domain: core
    lifecycle: context
    name: Validating Context
    description: Evaluate whether the gathered context is sufficient, relevant and consistent.
    previous:
      - core:CONTEXT_GATHERED
    next:
      - core:CONTEXT_READY
      - core:NEEDS_CLARIFICATION
      - core:RECOVERY
    artifacts_input:
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
    artifacts_output:
      - CONTEXT_VALIDATION_REPORT.md
    workflow: .agents/orchestrators/core/workflow/04-validate-context.md
    harness:
      - H03-context-validation
    actor: orchestrator
    profile: context_validator

  "core:CONTEXT_READY":
    kind: state
    domain: core
    lifecycle: context
    name: Context Ready
    description: Specification and context are validated; planning can begin.
    previous:
      - core:VALIDATING_CONTEXT
    next:
      - core:PLANNING
    artifacts_input:
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
      - CONTEXT_VALIDATION_REPORT.md
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:PLANNING":
    kind: state
    domain: core
    lifecycle: planning
    name: Planning
    description: Define how the task will be executed.
    previous:
      - core:CONTEXT_READY
      - core:ANALYZING_TASK
      - core:RECOVERY
    next:
      - core:PLAN_READY
      - core:NEEDS_CLARIFICATION
      - core:RECOVERY
    artifacts_input:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
      - CONTEXT_VALIDATION_REPORT.md
    artifacts_output:
      - EXECUTION_PLAN.md
    workflow: .agents/orchestrators/core/workflow/05-plan.md
    harness:
      - H04-execution-plan
    actor: orchestrator
    profile: planner

  "core:PLAN_READY":
    kind: state
    domain: core
    lifecycle: planning
    name: Plan Ready
    description: The execution strategy has been defined and validated.
    previous:
      - core:PLANNING
    next:
      - core:EXECUTING
    artifacts_input:
      - EXECUTION_PLAN.md
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:EXECUTING":
    kind: state
    domain: core
    lifecycle: execution
    name: Executing
    description: Perform the planned actions.
    previous:
      - core:PLAN_READY
    next:
      - core:VERIFYING
      - core:RECOVERY
    artifacts_input:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - CONTEXT_VALIDATION_REPORT.md
      - EXECUTION_PLAN.md
    artifacts_output:
      - EXECUTION_SUMMARY.md
    workflow: .agents/orchestrators/core/workflow/06-execute.md
    harness:
      - H05-execution-completed
    actor: orchestrator
    profile: executor

  "core:VERIFYING":
    kind: state
    domain: core
    lifecycle: execution
    name: Verifying
    description: Evaluate whether the result satisfies the original specification.
    previous:
      - core:EXECUTING
    next:
      - core:COMPLETED
      - core:RECOVERY
    artifacts_input:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - EXECUTION_PLAN.md
      - EXECUTION_SUMMARY.md
    artifacts_output:
      - VERIFICATION_REPORT.md
      - REVIEW_REPORT.md
    workflow: .agents/orchestrators/core/workflow/07-verify.md
    harness:
      - H06-verification-report
      - H07-scope-compliance
    actor: orchestrator
    profile: verifier

  "core:RECOVERY":
    kind: state
    domain: core
    lifecycle: exception
    name: Recovery
    description: Analyze failures and determine corrective actions.
    previous:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
      - core:BUILDING_TASK_SPECIFICATION
      - core:GATHERING_CONTEXT
      - core:VALIDATING_CONTEXT
      - core:PLANNING
      - core:EXECUTING
      - core:VERIFYING
    next:
      - core:PLANNING
      - core:NEEDS_CLARIFICATION
      - core:ABORT
      - core:ANALYZING_TASK
      - core:BUILDING_TASK_SPECIFICATION
      - core:GATHERING_CONTEXT
      - core:VALIDATING_CONTEXT
    artifacts_input:
      - VERIFICATION_REPORT.md
    artifacts_output:
      - RECOVERY_REPORT.md
    workflow: .agents/orchestrators/core/workflow/08-recovery.md
    harness:
      - H09-recovery-report
    actor: orchestrator
    profile: recovery_analyst

  "core:COMPLETED":
    kind: state
    domain: core
    lifecycle: final
    name: Completed
    description: The task has been completed and verified. Terminal state.
    previous:
      - core:VERIFYING
    next: []
    artifacts_input:
      - VERIFICATION_REPORT.md
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  "core:ABORT":
    kind: state
    domain: core
    lifecycle: final
    name: Abort
    description: Session terminated by an explicit abort action. Terminal state.
    previous:
      - core:RECOVERY
    next: []
    artifacts_input: []
    artifacts_output: []
    workflow: null
    harness: []
    actor: orchestrator
    profile: null

  # -------------------------------------------------------------------------
  # States — domain: system
  # -------------------------------------------------------------------------
  "system:SYSTEM_INIT":
    kind: state
    domain: system
    lifecycle: system
    name: System Init
    description: The ArgentOS System Agent role was loaded; bootstrap started.
    previous: []
    next:
      - system:VERIFYING_PROTOCOL_HEALTH
    artifacts_input: []
    artifacts_output: []
    workflow: .agents/orchestrators/system/workflow/00-bootstrap.md
    harness: []
    actor: system_agent
    profile: null

  "system:VERIFYING_PROTOCOL_HEALTH":
    kind: state
    domain: system
    lifecycle: system
    name: Verifying Protocol Health
    description: Apply the protocol health checklist and state-storage probe, and prepare the runtime environment.
    previous:
      - system:SYSTEM_INIT
      - system:BOOTSTRAP_FAILED
    next:
      - system:ENVIRONMENT_READY
      - system:BOOTSTRAP_FAILED
    artifacts_input: []
    artifacts_output:
      - KNOWLEDGE_INDEX.md
      - PROJECT_README.md
    workflow: .agents/orchestrators/system/workflow/00-bootstrap.md
    harness:
      - S00-system-ready
    actor: system_agent
    profile: null

  "system:ENVIRONMENT_READY":
    kind: state
    domain: system
    lifecycle: system
    name: Environment Ready
    description: Health check passed; hand control to the core Orchestrator.
    previous:
      - system:VERIFYING_PROTOCOL_HEALTH
    next:
      - core:SYSTEM_READY
    artifacts_input: []
    artifacts_output: []
    workflow: .agents/orchestrators/system/workflow/00-bootstrap.md
    harness: []
    actor: system_agent
    profile: null

  "system:BOOTSTRAP_FAILED":
    kind: state
    domain: system
    lifecycle: system
    name: Bootstrap Failed
    description: Health check failed; report and do not hand control to core.
    previous:
      - system:VERIFYING_PROTOCOL_HEALTH
    next:
      - system:VERIFYING_PROTOCOL_HEALTH
    artifacts_input: []
    artifacts_output: []
    workflow: .agents/orchestrators/system/workflow/00-bootstrap.md
    harness: []
    actor: system_agent
    profile: null

  # -------------------------------------------------------------------------
  # States — domain: discovery
  # This section must stay synchronized with the discovery state machine
  # (.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md).
  # -------------------------------------------------------------------------
  "discovery:DISCOVERY_INIT":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Init
    description: Initialize a discovery session and produce the initial discovery report.
    previous:
      - discovery:DISCOVERY_FAILED
    next:
      - discovery:DISCOVERY_RUNNING
      - discovery:DISCOVERY_FAILED
    artifacts_input: []
    artifacts_output:
      - KB_DISCOVERY_REPORT.md
      - KB_DISCOVERY_ENTRY.md
    workflow: .agents/orchestrators/discovery/workflow/00-discovery-init.md
    harness:
      - D00-discovery-init
    actor: discovery_orchestrator
    profile: init_worker

  "discovery:DISCOVERY_RUNNING":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Running
    description: The discovery session is initialized and the run may proceed.
    previous:
      - discovery:DISCOVERY_INIT
    next:
      - discovery:DISCOVERY_ENV
      - discovery:DISCOVERY_STACK
      - discovery:DISCOVERY_PATTERNS
      - discovery:DISCOVERY_BUSINESS
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - KB_DISCOVERY_REPORT.md
    artifacts_output: []
    workflow: .agents/orchestrators/discovery/workflow/00-discovery-init.md
    harness: []
    actor: discovery_orchestrator
    profile: null

  "discovery:DISCOVERY_ENV":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Environment
    description: Discover the runtime environment of the project.
    previous:
      - discovery:DISCOVERY_RUNNING
    next:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - discovery_input.json
    artifacts_output:
      - worker_environment.json
      - ENVIRONMENT_DISCOVERY.md
    workflow: .agents/orchestrators/discovery/workflow/01-discovery-env.md
    harness: []
    actor: discovery_orchestrator
    profile: environment_worker

  "discovery:DISCOVERY_STACK":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Stack
    description: Discover the technology stack.
    previous:
      - discovery:DISCOVERY_RUNNING
    next:
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - discovery_input.json
    artifacts_output:
      - worker_stack.json
    workflow: .agents/orchestrators/discovery/workflow/02-discovery-stack.md
    harness: []
    actor: discovery_orchestrator
    profile: stack_worker

  "discovery:DISCOVERY_FRAMEWORK":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Framework
    description: Discover frameworks in use.
    previous:
      - discovery:DISCOVERY_STACK
    next:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - worker_stack.json
    artifacts_output:
      - worker_framework.json
    workflow: .agents/orchestrators/discovery/workflow/03-discovery-framework.md
    harness: []
    actor: discovery_orchestrator
    profile: framework_worker

  "discovery:DISCOVERY_PATTERNS":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Patterns
    description: Discover architectural and code patterns.
    previous:
      - discovery:DISCOVERY_RUNNING
    next:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - discovery_input.json
    artifacts_output:
      - worker_patterns.json
      - DEVELOPMENT_PATTERNS.md
    workflow: .agents/orchestrators/discovery/workflow/04-discovery-patterns.md
    harness: []
    actor: discovery_orchestrator
    profile: patterns_worker

  "discovery:DISCOVERY_BUSINESS":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Business
    description: Discover the business domain.
    previous:
      - discovery:DISCOVERY_RUNNING
    next:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - discovery_input.json
    artifacts_output:
      - worker_business.json
    workflow: .agents/orchestrators/discovery/workflow/05-discovery-business.md
    harness: []
    actor: discovery_orchestrator
    profile: business_worker

  "discovery:DISCOVERY_MERGE":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Merge
    description: Merge partial discovery results.
    previous:
      - discovery:DISCOVERY_ENV
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_PATTERNS
      - discovery:DISCOVERY_BUSINESS
      - discovery:DISCOVERY_VALIDATE
    next:
      - discovery:DISCOVERY_VALIDATE
      - discovery:DISCOVERY_FAILED
    artifacts_input:
      - worker_environment.json
      - worker_stack.json
      - worker_framework.json
      - worker_patterns.json
      - worker_business.json
    artifacts_output:
      - DISCOVERY_MANIFEST.md
    workflow: .agents/orchestrators/discovery/workflow/06-discovery-merge.md
    harness: []
    actor: discovery_orchestrator
    profile: synthesis_worker

  "discovery:DISCOVERY_VALIDATE":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Validate
    description: Validate the merged discovery output.
    previous:
      - discovery:DISCOVERY_MERGE
    next:
      - discovery:DISCOVERY_READY
      - discovery:DISCOVERY_FAILED
      - discovery:DISCOVERY_MERGE
    artifacts_input:
      - DISCOVERY_MANIFEST.md
    artifacts_output: []
    workflow: .agents/orchestrators/discovery/workflow/07-discovery-validate.md
    harness:
      - D01-discovery-output
    actor: discovery_orchestrator
    profile: null

  "discovery:DISCOVERY_READY":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Ready
    description: Discovery output is validated and ready for consumption. Terminal state.
    previous:
      - discovery:DISCOVERY_VALIDATE
    next: []
    artifacts_input:
      - DISCOVERY_MANIFEST.md
    artifacts_output: []
    workflow: .agents/orchestrators/discovery/workflow/08-discovery-ready.md
    harness: []
    actor: discovery_orchestrator
    profile: null

  "discovery:DISCOVERY_FAILED":
    kind: state
    domain: discovery
    lifecycle: discovery
    name: Discovery Failed
    description: The discovery run failed. Terminal state until retried.
    previous:
      - discovery:DISCOVERY_INIT
      - discovery:DISCOVERY_RUNNING
      - discovery:DISCOVERY_ENV
      - discovery:DISCOVERY_STACK
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_PATTERNS
      - discovery:DISCOVERY_BUSINESS
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_VALIDATE
    next:
      - discovery:DISCOVERY_INIT
    artifacts_input: []
    artifacts_output: []
    workflow: null
    harness: []
    actor: discovery_orchestrator
    profile: null

  # -------------------------------------------------------------------------
  # Artifacts
  # -------------------------------------------------------------------------
  TASK_ANALYSIS.md:
    kind: artifact
    domain: core
    lifecycle: task
    tag: analysis
    description: Records the interpreted request, requirements, ambiguities and recommended next state.
    produced_by:
      - core:ANALYZING_TASK
    consumed_by:
      - core:BUILDING_TASK_SPECIFICATION
      - core:CONFIRMING_INTENT
    contract: .agents/orchestrators/core/contracts/TASK_ANALYSIS.md

  INTENT_REFLECTION.md:
    kind: artifact
    domain: core
    lifecycle: task
    tag: reflection
    description: Structured reflection of the user's intent for confirmation or correction.
    produced_by:
      - core:CONFIRMING_INTENT
    consumed_by:
      - core:BUILDING_TASK_SPECIFICATION
      - core:ANALYZING_TASK
    contract: .agents/orchestrators/core/contracts/INTENT_REFLECTION.md

  TASK_SPECIFICATION.md:
    kind: artifact
    domain: core
    lifecycle: task
    tag: specification
    description: Formal task specification with scope, constraints and acceptance criteria.
    produced_by:
      - core:BUILDING_TASK_SPECIFICATION
    consumed_by:
      - core:TASK_READY
      - core:VALIDATING_CONTEXT
      - core:EXECUTING
    contract: .agents/orchestrators/core/contracts/TASK_SPECIFICATION.md

  CONTEXT_ARTIFACT.md:
    kind: artifact
    domain: core
    lifecycle: context
    tag: context
    description: Gathered context about the environment where the task will be executed.
    produced_by:
      - core:GATHERING_CONTEXT
    consumed_by:
      - core:VALIDATING_CONTEXT
      - core:CONTEXT_READY
    contract: .agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md

  CONTEXT_VALIDATION_REPORT.md:
    kind: artifact
    domain: core
    lifecycle: context
    tag: validation_report
    description: Evaluation of context sufficiency, relevance and consistency.
    produced_by:
      - core:VALIDATING_CONTEXT
    consumed_by:
      - core:CONTEXT_READY
      - core:EXECUTING
    contract: .agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md

  EXECUTION_PLAN.md:
    kind: artifact
    domain: core
    lifecycle: planning
    tag: plan
    description: Step-by-step execution plan for the task.
    produced_by:
      - core:PLANNING
    consumed_by:
      - core:EXECUTING
    contract: .agents/orchestrators/core/contracts/EXECUTION_PLAN.md

  EXECUTION_SUMMARY.md:
    kind: artifact
    domain: core
    lifecycle: execution
    tag: summary
    description: Record of changes applied, steps executed and final project state.
    produced_by:
      - core:EXECUTING
    consumed_by:
      - core:VERIFYING
    contract: .agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md

  VERIFICATION_REPORT.md:
    kind: artifact
    domain: core
    lifecycle: execution
    tag: report
    description: Verification of the result against the specification and acceptance criteria.
    produced_by:
      - core:VERIFYING
    consumed_by:
      - core:COMPLETED
      - core:RECOVERY
    contract: .agents/orchestrators/core/contracts/VERIFICATION_REPORT.md

  RECOVERY_REPORT.md:
    kind: artifact
    domain: core
    lifecycle: exception
    tag: report
    description: Failure analysis, root cause classification and corrective action.
    produced_by:
      - core:RECOVERY
    consumed_by:
      - core:PLANNING
    contract: .agents/orchestrators/core/contracts/RECOVERY_REPORT.md

  KB_DISCOVERY_REPORT.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Initialization report of a discovery run (scope, inputs, invalidations).
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - discovery:DISCOVERY_RUNNING
    contract: .agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md

  KB_RECOMMENDATION.md:
    kind: artifact
    domain: core
    lifecycle: context
    tag: knowledge
    description: Knowledge-base entries recommended by the context_discoverer for the current task.
    produced_by:
      - core:GATHERING_CONTEXT
    consumed_by:
      - core:PLANNING
      - core:EXECUTING
      - core:VERIFYING
    contract: .agents/orchestrators/core/contracts/KB_RECOMMENDATION.md

  KB_DISCOVERY_ENTRY.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: A single knowledge-base entry produced by project discovery.
    produced_by:
      - discovery:DISCOVERY_ENV
      - discovery:DISCOVERY_STACK
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_PATTERNS
      - discovery:DISCOVERY_BUSINESS
      - discovery:DISCOVERY_MERGE
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md

  DISCOVERY_MANIFEST.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Manifest of the accumulative discovery knowledge base.
    produced_by:
      - discovery:DISCOVERY_MERGE
    consumed_by:
      - discovery:DISCOVERY_INIT
      - discovery:DISCOVERY_VALIDATE
    contract: .agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md

  DEVELOPMENT_PATTERNS.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Knowledge-base entry with the development patterns detected in the project.
    produced_by:
      - discovery:DISCOVERY_PATTERNS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    contract: .agents/orchestrators/discovery/contracts/DEVELOPMENT_PATTERNS.md

  ENVIRONMENT_DISCOVERY.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Knowledge-base entry with the execution environment detected by discovery.
    produced_by:
      - discovery:DISCOVERY_ENV
    consumed_by:
      - discovery:DISCOVERY_MERGE
    contract: .agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md

  EXECUTIVE_SUMMARY.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Canonical read-first knowledge-base entry that synthesizes the discovery KB.
    produced_by:
      - discovery:DISCOVERY_MERGE
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md

  API_SURFACE.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Knowledge-base entry documenting the contract surface the project exposes, parameterized by project_shape.
    produced_by:
      - discovery:DISCOVERY_FRAMEWORK
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/orchestrators/discovery/contracts/API_SURFACE.md

  file_map.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Knowledge-base entry mapping main folders and relevant files to their responsibilities.
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md

  INTER_WORKER_MESSAGE.md:
    kind: artifact
    domain: discovery
    lifecycle: discovery
    tag: knowledge
    description: Message exchanged between the workers of the Discovery Orchestrator.
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - discovery:DISCOVERY_MERGE
    contract: .agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md

  SESSION_LOG.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: log
    description: Chronological log of the session, maintained by the Orchestrator.
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:COMPLETED
      - core:RECOVERY
    contract: .agents/contracts/SESSION_LOG.md

  SESSION_BRIEF.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: brief
    description: Confirmed intent and prior clarifications of the current session.
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
    contract: .agents/contracts/SESSION_BRIEF.md

  KNOWLEDGE_INDEX.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: knowledge
    description: Index of the project knowledge base under `.project/knowledge/`.
    produced_by:
      - system:VERIFYING_PROTOCOL_HEALTH
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/contracts/KNOWLEDGE_INDEX.md

  PROJECT_README.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: knowledge
    description: Project-level README initialized by the System Agent in `.project/`.
    produced_by:
      - system:VERIFYING_PROTOCOL_HEALTH
    consumed_by:
      - core:GATHERING_CONTEXT
    contract: .agents/contracts/PROJECT_README.md

  REVIEW_REPORT.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: report
    description: Rubric-based review produced by the reviewer role during verification.
    produced_by:
      - core:VERIFYING
    consumed_by:
      - core:COMPLETED
    contract: .agents/contracts/REVIEW_REPORT.md

  HARNESS_REPORT.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: report
    description: Audit trail of harness trigger invocations, written by the Orchestrator at the session root.
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:RECOVERY
      - core:COMPLETED
      - discovery:DISCOVERY_READY
    contract: .agents/contracts/HARNESS_REPORT.md

  METRICS.md:
    kind: artifact
    domain: cross-cutting
    lifecycle: null
    tag: report
    description: Event data points of the protocol metrics model, recorded by the Orchestrator at the session root.
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:COMPLETED
    contract: .agents/contracts/METRICS.md

  # -------------------------------------------------------------------------
  # Harness policies
  # -------------------------------------------------------------------------
  H00-task-analysis:
    kind: harness
    domain: core
    harness_id: H00
    name: task-analysis
    lifecycle: task
    tag: task
    state: core:ANALYZING_TASK
    gates:
      - core:ANALYZING_TASK -> core:BUILDING_TASK_SPECIFICATION
      - core:ANALYZING_TASK -> core:CONFIRMING_INTENT
      - core:ANALYZING_TASK -> core:NEEDS_CLARIFICATION
    artifact_validated: TASK_ANALYSIS.md
    policy_file: .agents/orchestrators/core/harness/policies/H00-task-analysis.md

  H11-intent-reflection:
    kind: harness
    domain: core
    harness_id: H11
    name: intent-reflection
    lifecycle: task
    tag: task
    state: core:CONFIRMING_INTENT
    gates:
      - core:CONFIRMING_INTENT -> core:BUILDING_TASK_SPECIFICATION
    artifact_validated: INTENT_REFLECTION.md
    policy_file: .agents/orchestrators/core/harness/policies/H11-intent-reflection.md

  H01-task-specification:
    kind: harness
    domain: core
    harness_id: H01
    name: task-specification
    lifecycle: task
    tag: task
    state: core:BUILDING_TASK_SPECIFICATION
    gates:
      - core:BUILDING_TASK_SPECIFICATION -> core:TASK_READY
    artifact_validated: TASK_SPECIFICATION.md
    policy_file: .agents/orchestrators/core/harness/policies/H01-task-specification.md

  H02-context-artifact:
    kind: harness
    domain: core
    harness_id: H02
    name: context-artifact
    lifecycle: context
    tag: context
    state: core:GATHERING_CONTEXT
    gates:
      - core:GATHERING_CONTEXT -> core:CONTEXT_GATHERED
    artifact_validated: CONTEXT_ARTIFACT.md
    policy_file: .agents/orchestrators/core/harness/policies/H02-context-artifact.md

  H03-context-validation:
    kind: harness
    domain: core
    harness_id: H03
    name: context-validation
    lifecycle: context
    tag: context
    state: core:VALIDATING_CONTEXT
    gates:
      - core:VALIDATING_CONTEXT -> core:CONTEXT_READY
    artifact_validated: CONTEXT_VALIDATION_REPORT.md
    policy_file: .agents/orchestrators/core/harness/policies/H03-context-validation.md

  H04-execution-plan:
    kind: harness
    domain: core
    harness_id: H04
    name: execution-plan
    lifecycle: planning
    tag: planning
    state: core:PLANNING
    gates:
      - core:PLANNING -> core:PLAN_READY
    artifact_validated: EXECUTION_PLAN.md
    policy_file: .agents/orchestrators/core/harness/policies/H04-execution-plan.md

  H05-execution-completed:
    kind: harness
    domain: core
    harness_id: H05
    name: execution-completed
    lifecycle: execution
    tag: execution
    state: core:EXECUTING
    gates:
      - core:EXECUTING -> core:VERIFYING
    artifact_validated: EXECUTION_SUMMARY.md
    policy_file: .agents/orchestrators/core/harness/policies/H05-execution-completed.md

  H06-verification-report:
    kind: harness
    domain: core
    harness_id: H06
    name: verification-report
    lifecycle: execution
    tag: verification
    state: core:VERIFYING
    gates:
      - core:VERIFYING -> core:COMPLETED
    artifact_validated: VERIFICATION_REPORT.md
    policy_file: .agents/orchestrators/core/harness/policies/H06-verification-report.md

  H07-scope-compliance:
    kind: harness
    domain: core
    harness_id: H07
    name: scope-compliance
    lifecycle: execution
    tag: verification
    state: core:VERIFYING
    gates:
      - core:VERIFYING -> core:COMPLETED
    artifact_validated: VERIFICATION_REPORT.md
    policy_file: .agents/orchestrators/core/harness/policies/H07-scope-compliance.md

  H09-recovery-report:
    kind: harness
    domain: core
    harness_id: H09
    name: recovery-report
    lifecycle: exception
    tag: recovery
    state: core:RECOVERY
    gates:
      - core:RECOVERY -> core:PLANNING
    artifact_validated: RECOVERY_REPORT.md
    policy_file: .agents/orchestrators/core/harness/policies/H09-recovery-report.md

  H10-kb-discovery-report:
    kind: harness
    domain: core
    harness_id: H10
    name: kb-discovery-report
    lifecycle: context
    tag: context
    state: core:GATHERING_CONTEXT
    gates: []
    artifact_validated: KB_RECOMMENDATION.md
    policy_file: .agents/orchestrators/core/harness/policies/H10-kb-discovery-report.md

  H15-delegation-validity:
    kind: harness
    domain: core
    harness_id: H15
    name: delegation-validity
    lifecycle: null
    tag: delegation
    state: null
    gates: []
    artifact_validated: null
    policy_file: .agents/orchestrators/core/harness/policies/H15-delegation-validity.md

  D00-discovery-init:
    kind: harness
    domain: discovery
    harness_id: D00
    name: discovery-init
    lifecycle: discovery
    tag: discovery
    state: discovery:DISCOVERY_INIT
    gates:
      - discovery:DISCOVERY_INIT -> discovery:DISCOVERY_RUNNING
    artifact_validated: KB_DISCOVERY_REPORT.md
    policy_file: .agents/orchestrators/discovery/harness/policies/D00-discovery-init.md

  D01-discovery-output:
    kind: harness
    domain: discovery
    harness_id: D01
    name: discovery-output
    lifecycle: discovery
    tag: discovery
    state: discovery:DISCOVERY_VALIDATE
    gates:
      - discovery:DISCOVERY_VALIDATE -> discovery:DISCOVERY_READY
    artifact_validated: KB_DISCOVERY_ENTRY.md
    policy_file: .agents/orchestrators/discovery/harness/policies/D01-discovery-output.md

  S00-system-ready:
    kind: harness
    domain: system
    harness_id: S00
    name: system-ready
    lifecycle: system
    tag: system
    state: system:VERIFYING_PROTOCOL_HEALTH
    gates:
      - system:VERIFYING_PROTOCOL_HEALTH -> system:ENVIRONMENT_READY
    artifact_validated: .project/.last_health_check
    policy_file: .agents/orchestrators/system/harness/policies/S00-system-ready.md

  H13-protocol-taxonomy:
    kind: harness
    domain: cross-cutting
    harness_id: H13
    name: protocol-taxonomy
    lifecycle: null
    tag: taxonomy
    state: null
    gates: []
    artifact_validated: .agents/standards/runtime/PROTOCOL_TAXONOMY.md
    policy_file: .agents/harness/policies/H13-protocol-taxonomy.md

  # -------------------------------------------------------------------------
  # Actors
  # -------------------------------------------------------------------------
  system_agent:
    kind: actor
    domain: system
    name: ArgentOS System Agent
    description: Prepares and maintains the protocol runtime environment before any session.
    role_file: .agents/orchestrators/system/roles/argentos.md

  orchestrator:
    kind: actor
    domain: core
    name: Orchestrator
    description: Governs the complete lifecycle of a task, triggers the harness and delegates phases to workers.
    role_file: .agents/orchestrators/core/roles/orchestrator.md

  discovery_orchestrator:
    kind: actor
    domain: discovery
    name: Discovery Orchestrator
    description: Governs the knowledge-base discovery lifecycle.
    role_file: .agents/orchestrators/discovery/roles/discovery_orchestrator.md

  # -------------------------------------------------------------------------
  # Roles
  # -------------------------------------------------------------------------
  role:orchestrator:
    kind: role
    domain: core
    role_id: orchestrator
    actor: orchestrator
    role_file: .agents/orchestrators/core/roles/orchestrator.md

  role:argentos:
    kind: role
    domain: system
    role_id: argentos
    actor: system_agent
    role_file: .agents/orchestrators/system/roles/argentos.md

  role:worker:
    kind: role
    domain: cross-cutting
    role_id: worker
    actor: orchestrator
    role_file: .agents/roles/worker.md

  role:reviewer:
    kind: role
    domain: cross-cutting
    role_id: reviewer
    actor: orchestrator
    role_file: .agents/roles/reviewer.md

  role:verifier:
    kind: role
    domain: cross-cutting
    role_id: verifier
    actor: orchestrator
    role_file: .agents/roles/verifier.md

  role:context_discoverer:
    kind: role
    domain: cross-cutting
    role_id: context_discoverer
    actor: orchestrator
    role_file: .agents/roles/context_discoverer.md

  role:discovery_orchestrator:
    kind: role
    domain: discovery
    role_id: discovery_orchestrator
    actor: discovery_orchestrator
    role_file: .agents/orchestrators/discovery/roles/discovery_orchestrator.md

  # -------------------------------------------------------------------------
  # Workers
  # Phase workers (task_analyst, intent_reflector, ...) are roles the generic
  # Worker adopts per phase; specialized profiles live in .agents/roles/profiles/.
  # -------------------------------------------------------------------------
  task_analyst:
    kind: worker
    domain: core
    worker_id: task_analyst
    role_file: .agents/roles/task_analyst.md
    state: core:ANALYZING_TASK
    lifecycle: task
    actor: orchestrator
    input_artifacts: []
    output_artifacts:
      - TASK_ANALYSIS.md

  intent_reflector:
    kind: worker
    domain: core
    worker_id: intent_reflector
    state: core:CONFIRMING_INTENT
    lifecycle: task
    actor: orchestrator
    profile_file: .agents/roles/profiles/intent_reflector.md
    input_artifacts:
      - TASK_ANALYSIS.md
    output_artifacts:
      - INTENT_REFLECTION.md

  task_specification_writer:
    kind: worker
    domain: core
    worker_id: task_specification_writer
    role_file: .agents/roles/task_specification_writer.md
    state: core:BUILDING_TASK_SPECIFICATION
    lifecycle: task
    actor: orchestrator
    input_artifacts:
      - TASK_ANALYSIS.md
      - INTENT_REFLECTION.md
    output_artifacts:
      - TASK_SPECIFICATION.md

  context_gatherer:
    kind: worker
    domain: core
    worker_id: context_gatherer
    role_file: .agents/roles/context_gatherer.md
    state: core:GATHERING_CONTEXT
    lifecycle: context
    actor: orchestrator
    input_artifacts:
      - TASK_SPECIFICATION.md
    output_artifacts:
      - CONTEXT_ARTIFACT.md

  context_validator:
    kind: worker
    domain: core
    worker_id: context_validator
    role_file: .agents/roles/context_validator.md
    state: core:VALIDATING_CONTEXT
    lifecycle: context
    actor: orchestrator
    input_artifacts:
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
    output_artifacts:
      - CONTEXT_VALIDATION_REPORT.md

  planner:
    kind: worker
    domain: core
    worker_id: planner
    role_file: .agents/roles/planner.md
    state: core:PLANNING
    lifecycle: planning
    actor: orchestrator
    input_artifacts:
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
      - CONTEXT_VALIDATION_REPORT.md
    output_artifacts:
      - EXECUTION_PLAN.md

  executor:
    kind: worker
    domain: core
    worker_id: executor
    role_file: .agents/roles/executor.md
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    input_artifacts:
      - EXECUTION_PLAN.md
    output_artifacts:
      - EXECUTION_SUMMARY.md

  verifier:
    kind: worker
    domain: core
    worker_id: verifier
    state: core:VERIFYING
    lifecycle: execution
    actor: orchestrator
    input_artifacts:
      - TASK_SPECIFICATION.md
      - EXECUTION_SUMMARY.md
    output_artifacts:
      - VERIFICATION_REPORT.md

  recovery_analyst:
    kind: worker
    domain: core
    worker_id: recovery_analyst
    role_file: .agents/roles/recovery_analyst.md
    state: core:RECOVERY
    lifecycle: exception
    actor: orchestrator
    input_artifacts:
      - VERIFICATION_REPORT.md
    output_artifacts:
      - RECOVERY_REPORT.md

  backend_engineer:
    kind: worker
    domain: cross-cutting
    worker_id: backend_engineer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/backend_engineer.md

  database_engineer:
    kind: worker
    domain: cross-cutting
    worker_id: database_engineer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/database_engineer.md

  integration_engineer:
    kind: worker
    domain: cross-cutting
    worker_id: integration_engineer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/integration_engineer.md

  qa_engineer:
    kind: worker
    domain: cross-cutting
    worker_id: qa_engineer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/qa_engineer.md

  tech_writer:
    kind: worker
    domain: cross-cutting
    worker_id: tech_writer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/tech_writer.md

  functional_writer:
    kind: worker
    domain: cross-cutting
    worker_id: functional_writer
    state: core:EXECUTING
    lifecycle: execution
    actor: orchestrator
    profile_file: .agents/roles/profiles/functional_writer.md

  intent_reflection_reviewer:
    kind: worker
    domain: cross-cutting
    worker_id: intent_reflection_reviewer
    state: core:CONFIRMING_INTENT
    lifecycle: task
    actor: orchestrator
    profile_file: .agents/roles/profiles/intent_reflection_reviewer.md

  init_worker:
    kind: worker
    domain: discovery
    worker_id: init_worker
    subsystem: discovery
    state: discovery:DISCOVERY_INIT
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/init_worker.md
    input_artifacts: []
    output_artifacts:
      - discovery_input.json
      - invalidation_report.json

  environment_worker:
    kind: worker
    domain: discovery
    worker_id: environment_worker
    subsystem: discovery
    state: discovery:DISCOVERY_ENV
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/environment_worker.md
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - environment.md

  stack_worker:
    kind: worker
    domain: discovery
    worker_id: stack_worker
    subsystem: discovery
    state: discovery:DISCOVERY_STACK
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/stack_worker.md
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - stack.md
      - dependencies.md
      - containers.md
      - database.md

  framework_worker:
    kind: worker
    domain: discovery
    worker_id: framework_worker
    subsystem: discovery
    state: discovery:DISCOVERY_FRAMEWORK
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/framework_worker.md
    input_artifacts:
      - worker_stack.json
    output_artifacts:
      - architecture.md
      - configuration.md

  patterns_worker:
    kind: worker
    domain: discovery
    worker_id: patterns_worker
    subsystem: discovery
    state: discovery:DISCOVERY_PATTERNS
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/patterns_worker.md
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - development_patterns.md

  business_worker:
    kind: worker
    domain: discovery
    worker_id: business_worker
    subsystem: discovery
    state: discovery:DISCOVERY_BUSINESS
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/business_worker.md
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - business_rules.md
      - project_flow.md
      - technical_debt.md
      - known_errors.md

  synthesis_worker:
    kind: worker
    domain: discovery
    worker_id: synthesis_worker
    subsystem: discovery
    state: discovery:DISCOVERY_MERGE
    lifecycle: discovery
    actor: discovery_orchestrator
    profile_file: .agents/orchestrators/discovery/roles/workers/synthesis_worker.md
    input_artifacts:
      - worker_environment.json
      - worker_stack.json
      - worker_framework.json
      - worker_patterns.json
      - worker_business.json
    output_artifacts:
      - summary.md
      - .discovery_manifest

  # -------------------------------------------------------------------------
  # Workflows
  # -------------------------------------------------------------------------
  workflow:00-analyze-task:
    kind: workflow
    domain: core
    state: core:ANALYZING_TASK
    lifecycle: task
    previous_states:
      - core:TASK_RECEIVED
    next_states:
      - core:BUILDING_TASK_SPECIFICATION
      - core:CONFIRMING_INTENT
      - core:NEEDS_CLARIFICATION
      - core:PLANNING
    input_artifacts: []
    output_artifacts:
      - TASK_ANALYSIS.md
    harness:
      - H00-task-analysis
    actor: orchestrator
    profile: task_analyst
    file: .agents/orchestrators/core/workflow/00-analyze-task.md

  workflow:01-confirm-intent:
    kind: workflow
    domain: core
    state: core:CONFIRMING_INTENT
    lifecycle: task
    previous_states:
      - core:ANALYZING_TASK
    next_states:
      - core:BUILDING_TASK_SPECIFICATION
      - core:ANALYZING_TASK
      - core:NEEDS_CLARIFICATION
    input_artifacts:
      - TASK_ANALYSIS.md
    output_artifacts:
      - INTENT_REFLECTION.md
    harness:
      - H11-intent-reflection
    actor: orchestrator
    profile: intent_reflector
    file: .agents/orchestrators/core/workflow/01-confirm-intent.md

  workflow:02-build-task-specification:
    kind: workflow
    domain: core
    state: core:BUILDING_TASK_SPECIFICATION
    lifecycle: task
    previous_states:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
    next_states:
      - core:TASK_READY
      - core:NEEDS_CLARIFICATION
    input_artifacts:
      - TASK_ANALYSIS.md
      - INTENT_REFLECTION.md
    output_artifacts:
      - TASK_SPECIFICATION.md
    harness:
      - H01-task-specification
    actor: orchestrator
    profile: task_specification_writer
    file: .agents/orchestrators/core/workflow/02-build-task-specification.md

  workflow:03-gather-context:
    kind: workflow
    domain: core
    state: core:GATHERING_CONTEXT
    lifecycle: context
    previous_states:
      - core:TASK_READY
    next_states:
      - core:CONTEXT_GATHERED
      - core:NEEDS_CLARIFICATION
    input_artifacts:
      - TASK_SPECIFICATION.md
    output_artifacts:
      - CONTEXT_ARTIFACT.md
    harness:
      - H02-context-artifact
    actor: orchestrator
    profile: context_gatherer
    file: .agents/orchestrators/core/workflow/03-gather-context.md

  workflow:04-validate-context:
    kind: workflow
    domain: core
    state: core:VALIDATING_CONTEXT
    lifecycle: context
    previous_states:
      - core:CONTEXT_GATHERED
    next_states:
      - core:CONTEXT_READY
      - core:NEEDS_CLARIFICATION
    input_artifacts:
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
    output_artifacts:
      - CONTEXT_VALIDATION_REPORT.md
    harness:
      - H03-context-validation
    actor: orchestrator
    profile: context_validator
    file: .agents/orchestrators/core/workflow/04-validate-context.md

  workflow:05-plan:
    kind: workflow
    domain: core
    state: core:PLANNING
    lifecycle: planning
    previous_states:
      - core:CONTEXT_READY
      - core:ANALYZING_TASK
      - core:RECOVERY
    next_states:
      - core:PLAN_READY
      - core:NEEDS_CLARIFICATION
    input_artifacts:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - CONTEXT_ARTIFACT.md
      - CONTEXT_VALIDATION_REPORT.md
    output_artifacts:
      - EXECUTION_PLAN.md
    harness:
      - H04-execution-plan
    actor: orchestrator
    profile: planner
    file: .agents/orchestrators/core/workflow/05-plan.md

  workflow:06-execute:
    kind: workflow
    domain: core
    state: core:EXECUTING
    lifecycle: execution
    previous_states:
      - core:PLAN_READY
    next_states:
      - core:VERIFYING
      - core:RECOVERY
    input_artifacts:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - CONTEXT_VALIDATION_REPORT.md
      - EXECUTION_PLAN.md
    output_artifacts:
      - EXECUTION_SUMMARY.md
    harness:
      - H05-execution-completed
    actor: orchestrator
    profile: executor
    file: .agents/orchestrators/core/workflow/06-execute.md

  workflow:07-verify:
    kind: workflow
    domain: core
    state: core:VERIFYING
    lifecycle: execution
    previous_states:
      - core:EXECUTING
    next_states:
      - core:COMPLETED
      - core:RECOVERY
    input_artifacts:
      - TASK_ANALYSIS.md
      - TASK_SPECIFICATION.md
      - EXECUTION_PLAN.md
      - EXECUTION_SUMMARY.md
    output_artifacts:
      - VERIFICATION_REPORT.md
    harness:
      - H06-verification-report
      - H07-scope-compliance
    actor: orchestrator
    profile: verifier
    file: .agents/orchestrators/core/workflow/07-verify.md

  workflow:08-recovery:
    kind: workflow
    domain: core
    state: core:RECOVERY
    lifecycle: exception
    previous_states:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
      - core:BUILDING_TASK_SPECIFICATION
      - core:GATHERING_CONTEXT
      - core:VALIDATING_CONTEXT
      - core:PLANNING
      - core:EXECUTING
      - core:VERIFYING
    next_states:
      - core:PLANNING
      - core:NEEDS_CLARIFICATION
      - core:ABORT
      - core:ANALYZING_TASK
      - core:BUILDING_TASK_SPECIFICATION
      - core:GATHERING_CONTEXT
      - core:VALIDATING_CONTEXT
    input_artifacts:
      - VERIFICATION_REPORT.md
    output_artifacts:
      - RECOVERY_REPORT.md
    harness:
      - H09-recovery-report
    actor: orchestrator
    profile: recovery_analyst
    file: .agents/orchestrators/core/workflow/08-recovery.md

  workflow:discovery-00-discovery-init:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_INIT
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_FAILED
    next_states:
      - discovery:DISCOVERY_RUNNING
      - discovery:DISCOVERY_FAILED
    input_artifacts: []
    output_artifacts:
      - discovery_input.json
      - invalidation_report.json
      - KB_DISCOVERY_REPORT.md
      - file_map.md
    harness:
      - D00-discovery-init
    actor: discovery_orchestrator
    profile: init_worker
    file: .agents/orchestrators/discovery/workflow/00-discovery-init.md

  workflow:discovery-01-discovery-env:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_ENV
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_RUNNING
    next_states:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - worker_environment.json
      - ENVIRONMENT_DISCOVERY.md
    harness: []
    actor: discovery_orchestrator
    profile: environment_worker
    file: .agents/orchestrators/discovery/workflow/01-discovery-env.md

  workflow:discovery-02-discovery-stack:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_STACK
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_RUNNING
    next_states:
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - worker_stack.json
    harness: []
    actor: discovery_orchestrator
    profile: stack_worker
    file: .agents/orchestrators/discovery/workflow/02-discovery-stack.md

  workflow:discovery-03-discovery-framework:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_FRAMEWORK
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_STACK
    next_states:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - worker_stack.json
    output_artifacts:
      - worker_framework.json
    harness: []
    actor: discovery_orchestrator
    profile: framework_worker
    file: .agents/orchestrators/discovery/workflow/03-discovery-framework.md

  workflow:discovery-04-discovery-patterns:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_PATTERNS
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_RUNNING
    next_states:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - worker_patterns.json
      - DEVELOPMENT_PATTERNS.md
    harness: []
    actor: discovery_orchestrator
    profile: patterns_worker
    file: .agents/orchestrators/discovery/workflow/04-discovery-patterns.md

  workflow:discovery-05-discovery-business:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_BUSINESS
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_RUNNING
    next_states:
      - discovery:DISCOVERY_MERGE
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - discovery_input.json
    output_artifacts:
      - worker_business.json
    harness: []
    actor: discovery_orchestrator
    profile: business_worker
    file: .agents/orchestrators/discovery/workflow/05-discovery-business.md

  workflow:discovery-06-discovery-merge:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_MERGE
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_ENV
      - discovery:DISCOVERY_FRAMEWORK
      - discovery:DISCOVERY_PATTERNS
      - discovery:DISCOVERY_BUSINESS
    next_states:
      - discovery:DISCOVERY_VALIDATE
      - discovery:DISCOVERY_FAILED
    input_artifacts:
      - worker_environment.json
      - worker_stack.json
      - worker_framework.json
      - worker_patterns.json
      - worker_business.json
    output_artifacts:
      - DISCOVERY_MANIFEST.md
    harness: []
    actor: discovery_orchestrator
    profile: synthesis_worker
    file: .agents/orchestrators/discovery/workflow/06-discovery-merge.md

  workflow:discovery-07-discovery-validate:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_VALIDATE
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_MERGE
    next_states:
      - discovery:DISCOVERY_READY
      - discovery:DISCOVERY_FAILED
      - discovery:DISCOVERY_MERGE
    input_artifacts:
      - DISCOVERY_MANIFEST.md
    output_artifacts: []
    harness:
      - D01-discovery-output
    actor: discovery_orchestrator
    profile: null
    file: .agents/orchestrators/discovery/workflow/07-discovery-validate.md

  workflow:discovery-08-discovery-ready:
    kind: workflow
    domain: discovery
    state: discovery:DISCOVERY_READY
    lifecycle: discovery
    previous_states:
      - discovery:DISCOVERY_VALIDATE
    next_states: []
    input_artifacts:
      - DISCOVERY_MANIFEST.md
    output_artifacts: []
    harness: []
    actor: discovery_orchestrator
    profile: null
    file: .agents/orchestrators/discovery/workflow/08-discovery-ready.md

  workflow:system-00-bootstrap:
    kind: workflow
    domain: system
    state: system:VERIFYING_PROTOCOL_HEALTH
    lifecycle: system
    previous_states:
      - system:SYSTEM_INIT
      - system:BOOTSTRAP_FAILED
    next_states:
      - system:ENVIRONMENT_READY
      - system:BOOTSTRAP_FAILED
    input_artifacts: []
    output_artifacts:
      - .project/.last_health_check
    harness:
      - S00-system-ready
    actor: system_agent
    profile: null
    file: .agents/orchestrators/system/workflow/00-bootstrap.md

  # -------------------------------------------------------------------------
  # Contracts
  # -------------------------------------------------------------------------
  contract:TASK_ANALYSIS.md:
    kind: contract
    domain: core
    artifact: TASK_ANALYSIS.md
    lifecycle: task
    produced_by:
      - core:ANALYZING_TASK
    consumed_by:
      - core:BUILDING_TASK_SPECIFICATION
      - core:CONFIRMING_INTENT
    file: .agents/orchestrators/core/contracts/TASK_ANALYSIS.md

  contract:INTENT_REFLECTION.md:
    kind: contract
    domain: core
    artifact: INTENT_REFLECTION.md
    lifecycle: task
    produced_by:
      - core:CONFIRMING_INTENT
    consumed_by:
      - core:BUILDING_TASK_SPECIFICATION
      - core:ANALYZING_TASK
    file: .agents/orchestrators/core/contracts/INTENT_REFLECTION.md

  contract:TASK_SPECIFICATION.md:
    kind: contract
    domain: core
    artifact: TASK_SPECIFICATION.md
    lifecycle: task
    produced_by:
      - core:BUILDING_TASK_SPECIFICATION
    consumed_by:
      - core:TASK_READY
      - core:VALIDATING_CONTEXT
      - core:EXECUTING
    file: .agents/orchestrators/core/contracts/TASK_SPECIFICATION.md

  contract:CONTEXT_ARTIFACT.md:
    kind: contract
    domain: core
    artifact: CONTEXT_ARTIFACT.md
    lifecycle: context
    produced_by:
      - core:GATHERING_CONTEXT
    consumed_by:
      - core:VALIDATING_CONTEXT
      - core:CONTEXT_READY
    file: .agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md

  contract:CONTEXT_VALIDATION_REPORT.md:
    kind: contract
    domain: core
    artifact: CONTEXT_VALIDATION_REPORT.md
    lifecycle: context
    produced_by:
      - core:VALIDATING_CONTEXT
    consumed_by:
      - core:CONTEXT_READY
      - core:EXECUTING
    file: .agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md

  contract:EXECUTION_PLAN.md:
    kind: contract
    domain: core
    artifact: EXECUTION_PLAN.md
    lifecycle: planning
    produced_by:
      - core:PLANNING
    consumed_by:
      - core:EXECUTING
    file: .agents/orchestrators/core/contracts/EXECUTION_PLAN.md

  contract:EXECUTION_SUMMARY.md:
    kind: contract
    domain: core
    artifact: EXECUTION_SUMMARY.md
    lifecycle: execution
    produced_by:
      - core:EXECUTING
    consumed_by:
      - core:VERIFYING
    file: .agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md

  contract:VERIFICATION_REPORT.md:
    kind: contract
    domain: core
    artifact: VERIFICATION_REPORT.md
    lifecycle: execution
    produced_by:
      - core:VERIFYING
    consumed_by:
      - core:COMPLETED
      - core:RECOVERY
    file: .agents/orchestrators/core/contracts/VERIFICATION_REPORT.md

  contract:RECOVERY_REPORT.md:
    kind: contract
    domain: core
    artifact: RECOVERY_REPORT.md
    lifecycle: exception
    produced_by:
      - core:RECOVERY
    consumed_by:
      - core:PLANNING
    file: .agents/orchestrators/core/contracts/RECOVERY_REPORT.md

  contract:SESSION_LOG.md:
    kind: contract
    domain: cross-cutting
    artifact: SESSION_LOG.md
    lifecycle: null
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:COMPLETED
      - core:RECOVERY
    file: .agents/contracts/SESSION_LOG.md

  contract:SESSION_BRIEF.md:
    kind: contract
    domain: cross-cutting
    artifact: SESSION_BRIEF.md
    lifecycle: null
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:ANALYZING_TASK
      - core:CONFIRMING_INTENT
    file: .agents/contracts/SESSION_BRIEF.md

  contract:KNOWLEDGE_INDEX.md:
    kind: contract
    domain: cross-cutting
    artifact: KNOWLEDGE_INDEX.md
    lifecycle: null
    produced_by:
      - system:VERIFYING_PROTOCOL_HEALTH
    consumed_by:
      - core:GATHERING_CONTEXT
    file: .agents/contracts/KNOWLEDGE_INDEX.md

  contract:PROJECT_README.md:
    kind: contract
    domain: cross-cutting
    artifact: PROJECT_README.md
    lifecycle: null
    produced_by:
      - system:VERIFYING_PROTOCOL_HEALTH
    consumed_by:
      - core:GATHERING_CONTEXT
    file: .agents/contracts/PROJECT_README.md

  contract:REVIEW_REPORT.md:
    kind: contract
    domain: cross-cutting
    artifact: REVIEW_REPORT.md
    lifecycle: null
    produced_by:
      - core:VERIFYING
    consumed_by:
      - core:COMPLETED
    file: .agents/contracts/REVIEW_REPORT.md

  contract:HARNESS_REPORT.md:
    kind: contract
    domain: cross-cutting
    artifact: HARNESS_REPORT.md
    lifecycle: null
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:RECOVERY
      - core:COMPLETED
      - discovery:DISCOVERY_READY
    file: .agents/contracts/HARNESS_REPORT.md

  contract:METRICS.md:
    kind: contract
    domain: cross-cutting
    artifact: METRICS.md
    lifecycle: null
    produced_by:
      - core:TASK_RECEIVED
    consumed_by:
      - core:COMPLETED
    file: .agents/contracts/METRICS.md

  contract:KB_DISCOVERY_REPORT.md:
    kind: contract
    domain: discovery
    artifact: KB_DISCOVERY_REPORT.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - discovery:DISCOVERY_RUNNING
    file: .agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md

  contract:KB_RECOMMENDATION.md:
    kind: contract
    domain: core
    artifact: KB_RECOMMENDATION.md
    lifecycle: context
    produced_by:
      - core:GATHERING_CONTEXT
    consumed_by:
      - core:PLANNING
      - core:EXECUTING
      - core:VERIFYING
    file: .agents/orchestrators/core/contracts/KB_RECOMMENDATION.md

  contract:KB_DISCOVERY_ENTRY.md:
    kind: contract
    domain: discovery
    artifact: KB_DISCOVERY_ENTRY.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md

  contract:DISCOVERY_MANIFEST.md:
    kind: contract
    domain: discovery
    artifact: DISCOVERY_MANIFEST.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_MERGE
    consumed_by:
      - discovery:DISCOVERY_INIT
      - discovery:DISCOVERY_VALIDATE
    file: .agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md

  contract:DEVELOPMENT_PATTERNS.md:
    kind: contract
    domain: discovery
    artifact: DEVELOPMENT_PATTERNS.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_PATTERNS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/DEVELOPMENT_PATTERNS.md

  contract:ENVIRONMENT_DISCOVERY.md:
    kind: contract
    domain: discovery
    artifact: ENVIRONMENT_DISCOVERY.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_ENV
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md

  contract:EXECUTIVE_SUMMARY.md:
    kind: contract
    domain: discovery
    artifact: EXECUTIVE_SUMMARY.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_MERGE
    consumed_by:
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md

  contract:API_SURFACE.md:
    kind: contract
    domain: discovery
    artifact: API_SURFACE.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_FRAMEWORK
    consumed_by:
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/API_SURFACE.md

  contract:ARCHITECTURE.md:
    kind: contract
    domain: discovery
    artifact: ARCHITECTURE.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_FRAMEWORK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/ARCHITECTURE.md

  contract:BUSINESS_RULES.md:
    kind: contract
    domain: discovery
    artifact: BUSINESS_RULES.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_BUSINESS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/BUSINESS_RULES.md

  contract:CONFIGURATION.md:
    kind: contract
    domain: discovery
    artifact: CONFIGURATION.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_FRAMEWORK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/CONFIGURATION.md

  contract:CONTAINERS.md:
    kind: contract
    domain: discovery
    artifact: CONTAINERS.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_STACK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/CONTAINERS.md

  contract:DATABASE.md:
    kind: contract
    domain: discovery
    artifact: DATABASE.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_STACK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/DATABASE.md

  contract:DEPENDENCIES.md:
    kind: contract
    domain: discovery
    artifact: DEPENDENCIES.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_STACK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/DEPENDENCIES.md

  contract:DISTRIBUTION.md:
    kind: contract
    domain: discovery
    artifact: DISTRIBUTION.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_STACK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/DISTRIBUTION.md

  contract:ENTRYPOINT.md:
    kind: contract
    domain: discovery
    artifact: ENTRYPOINT.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_FRAMEWORK
    consumed_by:
      - discovery:DISCOVERY_MERGE
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/ENTRYPOINT.md

  contract:FILE_MAP.md:
    kind: contract
    domain: discovery
    artifact: FILE_MAP.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - discovery:DISCOVERY_MERGE
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/FILE_MAP.md

  contract:GLOSSARY.md:
    kind: contract
    domain: discovery
    artifact: GLOSSARY.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_BUSINESS
    consumed_by:
      - discovery:DISCOVERY_MERGE
      - core:GATHERING_CONTEXT
    file: .agents/orchestrators/discovery/contracts/GLOSSARY.md

  contract:KNOWN_ERRORS.md:
    kind: contract
    domain: discovery
    artifact: KNOWN_ERRORS.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_BUSINESS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/KNOWN_ERRORS.md

  contract:PROJECT_FLOW.md:
    kind: contract
    domain: discovery
    artifact: PROJECT_FLOW.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_BUSINESS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/PROJECT_FLOW.md

  contract:STACK.md:
    kind: contract
    domain: discovery
    artifact: STACK.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_STACK
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/STACK.md

  contract:TECHNICAL_DEBT.md:
    kind: contract
    domain: discovery
    artifact: TECHNICAL_DEBT.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_BUSINESS
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/TECHNICAL_DEBT.md

  contract:INTER_WORKER_MESSAGE.md:
    kind: contract
    domain: discovery
    artifact: INTER_WORKER_MESSAGE.md
    lifecycle: discovery
    produced_by:
      - discovery:DISCOVERY_INIT
    consumed_by:
      - discovery:DISCOVERY_MERGE
    file: .agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md

tags:
  domain:
    - core
    - discovery
    - system
    - cross-cutting
  lifecycle:
    - system
    - task
    - context
    - planning
    - execution
    - final
    - exception
    - discovery
  artifact:
    - analysis
    - reflection
    - specification
    - context
    - validation_report
    - plan
    - summary
    - report
    - log
    - brief
    - knowledge
  harness:
    - task
    - context
    - planning
    - execution
    - verification
    - recovery
    - discovery
    - system
    - taxonomy
    - delegation
  kind:
    - state
    - artifact
    - workflow
    - harness
    - actor
    - role
    - worker
    - contract
```
