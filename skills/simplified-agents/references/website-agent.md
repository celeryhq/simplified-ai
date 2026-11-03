# Website chat agent

Turning one website address into an agent answering visitors on that site. Done by hand this is eight steps; here it is one question.

## The agent

A website chat agent answers strangers, so it holds only search tools — the `knowledge` toolkit and `system` — and nothing that changes the account. You do the setup for it. Use an existing one if the workspace has it; otherwise build it as in [Building an agent](build-an-agent.md): answers only from its knowledge base, short replies, no invented prices or promises, never asks visitors for contact details, routes them to the team when it cannot help.

## The one question

Ask for the website address. Everything else comes from the site.

## Read the site

With your web-fetch tool:

1. `/sitemap.xml`, or the sitemap named in `/robots.txt`. A sitemap index points at sub-sitemaps — read the page and post ones.
2. Pick the **business pages**: home, about, services, pricing, industries, FAQ, contact, booking, case studies. Leave out page-builder leftovers (`/test/`, `/landing-page/`) and, by default, the blog — general advice crowds out answers about what the business sells.
3. From the home, about and contact pages note: the name as the site writes it, one sentence of what it does, the contact URL, any booking or consultation URL (look for Calendly links), the logo — a square icon from the site's `<link rel="icon">` set — and the accent colour.

## Propose it

The pages to index and the ones left out; the **About this business** text (below); the widget's title, opening line, two or three suggested questions, logo and colour; the domains it answers on (with and without `www`); handover — on notifies the publisher when a visitor wants a person, off points them to the contact page; and connectors, only if wanted. Then stop for a yes.

## Build, in order

```
agents_createKnowledgeBase    title (the field is "title", not "name")
agents_addKnowledgeSource     one call per page — a source is ONE page; links are not followed
agents_getAgent               read the agent's whole extra
agents_updateAgent            extra.metadata.knowledge_bases = [kb id]
agents_addAgentSkill          "About this business", injection_mode=system_prompt
agents_publishWebChatBot      allowed_origins, appearance
agents_updateWebChatBot       handover {"enabled": true|false}, lead form
agents_listKnowledgeSources   confirm ingest is moving
```

Traps, each hit for real:

- **`extra` is replaced whole** and holds the agent's toolkits. Read it, set `metadata.knowledge_bases`, send all of it back.
- **Publishing makes the bot live at once**, on the listed domains and its demo page. Safe — the snippet is not on their site yet — but do not call it a draft.
- **Ingest runs in the background and can stall.** Sources go `PENDING` → `READY`. If nothing moves for ten minutes, `agents_reingestKnowledgeBase`. Hand over once it is moving and say how many pages are in.

## About this business

A skill on the agent, facts from the site only:

```
Business: <name> — <website>
What it does: <one sentence from the site>
Contact page: <url>
Booking link: <url, if any>
Free consultation / audit: <url, if any>
```

## Connectors

Only when asked, each with its guard — this agent talks to strangers:

- **Book a call** — a booking link in About this business. Never calendar tools: a visitor must not be able to create events in the owner's calendar.
- **Lead to CRM** — narrowed to creating a contact or lead only. Never a tool that reads the CRM: on a public chat, a read tool lets any visitor ask for the owner's customer list.

## Hand over

The `embed_snippet` from the bot, to paste site-wide (usually the footer), and the `demo_url` to try it first.
