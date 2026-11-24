"""Isolated, tracked Git controls; never mutate the real product checkout."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from unittest.mock import patch

import verify_description as v

ORIGINAL = b'[project]\nname = "fixture"\nversion = "0.1.0"\ndependencies = []\n'
LINE = b'description = "argonauts-uat public (UAT)"\n'
GOOD = ORIGINAL.replace(b'dependencies', LINE + b'dependencies')


class DescriptionVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TMPDIR'])
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Isolated test fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'core.filemode', 'true')
        (self.root / 'pyproject.toml').write_bytes(ORIGINAL)
        (self.root / 'product.txt').write_bytes(b'original\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture baseline')
        self.base = self.git('rev-parse', 'HEAD').decode().strip()
        (self.root / 'pyproject.toml').write_bytes(GOOD)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True).stdout

    def test_positive_control_and_read_only(self):
        before = self.git('status', '--porcelain=v1', '-z')
        result = v.verify_repository(self.root, self.base)
        self.assertEqual(result['exit'], 0, result)
        self.assertEqual(before, self.git('status', '--porcelain=v1', '-z'))

    def reject(self, name, exit_code=1):
        result = v.verify_repository(self.root, self.base)
        self.assertEqual(result['exit'], exit_code, result)
        self.assertIs(result['checks'].get(name), False, result)
        if name != 'description_missing':
            self.assertNotEqual(result['checks'].get('description_missing'), False, result)

    def test_description_and_toml_mutations(self):
        mutations = [
            (ORIGINAL, 'description_missing'),
            (GOOD.replace(b'public (UAT)', b'public (UAT) (UAT)'), 'description_value'),
            (GOOD.replace(b'argonauts-uat', b' argonauts-uat'), 'description_value'),
            (GOOD.replace(b'(UAT)"', b'(UAT) "'), 'description_value'),
            (GOOD.replace(LINE, b'description = 42\n'), 'description_type'),
            (ORIGINAL + b'\n[other]\n' + LINE, 'description_missing'),
            (GOOD + LINE, 'worktree_toml'),
            (GOOD + b'broken = [\n', 'worktree_toml'),
            (GOOD.replace(b'fixture', b'changed'), 'other_data_unchanged'),
            (GOOD.replace(b'version =', b'version  ='), 'existing_bytes_unchanged'),
            (GOOD.replace(b'\n', b'\r\n'), 'existing_bytes_unchanged'),
            (GOOD + b'\n', 'existing_bytes_unchanged'),
        ]
        for raw, condition in mutations:
            with self.subTest(condition=condition, raw=raw):
                (self.root / 'pyproject.toml').write_bytes(GOOD)
                self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)
                (self.root / 'pyproject.toml').write_bytes(raw)
                self.reject(condition)

    def test_git_product_mutations(self):
        for state in ('unstaged', 'staged', 'committed', 'committed_then_restored',
                      'deleted', 'renamed', 'mode', 'untracked', 'prefix_spoof'):
            with self.subTest(state=state):
                self.git('reset', '--hard', self.base)
                self.git('clean', '-fd')
                (self.root / 'pyproject.toml').write_bytes(GOOD)
                self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)
                product = self.root / 'product.txt'
                if state in ('unstaged', 'staged', 'committed', 'committed_then_restored'):
                    product.write_bytes(b'changed\n')
                    if state != 'unstaged':
                        self.git('add', 'product.txt')
                    if state.startswith('committed'):
                        self.git('commit', '-qm', 'fixture mutation')
                    if state == 'committed_then_restored':
                        product.write_bytes(b'original\n')
                elif state == 'deleted':
                    product.unlink()
                elif state == 'renamed':
                    self.git('mv', 'product.txt', '.planning-renamed')
                elif state == 'mode':
                    product.chmod(0o755)
                else:
                    path = '.planning-fake.txt' if state == 'prefix_spoof' else 'new\nproduct.txt'
                    (self.root / path).write_bytes(b'new\n')
                condition = ('untracked_scope' if state in ('untracked', 'prefix_spoof')
                             else 'head_scope' if state.startswith('committed')
                             else 'index_scope' if state in ('staged', 'renamed')
                             else 'worktree_scope')
                self.reject(condition)

    def test_pyproject_deletion_rename_mode(self):
        for state in ('deleted', 'renamed', 'mode'):
            with self.subTest(state=state):
                self.git('reset', '--hard', self.base)
                self.git('clean', '-fd')
                path = self.root / 'pyproject.toml'
                path.write_bytes(GOOD)
                self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)
                if state == 'deleted':
                    path.unlink()
                elif state == 'renamed':
                    self.git('mv', 'pyproject.toml', '.planning-renamed.toml')
                else:
                    path.chmod(0o755)
                self.reject('index_scope' if state == 'renamed' else 'worktree_scope')

    def test_process_directories_allowed(self):
        for prefix in v.PROCESS_PREFIXES:
            path = self.root / prefix / 'record.txt'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'process\n')
        self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)
        self.git('add', '.')
        self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)
        self.git('commit', '-qm', 'fixture process and description')
        self.assertEqual(v.verify_repository(self.root, self.base)['exit'], 0)

    def test_environment_and_parse_failures_are_not_missing(self):
        saved = self.base
        self.base = '0' * 40
        self.reject('git_available', 2)
        self.base = saved
        (self.root / 'pyproject.toml').write_bytes(b'\xff')
        self.reject('worktree_utf8', 2)
        (self.root / 'pyproject.toml').write_bytes(GOOD)
        with patch.object(Path, 'read_bytes', side_effect=OSError('fixture I/O failure')):
            self.reject('worktree_io', 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
