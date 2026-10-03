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
  historical inventory of the older local `simplified-apikit` `mcp` profile. It does not represent today's source profiles or hosted deployment.
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
selected inventory snapshot. A historical snapshot can pass these checks while
missing new tools or carrying outdated schemas.

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
- An OAuth access token (`SMP_ACCESS_TOKEN`), configured privately; refresh it when expired.
- The apikit Python environment, which supplies `fastmcp`.
- AI credits only for opt-in image cases; select a current model explicitly.
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
/path/to/apikit/.venv/bin/python evals/run_evals.py # read-only MCP checks
/path/to/apikit/.venv/bin/python evals/run_evals.py --with-drafts # creates/cleans accountless drafts
/path/to/apikit/.venv/bin/python evals/run_evals.py --with-image --model <current-model-id> --with-drafts # spends credits, retains generated asset
/path/to/apikit/.venv/bin/python evals/run_evals.py --with-drafts --keep-drafts
```

The harness calls canonical MCP tools at `https://apikit.simplified.com/mcp`, including middleware and validation. Set `SMP_MCP_URL` for an explicitly chosen environment and `--space-id` only after resolving the intended teamspace. It never schedules or queues posts. There is no fixed image model or credit estimate: choose `--model` from the live catalog and review its current pricing. `--with-image` retains the generated asset. Draft cleanup uses only returned typed draft/group IDs and fails visibly if cleanup cannot be verified.

Exit code is non-zero if any run case fails. Skipped cases do not establish success. The harness covers C1/C3/C4/C5/C6 response contracts; C2 text rendering and composition remain a manual visual review.

Run harness regressions without credentials or network:

```bash
python3 -m unittest discover -s evals -p test_run_evals.py
```

## Asset and generation documentation review

See [media scenarios](media-scenarios.md) for the added asset/generation/client checks. The October 2026 documentation review compares local API contracts and read-only agent scenario responses. It does not replace authenticated live testing or prove that a hosted tool is deployed.

The current `run_evals.py` uses MCP rather than the legacy raw image route. Recorded older golden outputs remain historical and do not become evidence for the new harness. The new regression tests use simulated MCP responses; authenticated live mutation tests must be reported separately.

## Full source audit

All skills and references are covered in [the full audit](../docs/FULL-AUDIT-2026-10-02.md). Additional realistic scenarios are in [marketer cases](marketer-audit-scenarios.md), [social/PM cases](social-pm-audit-scenarios.md), and [brand/projects/workflow cases](brand-projects-workflow-audit-scenarios.md).

Run the source checker using the Python environment that has apikit dependencies installed:

```bash
/path/to/simplified-apikit/.venv/bin/python evals/check_source_contracts.py --apikit /path/to/simplified-apikit
```

It compares canonical tool names and literal smp command names/options/required fields/top-level enums against that checkout, without dispatching API calls. It does not validate arbitrary prose, all nested payload semantics, deployment availability, or live behavior. `--root` can point it at another skills tree. Use generated schemas and realistic traces to verify those remaining dimensions.

New image editing, transcription, narration and video-clipping operators have [static pressure scenarios](new-media-scenarios.md). Their document contracts are checked locally; no live media jobs or agent tool traces are implied.
