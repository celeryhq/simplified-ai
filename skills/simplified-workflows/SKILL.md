---
name: simplified-workflows
description: Build, publish, run and control Simplified workflows — multi-step automations that chain AI generation, media editing, HTTP calls and notifications. Use when the user asks to create, edit or publish a Simplified workflow, run or re-run one, check why a run failed, pause or stop a run, approve a step waiting on review, or automate a repeatable multi-step task in Simplified. Read the connector's workflow resources before writing a step graph.
---

# Simplified Workflows

A workflow definition is a reusable graph of steps; it becomes runnable when published. Choose each step from the live action catalog—
blocks include — AI text and image generation, video and audio editing, PDF
tools, HTTP calls, Slack and email, project tasks, and control flow. A run
executes that graph once against a set of inputs.

## Connection and scope

Workflow tools (`flows_*`), agent tools, and `smp_callApi` belong to the automation connector at `https://apikit.simplified.com/automation/mcp` in the current multi-profile layout. The plugin’s root `https://apikit.simplified.com/mcp` connection serves public content/project/social tools and does not automatically grant automation tools. Verify exposed capabilities first; connect the automation surface if missing. A full connector, when explicitly configured, also serves these tools.

Resolve named or uncertain workspace/teamspace context with `simplified-workspace` on the public/full connection and carry the resolved numeric `space_id` on every workflow tool and passthrough call. Scope is stateless. Workflow resources have no `space_id` argument: use `flows_getWorkflow(workflow_id=..., expand="extra", space_id=...)` for a scoped diagram, and scoped `flows_listWorkflowActions` calls for live action schemas. The static grammar/run-control resources are safe to use independently of teamspace selection.

## Read the reference before writing a graph

The connector ships its reference material as **MCP resources**. They are not
in context — read them with your client's resource tool.

| Task | Read first |
|---|---|
| Build or edit a workflow | `workflow://diagram-grammar` |
| Run, poll, or control a run | `workflow://run-control` |
| Choose a step | `workflow://actions`, then `workflow://actions/{slug}` |
| Copy a working workflow's shape | `workflow://workflows/{id}/diagram` |

**Do not write a step graph without reading `workflow://diagram-grammar`.** The
block-id convention, the connection handle format, and the rule that declaring
an input takes two separate places are not inferable from the tool schemas.
Guessing yields a workflow that publishes cleanly and then behaves wrongly.

If the client cannot read MCP resources, use an available authoritative local copy of the connector’s grammar/run-control references and the current tool descriptions. Do not guess a graph from schema fields alone. If no grammar reference can be accessed, explain that limitation and finish discovery or run-status work that does not depend on graph authoring.

The connector also offers a `build_workflow` prompt if the client surfaces prompts. Its request to wait before building should be interpreted against the user’s existing authorization: do not add another approval gate when the user has already requested that construction and scope.

## Running an existing workflow

This is the common case. Prefer it over building something new.

1. `flows_listWorkflows` with `search` — find it and read its `inputs` schema.
   That schema is the only statement of what the run accepts.
2. Read its diagram and resolve the requested inputs and effects before starting. `flows_startWorkflow(workflow_id=<definition integer>, input=<flat object>, space_id=...)` returns immediately; its `workflow_id` response field is the run UUID. Pass `input: {}` for a workflow with no inputs, and never inject a `context` key. Use a stable `idempotency_key` when retrying an uncertain start so it cannot create a second run.
3. `flows_getWorkflowRunStatus` — poll until the status is `COMPLETED`,
   `FAILED`, `TERMINATED` or `TIMED_OUT`. Runs take minutes and can take hours;
   poll at a sensible interval.
4. `flows_getWorkflowRun` — only when you need the task-by-task breakdown of a
   finished run.

If a run stalls at `RUNNING` with a task in progress, it may be waiting on a
human-approval step. `workflow://run-control` covers resolving one.

## Building a new workflow

```
flows_listWorkflowActions   find each action with search, read its current schema
flows_createWorkflow        an empty DRAFT
flows_updateWorkflow        write the step graph
flows_publishWorkflow       compile it; now runnable
```

The grammar’s worked example demonstrates shape; discover current action/provider/model choices and output paths rather than assuming its illustrative AI settings remain available.

When a test run is within the user’s authorized scope, run it once with realistic input and check the output. A request to build/publish alone does not authorize sending notifications, publishing content, or spending credits for an unsolicited test. Finish and report the saved/published workflow before seeking any missing run authorization.

Authoring details that repeatedly cost time:

- **Publish compiles and validates the executable graph.** Inspect a 400 from save or publish; the current update schema also documents validation errors. Read the offending block message rather than retrying blindly.
- **`extra` is replaced wholesale.** Read the existing definition before editing and send the complete merged `extra` including inputs, diagram, and unrelated fields. Author `extra.diagram`; publish rebuilds `extra.conductor`. Omit an explicit publish `version` unless the user intends to overwrite version history.
- **Edits are not live until republished.** A changed graph does not affect new
  runs until `flows_publishWorkflow` runs again.

## Tell the user the plan first

A workflow run has real, often external, effects: it sends email, posts to
social accounts, publishes content, and spends workspace credits. Each action's
`consumes_credits` flag says whether that step bills.

- Do not start a run to find out what a workflow does. Read its diagram.
- Explain the concrete steps, inputs, credit use, and external destinations. Proceed with construction and runs already authorized by the user; ask only for missing authorization or unresolved consequential scope. Never add a routine confirmation gate for requested reversible authoring.
- `flows_deleteWorkflow` and `flows_terminateWorkflowRun` are permanent.
- Clean up only definitions clearly created as temporary tests. Preserve requested deliverables and their run history; verify the exact target before deletion.

## Gotchas

- **`flows_startWorkflow` returns the RUN id in a field named `workflow_id`.**
  A UUID there is a run; a small integer is a workflow definition. Run-control calls take
  `run_id`; the approval endpoint also takes the run UUID despite using
  `/run/…` in its path.
- **`flows_listWorkflows` does not list drafts.** Use `flows_getWorkflow` for
  one you just created, with `expand=extra` to see its graph.
- **`flows_listWorkflowActions` caps `page_size` at 100** regardless of what
  you ask for, and returns 503 intermittently. Pass `search`; retry a 503.
- **Some required action fields list no valid values.** They draw them from a
  live endpoint — the action's `uiSchema` marks these `selectAsync` and names
  the URL. Fetch it and choose from the result; a made-up value is accepted and
  then misbehaves. `workflow://diagram-grammar` has the procedure.
- **resume, retry and restart are three different things.** Resume continues a paused run; retry recovers a `FAILED` run from its failed task. Restart reuses the same run UUID and input from the beginning and repeats effects and credits. After correcting and publishing a definition, pass `useLatestDefinitions: true` to restart against the fix; its default is false. To correct input, start a new run with corrected `input` rather than restarting the old input.
- **Approval input naming differs from output.** Read `reference_task_name` from status with `expand: "tasks"`, then pass its value as `task_reference_name` to `flows_approveWorkflowTask`, with `run_id` and `status: "COMPLETED"` or `"FAILED"`. Release only a gate the user has authorized you to resolve.
- **Paused runs and review gates need action.** Do not endlessly poll a run intentionally paused or waiting for human input; report the required action and continue only within authorized scope. Bound retries of transient action-list 503s (for example three attempts), keeping `page_size` at most 100.

## When a result looks wrong

Check a distinguishing field rather than the status code alone. A response can
arrive successfully and still be the wrong thing — an empty `inputs` schema, for
example, means either that the workflow genuinely takes no inputs *or* that its
definition is broken, and the two look identical.

If something surprising comes back, confirm what actually answered before
concluding the workflow is at fault.

## Reaching past the tools

`smp_callApi` takes `method`, a relative API `path`, optional `service` (`api` or `agents`), `query`, `body`, and `space_id`. Never pass a full URL or credentials. It returns `{status, body}`; inspect the status and parse the body before trusting results. Use `query` for selectAsync choices parameters rather than guessing values. Prefer a
real tool wherever one exists — the passthrough has no field documentation and
no validation. It is for the long tail: the choices endpoint behind a
`selectAsync` field, or anything the tool set does not cover.
