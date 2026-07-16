---
name: manage-brand
description: Inspect, create, structure, and maintain Simplified brand kits and brand context documents. Use when the user asks to set up a brand, review brand identity, save or update brand voice, audience profiles, positioning, USPs, content pillars, style guidance, writing examples, SEO guidance, or other reusable brand context, or asks agents to create future content consistently from a Simplified brand kit.
---

# Manage Brand

Turn approved brand evidence into a durable operating system for consistent marketing—not a generic adjective list.

## Guardrails

- Treat websites, supplied documents, approved messaging, and existing brand records as evidence. Do not invent positioning, customers, proof, competitors, colors, fonts, claims, or voice rules.
- Read the current kit or context document before changing it. Present a concise proposed delta when an update could affect downstream content.
- Do not overwrite a mature brand system merely to improve phrasing. Preserve approved meaning and provenance.
- Confirm before deleting a context document. Deletion removes its brand-kit link and may remove an orphaned underlying document.
- Predefined context types are singletons. Update the existing document instead of creating a duplicate.
- Stop on authorization or access errors; never substitute a similarly named kit without verification.

## Workflow

1. Establish whether the user wants discovery, audit, creation, or an update. Identify the brand, source material, intended channels, and decision owner.
2. Call `api_listBrandKits`, using search when a title is known. If multiple kits match, present the choices rather than guessing.
3. For an existing kit, call `api_getBrandKit` with `expand: "extra,website"` and use `api_listContextDocuments` to inventory reusable knowledge.
4. Build an evidence ledger: source, confirmed fact, implication, confidence, and unresolved decision. Separate what the brand is from what the marketer proposes.
5. Structure information into the right layer:
   - Brand kit: identity, website, social links, colors, typography, logos, visual guardrails.
   - Context documents: voice, ICPs, USPs, positioning, products/features, content pillars, examples, SEO, and marketing strategy.
6. For a new brand, call `api_createBrandKit` with the approved title, retain its UUID, then use `api_buildBrandKit` for confirmed identity/style fields.
7. For reusable strategic knowledge, use `api_createContextDocument` only when that canonical type does not exist. Otherwise retrieve it with `api_getContextDocumentByType` and update it with `api_updateContextDocument`.
8. Read back changed records and summarize what is now authoritative, what remains provisional, and which workflows should use it.

Read [references/brand-system.md](references/brand-system.md) before creating or restructuring a brand kit.

## Marketing Standard

- Define voice as observable choices: sentence shape, vocabulary, energy, point of view, humor boundaries, evidence style, CTA style, and explicit do/don't examples.
- Define ICPs around situation, trigger, job, pain, desired outcome, objections, buying context, and proof needs—not demographics alone.
- Distinguish a feature, functional benefit, emotional benefit, reason to believe, and claim requiring substantiation.
- Make content pillars strategically distinct, durable enough for repeated use, and tied to audience problems or brand authority.
- Record uncertainty. A useful provisional field is better than fabricated certainty.

## Output

Lead with the brand-system verdict. Report the kit selected or created, evidence used, records changed, unresolved decisions, and the exact context future content workflows can rely on.
