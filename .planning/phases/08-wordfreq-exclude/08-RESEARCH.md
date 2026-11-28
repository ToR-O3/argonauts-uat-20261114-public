# Phase 8: wordfreq exclude - Research

**Researched:** 2026-11-29 (JST)
**Domain:** existing Python stdlib CLI / exclusion acquisition, Unicode validation, shared selection, pytest regression design
**Confidence:** LOW (official confidence seam classifies the available `local`/`webfetch` providers LOW, even with `--verified`; this is not an unresolved product-policy decision). Findings below distinguish directly read originals from recommendations and unexecuted checks.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
<!-- DATA_c739a05e_START: verbatim 08-CONTEXT.md:14-24 -->
- D-01 / FR-1 / REQ-28: Optional --exclude FILE removes every specified normalized word's occurrences from ranking only; remaining counts/order and original HTML total unchanged. Unset behavior unchanged.
- D-02 / FR-2 / REQ-29: UTF-8; LF/CRLF/no final newline. Strip both ends, ignore empty/whitespace and # after strip. Validate complete Unicode `\w+` before casefold; accept digits/underscore/non-ASCII valid words. Reject multiple words, punctuation, hyphen, standalone combining mark, inline # note, leading BOM; no token splitting/BOM stripping to accept invalid lines.
- D-03 / FR-3: Existing str.casefold, never lower. Straße/STRASSE both excluded by STRASSE; HELLO/hello by Hello. Validate before casefold (e.g. U+0130 expands afterward); body tokenizer remains unchanged. Exclusion order/duplicates do not alter output.
- D-04 / FR-4 / REQ-30: All exclusion read failures (missing/permissions/directory/invalid UTF-8 and other I/O errors) produce FILE+reason stderr/exit2, empty stdout, no HTML/Traceback. Invalid line reports original 1-based line number including skipped rows. Do not freeze exact whole diagnostic.
- D-05 / FR-4 / AD-3: Existing argparse syntax/top/min-count validation first, exclusion acquisition AND full-line validation second, body acquisition only after success. Invalid-after-valid row must still fail before ANY body read. Both input roles failing yields exclusion diagnosis/exit2. Invalid numeric args read neither file. Valid/absent exclusions preserve existing body error exit1.
- D-06 / FR-5 / AD-4: Shared pairs across text/json/html: exclusion→min-count→frequency descending/stable normalized first-seen ties→top. Excluded words consume no top slots. Original full Counter remains intact; HTML total before all filters, including all-excluded positive total. Empty body total0; text empty/json[] newline/html existing zero-row form. Empty/comment-only/no-match files preserve results.
- D-07 / FR-6 / REQ-31: --help explains purpose/line format and exits0. README executable usage plus UTF-8, trim/comments/newlines, fullmatch invalid examples, casefold, all failures/line diagnostics/exit2, exclusion-first, original HTML total and unset compatibility.
- D-08 / FR-7 / REQ-32: Compare unset stdout BYTES with fixed baseline79d83ba14dd59d289d2ecd3e33c85e8de437972e using identical inputs/argv/environment, not candidate-self expectations. Fixtures include ties in reverse lexical order, Unicode, >10 unique words, empty body. Additional pytest covers every FR-2 invalid/valid boundary, all FR-4 read failures/order, all formats/min-count/top/empty/all-excluded, old body errors, README example and input+exclusion byte immutability; retain full existing suite. Quality independently runs at exact target head and writes VERIFICATION.md/CLI text evidence, commands/exits/expected-vs-actual/AC mapping. If images inspected, text records count/content/result; PM need not inspect images/archives.
- D-09 / RULE-1..4 / REQ-33: Preserve extraction/casefold/Counter first-seen/defaults, source acquisition boundary, pure count_words/top_words/formatters public contracts, existing text/json/static HTML escaping/basename/CSS/appearance. No new dependency/external network/CI/input rewrite/new source/full refactor. CLI alone owns exit codes; pure components have no file I/O.
- D-10 / all FR acceptance examples: Zoo apple APPLE zoo banana minus apple => 2 zoo/1 banana; minus zoo with min-count2/top1 => apple2 and HTML total5. All filtered => original total5, no data rows. Trimmed CRLF blank/comment/apple without final newline excludes only apple, not banana. Fourth original invalid row after blank/comment/valid => line4 and zero body reads. Unset outputs equal baseline across all formats.
- D-11 / governance: Decision2026-11-28T14:45:42.849521+00:00, user「提案のまま進めてください（1〜5 すべて提案どおり）。」 PM t_9da1db1e excludes architecture only from direct synthesis; planner/checker MUST read original architecture. New product uncertainty goes to PM, not guessed.
<!-- DATA_c739a05e_END -->

### Claude's Discretion
<!-- DATA_9bf715d2_START: verbatim 08-CONTEXT.md:27 -->
Helper names/module layout/set type and test organization within existing boundaries. No product-policy discretion. Thin feature tracer first, TDD before code. Plans max3 tasks, run sequentially on same request branch with predecessors' artifacts available. Independent tasks must also be verifiable without future plans; their real misbehavior must fail the listed command.
<!-- DATA_9bf715d2_END -->

### Deferred Ideas (OUT OF SCOPE)
<!-- DATA_f0c94a17_START: verbatim 08-CONTEXT.md:51 -->
Automatic stopword lists, regex exclusion, stdin '-', multi-file policy, persistent config, morphology, source expansion, service, migration, dependency/CI/appearance changes.
<!-- DATA_f0c94a17_END -->
</user_constraints>

## Summary

Implement this as a small extension of the existing acquisition-and-selection pipeline, not a new tokenizer or formatter. The existing CLI already has a single insertion point after argument validation and before body acquisition, followed by one shared candidate Counter and one shared pairs list. Preserve these boundaries. Reuse the UTF-8 file source for both roles, but handle its exceptions in separate CLI scopes so exclusion failures cannot inherit the body's exit status. [VERIFIED: wordfreq/__main__.py:22-48, exact existing exits `sys.exit(1)` and `sys.exit(0)`; wordfreq/sources.py:17-22, exact exception tuple `(OSError, UnicodeDecodeError)`; architecture/architecture.md:38-60 in the approved initiative]

Plan test-first vertical work: acquire and fully validate exclusions, exercise a real CLI exclusion, then expand Unicode/error/selection coverage and fixed-baseline compatibility. A successful subprocess result does not prove body-unread ordering: supplement subprocess tests with spies at the real acquisition boundary. The existing suite contains reusable examples of both techniques. [VERIFIED: tests/test_cli.py:16-20,418-441,624-644,759-793; tests/test_sources.py:64-80]

**Primary recommendation:** materialize the complete validated casefolded exclusion set before the body read, then filter ordered full-count items into a new display Counter before the unchanged ranking/formatting calls. This is a recommendation within the approved helper/layout discretion, not a new public API. [VERIFIED: PRD:108-135; architecture:42,48,54,60]

**Research execution boundary:** no product implementation, pytest execution, CLI feature execution, baseline capture, commit, push, or Kanban operation was performed. `pytest --version` was an environment probe and failed; see Environment Availability. All future commands below are design inputs, not claimed results.

## Project Constraints (from HERMES.md)

Neither `HERMES.md` nor `.hermes/HERMES.md`, `.hermes/skills/`, or `.agents/skills/` exists in this worktree (explicit shell existence checks). There are no project-local skill directives to import. `.planning/config.json:63` declares `"agent_skills": {}`; no additional agent-skills lookup was requested. [VERIFIED: .planning/config.json:63-64; terminal existence-check output]

Task-specific constraints remain binding: read files/JSON with read_file, extract fields with jq where available, use the launcher plus official `gsd_run` for GSD decisions, no inline scripts/heredocs, no running uncreated verification files during planning. Only this research artifact is a repository deliverable. Do not change historical Phase 7 debt or state focus to make Phase 8 look complete. [VERIFIED: 08-CONTEXT.md:9,21,24,47; .planning/STATE.md:94-104; user task]

## Phase Requirements
<phase_requirements>

The following is a coverage map; complete normative descriptions remain in `.planning/REQUIREMENTS.md:108-113` and the approved PRD. [VERIFIED: those lines, IDs `REQ-28`, `REQ-29`, `REQ-30`, `REQ-31`, `REQ-32`, `REQ-33`]

| ID | Description | Research Support |
|---|---|---|
| REQ-28 | Optional exclusion in all formats; remaining counts/ties; exclusion before min-count/rank/top; original HTML total | Shared ordered candidate seam, full Counter preservation, selection matrix |
| REQ-29 | UTF-8 line grammar, trim/comments/newlines, full Unicode validation before casefold, invalid examples, order/duplicate invariance | Pure eager line interpreter, Unicode matrix and original-line diagnostics |
| REQ-30 | All exclusion failures exit2; FILE/reason/line; stdout empty/no traceback; args→complete exclusions→body; old body exit1 | Separate role-sensitive error scopes; boundary spies plus real subprocess failures |
| REQ-31 | Help purpose/format exit0 and executable README usage with all approved semantics | Existing help/example test pattern, docs completeness/execution test |
| REQ-32 | Full added coverage and retained suite; fixed-baseline byte comparisons; both files immutable; independent readable evidence | Existing byte runner and HTML parser, Wave 0 gaps, fixed baseline capture design, quality handoff |
| REQ-33 | Preserve tokenizer/acquisition/pure public contracts, defaults and static HTML safety/appearance; no dependency/network/CI/source expansion | Unchanged pure components and public signatures; existing unit/safety regressions plus diff review |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| Argument parsing and exit policy | Local CLI orchestration | — | Input role determines failure status, not the file source |
| Both UTF-8 file reads | Acquisition boundary | CLI sequences reads | Reuse existing read-only FileSource, retain cause |
| Trim/comment/full-line validation/casefold | Pure line interpretation | CLI reports validation failure | No file I/O, argv or exit decisions in interpreter |
| Full counts and display candidate selection | Pure counting + CLI composition | Existing stable ranking | Keep full counts immutable; candidate ordering follows counts |
| text/json/html rendering | Pure formatters | CLI writes output | Same pairs, original total and basename remain caller-owned |
| Verification/evidence | Existing pytest and quality workflow | Git fixed baseline | Not a new runtime service or dependency |

Mapping follows the approved pipes-and-filters design. [VERIFIED: architecture:21-34,38-90; wordfreq/{sources,tokenizer,aggregator,formatters}.py read in this session]

## Standard Stack

### Core
| Library/component | Version/contract | Purpose | Why standard here |
|---|---|---|---|
| Local Python package | `version = "0.1.0"`; `dependencies = []` | Existing module CLI | Keep runtime stdlib-only [VERIFIED: pyproject.toml:5-12] |
| argparse | Current runtime stdlib; no new version pin | Optional FILE argument and existing syntax errors | Existing parser [VERIFIED: wordfreq/__main__.py:2,13-28] |
| re and str | `_WORD_RE = re.compile(r"\w+", re.UNICODE)`; `token.casefold()` | Whole exclusion-line validation and same normalization | Existing definition, but use fullmatch for exclusions, not findall [VERIFIED: wordfreq/tokenizer.py:6-18] |
| collections.Counter | Existing stdlib | Preserve normalized first-seen ordering and separate selected counts | Existing count and selection seam [VERIFIED: wordfreq/aggregator.py:6-17; wordfreq/__main__.py:34-38] |
| FileSource / InputError | `open(self._path, "r", encoding="utf-8")`; `except (OSError, UnicodeDecodeError)` | Read-only acquisition of either input role | Existing boundary already preserves cause/path [VERIFIED: wordfreq/sources.py:13-22] |

### Supporting
| Tool | Version | Use |
|---|---|---|
| pytest | Existing dev dependency `dev = ["pytest"]`; installed version NOT established | Unit, integration and real subprocess tests [VERIFIED: pyproject.toml:11-12; environment probe failed] |
| subprocess + HTMLParser | stdlib | Binary stdout comparison and semantic HTML checks [VERIFIED: tests/test_cli.py:201-239,418-441] |
| Git | Baseline object verified as `commit` | Execute/extract exact old source in isolated scratch; never derive expected bytes from candidate [VERIFIED: terminal `git cat-file -t`; PRD:104] |

**Installation:** no runtime package, starter, package-version upgrade or CI change. Builder must provision the already-approved dev dependency only if its interpreter lacks it. Do not infer CI Python support from the research host's version. [VERIFIED: pyproject.toml:9-12; architecture:71-73; PRD:110-117]

### Alternatives Considered

Use membership in an exclusion set, but iterate original counts, not the set. Do not make exclusions a new top_words parameter or a formatter concern; doing so expands pure public contracts without need. A separate small pure helper module is within discretion; its name is not a product contract. [VERIFIED: architecture:42,48,60,95]

## Package Legitimacy Audit

Not applicable: this phase installs no new external package. pytest is already declared as development-only; no registry freshness claim or package installation was made. [VERIFIED: pyproject.toml:9-12; PRD:112]

## Architecture Patterns

### System Architecture Diagram

```text
argv
  └─ parse + existing numeric checks
       ├─ invalid → argparse stderr / exit2; neither file read
       └─ valid
            └─ optional exclusion acquisition
                 └─ full eager line validation → casefolded membership set
                      ├─ read/line failure → FILE + reason[/line], stderr / exit2
                      │                      body read count = 0; stdout empty
                      └─ valid or absent
                           └─ body acquisition
                                ├─ failure → old body stderr / exit1
                                └─ tokenizer → casefold → full Counter
                                      ├─ original sum ──────────────────┐
                                      └─ exclusion membership filter    │
                                           → min-count → stable rank   │
                                           → top → shared pairs        │
                                                ├─ text                │
                                                ├─ JSON                │
                                                └─ HTML ← basename + total
```

This diagram is control order as well as data flow. Do not parallelize or lazily interleave the two reads. [VERIFIED: architecture:50-60,88; PRD:84-96]

### Concrete existing call boundaries

| Existing owner | Read source and exact seam | Recommended plan action |
|---|---|---|
| Parser | `build_parser()` adds `"filename"`, `"--top"`, `"--min-count"`, `"--format"`; defaults `10`, `1`, `"text"` [VERIFIED: wordfreq/__main__.py:13-19] | Add optional exclusion filename/help without altering existing defaults, positive-number checks or choices |
| CLI pre-I/O | `args = parser.parse_args(argv)` then `if args.top < 1` / `if args.min_count < 1` [VERIFIED: wordfreq/__main__.py:23-28] | Insert exclusion acquisition/full validation immediately after these checks, before the existing body try |
| Acquisition | `text = FileSource(args.filename).read_text()` [VERIFIED: wordfreq/__main__.py:29-33] | Reuse the boundary for exclusion; keep distinct try/except scope for exclusion versus body status |
| Tokenization | `_WORD_RE.findall(text)` and `(token.casefold() for token in tokenizer(text))` [VERIFIED: wordfreq/tokenizer.py:6-18] | Leave body tokenizer untouched; do not call it to accept malformed exclusion rows |
| Selection | `total = sum(counts.values())`; `Counter({word: count for word, count in counts.items() if count >= args.min_count})` [VERIFIED: wordfreq/__main__.py:34-38] | Add exclusion membership condition before threshold in candidate construction; do not delete from counts or recompute total from candidates |
| Ranking | `return sorted(counts.items(), key=lambda wc: -wc[1])[:n]` [VERIFIED: wordfreq/aggregator.py:11-17] | Retain exactly the frequency-only stable sort contract and original insertion-order candidates |
| Output | `format_html(pairs, basename, total)`, `format_json(pairs)`, `format_text(pairs)`; UTF-8 buffer write only for HTML [VERIFIED: wordfreq/__main__.py:39-53] | Keep unchanged signatures, one shared pairs list, metadata and encoding behavior |

### Pure line interpretation pattern (recommended, not implemented)

1. Receive fully acquired decoded text; return a fully materialized membership set or a validation exception containing the original row number. Enumerate original rows before discarding comments/blanks.
2. Trim both ends; skip empty or `#`-started rows after trim; fullmatch the remaining original row against Unicode word syntax; only after success call casefold. This sequence is the locked grammar, not a proposal. [VERIFIED: PRD:72-82; architecture:48]
3. Finish all rows before any body acquisition. Do not yield words lazily to the body pipeline and do not stop after finding one matching exclusion. [VERIFIED: PRD:88-90; spec delta:66-79]
4. Choose ordinary line iteration on acquired text without treating arbitrary intra-line Unicode separators as accepted record separators. Python `splitlines()` recognizes more separators than universal newlines; do not accidentally turn an invalid multi-word row into multiple accepted words. This is an implementation caution, not a new policy for extra line terminators; escalate new policy questions rather than inventing an acceptance rule. [CITED: https://docs.python.org/3.14/builtins/stdtypes.html#str.splitlines]

### Anti-patterns to avoid

- A shared try that maps both FileSource failures to body exit1.
- Using `findall`, `search`, lower, ASCII-only character classes, utf-8-sig, BOM stripping, punctuation stripping, or inline-comment splitting to make invalid rows valid.
- Validating casefolded text instead of original trimmed text; the locked U+0130 case distinguishes this order.
- Reconstructing candidates by iterating exclusions/a set, sorting ties lexically, excluding after top, or mutating the full Counter.
- Adding I/O or exit decisions to pure public count_words/top_words/formatters.

These are failure directions of the approved rules, not extra features. [VERIFIED: 08-CONTEXT.md:14-22; architecture:38-60]

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Unicode word acceptance | Custom ASCII/Unicode category table | stdlib Unicode regex fullmatch on original trimmed line | Same syntax as existing word rule, full-line acceptance [CITED: https://docs.python.org/3.14/library/re.html#re.fullmatch; VERIFIED: wordfreq/tokenizer.py:6] |
| Caseless matching | lower/manual ß replacements | Existing `str.casefold()` | Existing normalization and official documented distinction [CITED: https://docs.python.org/3.14/builtins/stdtypes.html#str.casefold; VERIFIED: wordfreq/tokenizer.py:18] |
| File errors | Custom stat/access preflight/error-code table | Existing FileSource exception chaining; CLI owns role | Handle actual read failure, do not assume chmod implies denial [VERIFIED: wordfreq/sources.py:17-22; tests/test_sources.py:64-80] |
| Ranking/HTML | New sorter or exclusion-aware formatter | Existing top_words and formatters | Preserve pure signatures and exact appearance [VERIFIED: wordfreq/aggregator.py:11-17; wordfreq/formatters.py:6-127] |
| Baseline expectations | Candidate-derived golden bytes | Exact approved historical revision | Candidate-self comparison misses regressions [VERIFIED: PRD:104-106] |

## Common Pitfalls

| Pitfall | Why it fails | Planning safeguard / failing assertion |
|---|---|---|
| Tests only assert exit2 | Both an early read and a correct preflight can return exit2 | Boundary call trace asserts body never read and numeric errors read neither |
| Valid row followed by invalid row | Lazy parsing may start body acquisition too soon | Original blank/comment/valid/invalid fixture, line4 and zero body reads |
| Normalization order swapped | Valid original Unicode can expand under casefold | Unit case from D-03 (U+0130), plus CLI match; no post-fold fullmatch |
| Inline comments/BOM silently accepted | Reuses permissive tokenizer/utf-8-sig | Parametrize each approved invalid example independently with line/path diagnostics |
| Filter after top | Exclusion consumes a display slot | Exclude leading tied word with top1; next eligible word must be shown |
| Filter corrupts total | All-excluded output might falsely report total0 | Positive original total and empty rows; spy on full Counter preservation |
| New candidate order | Set iteration/lexical ties alters remaining ranking | Multiple remaining tied words in reverse lexical order; exclusion permutations/duplicates/hashseed |
| chmod-only permission probe | Privileged runtime may still read | Mock PermissionError at open plus role-aware CLI seam; actual subprocess denial only with a proved unprivileged setup |
| Text-mode baseline capture | Newline/encoding normalization can hide byte changes | Binary subprocess stdout, identical argv/inputs/env, byte assertion |
| Reusing old min-count baseline as Phase8 baseline | Old suite baseline has its own history and metadata | Keep old regression; add separate baseline sourced from exact approved revision |
| Green test from wrong interpreter | pytest entrypoint exists but import fails | Provision known test environment before RED/GREEN; record interpreter/version/exits |

Sources: [VERIFIED: PRD:72-106; tests/test_cli.py:503-527,624-644,759-817; tests/test_sources.py:64-80; .planning/argonauts/r-e0a2598f-learnings.md:16-50]. Older learning's lexical-tie example is superseded: current `top_words` is frequency-only stable sort, not a secondary word key. [VERIFIED: wordfreq/aggregator.py:17; openspec/specs/wordfreq-cli/spec.md:81-90]

## Code Examples

Existing code only; these snippets are not proposed product implementation and were not executed.

```python
# Existing UTF-8 acquisition and normalized failure: wordfreq/sources.py:17-22
with open(self._path, "r", encoding="utf-8") as source:
    return source.read()
# Existing surrounding handler:
# except (OSError, UnicodeDecodeError) as error:
#     raise InputError(f"{self._path}: {error}") from error
```

[VERIFIED: wordfreq/sources.py:17-22, values `"r"`, `"utf-8"`, `(OSError, UnicodeDecodeError)` quoted verbatim above.]

```python
# Existing binary subprocess helper: tests/test_cli.py:418-422
return subprocess.run(
    [sys.executable, "-m", "wordfreq", *map(str, args)],
    cwd=ROOT, env=env, capture_output=True, timeout=10,
)
```

[VERIFIED: tests/test_cli.py:418-422, exact `"-m"`, `"wordfreq"`, `timeout=10`.]

Existing boundary-spy pattern: monkeypatch `FileSource.read_text`, capture calls, call CLI `main` in `pytest.raises(SystemExit)`, then assert status and call list separately. HTML success in-process uses a real buffer-capable capture/stream; for empty-output failures capsys is already the existing pattern. Prefer binary real subprocess checks for successful HTML. [VERIFIED: tests/test_cli.py:624-644,759-793; wordfreq/__main__.py:49-53]

## State of the Art

This is an additive local CLI feature, not a framework adoption or migration. The relevant current state is already a full Counter → threshold candidates → stable ranking/top → shared formatters pipeline; Phase8 adds exclusion before candidate selection and a pre-body acquisition step. No runtime state migration is required by scope. [VERIFIED: wordfreq/__main__.py:22-54; architecture:90-97]

## Environment Availability

| Dependency | Available/observed | Planning consequence |
|---|---|---|
| python3 | `Python 3.14.9` from version probe | Host observation only; not a project support-version declaration |
| pytest entrypoint | Found `/home/Yuki/.local/bin/pytest`, but `pytest --version` prints `ModuleNotFoundError: No module named 'pytest'` | Not a working test environment; no test results obtained |
| Worktree-local venv | `.venv/bin/python` and `.venv/bin/pytest` not executable/present in explicit checks | Builder must provision existing dev test environment before test-first work |
| uv | Executable found `/home/Yuki/.local/bin/uv` | Candidate setup path for existing dev extra; not run to install during research |
| jq | `/usr/bin/jq` | Used for configuration-field extraction |
| Git fixed baseline | `git cat-file -t 79d83ba14dd59d289d2ecd3e33c85e8de437972e` → `commit` | Historical object available, not yet captured/executed |
| GSD | Official launcher `gsd_run query init.phase-op 8` resolves phase `"08"`, `"wordfreq exclude"`, correct phase directory; graphify reports disabled | No graph context used; do not enable/change config |
| Documentation tooling | ctx7 not found; research-plan proposed jina, which is not exposed here | Used permitted web search + version-specific official docs extraction; no packages installed |

[VERIFIED: terminal probes in this research session; .planning/config.json:21-25,49,63.]

No executable test setup was established. Recommended Builder setup, using the already declared extra, is `uv run --extra dev python -m pytest ...`; its resolution/install must be reported honestly if blocked. This is a proposed execution path, not a successful research result. The same runner/interpreter must be used for baseline/candidate comparison. No new dev dependency, lockfile or metadata change is authorized by this recommendation. [VERIFIED: pyproject.toml:11-12; user no-dependency-change constraint]

Historical `.planning/argonauts/t_20f1102b/pytest-cli.txt:1-17` records a different worktree/interpreter and `702 passed in 208.99s (0:03:28)`. That is historical evidence only, not today's suite count/duration or a guarantee of a sub-30-second full run. [VERIFIED: that file:1-17, exact values quoted.]

## Validation Architecture

Nyquist is enabled: `"nyquist_validation": true`; security enforcement also enabled: `"security_enforcement": true`. [VERIFIED: .planning/config.json:21-25,49]

### Test Framework
| Property | Value |
|---|---|
| Framework | pytest, existing dev declaration; runnable installed version currently unknown |
| Config file | No pytest-named configuration found; existing pyproject has no pytest section [VERIFIED: pyproject.toml:1-15; file discovery] |
| Quick run command, existing boundaries | `uv run --extra dev python -m pytest tests/test_sources.py tests/test_sources_boundary.py tests/test_tokenizer.py tests/test_aggregator.py tests/test_formatters.py -q -x` |
| Quick CLI regression command, existing file | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'normalized_tie_top or min_count_invalid_before_read or min_count_selection_preserves_counter'` |
| Phase quick command after tests are authored in existing file | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` — NOT adequate until actual exclusion tests exist/are collected; zero selected tests is not a pass |
| Full suite command | `uv run --extra dev python -m pytest -q` |
| Current run status | None executed; dev interpreter must first be made usable; quick timing is not measured |

All listed test-file paths above were opened in this research. Prefixing with uv is environment setup, not evidence that a command has already succeeded. A plan must tie each feature task to tests it authors before running the command; never count the existing green boundary tests as coverage of unimplemented exclusion semantics.

### Existing verification surfaces versus Wave 0

| Existing test original | Existing behavior observed in source | Exact selective command (after environment setup) |
|---|---|---|
| tests/test_sources.py:7-80 | UTF-8/read-only/missing/decode/directory/permission chaining | `uv run --extra dev python -m pytest tests/test_sources.py -q -x` |
| tests/test_sources_boundary.py:7-42 | Pure aggregation has no I/O; explicit source crossing | `uv run --extra dev python -m pytest tests/test_sources_boundary.py -q -x` |
| tests/test_tokenizer.py:6-60 | casefold, punctuation, digits/underscore/CJK, injectable tokenizer | `uv run --extra dev python -m pytest tests/test_tokenizer.py -q -x` |
| tests/test_aggregator.py:17-55 | stable first occurrence, top, nonmutation | `uv run --extra dev python -m pytest tests/test_aggregator.py -q -x` |
| tests/test_formatters.py:9-262 | pure output, escaping/static safety, empty rows, fixed CSS | `uv run --extra dev python -m pytest tests/test_formatters.py -q -x` |
| tests/test_cli.py:242-263 | cross-format normalized tie/top and original metadata | `uv run --extra dev python -m pytest tests/test_cli.py::test_normalized_tie_top_is_shared_by_all_formats -q -x` |
| tests/test_cli.py:624-644 | invalid min-count before boundary I/O | `uv run --extra dev python -m pytest tests/test_cli.py::test_min_count_invalid_before_read -q -x` |
| tests/test_cli.py:759-793 | full Counter preservation and exact shared pairs passed to formatter | `uv run --extra dev python -m pytest tests/test_cli.py::test_min_count_selection_preserves_counter_and_shared_pairs -q -x` |
| tests/test_cli.py:796-817 | historical min-count default-byte baseline | `uv run --extra dev python -m pytest tests/test_cli.py::test_min_count_saved_default_bytes -q -x` |

[VERIFIED: all cited test definitions read; these commands are researched selectors, not execution results.]

### Phase Requirements → Test Map

Use the existing `tests/test_cli.py` for proposed `test_exclude_*` additions, so commands refer to an existing verification file. A new pure parser test module is optional within discretion and must be authored before any plan selects it. The proposed groups below are Wave0 authoring work, NOT already-existing test functions.

| Req ID / original AC | Behavior to verify | Type | Automated command after tests authored | Exists now? |
|---|---|---|---|---|
| REQ-28 / AC1 | All occurrences excluded across text/json/html; remaining counts/order, no consumed top slot | real CLI + selection spy | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` | File yes; exclusion cases NO — Wave0 |
| REQ-29 / AC2–3 | UTF-8 grammar, all valid/invalid rows, casefold/order/duplicates | pure parser + real CLI | same existing-file exclusion command | Cases NO — Wave0 |
| REQ-30 / AC4 | all read errors, line diagnostics, role precedence, zero body reads, numeric-first, body exit1 | source exception unit + boundary integration + real CLI | same exclusion command, plus `uv run --extra dev python -m pytest tests/test_sources.py -q -x` | Existing source contracts yes; exclusion/role cases NO — Wave0 |
| REQ-31 / AC5 | help exit0 explains option/line format; README contains complete semantics and runnable example | CLI/docs regression | same existing-file exclusion command | Existing min-count docs pattern yes; exclusion cases NO — Wave0 |
| REQ-32 / AC6 | exact baseline byte comparisons, immutability, all matrices, independent evidence | binary subprocess + pytest integration + quality review | exclusion command then `uv run --extra dev python -m pytest -q` | Helpers yes; new baseline and exclusion assertions NO — Wave0 |
| REQ-33 / AC6 + RULE/AD | old pure API, tokenizer, I/O boundary, HTML/CSS/static/basename, defaults/errors; restricted diff | unit + regression + source/diff review | quick boundary suite then full suite above | Existing regressions yes; exclusion interaction assertions NO — Wave0 |

Original six AC meanings are read from Brief success criteria and the phase context's six-criterion mapping; FR-1..7 and EX-1..5 remain distinct identifiers, not replaced by this summary. [VERIFIED: brief:55-62; 08-CONTEXT.md:47; PRD:66-106; spec delta:5-113]

### Required test cases and failure directions (Wave 0 design checklist)

| Group | Required fixtures/assertions | Must fail if implementation does this |
|---|---|---|
| Basic tracer | Original `Zoo apple APPLE zoo banana`, exclude apple; exact text `2\tzoo\n1\tbanana\n`; JSON/HTML semantic rows agree; original total5 | Ignores exclusion, decrements remaining counts, or differs by format |
| Trim/comments/newlines | LF, CRLF and no-final-newline; leading/trailing whitespace, whitespace-only and indented # lines; original ` \r\n  #banana\r\n apple ` excludes only apple | Processes comment text, fails final line, fails trim, modifies input |
| Valid original words | `123`, `_word_` and `a_b`, non-ASCII valid word; match existing body-normalized values | ASCII-only validator, digits/underscore disallowed |
| Invalid original words | Each of `foo bar`, `foo,`, `foo-bar`, standalone combining mark, `foo # note`, leading BOM; assert FILE and original row, exit2/stdout empty/no Traceback for every format | Token-splits, strips punctuation/BOM, accepts inline comments or partial matches |
| Unicode identity/order | `Straße STRASSE hello` minus STRASSE; `HELLO hello` minus Hello; U+0130 original-row acceptance per D-03; non-ASCII match; duplicate and reordered exclusion rows | lower instead of casefold, validates after casefold, mutates body tokenizer, leaks set order |
| Exclusion read errors | Missing, directory, invalid UTF-8 actual files; deterministic PermissionError and another OSError at real open boundary; path/reason preserved; each format | Catches only missing, maps error to exit1/empty success, loses reason/cause or prints result/traceback |
| Late invalid row | Blank/comment/valid/invalid original rows; valid word exists in body; assert original line4 and exclusion-only call trace | Enumerates after skipping rows or lazily starts body after first valid exclusion |
| Precedence | Both roles missing; body decode-bad + exclusion invalid; exclusion valid + each old body error; absent exclusion + old body error | Reads body early or maps body failure to exit2 |
| Arguments | Invalid top/min-count (0/negative/noninteger/value-missing), invalid format/syntax and missing --exclude value; monkeypatch acquisition to fail on any read | Opens either file before parsing/number validation |
| Selection | Exclude zoo + min-count2/top1 → apple2, total5; retain ties in reverse lexical order; threshold below/equal/above; swap option order | Filters after top, sorts ties lexically, applies threshold incorrectly, derives total from selected rows |
| Empty/no-op distinctions | Empty body and punctuation-only body; empty exclusion; comments-only; unmatched word; all words excluded; exclusion plus threshold removes everything | Collapses a read error to no-op, loses empty forms, changes no-op bytes, produces zero total for nonempty all-excluded body |
| Mutation/public boundary | Capture both input files' bytes before/after valid and failing CLI; source/Counter/pairs spies; retain pure component tests | Writes either input, mutates original counts/order, moves I/O into pure code |
| Docs | help status0 and option purpose/line format; actual README command with real temporary files and known expected result; completeness of UTF-8/trim/comments/newlines/invalids/casefold/errors/order/total/unset sections | Only adds option name, documents inline comments/BOM acceptance, example does not run |
| Unset compatibility | All formats, default text/top10 and existing top/min-count argv; reverse-lexical ties, Unicode, >10 words, empty body; identical env/argv/input paths across exact historical source and candidate | Self-generated expectations, wrong baseline, text decode comparison, default/order/JSON/HTML encoding/appearance regression |

[VERIFIED acceptance values: PRD:70-106; spec delta:8-113; 08-CONTEXT.md:15-23. Table is planned verification, not a claim of executed test coverage.]

### Fixed baseline architecture

Approved revision is exactly `79d83ba14dd59d289d2ecd3e33c85e8de437972e`. Its object exists; `git diff --name-only <that revision> -- wordfreq` returned no paths during research. This source comparison is NOT stdout equivalence evidence. [VERIFIED: PRD:104; terminal git output]

Builder should use a test fixture or an existing-on-disk verification script authored before execution to extract the baseline's package into isolated scratch and run its `-m wordfreq` separately from the candidate using the same interpreter. Use identical input pathname/basename, argv and explicitly recorded environment; avoid importing the candidate through inherited PYTHONPATH or cwd. Capture raw stdout, stderr, status and baseline provenance. Either compare live baseline/candidate runs or commit fixed expected bytes demonstrably captured from that exact revision. Do not replace the existing min-count baseline or read current candidate outputs as goldens. [Recommendation implementing PRD:104-106; existing byte helper tests/test_cli.py:418-441; old independent baseline tests/test_cli.py:796-817]

A fixture should fail clearly if the historical object/capture is unavailable, not skip the required compatibility check. Input-byte assertions must include both roles. Store metadata and evidence as readable text/JSON rather than relying on archives or screenshots for PM acceptance. [VERIFIED: 08-CONTEXT.md:21,47; OpenSpec tasks:16-17]

### Sampling Rate

- **Per test-first task:** actual new behavior tests from an existing file, then relevant existing quick boundary/CLI regression; RED must be the intended assertion or missing feature, not missing pytest.
- **Per sequential plan/wave:** accumulated exclusion tests plus retained affected regression files; do not depend on a future plan's not-yet-authored verifier.
- **Phase gate:** full existing suite plus all new tests; quality independently reruns at the exact target head and creates readable `VERIFICATION.md`/CLI evidence with commands, exits, expected/actual and AC/REQ mapping. Historical counts and Builder outputs are not independent quality evidence.
- **Timing:** target selective quick checks below 30 seconds, but no timing measured here. Do not promise a sub-30-second full run; the historical full run took longer.

### Wave 0 Gaps

- [ ] A usable pytest interpreter/environment using existing dev dependency; no new dependency or CI changes. Record the actual framework version once runnable.
- [ ] Author `test_exclude_*` coverage in the existing `tests/test_cli.py` before feature code. Optional pure parser module/tests must exist before their commands are listed as runnable.
- [ ] Source/open error injections for PermissionError and generic OSError; role-aware acquisition-call spy reusable for numeric-first, missing-value, exclusion-first and late-invalid cases.
- [ ] Binary fixed-baseline fixture/captures from the exact approved revision with input/argv/environment provenance; no Phase8 baseline artifact currently authored in this research.
- [ ] Explicit docs completeness and executable README example assertions.
- [ ] Both-role byte nonmutation and full Counter/shared pairs interaction checks.
- [ ] Independent quality evidence originals and final verification artifact. No new verification script is mandatory if pytest already exercises the acceptance surface; if a plan creates one, create/read it before execution and map each assertion to a genuine failure direction.

Do not add pytest configuration or conftest merely to satisfy a template: existing tmp_path/monkeypatch/capsys/subprocess patterns suffice until a real shared fixture is needed. [VERIFIED: tests/test_cli.py:16-20,418-441,624-644,759-817; tests/test_sources.py:64-80]

## Suggested Planning Decomposition (not PLAN files)

1. **Thin vertical tracer, test-first:** add tests for real exclusion, FILE acquisition/line interpretation, CLI connection and one correct exit path; implement only within current boundaries; help/README should already explain the delivered slice. Tests must detect actual missing/ignored exclusion, not merely parser acceptance. Map OpenSpec 2.1 and a thin part of 2.2.
2. **Complete approved edge/interaction surface, test-first:** finish grammar/Unicode/whole-file validation/error order and all formats/min-count/top/original total/empty variants; extend docs and tests. Map remaining 2.1/2.2.
3. **Regression and readable evidence:** fixed-baseline byte checks, both inputs immutable, all existing tests, restricted-diff review; hand off exact-head independent quality/evidence (3.1/3.2). Do not mark quality acceptance complete in a Builder-only task.

Keep plans sequential on the same request branch and at most three tasks per PLAN; the concrete split is planner discretion. Each task's verify command must exercise tests it authors now or that already exist; no task can claim a later plan's uncreated artifact as its proof. [VERIFIED: 08-CONTEXT.md:27; OpenSpec tasks:9-17]

## Security Domain

Enabled by project configuration. This is a local file-reading CLI with no new service, auth, session, datastore or cryptographic feature. [VERIFIED: .planning/config.json:49-51; architecture:90-97]

### Applicable ASVS Categories

| Category | Applies | Standard control / scope |
|---|---|---|
| V2 Authentication | No new authentication surface | Do not introduce one |
| V3 Session Management | No session surface | Not applicable |
| V4 Access Control | Local OS file permissions only | Preserve actual read failures; no permission bypass or rewrite |
| V5 Input Validation | Yes, argv and exclusion rows | argparse then eager Unicode fullmatch; fail closed before body I/O |
| V6 Cryptography | No cryptographic feature | Not applicable; no custom cryptography |

This is an applicability assessment, not an ASVS certification. Approved safety scope remains RULE-1..4. [VERIFIED: PRD:108-117]

### Known Threat Patterns

| Pattern | STRIDE | Mitigation / verification |
|---|---|---|
| Permissive row repair changes exclusion intent | Tampering | Original full-line validation; BOM/punctuation/inline-comment negatives |
| Swallowed I/O/decode failure looks successful | Tampering / repudiation | Retain cause/path and role; exit2 with no output and no body read |
| Exclusion path/contents leak into result HTML | Information disclosure | Continue body basename-only metadata; no new HTML metadata for exclusion file |
| HTML injection/remote resource introduction | Tampering / information disclosure | Keep existing escape/CSS/static formatter unchanged and existing tests retained |
| Input modified as preprocessing | Tampering | Both files read-only; byte assertions on success/failure |

[VERIFIED controls: architecture:42-69; wordfreq/sources.py:19-22; wordfreq/formatters.py:17-127; tests/test_formatters.py:94-262; PRD:131.]

## Assumptions Log

No new product-policy assumption is needed. Helper/module/test organization suggestions are explicitly recommendations within locked discretion. Runtime setup success, pytest version, test duration, baseline output equality and all acceptance results remain unverified, rather than assumed true. The CLI confidence seam's LOW rating is retained instead of upgrading provider trust manually.

## Open Questions

1. **Execution environment setup:** current pytest entrypoint cannot import pytest. Builder must provision the already-declared dev extra in an appropriate interpreter, record version and then run real tests. This is an execution prerequisite, not a request to change dependencies/CI or guess support versions.
2. **No unresolved approved product decision identified:** source requirements and adopted decisions agree on scope. New cases that require product policy, including expanding accepted record separators or multi-file behavior, must go to PM instead of being introduced by test expectations. [VERIFIED: PRD:158-160; architecture:92-97; 08-CONTEXT.md:24]

## Sources

### Direct primary originals opened in this session

- `.planning/phases/08-wordfreq-exclude/08-CONTEXT.md` (all locked decisions, canonical refs, discretion and deferred scope).
- `.planning/REQUIREMENTS.md:104-122`, `.planning/STATE.md` (Phase8 IDs and untouched historical context), `.planning/config.json` (Nyquist/security/agent configuration).
- `_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md`, `brief/brief-wordfreq-exclude.md`, `architecture/architecture.md`, `decision-update.md`, `checks/revision-independent-review.md` (all read in full).
- `openspec/changes/r-e0a2598f-wordfreq-exclude/{proposal,design,tasks}.md`, its `specs/wordfreq-cli/spec.md`, and `openspec/specs/wordfreq-cli/spec.md` (full original requirements and task IDs).
- `wordfreq/__main__.py`, `sources.py`, `tokenizer.py`, `aggregator.py`, `formatters.py`; `pyproject.toml`; `README.md` (current product source originals).
- `tests/test_cli.py`, `test_sources.py`, `test_sources_boundary.py`, `test_tokenizer.py`, `test_aggregator.py`, `test_formatters.py` (full original files read; no execution).
- `.planning/argonauts/r-e0a2598f-learnings.md` and both directly relevant `docs/solutions/best-practices/` originals (current contracts override historical lexical tie examples).

### Official documentation read

- https://docs.python.org/3.14/library/re.html#re.fullmatch — whole-string match and Unicode word semantics; fetched version-specific page, relevant section read from cached full text.
- https://docs.python.org/3.14/builtins/stdtypes.html#str.casefold — caseless matching versus lower, sharp-s expansion; section read.
- https://docs.python.org/3.14/builtins/stdtypes.html#str.splitlines — broader-than-universal-newline separator list; section read as implementation caution.

Research seam returned jina fetch suggestions; permitted fallback was search plus official-page extraction because no jina tool/ctx7 was available. Official confidence classification returned LOW for available provider names; digests were cached at that returned level. No package legitimacy/version claim was fabricated.

## Metadata

- Research date: 2026-11-29 JST, checked with `date +%F`.
- Evidence confidence: provider seam LOW; product findings grounded in directly read authoritative repository originals, library semantics cited to official docs. No acceptance pass asserted.
- Validity: re-read code/test line references and approved artifacts if target head changes; runtime availability must be checked at execution.
- Artifact scope: this `08-RESEARCH.md` only; no product/tests/CI/requirements/state changes intentionally made by research. Existing worktree modifications belonged to orchestration and were not rewritten. Research helper input/cache data was kept in the active profile scratch/runtime cache, not product source.
