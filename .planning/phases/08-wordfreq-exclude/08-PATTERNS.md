# Phase 8: wordfreq exclude - Pattern Map

**Mapped:** 2026-11-29 (JST)
**Files analyzed:** 7 prospective file assignments (3 required existing-file edits, 2 optional helper/test files, 2 evidence assignments)
**Analogs found:** 5 / 7 assignments; partial and role matches are not existing exclusion implementations.
**Status:** Read-only source mapping complete; no implementation or tests executed.

## Scope and Authority

Read the official `gsd-pattern-mapper` agent and full `08-CONTEXT.md` / `08-RESEARCH.md` before analysis. Official launcher + `gsd_run query init.phase-op 8` resolves phase `08`, name `wordfreq exclude`, and this phase directory. Configuration extraction with jq confirms `agent_skills: {}` and `workflow.pattern_mapper: true`. Root `HERMES.md`, `.hermes/HERMES.md`, `.hermes/skills/`, and `.agents/skills/` are absent.

Directly read the approved original architecture (`_bmad-output/initiative-r-e0a2598f/architecture/architecture.md`, especially AD-1..4 at lines 38–60), PRD, and OpenSpec design/tasks. This map supplements, never replaces, the canonical references in CONTEXT: planner/checker must still read those originals. No product-policy discretion is introduced.

Extraction from CONTEXT D-01..09 and RESEARCH Architecture Patterns / Wave 0 yields CLI composition, pure exclusion-line interpretation, tests, README, exact-baseline compatibility, and independent evidence. Helper/test filenames and baseline storage below are **candidate layout choices**, not approved mandatory module names. No optional file is a prerequisite to a plan unless that plan authors it.

## File Classification

Paths are repository-relative. `phase_dir` means `.planning/phases/08-wordfreq-exclude`.

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `wordfreq/__main__.py` — modify | controller | argv request-response + ordered file-I/O + transform | `wordfreq/__main__.py` | exact: existing additive min-count composition seam |
| `wordfreq/exclusions.py` — optional new pure helper; name discretionary | utility | eager batch/transform, no file-I/O | `wordfreq/tokenizer.py` | role-match: Unicode interpretation/normalization, but extraction is not validation |
| `tests/test_exclusions.py` — optional if helper is split out | test | batch/transform assertions | `tests/test_cli.py` | role-match: pytest parametrization and Unicode fixtures; no existing pure exclusion parser test |
| `tests/test_cli.py` — modify | test | subprocess request-response + file-I/O + boundary spies | `tests/test_cli.py` | exact: same integration boundary and output contracts |
| `README.md` — modify | documentation (utility-facing contract) | human request-response / executable examples | `README.md` | exact: existing option, errors, selection and HTML documentation |
| `.planning/argonauts/r-e0a2598f/baseline/index.json` — optional new captured-baseline manifest; path discretionary | config/evidence | file-I/O, immutable captured bytes + provenance | None assigned | no code analog: existing consumer pattern is available, but provenance/schema must be grounded separately |
| `phase_dir/08-VERIFICATION.md` — future independent quality artifact, plus CLI text evidence at quality-selected paths | test/evidence | exact-head verification results → readable report | None assigned | no source analog assigned; follow official verification workflow, not copied historical verdicts |

The seven assignments are not seven mandatory product edits. If live baseline comparison is authored inside `tests/test_cli.py`, no saved manifest is needed. If line interpretation stays in an existing pure module, the two optional helper/test paths can collapse into that layout without changing approved contracts.

### Existing named surfaces to preserve, not automatically edit

These resolve other named files in RESEARCH; they are dependencies/regression surfaces, not unrequested refactor tasks.

| Existing File | Role | Data Flow | Phase 8 disposition |
|---|---|---|---|
| `wordfreq/sources.py` | provider | file-I/O | Reuse `FileSource` unchanged for both input roles; CLI chooses exits. |
| `wordfreq/tokenizer.py` | utility | transform | Keep body findall/casefold behavior and public contract unchanged. Optional helper placement must not alter body extraction. |
| `wordfreq/aggregator.py` | utility | batch/transform | Preserve Counter and stable frequency-only ranking signatures. |
| `wordfreq/formatters.py` | component | transform | Preserve pairs, HTML total/basename/escaping/UTF-8/CSS/empty form. |
| `tests/test_sources.py` | test | file-I/O | Retain source exceptions/nonmutation tests; extend only if new source assertions are actually needed. |
| `tests/test_sources_boundary.py` | test | file-I/O boundary | Retain pure-component/no-I/O regressions. |
| `tests/test_tokenizer.py` | test | transform | Retain existing normalization/extraction contract tests. |
| `tests/test_aggregator.py` | test | batch/transform | Retain first-seen ties and nonmutation regressions. |
| `tests/test_formatters.py` | test | transform | Retain static safety, escaping, metadata and CSS regressions. |
| `pyproject.toml` | config | dependency/build configuration | No edit: lines 9–12 already declare no runtime dependencies and existing pytest dev extra. |

CONTEXT/RESEARCH, canonical requirement documents, historical phase debt, CI and input files are not feature-edit targets. Do not pre-check OpenSpec tasks 2.1/2.2/3.1/3.2.

## Pattern Assignments

### `wordfreq/__main__.py` (controller, request-response + file-I/O)

**Analog:** same tracked file; closest additive feature is existing min-count orchestration.

**Imports** (`wordfreq/__main__.py:2–10`):

```python
import argparse
from collections import Counter
import os
import sys

from .aggregator import count_words, top_words
from .formatters import format_html, format_json, format_text
from .sources import FileSource, InputError
from .tokenizer import iter_tokens
```

Use stdlib and relative component imports; add no dependency. No auth middleware/guard exists or is needed for this local CLI.

**Validation and role-sensitive failure seam** (`wordfreq/__main__.py:23–33`):

```python
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    if args.min_count < 1:
        parser.error("--min-count must be >= 1")
    try:
        text = FileSource(args.filename).read_text()
    except InputError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
```

Add optional `--exclude FILE` and purpose/line-format help in `build_parser` (lines 13–19). After both existing numeric checks, acquire exclusions and **finish all original-row validation** before entering the body-read scope. Exclusion failures need a distinct CLI handler: FILE + reason, and original 1-based row for invalid lines, stderr/exit2, empty stdout/no HTML/Traceback. Do not broaden the existing body handler into a shared exit policy: body errors stay exit1. Invalid argv/numerics must read neither role. A valid exclusion row followed by an invalid fourth original row must still cause zero body reads.

**Shared selection** (`wordfreq/__main__.py:34–38`):

```python
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count})
    pairs = top_words(selected_counts, args.top)
```

Extend only candidate membership: exclude first, threshold next, existing stable rank/top next. Iterate `counts.items()`, not the exclusion set. Preserve `counts` and its insertion order; `total` is original full counts, including all-excluded nonempty input. The single `pairs` already feeds HTML/JSON/text at lines 39–48. Preserve basename conversion and HTML `sys.stdout.buffer.write(output.encode("utf-8"))` at lines 39–53.

### Optional `wordfreq/exclusions.py` (utility, eager transform)

**Closest analog:** `wordfreq/tokenizer.py` (same pure Unicode interpretation responsibility, not identical grammar). Its existing core is:

```python
# wordfreq/tokenizer.py:6
_WORD_RE = re.compile(r"\w+", re.UNICODE)

# wordfreq/tokenizer.py:9–11
def default_tokenizer(text: str) -> list[str]:
    """Extract maximal Unicode word-character sequences."""
    return _WORD_RE.findall(text)

# wordfreq/tokenizer.py:14–18
def iter_tokens(
    text: str, tokenizer: Callable[[str], list[str]] = default_tokenizer
) -> Iterator[str]:
    """Yield normalized tokens in their input order."""
    return (token.casefold() for token in tokenizer(text))
```

**Copy:** pure input-text → interpreted data structure boundary; stdlib regex and `casefold` identity.

**Do not copy:** permissive `findall` or laziness. Exclusions must trim each original row, skip empty/#-started rows, **fullmatch original trimmed Unicode `\w+` before casefold**, then eagerly materialize all valid normalized membership values. Return data or a pure validation exception carrying original row information; no open/argv/print/exit in the helper. CLI adds path/exit policy. The helper's exact exception/type/name is discretionary, not a new public API mandate.

Digits/underscore/non-ASCII words are valid. Multiword rows, punctuation/hyphen, standalone combining mark, inline # note and leading BOM must not be repaired into acceptance. U+0130 distinguishes pre-fold validation from invalid post-fold revalidation. Do not use `utf-8-sig`, lower, token splitting, BOM stripping or inline-comment stripping. Preserve LF/CRLF/no-final-newline without silently accepting additional intra-line separators via permissive splitting; new policy questions go to PM.

### Optional `tests/test_exclusions.py` (test, transform)

**Analog:** pytest parametrization and Unicode fixtures in tracked `tests/test_cli.py`; role-match only, not an existing parser suite. Imports follow `tests/test_cli.py:1–11` (stdlib, blank line, pytest); pure parser tests need only the relevant imports.

**Parametrized fixture structure** (`tests/test_cli.py:686–695`):

```python
@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("content,minimum,expected,total", [
    ("beta beta beta alpha gamma alpha delta", 1,
     [("beta", 3), ("alpha", 2), ("gamma", 1), ("delta", 1)], 7),
    ("beta beta beta alpha gamma alpha delta", 2, [("beta", 3), ("alpha", 2)], 7),
    ("beta beta beta alpha gamma alpha delta", 3, [("beta", 3)], 7),
    ("Zoo apple APPLE zoo banana", 2, [("zoo", 2), ("apple", 2)], 5),
    ("Straße STRASSE", 2, [("strasse", 2)], 2),
    ("日本語 日本語 Café CAFÉ banana", 2, [("日本語", 2), ("café", 2)], 5),
])
```

Reuse table-driven cases, not unrelated threshold assertions. Cover every approved valid/invalid row boundary, trim/comment/newline cases, original line4 after skipped rows, casefold expansion, duplicates/order invariance, and eager rejection after an earlier valid word. Keep file-I/O tests in CLI/source surfaces. If no separate parser module is introduced, keep these assertions in the existing test organization instead.

### `tests/test_cli.py` (test, real subprocess + boundary spies)

**Analog:** same tracked file. Preserve existing helpers and all existing tests.

**Binary runner** (`tests/test_cli.py:418–422`):

```python
def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
```

Reuse `assert_output_bytes` (lines 425–441) for exact text, JSON semantics/newline and HTML rows/basename/total. `CLIHTML` (lines 201–239) extracts semantic HTML without changing appearance. Add all-format exclusion matrices with explicit expected remaining words, top/min-count, empty/no-op/all-excluded distinctions and positive original total when rows vanish.

**Pre-I/O spy** (`tests/test_cli.py:629–641`):

```python
    calls = []

    def spy(source):
        calls.append(source)
        raise AssertionError("invalid threshold must not read input")

    monkeypatch.setattr(FileSource, "read_text", spy)
    with pytest.raises(SystemExit) as caught:
        main([str(tmp_path / "missing"), "--format", output_format, *options])
    assert caught.value.code == 2
    assert calls == []
    output = capsys.readouterr()
    assert output.out == "" and "--min-count" in output.err
```

Adapt to distinguish both source roles and assert the exact read trace: numeric errors none; exclusion failure only exclusion; success exclusion then body. Include both-role failures and invalid-after-valid original line4. Exit2 alone is not proof of body-unread behavior.

**Counter/pairs nonmutation spy** (`tests/test_cli.py:771–783`):

```python
    def top_spy(counts, n):
        assert counts is not original_counts
        assert list(counts.items()) == [("zoo", 2), ("apple", 2)]
        pairs = real_top(counts, n)
        selected.append(pairs)
        return pairs

    def formatter_spy(pairs, *metadata):
        assert pairs is selected[0]
        assert pairs == [("zoo", 2)]
        assert metadata == (("input.txt", 5) if output_format == "html" else ())
        calls.append(True)
        return real_formatter(pairs, *metadata)
```

Adapt expected candidates for exclusion and assert original items unchanged as existing lines 792–793 do. Real subprocess successful HTML is preferable for binary-output checks. Both input roles need before/after bytes on successful and failed execution.

**Historical baseline consumer, not Phase8 provenance** (`tests/test_cli.py:814–817`):

```python
    for minimum in [[], ["--min-count", "1"]]:
        result = run_cli_bytes(path, *options, *minimum, env=env)
        assert (result.returncode, result.stderr) == (0, b"")
        assert result.stdout == expected
```

Lines 796–813 obtain expected bytes and recorded environment from the older min-count baseline. Retain that regression. Add a separate compatibility fixture/capture sourced from **exactly `79d83ba14dd59d289d2ecd3e33c85e8de437972e`**, not that older baseline or candidate-self output. Run baseline and candidate with identical argv/input paths/environment/interpreter, isolate old source from candidate cwd/PYTHONPATH, compare raw stdout bytes, and fail rather than skip if required provenance is unavailable. Fixtures must include reverse-lexical ties, Unicode, >10 unique words, empty input and existing top/min-count variants. No baseline execution or byte equality is asserted by this map.

### `README.md` (documentation, executable contract)

**Analog:** same tracked file. Existing executable CLI block (`README.md:15–17`):

```sh
python -m wordfreq input.txt --min-count 3
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
```

Existing option prose (`README.md:28`):

> `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。

Follow this compact usage + explicit semantics style, backed by the actual README-example test pattern at `tests/test_cli.py:672–682`. Add reproducible body/exclusion contents and a command whose known result the test executes. Explain UTF-8, trim/comments, LF/CRLF/no final newline, whole-line valid/invalid examples, validation-before-casefold, failure path/reason/original line/exit2, argv→complete exclusions→body, all formats, unchanged counts and original HTML total, and unset compatibility.

Update existing selection/total/error prose consistently (README lines 32–35 and 41): do not leave statements implying all file failures exit1 or HTML total is only before min-count/top. Keep existing usage examples, static HTML/escaping/privacy claims and pure API description intact.

## Shared Patterns

### Read-only acquisition with cause preservation

**Source:** tracked `wordfreq/sources.py:17–22`; applies to CLI acquisition of both roles. This is a shared boundary dependency, not a new component to rewrite.

```python
    def read_text(self) -> str:
        try:
            with open(self._path, "r", encoding="utf-8") as source:
                return source.read()
        except (OSError, UnicodeDecodeError) as error:
            raise InputError(f"{self._path}: {error}") from error
```

The provider already handles missing, directory, decode, permissions and other OSError failures with path/reason/cause. Preserve role at the caller. Never add exit2 inside FileSource, and never move file reads into aggregator/formatters.

**Deterministic permission test** (`tests/test_sources.py:67–80`):

```python
    original = PermissionError(13, "Permission denied", "private.txt")
    calls = []

    def denied(*args, **kwargs):
        calls.append((args, kwargs))
        raise original

    monkeypatch.setattr("builtins.open", denied)
    with pytest.raises(InputError) as caught:
        FileSource("private.txt").read_text()
    assert caught.value.__cause__ is original
    assert "private.txt" in str(caught.value)
    assert "Permission denied" in str(caught.value)
    assert calls == [(("private.txt", "r"), {"encoding": "utf-8"})]
```

Reuse this open-boundary injection for exclusion PermissionError and generic OSError; combine with role-aware CLI status/read-order assertions. Existing real CLI permission tests at `tests/test_cli.py:503–527,647–669` explicitly prove effective denial; chmod alone is not deterministic under root. No permission bypass is part of the feature.

### Stable ranking and unchanged pure public APIs

**Source:** tracked `wordfreq/aggregator.py:11–17`, especially:

```python
    return sorted(counts.items(), key=lambda wc: -wc[1])[:n]
```

Frequency-only stable sort preserves input Counter insertion order. Do not add a lexical tie key or iterate a set to rebuild candidates. `count_words(tokens)`, `top_words(counts, n)` and formatter signatures remain unchanged. No I/O/argv/exit ownership moves to these pure components.

### Formatting and original metadata stay outside exclusion interpretation

**Source:** tracked `wordfreq/formatters.py:11–19,22–37`; applies to all output assertions, not a formatter rewrite.

```python
# wordfreq/formatters.py:11–14
def format_json(pairs: list[tuple[str, int]]) -> str:
    """Format ordered word/count objects as one ASCII-safe JSON line."""
    items = [{"word": word, "count": count} for word, count in pairs]
    return json.dumps(items, ensure_ascii=True) + "\n"

# wordfreq/formatters.py:17–19
def _html_text(value: str) -> str:
    """Escape once, protecting CR from HTML's input newline normalization."""
    return escape(value, quote=True).replace("\r", "&#13;")
```

HTML already receives `(pairs, basename, total)` and chooses the existing empty message for no pairs. Keep static document/CSS lines 39–127 unchanged. Never expose exclusion filename/content as new HTML metadata, and never recompute total from remaining rows.

### Test-first sequencing and evidence ownership

The map is not a test run. Plan a thin real exclusion tracer first, then complete grammar/error/selection coverage, then exact-baseline compatibility and independent quality evidence, retaining all requirements. At most three tasks per plan; sequential plans on the same request branch. Every verify selector must exercise tests authored by then, not a future file or zero selected cases. No new dependencies, network, CI, appearance changes, source expansion or full refactor.

Builder results do not fulfill independent quality task 3.2. Quality must independently execute at exact target head and save readable commands/exits/expected-vs-actual/AC mapping. If images are inspected, record count/content/result in text. Do not copy historical acceptance verdicts into Phase8.

## No Analog Found

| File | Role | Data Flow | Reason / planner guidance |
|---|---|---|---|
| Optional new Phase8 baseline manifest/captures | config/evidence | file-I/O | The existing CLI test gives a consumer pattern, not proof that any stored data came from the required Phase8 revision. No manifest source was assigned/read as an analog. Author a live historical fixture or a provenance-backed manifest/capture before execution; never invent bytes or reuse older baseline provenance. |
| Future `phase_dir/08-VERIFICATION.md` and quality CLI evidence | test/evidence | exact-head results → report | Historical verification reports are not implementation code or current acceptance evidence. No report analog assigned; follow official quality workflow and record actual independent results. |

There is also **no exact existing exclusion grammar implementation**: the pure helper's tokenizer match is explicitly role-only. It supplies Unicode syntax/casefold conventions, not whole-file-validation logic.

## Metadata

- **Analog search scope:** tracked `wordfreq/`, `tests/`, `README.md`; evidence filename discovery only under `.planning/`.
- **Strong assignment source files:** 4 unique files (`wordfreq/__main__.py`, `wordfreq/tokenizer.py`, `tests/test_cli.py`, `README.md`); search stopped after covering the five matched assignments.
- **Additional shared source originals read:** `wordfreq/sources.py`, `wordfreq/aggregator.py`, `wordfreq/formatters.py`, `tests/test_sources.py`, `pyproject.toml`.
- **Files scanned:** 9 unique product/test/config originals read in full; governing documents listed above are additional context, not included in that source count.
- **Tracked-source gate:** `git ls-files --` printed every named code/test/config/documentation analog and shared source path. No ignored runtime/install mirror is used as an analog.
- **Pattern extraction date:** 2026-11-29, observed with `date +%F`.
- **Verification performed:** official phase resolution, configuration extraction, source reads and tracked-path checks only. No feature invocation, pytest, baseline capture, dependency installation or uncreated verification command was run.
- **Write scope:** only this `08-PATTERNS.md`. Existing `.planning/state.json` modification and orchestration/research untracked artifacts were present before mapping and left untouched. No product edits, commit, push or Kanban action.
