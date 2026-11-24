"""Read-only verifier self-tests; all mutation fixtures live under TMPDIR."""
import importlib.util
from pathlib import Path
import unittest
import os
import json
import subprocess
import tempfile
from unittest import mock
import contextlib
import io

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

    def test_non_table_project_is_requirement_failure(self):
        result = self.checked(driver(), BASE, b'project = 42\n')
        self.assertEqual(result['exit_code'], 1)
        self.assertIn('VALUE_EXACT', result['failures'])

    def test_crlf_baseline_preserves_crlf_inserted_line(self):
        result = driver().verify_content(BASE.replace(b'\n', b'\r\n'), GOOD.replace(b'\n', b'\r\n'))
        self.assertEqual(result['exit_code'], 0)

    def test_baseline_parse_and_limit_are_execution_errors(self):
        v = driver()
        for baseline, candidate in ((b'[project', GOOD), (BASE, b'x' * (1024 * 1024 + 1))):
            with self.subTest(baseline=baseline):
                result = self.checked(v, baseline, candidate)
                self.assertEqual(result['exit_code'], 2)
                self.assertTrue(result['error']['type'])


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.v = driver()
        self.temp = tempfile.TemporaryDirectory(dir=os.environ['TMPDIR'])
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        self.git('remote', 'add', 'origin', 'https://github.com/ToR-O3/argonauts-uat-20261114-public.git')
        (self.root / 'pyproject.toml').write_bytes(BASE)
        (self.root / 'other.txt').write_bytes(b'unchanged\n')
        (self.root / '.gitignore').write_text('ignored.txt\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture baseline')
        self.base = self.git('rev-parse', 'HEAD').strip().decode()
        (self.root / 'pyproject.toml').write_bytes(GOOD)
        self.git('add', 'pyproject.toml')
        self.git('commit', '-qm', 'fixture product')
        self.product = self.git('rev-parse', 'HEAD').strip().decode()
        self.git('update-ref', 'refs/remotes/origin/argonauts/r-774f3cd6', self.base)
        self.paths = {'schema_version': 1, 'entries': []}

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True, timeout=30).stdout

    def collect(self):
        self.assertTrue(callable(getattr(self.v, 'collect_repository', None)), 'REPOSITORY_IMPLEMENTATION_MISSING')
        before = (self.root / 'pyproject.toml').read_bytes(), self.git('status', '--porcelain=v1', '-z', '--ignored')
        result = self.v.collect_repository(self.root, self.base, self.product, self.paths)
        after = (self.root / 'pyproject.toml').read_bytes(), self.git('status', '--porcelain=v1', '-z', '--ignored')
        self.assertEqual(before, after, 'verifier mutated fixture')
        return result

    def control(self):
        result = self.collect()
        self.assertEqual(result['exit_code'], 0, result)
        return result

    def test_repository_fixed_blob_tracer(self):
        result = self.control()
        self.assertEqual(result['hashes']['actual_input_sha256'], self.v.sha(GOOD))
        self.assertEqual(result['product_commit'], self.product)
        self.assertTrue(result['git_state']['tree']['entries'])

    def test_all_git_scopes_reject_unknown_paths(self):
        self.control()
        (self.root / '.planning').mkdir()
        (self.root / '.planning/unknown.py').write_text('unknown code\n')
        self.assertIn('UNTRACKED_SCOPE', self.collect()['failures'])
        self.git('add', '.planning/unknown.py')
        self.assertIn('INDEX_SCOPE', self.collect()['failures'])
        self.git('commit', '-qm', 'unknown')
        self.assertIn('INDEX_SCOPE', self.collect()['failures'])

    def test_other_product_worktree_change(self):
        self.control()
        (self.root / 'other.txt').write_text('changed\n')
        self.assertIn('WORKTREE_SCOPE', self.collect()['failures'])

    def test_other_product_index_worktree_cancellation(self):
        self.control()
        (self.root / 'other.txt').write_text('changed\n')
        self.git('add', 'other.txt')
        (self.root / 'other.txt').write_text('unchanged\n')
        result = self.collect()
        self.assertIn('INDEX_SCOPE', result['failures'])
        self.assertIn('WORKTREE_SCOPE', result['failures'])

    def test_tree_change_add_delete_rename_mode(self):
        self.control()
        mutations = ['modify', 'add', 'delete', 'rename', 'mode', 'symlink', 'submodule']
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.git('reset', '--hard', self.product)
                p = self.root / 'other.txt'
                if mutation == 'modify':
                    p.write_text('changed')
                elif mutation == 'add':
                    (self.root / 'new.txt').write_text('new')
                elif mutation == 'delete':
                    p.unlink()
                elif mutation == 'rename':
                    p.rename(self.root / 'renamed.txt')
                elif mutation == 'mode':
                    p.chmod(0o755)
                elif mutation == 'symlink':
                    p.unlink()
                    p.symlink_to('pyproject.toml')
                elif mutation == 'submodule':
                    self.git('update-index', '--add', '--cacheinfo', f'160000,{self.base},module')
                if mutation != 'submodule':
                    self.git('add', '-A')
                self.git('commit', '-qm', mutation)
                target = self.git('rev-parse', 'HEAD').strip().decode()
                result = self.v.collect_repository(self.root, self.base, target, self.paths)
                self.assertEqual(result['exit_code'], 1)
                self.assertIn('TREE_SCOPE', result['failures'])

    def test_unmerged_index_is_rejected(self):
        self.control()
        oid = self.git('rev-parse', f'{self.base}:other.txt').strip().decode()
        self.git('update-index', '--force-remove', 'other.txt')
        stages = ''.join(f'100644 {oid} {stage}\tother.txt\n' for stage in (1, 2, 3)).encode()
        subprocess.run(['git', 'update-index', '--index-info'], input=stages, cwd=self.root, check=True, capture_output=True)
        result = self.collect()
        self.assertEqual(result['exit_code'], 1)
        self.assertIn('INDEX_SCOPE', result['failures'])

    def test_ignored_inventory(self):
        self.control()
        (self.root / 'ignored.txt').write_text('cache')
        self.assertIn('IGNORED_INVENTORY', self.collect()['failures'])

    def test_registry_exact_path_positive_and_invalid_entries(self):
        self.control()
        p = self.root / '.planning/evidence.md'
        p.parent.mkdir()
        p.write_text('process evidence')
        entry = dict(path='.planning/evidence.md', purpose='fixture CLI evidence', allowed_changes=['A', 'M'], scopes=['tree', 'index', 'worktree', 'untracked'])
        self.paths['entries'] = [entry]
        self.control()
        self.git('add', '.planning/evidence.md')
        self.control()
        for path in ('../escape', '/absolute', '.planning/*', '.planning/', 'pyproject.toml', 'other.txt'):
            with self.subTest(path=path):
                self.paths['entries'] = [dict(entry, path=path)]
                self.assertIn('PROCESS_PATHS_VALID', self.collect()['failures'])
        for entries in ([dict(entry, purpose='')], [entry, entry], [dict(entry, scopes=['bogus'])], [dict(entry, allowed_changes=['*'])]):
            self.paths['entries'] = entries
            self.assertIn('PROCESS_PATHS_VALID', self.collect()['failures'])
        self.paths['entries'] = [entry]
        p.unlink()
        p.symlink_to(self.root / 'pyproject.toml')
        self.assertIn('PROCESS_PATHS_VALID', self.collect()['failures'])

    def test_working_product_hash_and_mode(self):
        self.control()
        (self.root / 'pyproject.toml').write_bytes(BASE)
        self.assertIn('BLOB_INPUT_SHA256', self.collect()['failures'])
        (self.root / 'pyproject.toml').write_bytes(GOOD)
        (self.root / 'pyproject.toml').chmod(0o755)
        self.assertIn('MODE_UNCHANGED', self.collect()['failures'])

    def test_git_failure_timeout_and_head_drift(self):
        self.control()
        for fault in (subprocess.CalledProcessError(1, ['git'], stderr=b'fixture failure'), subprocess.TimeoutExpired(['git'], 30)):
            with mock.patch.object(self.v.subprocess, 'run', side_effect=fault):
                result = self.v.collect_repository(self.root, self.base, self.product, self.paths)
                self.assertEqual(result['exit_code'], 2)
                self.assertTrue(result['error']['type'])
        real_git = self.v.git
        calls = 0
        def changing_head(root, *args):
            nonlocal calls
            if args == ('rev-parse', 'HEAD'):
                calls += 1
                if calls > 1:
                    return b'0' * 40 + b'\n'
            return real_git(root, *args)
        with mock.patch.object(self.v, 'git', side_effect=changing_head):
            self.assertIn('HEAD_STABLE', self.collect()['failures'])

    def test_cli_preflight_expect_red_and_fixed_repository(self):
        self.control()
        p = self.root / '.planning'
        p.mkdir()
        inputs = dict(self.v.FIXED_INPUTS, baseline_commit=self.base, approved_spec_commit=self.base,
                      approval_checked_by='fixture source review', approval_checked_at='2026-11-24T14:13:25Z', start_head=self.base)
        self.paths['entries'] = [dict(path=f'.planning/{name}.json', purpose=f'isolated {name} input', allowed_changes=['A', 'M'], scopes=['untracked', 'tree', 'index', 'worktree']) for name in ('inputs', 'paths', 'target')]
        (p / 'inputs.json').write_text(json.dumps(inputs))
        (p / 'paths.json').write_text(json.dumps(self.paths))
        hashes = self.collect()['hashes']
        target: dict = dict(schema_version=1, request_id='r-774f3cd6', baseline_commit=self.base,
            approved_spec_commit=self.base, product_commit=self.product, path='pyproject.toml',
            product_blob_oid=self.git('rev-parse', f'{self.product}:pyproject.toml').strip().decode(),
            baseline_blob_sha256=hashes['baseline_blob_sha256'], product_blob_sha256=hashes['candidate_blob_sha256'],
            actual_input_sha256=hashes['actual_input_sha256'], verifier_sha256=hashes['verifier_sha256'], selftest_sha256=hashes['selftest_sha256'],
            process_paths_sha256=self.v.sha((p / 'paths.json').read_bytes()), builder_head_start=self.product,
            builder_head_end=self.product, recorded_by='fixture', recorded_at='2026-11-24T14:13:25Z')
        def run(mode, extra):
            output, stderr = io.StringIO(), io.StringIO()
            with contextlib.chdir(self.root), contextlib.redirect_stdout(output), contextlib.redirect_stderr(stderr), mock.patch.dict(os.environ, {'HERMES_KANBAN_WORKSPACE': str(self.root)}), mock.patch.object(self.v, 'BASELINE', self.base), mock.patch.object(self.v, 'FIXED_INPUTS', dict(self.v.FIXED_INPUTS, baseline_commit=self.base, approved_spec_commit=self.base)):
                rc = self.v.main([mode, '--baseline', self.base, *extra])
            data = json.loads(output.getvalue())
            self.assertEqual(rc, data['exit_code'])
            self.assertEqual(stderr.getvalue(), '')
            return data
        args = ['--candidate', 'pyproject.toml', '--inputs', '.planning/inputs.json', '--process-paths', '.planning/paths.json']
        self.git('reset', '--hard', self.base)
        self.assertEqual(run('preflight', args)['exit_code'], 0)
        red = run('expect-red', args)
        self.assertEqual(red['exit_code'], 0)
        self.assertEqual(red['inner_exit'], 1)
        self.assertEqual(red['inner_result']['failures'], ['VALUE_EXACT'])
        wrong = dict(inputs, expected_value='WRONG')
        (p / 'inputs.json').write_text(json.dumps(wrong))
        self.assertIn('APPROVAL_BINDING', run('preflight', args)['failures'])
        self.assertNotEqual(run('expect-red', args)['exit_code'], 0)
        (p / 'inputs.json').write_text(json.dumps(inputs))
        self.git('reset', '--hard', self.product)
        (p / 'target.json').write_text(json.dumps(target))
        repo_args = ['--target-record', '.planning/target.json', '--process-paths', '.planning/paths.json', '--actor', 'quality']
        self.assertEqual(run('repository', repo_args)['exit_code'], 0)
        for key, condition_id in [('product_blob_sha256', 'BLOB_INPUT_SHA256'), ('actual_input_sha256', 'BLOB_INPUT_SHA256'), ('verifier_sha256', 'TOOL_HASHES'), ('selftest_sha256', 'TOOL_HASHES'), ('process_paths_sha256', 'TOOL_HASHES'), ('product_blob_oid', 'PRODUCT_COMMIT_FIXED')]:
            with self.subTest(key=key):
                (p / 'target.json').write_text(json.dumps(dict(target, **{key: '0' * len(target[key])})))
                self.assertIn(condition_id, run('repository', repo_args)['failures'])
        self.assertIn('CURRENT_DESCRIPTION_ABSENT', run('preflight', args)['failures'])
        self.assertEqual(run('content', ['--candidate', 'pyproject.toml'])['exit_code'], 0)
        self.assertEqual(run('content', ['--candidate', '../pyproject.toml'])['exit_code'], 2)
        outside_args = ['--candidate', 'pyproject.toml', '--inputs', str(p / 'inputs.json'), '--process-paths', '.planning/paths.json']
        self.assertEqual(run('preflight', outside_args)['exit_code'], 2)

    def test_cli_returns_json_exit2_for_bad_arguments_and_environment(self):
        self.assertTrue(callable(getattr(self.v, 'main', None)), 'CLI_IMPLEMENTATION_MISSING')
        for argv in ([], ['no-mode'], ['content', '--baseline', 'HEAD', '--candidate', 'pyproject.toml']):
            output = io.StringIO()
            with contextlib.redirect_stdout(output), mock.patch.dict(os.environ, {'HERMES_KANBAN_WORKSPACE': str(self.root)}):
                rc = self.v.main(argv)
            data = json.loads(output.getvalue())
            self.assertEqual(rc, 2)
            self.assertEqual(data['exit_code'], rc)
            self.assertTrue(data['error'])


if __name__ == '__main__':
    unittest.main()
