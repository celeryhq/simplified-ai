import importlib.util
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'bin'))
from validate_skills import validate_tree

class StructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.skill=self.root/'skills'/'sample';(self.skill/'agents').mkdir(parents=True)
        self.doc=self.skill/'SKILL.md';self.doc.write_text('---\nname: sample\ndescription: Use for a concrete sample task.\n---\n# Sample\n')
        self.meta=self.skill/'agents/openai.yaml';self.meta.write_text('interface:\n  display_name: "Sample"\n  short_description: "Perform a concrete sample task."\n  default_prompt: "Use $sample for this sample task."\npolicy:\n  allow_implicit_invocation: true\n')
    def test_valid(self):self.assertEqual(validate_tree(self.root),[])
    def test_name_mismatch(self):
        self.doc.write_text(self.doc.read_text().replace('name: sample','name: other'));self.assertTrue(validate_tree(self.root))
    def test_invalid_yaml(self):
        self.doc.write_text('---\nname: [broken\n---\n');self.assertTrue(validate_tree(self.root))
    def test_description_limit(self):
        self.doc.write_text('---\nname: sample\ndescription: '+('x'*1025)+'\n---\n');self.assertTrue(validate_tree(self.root))
    def test_metadata_default_prompt(self):
        self.meta.write_text(self.meta.read_text().replace('$sample','sample'));self.assertTrue(validate_tree(self.root))
    def test_missing_icon(self):
        self.meta.write_text(self.meta.read_text().replace('  display_name:', '  icon_small: "assets/missing.png"\n  display_name:'));self.assertTrue(validate_tree(self.root))
    def test_broken_reference(self):
        self.doc.write_text(self.doc.read_text()+'[Details](references/missing.md)\n');self.assertTrue(validate_tree(self.root))
    def test_valid_reference(self):
        (self.skill/'references').mkdir();(self.skill/'references'/'details.md').write_text('# Details')
        self.doc.write_text(self.doc.read_text()+'[Details](references/details.md)\n');self.assertEqual(validate_tree(self.root),[])
    def test_policy_type(self):
        self.meta.write_text(self.meta.read_text().replace('true','"true"'));self.assertTrue(validate_tree(self.root))
    def test_no_skills(self):self.assertTrue(validate_tree(self.root/'absent'))
