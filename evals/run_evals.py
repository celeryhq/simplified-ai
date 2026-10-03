#!/usr/bin/env python3
"""Exercise the hosted MCP connector, including middleware and tool validation.

Default: read-only account, asset-discovery, model and analytics checks.
--with-drafts creates accountless drafts and deletes only returned draft/group IDs.
--with-image spends credits, requires --model, and also stores a generated asset.
Use the apikit Python environment (fastmcp), SMP_ACCESS_TOKEN, and optional
SMP_MCP_URL (default https://apikit.simplified.com/mcp). Never publishes posts.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import sys
import time
from datetime import date, timedelta


class EvalFailure(RuntimeError):
    pass


def previous_month(today):
    end = today.replace(day=1) - timedelta(days=1)
    return end.replace(day=1).isoformat(), end.isoformat()


class Evaluator:
    def __init__(self, client, space_id=None, timeout=300):
        self.client = client
        self.scope = {} if space_id is None else {'space_id': space_id}
        self.timeout = timeout
        self.poll_interval = 4

    async def call(self, name, arguments):
        result = await self.client.call_tool(name, {**arguments, **self.scope}, raise_on_error=False)
        if result.is_error:
            # Avoid dumping potentially signed URLs, credentials or customer records.
            raise EvalFailure(f'{name} returned an MCP error')
        payload = result.structured_content
        if payload is None:
            for block in result.content:
                if getattr(block, 'type', None) == 'text':
                    try:
                        payload = json.loads(block.text)
                        break
                    except (ValueError, TypeError):
                        continue
        if not isinstance(payload, (dict, list)):
            raise EvalFailure(f'{name} returned no JSON payload')
        if isinstance(payload, dict) and payload.get('error'):
            task = payload.get('task_id')
            hint = f'; retain task_id={task} for follow-up, do not regenerate' if task else ''
            raise EvalFailure(f'{name} returned an application error{hint}')
        return payload

    async def image(self, model, parameters, storage):
        final = await self.call('api_generateImage', {
            'model': model, 'capability': 'prompt', 'storage': storage,
            'parameters': parameters})
        deadline = time.monotonic() + self.timeout
        while isinstance(final, dict) and final.get('status') in {'PENDING', 'STARTED', 'RETRY', 'PROGRESS'}:
            task_id = final.get('task_id')
            if not task_id or time.monotonic() >= deadline:
                raise EvalFailure('Generation pending; retain its task ID rather than regenerate')
            await asyncio.sleep(self.poll_interval)
            polled = await self.call('api_getTaskResult', {'task_id': task_id})
            final = {**polled, 'task_id': task_id}
        if not isinstance(final, dict) or final.get('status') != 'SUCCESS':
            raise EvalFailure('Generation did not return SUCCESS')
        detail = final.get('detail') or final.get('info') or {}
        results = detail.get('result', []) if isinstance(detail, dict) else []
        if not results:
            raise EvalFailure('Generation returned no images')
        item = results[0]
        if storage == 'asset':
            if not isinstance(item, dict) or not item.get('asset_id') or not item.get('url'):
                raise EvalFailure('Asset generation did not return asset_id and URL')
        elif not isinstance(item, str) or not item.startswith(('https://', 'http://')):
            raise EvalFailure('Transient generation did not return a URL')
        return item

    async def draft(self, keep=False, media=None):
        args = {'message': 'Simplified connector eval draft (safe to delete)', 'action': 'draft'}
        if media:
            args['media'] = media
        response = await self.call('social_createSocialMediaPost', args)
        if not isinstance(response, dict):
            raise EvalFailure('Draft create returned an unexpected payload; inspect before cleanup')
        if response.get('draft_id'):
            cleanup = {'draft_ids': [str(response['draft_id'])]}
        elif response.get('group_id'):
            cleanup = {'group_id': str(response['group_id'])}
        else:
            raise EvalFailure('Draft created but no typed draft/group ID returned; inspect manually, do not guess cleanup IDs')
        if not keep:
            try:
                await self.call('social_deleteSocialMediaDraft', cleanup)
            except Exception as exc:
                raise EvalFailure(f'Cleanup failed; manually remove eval draft using {cleanup}') from exc
        return cleanup

    async def analytics(self, accounts):
        if not accounts:
            return 'SKIP: no connected accounts'
        start, end = previous_month(date.today())
        response = await self.call('social_getSocialMediaAnalyticsAggregated', {
            'account_id': int(accounts[0]['id']), 'date_from': start, 'date_to': end})
        baseline = response.get('baseLine') if isinstance(response, dict) else None
        if not isinstance(baseline, dict):
            raise EvalFailure('Analytics returned no baseLine')
        expected = {'impressions_aggregated', 'engagement_aggregated', 'followers_aggregated', 'publishing_aggregated'}
        if expected - baseline.keys():
            raise EvalFailure('Analytics baseline missing requested KPI envelopes')
        return 'KPI envelopes present; availability/value interpretation requires account-specific review'


async def run(args, client):
    runner = Evaluator(client, args.space_id, args.timeout)
    failed = 0
    async def check(name, operation):
        nonlocal failed
        try:
            value = await operation()
            print(f'PASS {name}')
            return value
        except Exception as exc:
            failed += 1
            # Transport errors may contain request details, so print only type.
            detail = str(exc) if isinstance(exc, EvalFailure) else type(exc).__name__
            print(f'FAIL {name}: {detail}')
            return None
    async def accounts_check():
        response = await runner.call('social_getSocialMediaAccounts', {})
        accounts = response.get('accounts', response.get('results')) if isinstance(response, dict) else response
        if not isinstance(accounts, list) or any(not isinstance(a, dict) or 'id' not in a for a in accounts):
            raise EvalFailure('Invalid accounts envelope')
        return accounts
    accounts = await check('C3 accounts', accounts_check)
    async def assets_check():
        response = await runner.call('api_listAssets', {'page': 1, 'page_size': 1})
        if not isinstance(response, dict) or not isinstance(response.get('results'), list):
            raise EvalFailure('Invalid paginated asset-discovery envelope')
    await check('asset discovery', assets_check)
    await check('image model catalog', lambda: runner.call('api_listImageModels', {'capability': 'prompt'}))
    await check('video model catalog', lambda: runner.call('api_listVideoModels', {'capability': 'prompt'}))
    if accounts:
        await check('C5 analytics', lambda: runner.analytics(accounts))
    else:
        print('SKIP C5 analytics: no available account')
    if args.with_drafts:
        await check('C4 accountless draft + cleanup', lambda: runner.draft(args.keep_drafts))
    if args.with_image:
        fields = await check('current selected model fields', lambda: runner.call('api_getImageModelFields', {'model_id': args.model, 'capability': 'prompt'}))
        if fields is not None:
            # Model-specific required defaults; no stale count/aspect-ratio assumptions.
            definitions = fields.get('fields', {})
            parameters = {'prompt': 'a white ceramic coffee cup on a white background'}
            if not isinstance(definitions, dict) or 'prompt' not in definitions:
                raise EvalFailure('Model field response has no prompt schema')
            for key, field in definitions.items():
                if key != 'prompt' and field.get('required'):
                    if 'default_value' not in field:
                        raise EvalFailure(f'Model requires {key}; supply a model with defaults for this smoke test')
                    parameters[key] = field['default_value']
            await check('C1 transient image', lambda: runner.image(args.model, parameters, 'transient'))
            asset = await check('C6 persistent image', lambda: runner.image(args.model, parameters, 'asset'))
            if asset and args.with_drafts:
                async def asset_draft():
                    details = await runner.call('api_getAsset', {'id': asset['asset_id']})
                    if details.get('status') != 4:
                        raise EvalFailure('Generated asset not ready; retained for follow-up without creating a draft')
                    return await runner.draft(args.keep_drafts, [asset['asset_id']])
                await check('C6 asset-to-draft + cleanup', asset_draft)
            if asset:
                print(f'Generated asset retained: {asset["asset_id"]}')
    print(f'{failed} failed; skipped/opt-in cases are not evidence of live success')
    return int(bool(failed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-drafts', action='store_true')
    parser.add_argument('--with-image', action='store_true')
    parser.add_argument('--model', default=os.environ.get('SMP_EVAL_MODEL'))
    parser.add_argument('--keep-drafts', action='store_true')
    parser.add_argument('--space-id', type=int)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    if args.with_image and not args.model:
        parser.error('--with-image requires --model (select from the live catalog; consumes credits)')
    if args.keep_drafts and not args.with_drafts:
        parser.error('--keep-drafts requires --with-drafts')
    token = os.environ.get('SMP_ACCESS_TOKEN')
    if not token:
        print('ERROR: set SMP_ACCESS_TOKEN privately for authenticated MCP checks.', file=sys.stderr)
        return 2
    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport
    except ImportError:
        print('ERROR: run with the simplified-apikit Python environment (fastmcp).', file=sys.stderr)
        return 2
    async def connected():
        transport = StreamableHttpTransport(os.environ.get('SMP_MCP_URL', 'https://apikit.simplified.com/mcp'), headers={'Authorization': f'Bearer {token}'})
        async with Client(transport, timeout=args.timeout) as client:
            return await run(args, client)
    try:
        return asyncio.run(connected())
    except Exception as exc:
        print(f'ERROR: connector run stopped ({type(exc).__name__}).', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
