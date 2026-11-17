# Phase 1: wordfreq CLI - Pattern Map

**Mapped:** 2026-11-17 (JST)
**Files analyzed:** 13 (12 new + 1 new config file)
**Analogs found:** 3 partial (role-match, `_bmad/scripts/` CLI 規約) / 13 total — 実質 greenfield

## Repository Baseline (greenfield 確認)

- `git ls-files` 実測: `wordfreq/`、`tests/`、`pyproject.toml` は**いずれも未作成・未追跡**（`git ls-files 'tests/*' 'wordfreq/*' 'pyproject.toml'` は空）。
- リポジトリ内の Python は `_bmad/scripts/*.py` 13 本のみ（BMad ツール配布物。単一ファイル CLI スクリプトで、インポート可能パッケージ・pytest 試験・ビルド設定の先行例は**存在しない**）。
- CI 設定（`.github/` 等）なし（RESEARCH.md Pitfall 8 と一致。task 3.3 の block 判定が確定的）。
- `CLAUDE.md` / `AGENTS.md` / `.claude/skills/` / `.agents/skills/` なし。プロジェクト固有の追加規約なし。
- したがって**基準構成は承認済み仕様 `openspec/changes/r-5a3b8a3f-wordfreq/`（spec.md / design.md D-A〜F / tasks.md 1.1〜3.3）と 01-RESEARCH.md の推奨構成**とする。`_bmad/scripts/` の Python は「リポジトリに Python を書くときの見た目の慣習」（argparse 使用、stderr へ `error: ` 前書き、戻り値 int → exit code、`main(argv)` 署名）の弱いアナログとしてのみ参照する。

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `wordfreq/__init__.py` | config (package marker) | none | — (空で可、design D-A) | none |
| `wordfreq/__main__.py` | controller (CLI 合成・exit code 分岐) | request-response, file-I/O | `_bmad/scripts/resolve_config.py` | role-match (partial) |
| `wordfreq/tokenizer.py` | utility (計算部品・注入点) | transform | — | none (RESEARCH Code Examples / design D-D が基準) |
| `wordfreq/aggregator.py` | utility (計算部品) | transform, batch | — | none (RESEARCH Code Examples / design D-A・D-2 が基準) |
| `wordfreq/sources.py` | provider (入力取得境界) | file-I/O | — | none (RESEARCH Pattern 2 / design D-B が基準) |
| `wordfreq/formatters.py` | utility (出力境界) | transform, request-response | `_bmad/scripts/resolve_config.py` (`write_json_stdout`) | role-match (weak — ensure_ascii 値は逆、下記注意) |
| `pyproject.toml` | config | none | — (PEP 723 インラインメタは `_bmad/scripts/*.py` 先頭にあるが別物) | none (RESEARCH Open Question 3 / design D-F が基準) |
| `tests/test_tokenizer.py` | test | unit | — | none (pytest 未導入・tests/ 皆無) |
| `tests/test_aggregator.py` | test | unit | — | none |
| `tests/test_sources.py` | test | unit, file-I/O | — | none |
| `tests/test_formatters.py` | test | unit | — | none |
| `tests/test_sources_boundary.py` | test | unit, boundary | — | none |
| `tests/test_cli.py` | test | integration (subprocess/SystemExit) | — | none |

## Pattern Assignments

### `wordfreq/__main__.py` (controller, request-response + file-I/O)

**Analog:** `_bmad/scripts/resolve_config.py`（tracked 確認済み: `git ls-files _bmad/scripts/config_utils.py` 等で `_bmad/scripts/` 配下は git 追跡下）

**argparse + エラー→stderr→exit code の流れ** (`resolve_config.py` lines 45-66, 79-84):
```python
def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve BMad central config using three-layer TOML merge.")
    parser.add_argument(
        "--project-root",
        "-p",
        required=True,
        help="Absolute project root containing _bmad/",
    )
    ...
    args = parser.parse_args()

    try:
        merged = load_central_config(Path(args.project_root).resolve())
    except ConfigError as error:
        sys.stderr.write(f"error: {error}\n")
        return 1
    ...
    return 0

if __name__ == "__main__":
    ...
    raise SystemExit(main())
```
**何をコピーしてよいか:** 「例外は 1 種類の独自エラー型（向こうは `ConfigError` → 本件は `InputError`）だけを捕捉し、stderr へ 1 行出して exit 1」「使いエラーは argparse 組み込み（exit 2）に完全委譲」「合成関数は int を返す」。
**コピーしてはいけない:** `sys.dont_write_bytecode = True`・PEP 723 `# /// script` ヘッダ・win32 stdout reconfigure — これらは `_bmad` の単一ファイルスクリプト配布用で、`python -m wordfreq`（パッケージ実行・UTF-8 入力固定）では design D-A/D-E の仕様が正。Windows stdout エンコーディング問題は spec の範囲外として持ち込まない。

**`main(argv)` 署名のリポジトリ慣習** (`_bmad/scripts/stamp_release.py:123` / `_bmad/scripts/roster.py:39`, grep 実測):
```python
def main(argv: list[str] | None = None) -> int:
```
RESEARCH の CLI 合成例（`main(argv: list[str] | None = None) -> None` + 内部 `sys.exit`）とも両立。CLI 試験を `subprocess` と `main()+pytest.raises(SystemExit)` 両方で叩く予定なので、`argv` を注入できるこの署名を推奨（Pitfall 5: 捕捉は `InputError` 限定、`except BaseException` 禁止）。

**exit code 分岐の唯一の置き場（D-C）:** argparse error → stderr+exit 2 / `InputError` → stderr+exit 1 / 正常（0 件含む）→ stdout+exit 0。tokenizer・aggregator・sources・formatters に `sys.exit` を置かない（Anti-pattern、RESEARCH 明記）。

---

### `wordfreq/tokenizer.py` (utility, transform)

**Analog:** なし（リポジトリに計算部品・正規化モジュールの先行例なし）。基準は 01-RESEARCH.md「Code Examples → tokenizer」+ design.md D-D。要点（planner は this を plan の action に書く）:
- `re.compile(r"\w+", re.UNICODE)` のモジュールレベル定数 + `str.casefold()` 適用。
- 差し替え点: `iter_tokens(text, tokenizer=default_tokenizer)` 相当の関数引数注入（D-D「注入点の存在を spec の境界試験が要求」）。
- underscore・数字混在（`snake_case`、`abc123`）は 1 語として**受け入れ・試験で固定**（Pitfall 9）。

### `wordfreq/aggregator.py` (utility, transform/batch)

**Analog:** なし。基準は RESEARCH「Code Examples → aggregator」+ design.md D-A/D-2:
```python
def count_words(tokens: Iterable[str]) -> Counter:
    return Counter(tokens)

def top_words(counts: Counter, n: int) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]
```
- `Counter.most_common` をソートに**使わない**（同数順不定、Pitfall 4）。
- ファイルパス・ストリームを知らない（`str`/トークンのみ受け取る、D-B・Pitfall: aggregator にパスを渡すな）。

### `wordfreq/sources.py` (provider, file-I/O)

**Analog:** なし（Protocol 境界の先行例なし）。基準は RESEARCH Pattern 2 + design.md D-A/D-B — `InputError(Exception)` / `TextSource(Protocol).read_text() -> str` / `FileSource` が `open(path, encoding="utf-8")` を閉じ込め `(OSError, UnicodeDecodeError)` → `InputError` へ正規化（verbatim な実装例は RESEARCH Pattern 2 のコードブロックを plan へ転記）。

### `wordfreq/formatters.py` (utility, request-response 出力)

**Analog:** `_bmad/scripts/resolve_config.py` `write_json_stdout` (lines 37-42):
```python
def write_json_stdout(output) -> None:
    """Pin stdout to UTF-8 — a Windows cp1252 default cannot encode emoji icons."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
```
**注意（値が逆）:** `_bmad` は `ensure_ascii=False` + `indent=2` だが、本件は design D-E 固定で **`ensure_ascii=True`・indent 無し・改行 1 つ**。このアナログから拾うのは「`json.dumps(...) + "\n"` を `sys.stdout.write` で出す（print に依存しない）」形だけ。text 側は `<count>\t<word>` 1 行連結（D-A）、0 件は `""` / `"[]\n"`（Pitfall 6: formatter が `None` を返さない）。

### `wordfreq/__init__.py` (config, none)

**Analog:** なし（空で可、design D-A）。docstring 1 行程度まで。

### `pyproject.toml` (config, none)

**Analog:** なし（リポジトリ直下にビルド設定なし）。基準は RESEARCH Open Question 3 + design D-F: setuptools バックエンド最小形 + `[project] name/version + dependencies = []` + pytest を dev 依存。`python -m` 実行にインストール不要（Pitfall 1: cwd が sys.path に入る）を前提に「実行のためでない最小差分」を plan に明記。危険なパス（smart マージ方針・人レビュー想定）。`_bmad/scripts/*.py` 先頭の `# /// script`（PEP 723）は単一ファイル用メタであり pyproject のアナログではない。

### `tests/test_*.py` 6 ファイル (test)

**Analog:** なし（pytest 未導入・`tests/` 皆無・conftest.py 不要=共有 fixture なし、`tmp_path` 組み込みで足りる）。基準は RESEARCH「Validation Architecture → Phase Requirements → Test Map」+「境界越し試験」コード例（task 2.3 の spy 方式、`FakeSource` 二重化）。試験実行は常に `python -m pytest`（素の `pytest` は壊れたシム、RESEARCH 注意）。テストファイル分割は Claude's Discretion（CONTEXT）。

## Shared Patterns

### argparse への使いエラー委譲（exit 2）
**Source:** CPython 3.14.9 `argparse.py`（RESEARCH Pattern 1 で verbatim 検証済み）+ リポジトリ慣習として `_bmad/scripts/` 11 ファイルが argparse 使用（grep 実測）
**Apply to:** `__main__.py` のみ
位置引数 `filename` ちょうど 1 個（`nargs` 付けない、Pitfall 2）、`--top` は `type=int, default=10`、`--format` は `choices=["text","json"], default="text"`。自前検証は `args.top < 1` → `parser.error(...)` のみ（委譲できる検査を書き分けない、Anti-pattern）。`--top=-1` と `--top -1` 両方の試験ケースを持つ（Pitfall 3 / Assumption A1）。

### 例外→stderr 1 行→exit 1
**Source:** `_bmad/scripts/resolve_config.py:62-66`（`except ConfigError as error: sys.stderr.write(f"error: {error}\n"); return 1`）
**Apply to:** `__main__.py` のみ（`InputError` に限定捕捉）。結果は stdout、エラーは stderr 完全分離（Pitfall 7: CLI 試験で stdout/stderr をマージして検査しない）。

### 「戻り値 int → SystemExit」または「内部 sys.exit」のどちらか 1 系統に統一
**Source:** `_bmad/scripts/stamp_release.py:143`（`sys.exit(main())`）/ `resolve_config.py:84`（`raise SystemExit(main())`）
**Apply to:** `__main__.py`。RESEARCH の合成例は `main() -> None` + 末尾 `sys.exit(0)`。いずれでも exit code は 0/1/2 の 3 値のみを spec D-C と同じ意味で使う。

### Python 記述の見た目慣習（弱い参照）
**Source:** `_bmad/scripts/*.py`（例 `resolve_config.py:1-13`, `roster.py:39`）
**Apply to:** 全新規 Python ファイル。モジュール冒頭 docstring、型注釈（`list[str] | None` 等の 3.9+ 記法。3.14 専用機能は使わない — RESEARCH Open Question 2 の方針）。shebang/PEP 723 ヘッダは本パッケージでは**付けない**（スクリプト配布用のため）。

## No Analog Found

Files with no close match in the codebase (planner should use RESEARCH.md patterns instead):

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `wordfreq/tokenizer.py` | utility | transform | リポジトリに正規化・トークン化モジュールの先行例なし |
| `wordfreq/aggregator.py` | utility | transform/batch | Counter・決定論ソートの先行例なし |
| `wordfreq/sources.py` | provider | file-I/O | typing.Protocol 境界の先行例なし |
| `wordfreq/__init__.py` | config | none | インポート可能パッケージ自体が初 |
| `pyproject.toml` | config | none | ビルド設定の先行例なし（PEP 723 は別物） |
| `tests/*` (6 files) | test | unit/integration | pytest 未導入・tests/ 皆無（Wave 0） |

## Metadata

**Analog search scope:** リポジトリ全体（`git ls-files` 全 58 エントリ）・`_bmad/scripts/`（唯一の Python 所在）・`openspec/changes/r-5a3b8a3f-wordfreq/`（承認済み基準仕様）・`.planning/phases/01-wordfreq-cli/01-{CONTEXT,RESEARCH}.md`
**Files scanned:** tracked Python 13 本（argparse 使用 11 本 grep 実測）・ルートに CI/pyproject/tests 不在を確認
**Pattern extraction date:** 2026-11-17
**Tracked-source gate (#3645):** 参照したアナログ `_bmad/scripts/resolve_config.py`・`stamp_release.py`・`roster.py` はすべて `git ls-files` 追跡下を確認（gitignore ミラーなし）
