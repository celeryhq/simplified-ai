# Choosing tools

What an agent can reach, and what it should not be carrying.

## Read the catalogue, do not remember it

```
agents_listToolkits          what exists, and the tools inside each
agents_listAvailableTools    individual tools available to an agent
agents_listAvailableModels   models you may set
```

Check at build time, every time. A remembered list produces an agent that fails on its first run with an error the person cannot interpret. Never invent a model string; pick from the list or leave it unset for the platform default.

## Match tools to the job, not the topic

Walk the person's example through: to do that one task, what must the agent read, and what must it change? Those are the tools. Anything that merely relates to the subject is not. An agent that drafts posts needs to write posts; it needs analytics only if drafting uses them.

## Some capabilities come with the job

Narrow means nothing the job does not need. It does not mean leaving out what it cannot work without. Three requirements are implied rather than stated:

| When the job… | it needs | because without it |
|---|---|---|
| acts on an account the person owns — posts to Instagram, reads LinkedIn analytics, sends to Slack | the tools that act on it, **and** `interrupt` for `social_connect` (social accounts) or `mcp_connect` (other apps) | the first run hits an unconnected account with no way to ask for it |
| happens on a cadence — "every Monday", "three times a week" | `triggers` | it runs once, when someone remembers, and never again |
| produces something the person looks at — a post, a carousel, an image | `display` | the person reads a description instead of seeing it, and approves something they never saw |

Social tools are in the `simplified-api` toolkit as `simplified_social__*`; attach it and narrow it to the ones the job uses. When the person wants to review before anything goes out, `interrupt` also carries `request_approval`, which makes that a real gate.

Attaching is half of it: the agent's skills must say when each tool is used — connect before the first post, show the draft before asking approval, create its schedule once the cadence is confirmed. A tool the agent was never told about usually goes unused.

Worked example — "an Instagram educator, three finance carousels a week, I see each one first":

- `simplified-api`, narrowed to connected accounts, drafts and scheduling, the review bundle, and image generation
- `interrupt` — `social_connect`, `request_approval`
- `display` — each carousel shown as a carousel
- `triggers` — Monday, Wednesday, Friday without being asked

Not analytics: nothing in the job reads performance. Say so.

## Every tool costs something on every turn

Each attached tool's schema is in front of the model on every turn. A model holding forty tools picks the wrong one more often than one holding six, and with write tools the wrong pick is a wrong action. Attach the toolkit, then narrow it with `agents_updateAgentToolkit` to the tools in use. Adding one later is a thirty-second change.

## In the proposal

One line per toolkit and the part of the job it serves; which tools you kept when you narrowed; anything the person might expect that you left out, and why. And what the first run will ask of them — which account to connect, when the schedule starts.
