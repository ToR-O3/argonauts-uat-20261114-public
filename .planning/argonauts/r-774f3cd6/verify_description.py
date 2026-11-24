"""Read-only package-description acceptance verifier (stdlib only)."""
import copy
import hashlib
import tomllib

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
    condition(result, 'VALUE_EXACT', isinstance(project.get('description'), str) and project.get('description') == EXPECTED and len(allowed) == 1, 'fixed string plus one exact line immediately after project.version')
    reduced = copy.deepcopy(after)
    reduced.get('project', {}).pop('description', None)
    condition(result, 'STRUCTURE_UNCHANGED', reduced == before, 'only project.description removed from deep copy')
    raw = b''.join(line for i, line in enumerate(lines) if i not in allowed)
    condition(result, 'BYTES_UNCHANGED', raw == baseline, 'only allowed line removed; no whitespace normalization')
    return result
