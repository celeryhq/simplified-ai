import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from datetime import date
import run_evals as ev

class ConnectorTests(unittest.IsolatedAsyncioTestCase):
    def evaluator(self, responses):
        client=SimpleNamespace(call_tool=AsyncMock(side_effect=responses))
        return ev.Evaluator(client, space_id=42),client
    def result(self, data, error=False):
        return SimpleNamespace(is_error=error,structured_content=data,content=[])
    async def test_completed_image_does_not_regenerate_or_poll(self):
        runner,client=self.evaluator([self.result({'status':'SUCCESS','detail':{'result':[{'asset_id':'abc','url':'https://example.com/a'}]}})])
        out=await runner.image('asset',{'prompt':'coffee'},'asset')
        self.assertEqual(out['asset_id'],'abc')
        self.assertEqual(client.call_tool.await_count,1)
        self.assertEqual(client.call_tool.call_args.args,('api_generateImage',{'model':'asset','capability':'prompt','storage':'asset','parameters':{'prompt':'coffee'},'space_id':42}))
    async def test_pending_image_only_polls_returned_task(self):
        runner,client=self.evaluator([self.result({'task_id':'t','status':'PENDING'}),self.result({'status':'SUCCESS','detail':{'result':['https://example.com/a']}})])
        runner.poll_interval=0
        self.assertEqual(await runner.image('m',{'prompt':'coffee'},'transient'),'https://example.com/a')
        self.assertEqual(client.call_tool.call_args.args,('api_getTaskResult',{'task_id':'t','space_id':42}))
    async def test_mcp_errors_and_missing_payload_fail(self):
        runner,_=self.evaluator([self.result({'error':'denied'},True)])
        with self.assertRaises(ev.EvalFailure): await runner.call('api_getAsset',{})
        runner,_=self.evaluator([self.result(None)])
        with self.assertRaises(ev.EvalFailure): await runner.call('api_getAsset',{})
    async def test_group_cleanup_uses_group_id_not_draft_ids(self):
        runner,client=self.evaluator([self.result({'group_id':'group'}),self.result({'ok':True})])
        await runner.draft()
        self.assertEqual(client.call_tool.call_args.args,('social_deleteSocialMediaDraft',{'group_id':'group','space_id':42}))
    async def test_cleanup_failure_is_reported(self):
        runner,_=self.evaluator([self.result({'draft_id':'d'}),self.result({'error':'cleanup failed'},True)])
        with self.assertRaises(ev.EvalFailure): await runner.draft()
    async def test_unknown_draft_shape_does_not_guess_id(self):
        runner,client=self.evaluator([self.result({'id':'untyped'})])
        with self.assertRaises(ev.EvalFailure): await runner.draft()
        self.assertEqual(client.call_tool.await_count,1)
    async def test_text_only_mcp_response_is_decoded(self):
        runner,_=self.evaluator([SimpleNamespace(is_error=False,structured_content=None,content=[SimpleNamespace(type='text',text='{"results":[]}')])])
        self.assertEqual(await runner.call('api_listAssets',{}), {'results':[]})
    async def test_timeout_error_retains_task_for_followup(self):
        runner,_=self.evaluator([self.result({'error':True,'task_id':'t','message':'timeout'})])
        with self.assertRaisesRegex(ev.EvalFailure,'task_id=t'):
            await runner.call('api_generateImage',{})
    def test_previous_month_is_inclusive_completed_month(self):
        self.assertEqual(ev.previous_month(date(2026,1,7)),('2025-12-01','2025-12-31'))

if __name__=='__main__': unittest.main()
