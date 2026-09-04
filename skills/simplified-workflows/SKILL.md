---
name: simplified-workflows
description: Build, publish, run and control Simplified workflows — multi-step automations that chain AI generation, media editing, HTTP calls and notifications. Use when the user asks to create, edit or publish a Simplified workflow, run or re-run one, check why a run failed, pause or stop a run, approve a step waiting on review, or automate a repeatable multi-step task in Simplified. Read the connector's workflow resources before writing a step graph.
---

# Simplified Workflows

A workflow is a published, reusable graph of steps. Each step is one of ~250
action blocks — AI text and image generation, video and audio editing, PDF
tools, HTTP calls, Slack and email, project tasks, and control flow. A run
executes that graph once against a set of inputs.

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

The connector also offers a `build_workflow` prompt — the same procedure as a
slash command, if the client surfaces prompts.

## Running an existing workflow

This is the common case. Prefer it over building something new.

1. `flows_listWorkflows` with `search` — find it and read its `inputs` schema.
   That schema is the only statement of what the run accepts.
2. `flows_startWorkflow` — returns immediately with a run ID. It does not wait.
3. `flows_getWorkflowRunStatus` — poll until the status is `COMPLETED`,
   `FAILED`, `TERMINATED` or `TIMED_OUT`. Runs take minutes and can take hours;
   poll at a sensible interval.
4. `flows_getWorkflowRun` — only when you need the task-by-task breakdown of a
   finished run.

If a run stalls at `RUNNING` with a task in progress, it may be waiting on a
human-approval step. `workflow://run-control` covers resolving one.

## Building a new workflow

```
flows_listWorkflowActions   find the action for each step, read its schema
flows_createWorkflow        an empty DRAFT
flows_updateWorkflow        write the step graph
flows_publishWorkflow       compile it; now runnable
```

Then run it once with realistic input and check the output before handing it
over.

Two things that repeatedly cost time:

- **Publish validates; save does not.** A 400 from publish names the offending
  block. Read the message rather than retrying.
- **Edits are not live until republished.** A changed graph does not affect new
  runs until `flows_publishWorkflow` runs again.

## Tell the user the plan first

A workflow run has real, often external, effects: it sends email, posts to
social accounts, publishes content, and spends workspace credits. Each action's
`consumes_credits` flag says whether that step bills.

- Do not start a run to find out what a workflow does. Read its diagram.
- Confirm the plan before building something, and before the first run of
  anything with outside effects.
- `flows_deleteWorkflow` and `flows_terminateWorkflowRun` are permanent.
- Delete workflows you created only for testing.

## Gotchas

- **`flows_startWorkflow` returns the RUN id in a field named `workflow_id`.**
  A UUID there is a run; a small integer is a workflow definition. Every
  `/executions/…` operation wants the run ID.
- **`flows_listWorkflows` does not list drafts.** Use `flows_getWorkflow` for
  one you just created, with `expand=extra` to see its graph.
- **`flows_listWorkflowActions` caps `page_size` at 100** regardless of what
  you ask for, and returns 503 intermittently. Pass `search`; retry a 503.
- **Some required action fields list no valid values.** They draw them from a
  live endpoint — the action's `uiSchema` marks these `selectAsync` and names
  the URL. Fetch it and choose from the result; a made-up value is accepted and
  then misbehaves. `workflow://diagram-grammar` has the procedure.
- **resume, retry and restart are three different things.** Resume continues a
  paused run, retry recovers a failed one from where it broke, restart re-runs
  from the beginning and spends credits again.

## When a result looks wrong

Check a distinguishing field rather than the status code alone. A response can
arrive successfully and still be the wrong thing — an empty `inputs` schema, for
example, means either that the workflow genuinely takes no inputs *or* that its
definition is broken, and the two look identical.

If something surprising comes back, confirm what actually answered before
concluding the workflow is at fault.

## Reaching past the tools

`smp_callApi` calls any Simplified endpoint by `method` and `path`. Prefer a
real tool wherever one exists — the passthrough has no field documentation and
no validation. It is for the long tail: the choices endpoint behind a
`selectAsync` field, or anything the tool set does not cover.
