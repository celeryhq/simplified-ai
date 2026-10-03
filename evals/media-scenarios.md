# Media documentation scenarios

Run these with an assistant given the revised skills and actual tool discovery. Use mocked/recorded outputs for documentation evaluation; paid/live runs need their own authorized scope.

| Prompt / environment | Required behavior | Failure to catch |
|---|---|---|
| Edit a ready image asset with Flux | Use `api_generateImage.parameters.reference_images` with UUID; retain scope | Provider-only `input_image`, unnecessary signed-URL conversion |
| Make a text video; tool returns `DONE` | Return terminal result; no manual polling | Treat response variation ID as art ID; poll a completed job |
| Video returns pending identifiers | Continue only existing variation with actual art/variation IDs | Poll submission task or pay for a duplicate |
| Find all images named car across three result pages | `api_listAssets(search: car, asset_type: 0)`; preserve scope/filters and collect pages | Only first page, guessed UUIDs, semantic claims |
| Use all images in Dynamic Auto folder | Explain unsupported folder enumeration; obtain supported asset selection | Folder name used as proof of complete search |
| ChatGPT attachment but no byte access/PUT tool | Use provided downloadable URL or user upload | Sign/register without transfer; hosted local path |
| Use an existing transient image in a draft | Import accessible URL; preserve returned UUID, check readiness, draft | Regenerate unnecessarily or invent permanent ID |
| Client lacks asset discovery | Check tool exposure; explain deployment/profile limitation | Claim installing skill adds tools |

Baseline review found stale image reference fields and storage defaults, missing asset discovery/pagination, missing attachment capability gate, and incomplete transient-to-asset guidance. Revised documents address those failures. Read-only scenario review is recorded separately from live integration results.
