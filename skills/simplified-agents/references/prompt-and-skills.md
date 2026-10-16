# Prompt and skills

How to write the words an agent runs on.

## The split

A **prompt** answers: who is this, what is it for, what must always be true. It is short — a few hundred words for most agents — and changes rarely.

A **skill** answers: how do I do this particular thing well. It is where the real behaviour lives, and there is usually more than one.

They change at different rates and are edited by different people. Someone tuning how weekly reports get written should open the weekly-report skill and change it without reading, or risking, everything else.

The failure this prevents: everything in one long prompt. It works at first and then rots — nobody can find the sentence causing a behaviour, every edit risks the rest, and the whole thing reloads on every turn. When a prompt grows past role and constraints, cut a skill.

## Writing the prompt

Four things, in order:

1. **What it is and what it is for** — one or two concrete sentences. "You draft replies to customer emails about billing" beats "You are a helpful assistant."
2. **How it thinks** — the two or three principles that decide cases you did not anticipate.
3. **What must always be true** — never promise a refund, always cite the source, never send without showing a draft first.
4. **Voice** — a sentence or two, with an example if it is unusual.

Write the desired outcome rather than the forbidden one. Naming a thing to avoid it is the most reliable way to summon it. Explain why a constraint exists when it is not obvious; a constraint with a reason survives a case nobody foresaw.

Skip role-play flourish, capability lists, and anything the tools already make obvious.

## Writing a skill

Open with what it is for and when it applies. Then the method — the steps, the shape of good output, the decisions and how to make them. Show an example of finished output when the format is not obvious.

Say what "good" looks like in a way that can be checked: "three to five bullets, each naming a specific number", not "high quality". Name the failure modes you know about. Keep one skill to one job.

`agents_addAgentSkill` takes `title`, `content_text`, `doc_type` (use `skill` — other values are not shown in the agent's settings) and `injection_mode`. `context_only` keeps a skill out of the prompt until the agent chooses to open it, and agents often do not; anything that must always apply — the onboarding checklist, a hard rule — goes in as `system_prompt`.

## Borrow the voice that already exists

For an agent whose output a customer reads, read the brand first — `api_listBrandKits`, `api_getBrandKit`, `api_listContextDocuments` — and write the voice from what you find, saying where it came from. A generic "friendly and professional" is what gets written when nobody looked. Where there is no brand kit, ask for one line on how it should sound.

## Before you propose it

Read the prompt back as the agent. Clear on a normal request? On a weird one? Any rule without a reason? Cut anything the tools, skills or platform already establish.
