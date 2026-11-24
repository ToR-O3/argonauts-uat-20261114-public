"""Read-only verification for the approved single description insertion."""
import copy
import json
import tomllib
from pathlib import Path
import subprocess

BASE = 'c572613dc626160db2eb3bf4a41c95fc8283b828'
EXPECTED_DESCRIPTION = 'argonauts-uat public (UAT)'
EXPECTED_LINE = b'description = "argonauts-uat public (UAT)"\n'
PROCESS_PREFIXES = ('.planning/', 'openspec/', '_bmad-output/',
                    '.compound-engineering/', 'docs/solutions/')


def verify_repository(root, base):
    """Return explicit conditions and provenance; no writes or index repair."""
    root = Path(root)
    result = {'exit': 0, 'base': base, 'root': str(root), 'checks': {}}
    checks = result['checks']

    def check(name, passed):
        checks[name] = bool(passed)
        if not passed:
            result['exit'] = max(result['exit'], 1)
        return passed

    def git(*args):
        return subprocess.run(['git', *args], cwd=root, check=True,
                              capture_output=True).stdout

    try:
        result['head'] = git('rev-parse', 'HEAD').decode('ascii').strip()
        baseline = git('show', base + ':pyproject.toml')
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        checks['git_available'] = False
        result.update(exit=2, error=str(exc))
        return result
    checks['git_available'] = True
    try:
        result['changes'] = {}
        for label, refs in [('head', [base, 'HEAD']),
                            ('index', ['--cached', base]),
                            ('worktree', [base])]:
            raw = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                      '--raw', '--no-abbrev', '-z', *refs, '--')
            tokens = raw.split(b'\0')
            if tokens[-1] != b'' or (len(tokens) - 1) % 2:
                raise ValueError('malformed Git raw NUL output')
            records = []
            allowed = True
            for i in range(0, len(tokens) - 1, 2):
                fields = tokens[i].decode('ascii').split()
                if len(fields) != 5 or not fields[0].startswith(':'):
                    raise ValueError('malformed Git raw metadata')
                old_mode, new_mode = fields[0][1:], fields[1]
                status = fields[4]
                path = tokens[i + 1].decode('utf-8')
                process = path.startswith(PROCESS_PREFIXES)
                valid = process or (path == 'pyproject.toml' and status == 'M'
                                    and old_mode == new_mode == '100644')
                records.append({'path': path, 'status': status, 'old_mode': old_mode,
                                'new_mode': new_mode, 'process': process, 'allowed': valid})
                allowed = allowed and valid
            result['changes'][label] = records
            check(label + '_scope', allowed)
        untracked = [p.decode('utf-8') for p in
                     git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if p]
        result['changes']['untracked'] = untracked
        check('untracked_scope', all(p.startswith(PROCESS_PREFIXES) for p in untracked))
        result['dirty'] = git('status', '--porcelain=v1', '-z',
                              '--untracked-files=all').decode('utf-8').split('\0')
        result['patch'] = git('diff', '--no-ext-diff', '--no-textconv', base,
                              '--', 'pyproject.toml').decode('utf-8', errors='backslashreplace')
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError) as exc:
        checks['git_state_readable'] = False
        result.update(exit=2, error=str(exc))
        return result
    checks['git_state_readable'] = True
    # Reject a removed/renamed/type-changed target before treating it as I/O failure.
    if any(record['path'] == 'pyproject.toml' and not record['allowed']
           for records in (result['changes'][key] for key in ('head', 'index', 'worktree'))
           for record in records):
        return result
    try:
        current = (root / 'pyproject.toml').read_bytes()
    except OSError as exc:
        checks['worktree_io'] = False
        result.update(exit=2, error=str(exc))
        return result
    checks['worktree_io'] = True
    parsed = {}
    for label, raw in [('baseline', baseline), ('worktree', current)]:
        try:
            text = raw.decode('utf-8')
        except UnicodeError as exc:
            checks[label + '_utf8'] = False
            result.update(exit=2, error=str(exc))
            return result
        checks[label + '_utf8'] = True
        try:
            parsed[label] = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            check(label + '_toml', False)
            result['error'] = str(exc)
            return result
        checks[label + '_toml'] = True
    before, after = parsed['baseline'], parsed['worktree']
    original_project = before.get('project', {})
    project = after.get('project', {})
    if not check('baseline_description_absent', isinstance(original_project, dict)
                 and 'description' not in original_project):
        return result
    present = isinstance(project, dict) and 'description' in project
    if not check('description_missing', present):
        # Missing is a dedicated semantic failure, not an environmental RED.
        return result
    value = project['description']
    result['description'] = value
    check('description_type', isinstance(value, str))
    check('description_value', value == EXPECTED_DESCRIPTION)
    without = copy.deepcopy(after)
    del without['project']['description']
    check('other_data_unchanged', without == before)
    lines = current.splitlines(keepends=True)
    count = lines.count(EXPECTED_LINE)
    check('single_expected_line', count == 1)
    if count == 1:
        lines.remove(EXPECTED_LINE)
    check('existing_bytes_unchanged', count == 1 and b''.join(lines) == baseline)
    return result


def main():
    result = verify_repository(Path(__file__).resolve().parents[3], BASE)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return result['exit']


if __name__ == '__main__':
    raise SystemExit(main())
