# Onboarding checklist

An agent that needs an Instagram account will be opened by someone who has not connected one. Without a checklist its first real request fails halfway and the person concludes it is broken. With one, the first thing it says is "connect Instagram, then I'll start".

So every agent you build gets an **Onboarding** skill. No exceptions — one with nothing to set up gets a one-item checklist saying so.

## Deriving the checklist

Walk the job and the toolkits you chose, and list what must exist before the first real piece of work:

| Source | Item | How the agent checks it |
|---|---|---|
| It acts on an account the person owns | "Instagram connected" | with a tool — list connected accounts, do not remember it |
| An input it cannot infer — who to watch, the audience, the product | "Competitors named" | memory: asked once, stored, read back |
| It runs on a cadence | "Schedule confirmed and created" | list its own triggers |
| It writes anything a customer reads | "Brand voice known" | the brand kit, or one stored line from the person |

Only what blocks the work. Eight items is a form, and people abandon forms. Order: connections, then inputs, then the schedule last — a schedule set before the inputs exist fires into nothing.

## What the skill tells the agent

1. At the start of every conversation, check every item before doing what was asked — with a tool wherever one exists; connections expire.
2. When something is missing, say what, and fix it one item at a time; then carry on with the original request.
3. No real work while an item is incomplete — not a partial draft.
4. Once everything is in place, say nothing about it.
5. On a run with nobody to ask, such as a scheduled one, do not try to onboard: stop and say exactly what is missing.

Write the items as a short numbered list at the top, then the rules, in the agent's own terms.

## Attaching it

`agents_addAgentSkill`, titled "Onboarding", `doc_type` `skill`, `injection_mode` `system_prompt` — a gate the agent can choose not to open is not a gate. Make sure the toolkits support every check: `interrupt` for the connect step, `memory` for stored inputs, `triggers` for the schedule.

Show the checklist in the proposal as its own list — it is the first thing the person meets.
