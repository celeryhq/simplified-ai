# Evals — Simplified for AI

Internal QA for the plugin: how we validate the skills + connector before and after
release. Not required to *use* the plugin — kept in the repo for transparency and
contributors. Safe to ignore if you're just installing the skills.

## Files
- [openai-test-cases.md](openai-test-cases.md) — the review cases in OpenAI's
  submission format (Scenario / User prompt / Tool triggered / Expected output).
  Paste into the form.
- [cases.md](cases.md) — canonical definitions: expected tool sequence, argument
  contract, and assertions for each case (agent layer + I/O layer).
- [skill-cases.json](skill-cases.json) — 38 machine-readable routing scenarios:
  26 marketer cases (at least three per workflow) plus 12 source-profile cases for AI
  video, brand management, marketing projects, and workspace/teamspace context.
- [hosted-tool-inventory.json](hosted-tool-inventory.json) — authenticated snapshot
  of the live hosted tool names and critical input schemas.
- [source-profile-tool-inventory.json](source-profile-tool-inventory.json) — generated
  inventory of the compact local `simplified-apikit` `mcp` profile. The hosted
  deployment currently exposes a broader 105-tool allowlist.
- [run_skill_evals.py](run_skill_evals.py) — zero-credential contract validator and
  optional agent-trace grader for routing, tool order, arguments, handoffs, and safety.
- [fixtures/sample-skill-traces.json](fixtures/sample-skill-traces.json) — example
  trace showing the expected capture format and image asset handoff.
- [fixtures/live-routing-smoke-2026-07-14.json](fixtures/live-routing-smoke-2026-07-14.json)
  — captured 5/5 skill-selection smoke result from the locally installed plugin.
- [marketer-workflow-cases.md](marketer-workflow-cases.md) — human-readable smoke
  scenarios and pass criteria for the marketer workflows.
- [run_evals.py](run_evals.py) — runnable harness that checks the **I/O layer**
  (the tools behave as the skills claim) against the live API.
- [results.md](results.md) — golden outputs captured from live runs + pass/fail log.

## What the layers mean
- **Contract layer** — do all platform and workflow skill files plus the eval catalog contain the required
  safety and orchestration contracts? `run_skill_evals.py` checks this locally and in CI.
- **Agent layer** — does the model select the intended skill and call the right tools
  in the right order with safe arguments? Capture traces and grade them with
  `run_skill_evals.py --traces`.
- **I/O layer** — do the tools return what the skills promise? `run_evals.py`
  automates this deterministically (no model in the loop).

## Run skill and agent evals

The contract suite has no third-party dependencies, credentials, network calls, or
live mutations. It also rejects eval cases that reference tools absent from the
verified hosted inventory:

```bash
python3 evals/run_skill_evals.py
```

To grade agent runs, capture a JSON list or JSONL file with each selected skill,
tool call, arguments, optional tool result, and final output:

```json
{
  "id": "C2-generate-campaign-asset",
  "skill": "cross-platform-campaign",
  "tools": [
    {"name": "api_generateImage", "arguments": {"storage": "asset"},
     "result": {"detail": {"result": [{"asset_id": "asset-123"}]}}},
    {"name": "social_createSocialMediaPost",
     "arguments": {"action": "draft", "media": ["asset-123"]}}
  ],
  "output": "Drafts created for review."
}
```

Grade all catalog cases, or a partial development capture:

```bash
python3 evals/run_skill_evals.py --traces /path/to/traces.json
python3 evals/run_skill_evals.py --traces /path/to/traces.json --allow-missing
```

Without `--allow-missing`, every catalog case must have a trace. The grader checks:

- intended skill selection;
- required, forbidden, and ordered tools;
- required and forbidden tool arguments;
- generated asset IDs passed unchanged into social `media`;
- required safety language in the final output.

## Prerequisites
- An OAuth access token (`SMP_ACCESS_TOKEN`). Tokens last ~1 hour.
- AI credits (only for image cases, run with `--with-image`).
- A connected social account in the workspace (only for the analytics case; the
  draft cases use accountless drafts and need no connected account).

## Minting an access token (DCR + PKCE)

The static OAuth apps aren't loaded on prod, so register a client dynamically:

```bash
# 1. Register a public client (RFC 7591 DCR) — returns a client_id
curl -s -X POST "https://api.simplified.com/api/o/register/" \
  -H "Content-Type: application/json" \
  -d '{"client_name":"eval client","redirect_uris":["http://localhost:3000/oauth/callback"],"token_endpoint_auth_method":"none"}'

# 2. Build a PKCE challenge
python3 - <<'PY'
import secrets,hashlib,base64,json
v=base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b'=').decode()
c=base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b'=').decode()
open('/tmp/pkce.json','w').write(json.dumps({'verifier':v,'challenge':c}))
print('challenge:',c)
PY

# 3. Open the authorize URL in a browser, log in, approve. Copy `code` from the
#    redirect (http://localhost:3000/oauth/callback?code=...&state=...):
#    https://api.simplified.com/api/o/authorize/?response_type=code
#      &client_id=<CLIENT_ID>&redirect_uri=http://localhost:3000/oauth/callback
#      &scope=openid+read+write+ai:generate+social:write
#      &code_challenge=<CHALLENGE>&code_challenge_method=S256&state=x

# 4. Exchange the code for a token
VERIFIER=$(python3 -c "import json;print(json.load(open('/tmp/pkce.json'))['verifier'])")
curl -s -X POST "https://api.simplified.com/api/o/token/" \
  -d grant_type=authorization_code -d code=<CODE> \
  --data-urlencode redirect_uri=http://localhost:3000/oauth/callback \
  -d client_id=<CLIENT_ID> -d code_verifier=$VERIFIER
# → copy access_token
```

## Run live connector I/O evals

```bash
export SMP_ACCESS_TOKEN=<access_token>
python3 evals/run_evals.py              # read-only + draft cases (no credit spend)
python3 evals/run_evals.py --with-image # also image-gen + cross-skill (consume credits)
python3 evals/run_evals.py --keep-drafts
```

Exit code is non-zero if any non-skipped case fails. Image cases default to
`flux.flux-schnell` (8 credits); override with `SMP_EVAL_MODEL`.
