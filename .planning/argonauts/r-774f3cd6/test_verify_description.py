"""Read-only verifier self-tests; all mutation fixtures live under TMPDIR."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
BASE = b'[project]\nname = "fixture"\nversion = "0.1.0"\ndependencies = []\n\n[tool.fixture]\nflag = true\n'
LINE = b'description = "argonauts-uat public (UAT)"\n'
GOOD = BASE.replace(b'version = "0.1.0"\n', b'version = "0.1.0"\n' + LINE)


def driver():
    path = HERE / 'verify_description.py'
    assert path.is_file(), 'IMPLEMENTATION_MISSING: read-only description verifier'
    spec = importlib.util.spec_from_file_location('description_verifier', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContentTests(unittest.TestCase):
    def test_correct_single_line_is_accepted(self):
        result = driver().verify_content(BASE, GOOD)
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['failures'], [])
        self.assertTrue(all(c['status'] == 'PASS' for c in result['conditions']))


if __name__ == '__main__':
    unittest.main()
