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
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContentTests(unittest.TestCase):
    def checked(self, v, baseline, candidate):
        try:
            return v.verify_content(baseline, candidate)
        except Exception as error:
            self.fail(f'CONTENT_RESULT_MISSING: expected structured result, got {type(error).__name__}: {error}')

    def test_correct_single_line_is_accepted(self):
        result = driver().verify_content(BASE, GOOD)
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(result['failures'], [])
        self.assertTrue(all(c['status'] == 'PASS' for c in result['conditions']))

    def test_content_negative_conditions(self):
        v = driver()
        cases = [
            (BASE, 'VALUE_EXACT'),
            (GOOD.replace(b'public (UAT)', b'public (UAT) (UAT)'), 'VALUE_EXACT'),
            (GOOD.replace(b'public (UAT)', b'other'), 'VALUE_EXACT'),
            (GOOD.replace(b'fixture"', b'changed"'), 'STRUCTURE_UNCHANGED'),
            (GOOD.replace(b'flag = true', b'flag = false'), 'STRUCTURE_UNCHANGED'),
            (GOOD + b'\n', 'BYTES_UNCHANGED'),
            (GOOD.replace(b'name =', b'name  ='), 'BYTES_UNCHANGED'),
            (GOOD.replace(b'\n', b'\r\n'), 'BYTES_UNCHANGED'),
            (GOOD.replace(LINE, b'description = 42\n'), 'VALUE_EXACT'),
            (BASE + LINE, 'VALUE_EXACT'),
        ]
        for candidate, ident in cases:
            with self.subTest(ident=ident, candidate=candidate):
                result = self.checked(v, BASE, candidate)
                self.assertEqual(result['exit_code'], 1)
                self.assertIn(ident, result['failures'])
        self.assertEqual(v.verify_content(BASE, BASE)['failures'], ['VALUE_EXACT'])

    def test_candidate_parse_error_is_requirement_failure(self):
        v = driver()
        for candidate in (b'[project', GOOD.replace(LINE, LINE + LINE), b'\xff'):
            with self.subTest(candidate=candidate):
                result = self.checked(v, BASE, candidate)
                self.assertEqual(result['exit_code'], 1)
                self.assertIn('CANDIDATE_PARSE', result['failures'])
                self.assertIsNone(result['error'])

    def test_baseline_parse_and_limit_are_execution_errors(self):
        v = driver()
        for baseline, candidate in ((b'[project', GOOD), (BASE, b'x' * (1024 * 1024 + 1))):
            with self.subTest(baseline=baseline):
                result = self.checked(v, baseline, candidate)
                self.assertEqual(result['exit_code'], 2)
                self.assertTrue(result['error']['type'])


if __name__ == '__main__':
    unittest.main()
