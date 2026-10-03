import unittest
from run_skill_evals import grade_trace

class GraderTests(unittest.TestCase):
    def case(self,expected):return {'id':'sample','skill':'sample','expected':expected}
    def trace(self,tools):return {'skill':'sample','tools':tools}
    def test_omission_means_absent_not_null(self):
        case=self.case({'required_args':[{'tool':'create','path':'account_ids','absent':True}]})
        self.assertTrue(grade_trace(case,self.trace([{'name':'create','arguments':{}}])).passed)
        self.assertFalse(grade_trace(case,self.trace([{'name':'create','arguments':{'account_ids':None}}])).passed)
    def test_duplicate_submission_rejected(self):
        case=self.case({'max_tool_calls':{'create':1}})
        self.assertTrue(grade_trace(case,self.trace(['create','get','get'])).passed)
        self.assertFalse(grade_trace(case,self.trace(['create','create'])).passed)
    def test_wrong_resource_id_rejected(self):
        case=self.case({'handoffs':[{'from_tool':'create','from_path':'result.id','to_tool':'get','to_path':'arguments.project_id'}]})
        self.assertTrue(grade_trace(case,self.trace([{'name':'create','result':{'id':'project-1'}},{'name':'get','arguments':{'project_id':'project-1'}}])).passed)
        self.assertFalse(grade_trace(case,self.trace([{'name':'create','result':{'id':'project-1'}},{'name':'get','arguments':{'project_id':'asset-1'}}])).passed)
    def test_route_and_order_rejected(self):
        case=self.case({'ordered_tools':['create','get']})
        self.assertFalse(grade_trace(case,{'skill':'wrong','tools':['get','create']}).passed)
