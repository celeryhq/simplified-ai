<p align="center"><img src="assets/simplified-logo.png" alt="Simplified" width="120" /></p>

# Simplified for AI

Use Simplified from Claude, ChatGPT, Codex, Cursor, or another compatible MCP client. Find uploaded assets, generate images and videos, create social drafts, manage brand context and projects, and schedule approved content.

This repository provides **skills**: instructions that teach an assistant how to use Simplified. The hosted **MCP connector** supplies the actual tools. A skill installation and a connector connection are separate: you need an authorized connector to run the workflows.

## Start here

1. [Connect your assistant](docs/CLIENTS.md) and complete Simplified sign-in.
2. Ask “Which Simplified workspace am I connected to?” to check scope.
3. Try an asset search or create an image with one of the prompts below.

| Your goal | Start with |
|---|---|
| Find/import/upload media, or reuse an existing asset | [Manage assets](skills/manage-assets/SKILL.md) |
| Generate an image from text or references | [Generate image](skills/generate-image/SKILL.md) |
| Remove/replace backgrounds, restore/upscale, or make masked image edits | [Edit image](skills/edit-image/SKILL.md) |
| Transcribe a recording or export subtitles | [Transcribe media](skills/transcribe-media/SKILL.md) |
| Create narration from an approved script | [Generate voiceover](skills/generate-voiceover/SKILL.md) |
| Turn a webinar, interview, or podcast into rendered clips and drafts | [Repurpose video](skills/repurpose-video/SKILL.md) |
| Animate an image or create a video | [Generate video](skills/generate-video/SKILL.md) |
| Create social drafts or schedule approved posts | [Simplified social](skills/simplified-social/SKILL.md) |
| Plan campaigns, review drafts, manage brands/projects, analyze results | [Skill catalog](SKILL_TREE.md) |

For a step-by-step walkthrough, see [Assets, images, and videos](docs/MEDIA.md). For integration details and profiles, see [MCP reference](docs/MCP.md).

## Prompts to try

- “Find uploaded images with ‘car’ in their name or tags and use them to create social drafts.”
- “Create a vertical product image and save it in my Asset Library.”
- “Use this asset ID to make a poster, keeping the product unchanged.”
- “Animate this uploaded product image into a short video and save it for reuse.”
- “Create two image variations for review; do not publish them.”
- “Turn this YouTube webinar into five vertical clips, preserve source timestamps, and save social drafts.”
- “Export an SRT transcript for this recording.”
- “Use a British-English voice for this approved narration script.”

Asset search is name/tag matching, not visual search. A folder name does not select its contents: named-folder browsing is not exposed by the current asset-list tool. A file attached to a chat is not automatically uploaded to Simplified.

## Install skills

### Claude Code plugin

```text
/plugin marketplace add celeryhq/simplified-ai
/plugin install simplified-ai@simplified-ai
```

The plugin declares the hosted connector in [`.mcp.json`](.mcp.json). Complete its OAuth authorization in the client.

### Compatible local agents

```bash
npx skills add celeryhq/simplified-ai
```

Select the skills and agent supported by your installed skills CLI. Run `npx skills --help` for current install/update options. Installing skills alone does not configure or authenticate MCP: follow [client setup](docs/CLIENTS.md).

### ChatGPT and Claude web/desktop

Connect Simplified through the client's app/connector interface. Use the listed Simplified app where available, or an authorized custom MCP connection when your account supports it. You do not paste CLI commands into a normal chat. The client may use tools without loading this repository's skills; use the [walkthrough](docs/MEDIA.md) as a human guide. Details and limitations are in [client setup](docs/CLIENTS.md).

## What to expect

- Asset IDs are reusable. File/thumbnail URLs can expire, even for saved assets.
- Image references accept asset IDs or absolute HTTP(S) URLs; video reference slots require asset IDs.
- Image/video generation spends credits. Explicit generation requests authorize the requested job; clarify significant ambiguity before spending.
- Current generation tools wait for a result. If they return a pending/timeout response, retain the identifiers and continue the existing job where supported; do not submit a duplicate.
- Creating media or drafts is separate from authorizing social publication. Preview drafts and obtain explicit publishing authorization before scheduling or queueing.
- Hosted tools, model availability, and client permissions change independently of these files. Check the tools exposed in the current connection. Old inventory snapshots are historical evidence, not a current capability guarantee.

## Contributing and validation

Canonical skill instructions live under `skills/`; `agents/openai.yaml` adds client metadata. Contributor checks:

```bash
python3 evals/run_skill_evals.py
python3 bin/build-codex-skills.py --out /tmp/simplified-ai-skills
```

See [evals](evals/README.md) for the difference between document checks, agent evaluations, and live tool tests. Packaging success does not prove a hosted deployment works. The ChatGPT skill bundle omits CLI-only and automation-only skills whose tools are unavailable on the declared connector.

AI-authored commits should include a `Co-Authored-By:` line naming the model. Licensed under [MIT](LICENSE).
