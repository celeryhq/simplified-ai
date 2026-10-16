# Building an agent

The path from "I want something that does X" to a working agent the person can open.

## What you need to know

Four things decide almost everything. You will usually infer three of them.

**The job.** What the agent does, in the person's own words, with one concrete example of a time they would have used it. The example matters more than the description — it tells you what the output actually has to be.

**Who talks to it.** Just them, their team, or their customers. This sets the voice and how much it should assume.

**What it needs to touch.** Their brand kit, social accounts, projects, the web, files they upload. Usually answered by the job rather than by asking.

**What "done" looks like.** A drafted post, a filled spreadsheet, a short answer, a decision. An agent with no clear finish line rambles.

Ask about the job and the example. Infer the rest and say what you inferred. If two readings of the request would produce genuinely different agents, that is the one question worth asking outright.

## Look before you ask

`agents_listAgents` shows what the workspace already has. A near-match changes the conversation — cloning and adjusting (`agents_cloneAgent`) beats building from nothing, and the person may not know the near-match exists.

List the whole workspace. Pass `space_id` only when the person named a teamspace: a wrong scope returns an empty list rather than an error, and "you have no agents" is then a confident wrong answer.

## The proposal

One message, written to be read once:

- the agent's name and a one-line description
- the system prompt, in full, as you will send it — a summary of a prompt is not reviewable
- each skill and what it makes the agent do
- the toolkits and why each is there ([Choosing tools](choosing-tools.md))
- its onboarding checklist ([Onboarding checklist](onboarding-checklist.md))

Then stop. The build is the next turn.

## The build, in order

```
agents_createAgent          title, description, model, system_prompt, status=draft
agents_addAgentSkill        one call per skill; the Onboarding skill with injection_mode=system_prompt
agents_attachAgentToolkit   one call per toolkit
agents_updateAgentToolkit   narrow a broad toolkit to the tools the job uses
agents_createTrigger        only if the job runs on a schedule and the person confirmed it
agents_getAgent             read back what was actually created
```

Create as a draft. Draft is the state where the person can look at the thing before it can run.

Attach skills before toolkits: if something fails partway, an agent with its behaviour and no tools is easier to finish than the reverse.

## Handing it over

Report what exists: the name, its status, the skills and toolkits on it, and where to open it. Then the one next step — usually reviewing the prompt and activating it, which is its own confirmed turn. If anything did not land as proposed, that goes first.
