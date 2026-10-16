# Changing an agent

For "what does this agent do", "why does it keep asking me", "make it shorter", "add Slack".

## Find it, then read all of it

If the person did not say which agent, find it with `agents_listAgents` (`search` by name) and confirm the one you found. Then, before your first answer about it:

```
agents_getAgent             prompt, model, status, settings
agents_listAgentSkills      what it carries, and which skills are editable
agents_listAgentToolkits    what it can reach
agents_listTriggers         whether it runs on a schedule
```

Answering from the name is guessing, and the person can see the real configuration in their settings.

## Explaining

Answer from what you read and point at the source — "its prompt tells it to ask before posting", "it has no Slack connection, so it can't post there". Quote the line when the question is about wording.

"Why did it do X" is often about a run you cannot see. Say so; then check what you can — `agents_listTriggerRuns` shows recent scheduled fires and their status. A cause inferred from the configuration is a likely cause; say it that way.

## Changing it

Propose, then apply after a yes. Show exactly what changes — the lines before and after, the toolkit added or removed — and nothing else. Look for every place the thing lives: a word limit set in the prompt and in a skill needs changing in both.

Then apply (`agents_updateAgent`, `agents_updateAgentSkill`, `agents_attachAgentToolkit` / `agents_detachAgentToolkit`) and read it back.

Two traps:

- `extra` is replaced whole on `agents_updateAgent`, and it also holds the agent's toolkits. Read it, change the field, send all of it back.
- A skill that ships with the platform may be read-only (`editable: false`). Say so and offer a new skill alongside — the expected answer, not a fault.

If the request is really a new agent — "one like this for German customers" — say so and offer `agents_cloneAgent` rather than quietly turning this one into something else.
