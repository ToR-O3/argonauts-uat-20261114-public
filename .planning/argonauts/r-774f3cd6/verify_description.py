"""Read-only package-description acceptance verifier (stdlib only)."""
import copy
import hashlib
import tomllib
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

BASELINE = 'b34cba0d008923e7f5267ce52d5403492ea53925'
REPO = 'ToR-O3/argonauts-uat-20261114-public'
BRANCH = 'argonauts/r-774f3cd6'
HERE = Path(__file__).resolve().parent
FIXED_INPUTS = dict(schema_version=1, request_id='r-774f3cd6', repo=REPO,
    request_branch=BRANCH, path='pyproject.toml', baseline_commit=BASELINE,
    approved_spec_commit='56b70bdca4349c6d2f9eaeb62be2e340a3e04b49',
    approval_task='t_b8e9c36c', approval_run=37, decision_task='t_78c8849e',
    decision_at='2026-11-24T13:00:38.567271+00:00',
    decision_quote='②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。',
    source_string='argonauts-uat public', expected_value='argonauts-uat public (UAT)',
    observed_description_present=False)
CONTENT_IDS = ('BASELINE_FETCH', 'BASELINE_PARSE', 'BASELINE_DESCRIPTION_ABSENT', 'CANDIDATE_READ', 'CANDIDATE_PARSE', 'VALUE_EXACT', 'STRUCTURE_UNCHANGED', 'BYTES_UNCHANGED')
SCOPE_IDS = ('PROCESS_PATHS_VALID', 'TREE_SCOPE', 'INDEX_SCOPE', 'WORKTREE_SCOPE', 'UNTRACKED_SCOPE', 'IGNORED_INVENTORY')


EXPECTED = 'argonauts-uat public (UAT)'
LIMIT = 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def condition(result, ident, passed, detail):
    result['conditions'].append(dict(id=ident, status='PASS' if passed else 'FAIL', detail=detail))
    if not passed:
        result['failures'].append(ident)
        result['exit_code'] = 1


def verify_content(baseline: bytes, candidate: bytes) -> dict:
    result = dict(conditions=[], failures=[], exit_code=0, error=None)
    if max(len(baseline), len(candidate)) > LIMIT:
        return dict(result, exit_code=2, error=dict(type='InputLimit', detail='input exceeds 1MiB'))
    condition(result, 'BASELINE_FETCH', True, 'baseline bytes supplied')
    try:
        before = tomllib.loads(baseline.decode('utf-8'))
    except (ValueError, UnicodeError) as error:
        return dict(result, exit_code=2, error=dict(type=type(error).__name__, detail=str(error)))
    condition(result, 'BASELINE_PARSE', True, 'whole TOML parsed')
    condition(result, 'BASELINE_DESCRIPTION_ABSENT', 'description' not in before.get('project', {}), 'baseline is not a source description')
    condition(result, 'CANDIDATE_READ', True, 'candidate bytes supplied')
    try:
        after = tomllib.loads(candidate.decode('utf-8'))
    except (ValueError, UnicodeError) as error:
        condition(result, 'CANDIDATE_PARSE', False, str(error))
        for ident in ('VALUE_EXACT', 'STRUCTURE_UNCHANGED', 'BYTES_UNCHANGED'):
            result['conditions'].append(dict(id=ident, status='SKIP', detail='candidate parse failed'))
        return result
    condition(result, 'CANDIDATE_PARSE', True, 'whole TOML parsed')
    lines = candidate.splitlines(keepends=True)
    baseline_lines = baseline.splitlines(keepends=True)
    section = None
    allowed = []
    for i, line in enumerate(baseline_lines):
        if line.startswith(b'['):
            section = line.rstrip(b'\r\n')
        if section == b'[project]' and line.startswith(b'version = '):
            newline = b'\r\n' if line.endswith(b'\r\n') else b'\n'
            inserted = b'description = "' + EXPECTED.encode() + b'"' + newline
            if i + 1 < len(lines) and lines[i + 1] == inserted:
                allowed.append(i + 1)
    project = after.get('project', {})
    condition(result, 'VALUE_EXACT', isinstance(project, dict) and isinstance(project.get('description'), str) and project.get('description') == EXPECTED and len(allowed) == 1, 'fixed string plus one exact line immediately after project.version')
    reduced = copy.deepcopy(after)
    if isinstance(reduced.get('project'), dict):
        reduced['project'].pop('description', None)
    condition(result, 'STRUCTURE_UNCHANGED', reduced == before, 'only project.description removed from deep copy')
    raw = b''.join(line for i, line in enumerate(lines) if i not in allowed)
    condition(result, 'BYTES_UNCHANGED', raw == baseline, 'only allowed line removed; no whitespace normalization')
    return result


def empty_result(mode=None) -> dict:
    return dict(schema_version=1, mode=mode, argv=[], cwd=None, actor='builder',
        baseline_commit=None, product_commit=None, head_start=None, head_end=None,
        hashes=dict.fromkeys(('baseline_blob_sha256', 'candidate_blob_sha256', 'actual_input_sha256', 'verifier_sha256', 'selftest_sha256', 'process_paths_sha256')),
        conditions=[], failures=[], exit_code=0, error=None, git_state={})


def execution_error(result, error):
    result['exit_code'] = 2
    result['error'] = dict(type=type(error).__name__, detail=str(error))
    return result


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True,
                          timeout=30, shell=False).stdout


def read_bytes(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'not a regular non-symlink input: {path}')
    with path.open('rb') as handle:
        data = handle.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError(f'input exceeds 1MiB: {path}')
    return data


def blob(root, commit, path='pyproject.toml'):
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('full commit ID required')
    data = git(root, 'show', f'{commit}:{path}')
    if len(data) > LIMIT:
        raise ValueError('blob exceeds 1MiB')
    return data


def valid_registry(root, registry):
    if not isinstance(registry, dict) or registry.get('schema_version') != 1 or not isinstance(registry.get('entries'), list):
        return None
    entries = {}
    for entry in registry['entries']:
        if not isinstance(entry, dict):
            return None
        path = entry.get('path')
        if not isinstance(path, str) or not path or path in entries:
            return None
        parts = PurePosixPath(path).parts
        if path != PurePosixPath(path).as_posix() or path.endswith('/') or any(c in path for c in '*?[]\\\x00') or '..' in parts or path.startswith('/'):
            return None
        # A namespace constraint is not a scope exemption: every path needs an entry.
        if not path.startswith(('.planning/', 'openspec/', '_bmad-output/')):
            return None
        full = root / path
        if any(parent.is_symlink() for parent in (full, *full.parents)):
            return None
        if full.exists() and not full.is_file():
            return None
        if not isinstance(entry.get('purpose'), str) or not entry['purpose'].strip():
            return None
        changes, scopes = entry.get('allowed_changes'), entry.get('scopes')
        if not isinstance(changes, list) or not changes or not set(changes) <= set('AMD'):
            return None
        if not isinstance(scopes, list) or not scopes or not set(scopes) <= {'tree', 'index', 'worktree', 'untracked', 'ignored'}:
            return None
        entries[path] = entry
    return entries


def raw_diff(root, *args):
    raw = git(root, 'diff', '--no-ext-diff', '--no-textconv', '--raw', '--no-abbrev', '--no-renames', '-z', *args, '--')
    tokens = raw.split(b'\x00')
    entries = []
    i = 0
    while i < len(tokens) and tokens[i]:
        header = tokens[i].decode('ascii').split()
        if len(header) != 5 or not header[0].startswith(':') or i + 1 >= len(tokens):
            raise ValueError('invalid raw Git diff')
        path = os.fsdecode(tokens[i + 1])
        old_mode, new_mode, old_blob, new_blob, status_code = header
        entries.append(dict(path=path, status=status_code, old_mode=old_mode[1:], new_mode=new_mode, old_blob=old_blob, new_blob=new_blob))
        i += 2
    patch = git(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames', *args, '--').decode('utf-8', 'backslashreplace')
    return dict(entries=entries, patch=patch)


def inventory(root, path, status_code):
    full = root / path
    mode = full.lstat().st_mode
    data = os.fsencode(os.readlink(full)) if stat.S_ISLNK(mode) else (full.read_bytes() if full.is_file() else b'')
    return dict(path=path, status=status_code, mode=oct(mode), blob=sha(data), regular=stat.S_ISREG(mode))


def collect_repository(root, baseline_commit, product_commit, process_paths) -> dict:
    result = empty_result('repository')
    root = Path(root).resolve()
    result.update(cwd=str(root), baseline_commit=baseline_commit, product_commit=product_commit)
    try:
        result['head_start'] = git(root, 'rev-parse', 'HEAD').strip().decode()
        baseline = blob(root, baseline_commit)
        candidate = blob(root, product_commit)
        content = verify_content(baseline, candidate)
        result.update({k: content[k] for k in ('conditions', 'failures', 'exit_code', 'error')})
        if result['exit_code'] == 2:
            return result
        result['hashes'].update(baseline_blob_sha256=sha(baseline), candidate_blob_sha256=sha(candidate), actual_input_sha256=sha(candidate),
            verifier_sha256=sha(read_bytes(Path(__file__))), selftest_sha256=sha(read_bytes(HERE / 'test_verify_description.py')))
        registry = valid_registry(root, process_paths)
        condition(result, 'PROCESS_PATHS_VALID', registry is not None, 'exact paths, declared purposes/scopes/statuses, regular files only')
        registry = registry or {}
        states = dict(tree=raw_diff(root, baseline_commit, product_commit),
            index=raw_diff(root, '--cached', product_commit), worktree=raw_diff(root))
        states['product_to_worktree'] = dict(patch=git(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames', product_commit, '--').decode('utf-8', 'backslashreplace'))
        status_bytes = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=none')
        tokens = status_bytes.split(b'\x00')
        statuses, untracked, i = [], [], 0
        while i < len(tokens) and tokens[i]:
            token = tokens[i]
            code, path = token[:2].decode('ascii'), os.fsdecode(token[3:])
            item = dict(status=code, path=path)
            if 'R' in code or 'C' in code:
                i += 1
                item['original_path'] = os.fsdecode(tokens[i])
            statuses.append(item)
            if code == '??':
                untracked.append(inventory(root, path, 'A'))
            i += 1
        ignored = [inventory(root, os.fsdecode(path), 'A') for path in git(root, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').split(b'\x00') if path]
        states.update(status=statuses, untracked=dict(entries=untracked), ignored=dict(entries=ignored))
        result['git_state'] = states
        def permitted(item, scope):
            path, code = item['path'], item['status']
            if path == 'pyproject.toml':
                return scope == 'tree' and code == 'M' and item['old_mode'] == item['new_mode'] == '100644' and content['failures'] == []
            entry = registry.get(path)
            normal = item.get('regular', True) and all(item.get(k, '100644') in ('000000', '100644') for k in ('old_mode', 'new_mode'))
            return bool(entry and normal and scope in entry['scopes'] and code in entry['allowed_changes'])
        for scope in ('tree', 'index', 'worktree', 'untracked', 'ignored'):
            rejected = [item for item in states[scope]['entries'] if not permitted(item, scope)]
            ident = 'IGNORED_INVENTORY' if scope == 'ignored' else scope.upper() + '_SCOPE'
            condition(result, ident, not rejected, dict(rejected=rejected, examined=len(states[scope]['entries'])))
        condition(result, 'PRODUCT_COMMIT_FIXED', git(root, 'rev-parse', f'{product_commit}^{{commit}}').strip().decode() == product_commit, 'full immutable product commit')
        working = read_bytes(root / 'pyproject.toml')
        condition(result, 'BLOB_INPUT_SHA256', working == candidate and sha(working) == result['hashes']['actual_input_sha256'], 'working bytes equal the exact blob bytes passed to verify_content')
        baseline_mode = git(root, 'ls-tree', baseline_commit, '--', 'pyproject.toml').split()[0]
        product_mode = git(root, 'ls-tree', product_commit, '--', 'pyproject.toml').split()[0]
        working_mode = (root / 'pyproject.toml').stat().st_mode
        condition(result, 'MODE_UNCHANGED', baseline_mode == product_mode == b'100644' and not working_mode & 0o111, 'regular non-executable product mode unchanged')
        patch = git(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames', baseline_commit, product_commit, '--', 'pyproject.toml').decode('utf-8')
        added = [line for line in patch.splitlines() if line.startswith('+') and not line.startswith('+++')]
        removed = [line for line in patch.splitlines() if line.startswith('-') and not line.startswith('---')]
        condition(result, 'PATCH_ONE_LINE', added == ['+description = "' + EXPECTED + '"'] and not removed, patch)
        condition(result, 'TOOL_HASHES', True, 'tool bytes hashed directly; repository CLI additionally binds target-record hashes')
        result['head_end'] = git(root, 'rev-parse', 'HEAD').strip().decode()
        condition(result, 'HEAD_STABLE', result['head_start'] == result['head_end'], 'HEAD observed before and after collection')
    except Exception as error:
        execution_error(result, error)
    return result


class JsonParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def selected_root():
    workspace = os.environ.get('HERMES_KANBAN_WORKSPACE')
    if not workspace:
        raise ValueError('HERMES_KANBAN_WORKSPACE required; no fallback')
    root = Path(workspace).resolve(strict=True)
    if Path.cwd().resolve() != root or Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip()).resolve() != root:
        raise ValueError('cwd, workspace and Git top-level must be identical')
    return root


def identity(root, result):
    remote = git(root, 'remote', 'get-url', 'origin').strip().decode()
    condition(result, 'REPO_IDENTITY', remote in (f'https://github.com/{REPO}.git', f'https://github.com/{REPO}', f'git@github.com:{REPO}.git'), remote)
    ref = git(root, 'rev-parse', '--verify', f'refs/remotes/origin/{BRANCH}^{{commit}}').strip().decode()
    condition(result, 'REQUEST_BRANCH', bool(re.fullmatch('[0-9a-f]{40}', ref)) and git(root, 'merge-base', ref, 'HEAD').strip().decode() == ref, dict(remote_ref=ref, local_branch=git(root, 'branch', '--show-current').strip().decode()))


def approval(root, inputs, result):
    checked = all(type(inputs.get(k)) is type(value) and inputs.get(k) == value for k, value in FIXED_INPUTS.items())
    checked = checked and all(isinstance(inputs.get(k), str) and inputs[k] for k in ('approval_checked_by', 'approval_checked_at', 'start_head'))
    if checked:
        checked = bool(re.fullmatch('[0-9a-f]{40}', inputs['start_head'])) and git(root, 'merge-base', inputs['start_head'], 'HEAD').strip().decode() == inputs['start_head']
        checked = checked and git(root, 'merge-base', inputs['approved_spec_commit'], 'HEAD').strip().decode() == inputs['approved_spec_commit']
    condition(result, 'APPROVAL_BINDING', checked, 'fixed attribution checked against JSON; human source review remains independently required')


def trim_conditions(result, excluded):
    result['conditions'] = [item for item in result['conditions'] if item['id'] not in excluded]
    result['failures'] = [ident for ident in result['failures'] if ident not in excluded]
    if result['exit_code'] != 2:
        result['exit_code'] = int(bool(result['failures']))


def check_target(root, target, result, paths_hash):
    required = ('schema_version', 'request_id', 'baseline_commit', 'approved_spec_commit', 'product_commit', 'path', 'product_blob_oid', 'baseline_blob_sha256', 'product_blob_sha256', 'actual_input_sha256', 'verifier_sha256', 'selftest_sha256', 'process_paths_sha256', 'builder_head_start', 'builder_head_end', 'recorded_by', 'recorded_at')
    valid = all(k in target for k in required)
    valid = valid and target['schema_version'] == 1 and target['request_id'] == 'r-774f3cd6' and target['baseline_commit'] == BASELINE and target['approved_spec_commit'] == FIXED_INPUTS['approved_spec_commit'] and target['path'] == 'pyproject.toml'
    valid = valid and all(isinstance(target[k], str) and target[k] for k in required if k != 'schema_version')
    if valid:
        valid = git(root, 'rev-parse', f"{target['product_commit']}:pyproject.toml").strip().decode() == target['product_blob_oid']
        valid = valid and git(root, 'merge-base', target['product_commit'], 'HEAD').strip().decode() == target['product_commit']
        valid = valid and all(re.fullmatch('[0-9a-f]{40}', target[k]) for k in ('builder_head_start', 'builder_head_end'))
    condition(result, 'PRODUCT_COMMIT_FIXED', bool(valid), 'all target provenance fields plus immutable blob/ancestor')
    hashes = result['hashes']
    condition(result, 'BLOB_INPUT_SHA256', target.get('baseline_blob_sha256') == hashes['baseline_blob_sha256'] and target.get('product_blob_sha256') == hashes['candidate_blob_sha256'] and target.get('actual_input_sha256') == hashes['actual_input_sha256'], 'record hashes independently compared with retrieved blob inputs')
    condition(result, 'TOOL_HASHES', target.get('verifier_sha256') == hashes['verifier_sha256'] and target.get('selftest_sha256') == hashes['selftest_sha256'] and target.get('process_paths_sha256') == paths_hash, 'record tool hashes compared with actual files')


def main(argv=None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    result = empty_result()
    result['argv'] = [sys.executable, '-B', str(Path(__file__)), *args_list]
    result['cwd'] = str(Path.cwd().resolve())
    try:
        parser = JsonParser(add_help=False)
        parser.add_argument('mode', choices=('content', 'preflight', 'expect-red', 'repository'))
        parser.add_argument('--baseline', required=True)
        parser.add_argument('--candidate')
        parser.add_argument('--inputs')
        parser.add_argument('--process-paths')
        parser.add_argument('--target-record')
        parser.add_argument('--actor', choices=('builder', 'quality'), default='builder')
        args = parser.parse_args(args_list)
        result.update(mode=args.mode, actor=args.actor, baseline_commit=args.baseline)
        if args.baseline != BASELINE:
            raise ValueError('baseline must be the approved immutable full commit')
        root = selected_root()
        for input_name in ('candidate', 'inputs', 'process_paths', 'target_record'):
            name = getattr(args, input_name)
            if name is not None:
                path = PurePosixPath(name)
                if path.is_absolute() or '..' in path.parts or name != path.as_posix() or '\\' in name:
                    raise ValueError('all input paths must be exact repository-relative paths')
                full = root / name
                if not full.resolve().is_relative_to(root) or any(p.is_symlink() for p in (full, *full.parents)):
                    raise ValueError('symlink or boundary escape input forbidden')
        result['head_start'] = git(root, 'rev-parse', 'HEAD').strip().decode()
        if args.mode == 'repository':
            if not args.target_record or not args.process_paths:
                raise ValueError('target-record and process-paths required')
            target = json.loads(read_bytes(root / args.target_record))
            product = target.get('product_commit')
            paths_bytes = read_bytes(root / args.process_paths)
            collected = collect_repository(root, BASELINE, product, json.loads(paths_bytes))
            result.update({k: v for k, v in collected.items() if k not in ('argv', 'mode', 'actor')})
            result['hashes']['process_paths_sha256'] = sha(paths_bytes)
            if result['exit_code'] != 2:
                identity(root, result)
                check_target(root, target, result, sha(paths_bytes))
            trim_conditions(result, {'BASELINE_DESCRIPTION_ABSENT'})
        else:
            if args.candidate != 'pyproject.toml':
                raise ValueError('candidate must be repository-relative pyproject.toml')
            baseline = blob(root, BASELINE)
            candidate = read_bytes(root / args.candidate)
            measured = verify_content(baseline, candidate)
            result.update({k: measured[k] for k in ('conditions', 'failures', 'exit_code', 'error')})
            result['hashes'].update(baseline_blob_sha256=sha(baseline), candidate_blob_sha256=sha(candidate), actual_input_sha256=sha(candidate), verifier_sha256=sha(read_bytes(Path(__file__))), selftest_sha256=sha(read_bytes(HERE / 'test_verify_description.py')))
            identity(root, result)
            if args.mode in ('preflight', 'expect-red') and result['exit_code'] != 2:
                if not args.inputs or not args.process_paths:
                    raise ValueError('inputs and process-paths required')
                inputs = json.loads(read_bytes(root / args.inputs))
                paths_bytes = read_bytes(root / args.process_paths)
                snapshot = collect_repository(root, BASELINE, result['head_start'], json.loads(paths_bytes))
                if snapshot['exit_code'] == 2:
                    raise RuntimeError(snapshot['error'])
                result['git_state'] = snapshot['git_state']
                result['hashes']['process_paths_sha256'] = sha(paths_bytes)
                for item in snapshot['conditions']:
                    if item['id'] in SCOPE_IDS:
                        condition(result, item['id'], item['status'] == 'PASS', item['detail'])
                approval(root, inputs, result)
                parsed = tomllib.loads(candidate.decode('utf-8')) if not any(c['id'] == 'CANDIDATE_PARSE' and c['status'] == 'FAIL' for c in result['conditions']) else {}
                condition(result, 'CURRENT_DESCRIPTION_ABSENT', 'description' not in parsed.get('project', {}), 'actual working file, not designated source string')
                condition(result, 'CURRENT_BYTES_BASELINE', candidate == baseline, 'working file raw bytes equal fixed baseline')
                if args.mode == 'preflight':
                    trim_conditions(result, {'VALUE_EXACT'})
                else:
                    inner = copy.deepcopy(result)
                    expected = inner['exit_code'] == 1 and inner['failures'] == ['VALUE_EXACT'] and all(c['status'] == 'PASS' for c in inner['conditions'] if c['id'] != 'VALUE_EXACT')
                    result.update(inner_result=inner, inner_exit=inner['exit_code'], outer_exit=0 if expected else (2 if inner['exit_code'] == 2 else 1), exit_code=0 if expected else (2 if inner['exit_code'] == 2 else 1))
        result['head_end'] = git(root, 'rev-parse', 'HEAD').strip().decode()
        condition(result, 'HEAD_STABLE', result['head_start'] == result['head_end'], 'HEAD observed before and after CLI')
    except Exception as error:
        execution_error(result, error)
    required = list(CONTENT_IDS)
    if result['mode'] in ('preflight', 'expect-red'):
        required += list(SCOPE_IDS) + ['APPROVAL_BINDING', 'REPO_IDENTITY', 'REQUEST_BRANCH', 'CURRENT_DESCRIPTION_ABSENT', 'CURRENT_BYTES_BASELINE', 'HEAD_STABLE']
    if result['mode'] == 'preflight':
        required.remove('VALUE_EXACT')
    if result['mode'] == 'repository':
        required.remove('BASELINE_DESCRIPTION_ABSENT')
        required += list(SCOPE_IDS) + ['PRODUCT_COMMIT_FIXED', 'PATCH_ONE_LINE', 'MODE_UNCHANGED', 'BLOB_INPUT_SHA256', 'TOOL_HASHES', 'HEAD_STABLE', 'REPO_IDENTITY', 'REQUEST_BRANCH']
    for ident in required:
        if not any(c['id'] == ident for c in result['conditions']):
            result['conditions'].append(dict(id=ident, status='SKIP', detail='not evaluated due to earlier input/execution failure'))
    if result['mode'] == 'expect-red':
        result.setdefault('inner_result', None)
        result.setdefault('inner_exit', None)
        result['outer_exit'] = result['exit_code']
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
