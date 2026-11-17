# Phase 1: wordfreq CLI - Research

**Researched:** 2026-11-17 (JST)
**Domain:** stdlib-only Python CLI（トークン化・集計・入出力境界・exit code 規約・pytest 試験）
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### 実行方法と入力（FR-1）
- `python -m wordfreq <file>` はファイル引数ちょうど 1 個を受け取る。UTF-8 として読んで集計結果を出力する。
- 存在しない・開けない・UTF-8 デコード不可 → stderr にエラーメッセージ、exit 1、stdout には結果を出さない。
- ファイル引数 0 個または 2 個以上 → 使い方エラー、stderr、exit 2。
- 空ファイルは結果 0 件（text は出力なし、json は `[]`）で exit 0。

#### 件数・形式オプション（FR-2・FR-3）
- `--top N` は 1 以上の整数、既定 10。整数でない・0 以下は exit 2。結果が N 満たなければ全件。
- `--format text|json`、既定 text。text は 1 語 1 行で列書式は design.md D-A の `<count>\t<word>`。json は `{"word": <str>, "count": <int>}` の配列で `json.loads` 可読、順序は text と同一。不正形式は exit 2。

#### 切り出し・正規化（D-3）
- 単語は Unicode の単語構成文字（Python `\w`、`re.UNICODE`）の連続する最大長。各トークンに `str.casefold()` を適用。
- 句読点・記号・空白は語に含めない。大文字小文字のみ異なる語は同一視（"Hello hello HELLO" → hello 3）。
- トークナイザは差し替え可能な部品として実装する。日本語は形態素解析せず `\w` ルールの結果が決定論的ならよい。

#### 順序の決定論性（FR-4・D-2）
- 出現回数の降順、同回数なら正規化後単語の昇順。同じ入力・同じオプションの出力は決定論的。

#### 部品分離と入力元拡張（FR-5・FR-6）
- トークナイザ・集計・入力取得・出力整形を分離した部品構成にする（tasks.md のファイル配置: `wordfreq/tokenizer.py`、`aggregator.py`、`sources.py`（`TextSource` プロトコル + `FileSource` + `InputError`）、`formatters.py`）。
- 解析・集計はテキストを入力取得境界を介してのみ受け取る。各部品は単体で呼んで検証できること。
- 入力元（標準入力・URL）の追加は入力取得境界の実装追加で足りるという構成判断を design.md に記録済み。

#### 試験と実行環境（FR-7・FR-8）
- pytest 単体試験をリポジトリ CI の pytest ジョブで通す。試験は spec の全シナリオ（不存在ファイル、空ファイル、引数個数、不正 `--top`/`--format`、同数語の順序、大文字小文字同一視、UTF-8 デコード失敗、JSON 構造、部品単体・境界越し検証）を含む。
- 対象 Python は CI ジョブの CPython 3 の版。バージョン横断互換コードを書かない。ランタイム依存は標準ライブラリのみ（`pyproject.toml` の dev 依存に pytest は可）。
- CI に pytest ジョブが無ければ workflow 変更は人の対応扱い（Bot の権限外）。task 3.3 で有無を確認し、無ければ block 判定の準備をする。

### Claude's Discretion
- 関数・モジュール内部の細部（argparse の使い方、例外処理の内部構造、テストファイルの分割方法）は承認済み仕様の範囲で実装が決定してよい。
- `pyproject.toml` の最小限の設定内容（ビルドバックエンド選択等）は仕様「最低限のパッケージ設定は許容」の範囲で決定してよい（危険なパスのためレビュー対象になることは想定済み）。

### Deferred Ideas (OUT OF SCOPE)
- 日本語形態素解析（v1 範囲外。トークナイザ差し替え点だけ残す）
- 標準入力・URL からの入力（入力取得境界の実装追加で対応可能な状態を維持するだけがスコープ）
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-01 | `python -m wordfreq <file>`・ちょうど 1 個・UTF-8 読み・exit 0/1/2 規約 | Pattern 1（argparse 構成、`argparse.py:2785` の exit(2) 検証済み）、Pattern 2（FileSource + InputError 変換）、Pitfall 2/3/5 |
| REQ-02 | `--top N`（既定 10、1 以上整数、不正は exit 2、N 未満なら全件） | `type=int` + 明示的な `>= 1` チェックのみ自前（D-C）、Pitfall 3（`-1` の扱い）、`top_words` はソート後のスライス |
| REQ-03 | `--format text|json`（text=`<count>\t<word>`、json は word/count 配列、0 件は `[]`/出力なし） | formatters 部品 + D-E（`json.dumps(..., ensure_ascii=True)` + 改行 1 つ）、Code Examples |
| REQ-04 | 回数降順→正規化後単語昇順の決定論ソート | Pitfall 4: `Counter.most_common` の同数順は保証なし → `sorted(key=(-count, word))` を使用 |
| REQ-05 | tokenizer/aggregator 部品分離・単体試験 | D-A 4 分割 + Code Examples（`iter_tokens` / `count_words` / `top_words`）、Validation Architecture の試験マッピング |
| REQ-06 | `TextSource` 境界越し試験・入力元拡張構成 | D-B、Pattern 2（`typing.Protocol`）、tests/test_sources_boundary.py（task 2.3） |
| REQ-07 | pytest 一式・CI pytest ジョブで通る | Validation Architecture（Wave 0: pytest 未インストール、tests/ 未作成）、Environment Availability、CI ジョブ不在の発見（Pitfall 8） |
| REQ-08 | ランタイム依存ゼロ・pyproject.toml 必要最小限 | Standard Stack（stdlib のみ）、`python -m` は cwd を sys.path に足すためインストール不要で動く事実（Pitfall 1） |
</phase_requirements>

## Summary

この phase は greenfield の stdlib-only Python CLI で、未知のライブラリも外部サービスも無い。技術的なリスクはほぼ無く、成否は (1) exit code 0/1/2 の分岐を spec 通りに固定できるか、(2) 決定論ソート（同数語の昇順）を `Counter.most_common` に任せて壊していないか、(3) 部品境界（`TextSource`）を通す試験構造を作れるか、(4) pytest と CI という「今このリポジトリに存在しない足場」を Wave 0 でどう埋めるかの 4 点に集約される。

実行環境の実測では、リポジトリに CI workflow が一切存在しない（`.github/` 等なし）。つまり REQ-07 の「CI の pytest ジョブ」は現状成立せず、task 3.3 の block 判定（workflow 変更は人対応）が確定的に発火する。ローカル検証は `python -m pytest`（repo 直下実行）で行い、テスト実行の正は CI に置く設計のまま、CI 追加を人の対応として明示的に計画へ引き渡す必要がある。

もう 1 つの実測上の重要事実は、`python -m wordfreq` は repo 直下からインストール不要で動くこと（`-m` は cwd を sys.path 先頭に追加する）。したがって `pyproject.toml` は「実行のため」ではなく、パッケージメタデータと pytest dev 依存の宣言のための最小限変更で足りる（危険なパス方針と整合）。pytest はこのマシンに未インストール（`python3 -m pytest` 不可、`~/.local/bin/pytest` はモジュール欠落の壊れたシム）で、uv が利用可能。

**Primary recommendation:** 承認済み design.md の 4+1 分割（tokenizer / aggregator / sources / formatters + `__main__`）をそのまま実装し、ソートは `sorted(items, key=lambda wc: (-wc[1], wc[0]))` に固定、exit 分岐は argparse 組み込み exit(2) + `InputError` → exit(1) の 2 経路のみ。Wave 0 で pytest を uv でインストールし、CI pytest ジョブ不在は task 3.3 で block 判定として人へ引き渡す。

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| 引数解析・exit code 分岐 | CLI 実行プロセス（`__main__.py`） | — | design D-C: exit code 分岐は `__main__.py` のみ。他部品は exit を知らない |
| テキスト入力取得（ファイル・UTF-8） | 入力取得境界（`sources.py` / `TextSource`） | OS ファイル I/O | v1 のファイル入力も境界の背後。解析・集計は `str` だけ受け取る（D-B） |
| 切り出し・正規化 | 計算部品（`tokenizer.py`） | — | `re.findall(r"\w+")` + `casefold()`。他部品の知識ゼロ、注入点 |
| 頻度集計・決定論ソート | 計算部品（`aggregator.py`） | — | `count_words` / `top_words`。テキストの得方にも出力形式にも依存しない |
| 出力整形（text/JSON） | 出力境界（`formatters.py`） | stdout | 文字列を返すだけで、print も exit も `__main__` 側 |
| 試験実行 | pytest（dev 依存） | CI ジョブ（現状不在 → 人対応） | REQ-07。ローカルは `python -m pytest`、正は CI |

## Standard Stack

### Core（ランタイム依存 = 標準ライブラリのみ・REQ-08）

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python (CPython) | 3.14.9（本マシン `python3`）[VERIFIED: python3 --version] | 実行時 | リポジトリに既存 Python 足場なし。CI ジョブの CPython 3 の版が正（現状 CI 不在 → 未確定、Open Question 1） |
| `argparse`（stdlib） | CPython 3.14 同梱 [VERIFIED: lib/python3.14/argparse.py 読み合わせ] | 引数解析・使い方エラー exit 2 | D-C が argparse の `type=` / `choices=` を明示使用 |
| `re`（stdlib） | CPython 3.14 同梱 [CITED: docs.python.org/3/library/re.html] | `\w+` 最大長抽出 | D-D の抽出ルールそのもの |
| `collections.Counter`（stdlib） | CPython 3.14 同梱 [ASSUMED] | 語 → 回数の集計 | `count_words` の戻り値型（D-A） |
| `json`（stdlib） | CPython 3.14 同梱 [CITED: docs.python.org/3/library/json.html] | JSON 配列出力 | D-E `json.dumps(..., ensure_ascii=True)` |
| `typing.Protocol`（stdlib） | CPython 3.14 同梱 [ASSUMED] | `TextSource` プロトコル定義 | D-A の「プロトコル 1 つに実装 1 つ」 |

### Supporting（dev 依存のみ許可）

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 9.2.0（PyPI 最新）[VERIFIED: pip index versions pytest] | 単体試験ランナー | REQ-07。dev 依存のみ可（CONTEXT 許可済み） |
| uv | 利用可（`command -v uv`）[VERIFIED: 本セッション実測] | pytest インストール手段 | 対象 venv に pip モジュール無し（実測） |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `collections.Counter` | 素の dict + ループ | Counter は D-A が戻り値型として明記。素 dict でも足りるが design 逸脱 |
| setuptools（pyproject ビルドバックエンド） | hatchling | D-F が「setuptools or hatchling の minimum」を Claude's Discretion に委譲。最小差分なら setuptools。どちらでも `python -m` 実行には不要（Pitfall 1） |
| argparse | click / typer | 外部ランタイム依存になるため REQ-08 で禁止。論外 |

**Installation（dev 依存のみ。ランタイム追加なし）:**
```bash
uv pip install pytest   # 対象インタープリタは plan 時点で確定（Open Question 1 参照）
```

## Package Legitimacy Audit

公式シーム `gsd_run query package-legitimacy check --ecosystem pypi pytest` を実行（本セッション）:

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| pytest | PyPI | シーム判定 "too-new"（最新版 publish 2026-10-27 を根拠とするSignals。PyPI 履歴は 2.0 系まで全バージョンが並ぶ実績あるパッケージ）| unknown-downloads（シーム取得できず）| github.com/pytest-dev/pytest | [SUS] | Flagged — planner はインストール前に checkpoint を想定 |
| wordfreq | — | — | — | — | 対象外 | 本 phase は PyPI 公開しない（Out of Scope）。既存同名 PyPI パッケージは依存に追加しないため無関係 |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** pytest — `` `pytest` [WARNING: flagged as suspicious — verify before using.] `` ※"too-new" は最新版リリース日（2026-10-27）の信号で、`pip index versions pytest` は 2.0.x 以降の全履歴を返し `pytest-dev/pytest` を正リポジトリとして認識済み。SUS の理由（too-new / unknown-downloads）はメタデータ取得側の限界が主因と考えられるが、プロトコルどおり planner は human-verify チェックポイントを 1 回だけ前置してよい。

## Architecture Patterns

### System Architecture Diagram

```
argv ──► __main__.py (argparse: file ちょうど1個 / --top / --format)
  │            │ parse 失敗(引数個数・type・choices・top<1) ──► argparse error → stderr, exit 2
  │            ▼ 正常
  │      FileSource(path)  ◄── TextSource プロトコル（入力取得境界・sources.py）
  │            │ read_text() -> str（UTF-8）
  │            │ OSError / UnicodeDecodeError → InputError → stderr, exit 1
  │            ▼ str
  │      iter_tokens(text) ──► tokens        (tokenizer.py: re \w+ + casefold)
  │            ▼
  │      count_words(tokens) ──► Counter     (aggregator.py)
  │            ▼
  │      top_words(counts, n) ──► [(word, count)]  (回数降順→語昇順、先頭 n)
  │            ▼
  └──► format_text / format_json(pairs) ──► stdout, exit 0
                （text: "<count>\t<word>" 1行 / json: [{"word":..,"count":..},...]）
```

### Recommended Project Structure

```
wordfreq/              # 新パッケージ（stdlib only）
├── __init__.py        # 空で可
├── __main__.py        # argparse と合成のみ。exit code 分岐はここだけ（D-C）
├── tokenizer.py       # iter_tokens(text) -> Iterator[str]（注入点 = D-D）
├── aggregator.py      # count_words(tokens) -> Counter / top_words(counts, n)
├── sources.py         # TextSource プロトコル + FileSource + InputError
└── formatters.py      # format_text(pairs) / format_json(pairs)
tests/                 # pytest 試験（task 1.1〜3.1 に対応して増設）
├── test_tokenizer.py
├── test_aggregator.py
├── test_sources.py
├── test_formatters.py
├── test_sources_boundary.py   # task 2.3 境界越し試験
└── test_cli.py                # task 3.1 CLI 合成試験（exit code 含む）
pyproject.toml         # 新規（危険なパス・最小限。dev 依存に pytest）
```

### Pattern 1: argparse による exit 2 使いエラー（D-C と完全一致）

**What:** ファイル引数ちょうど 1 個・`--top` int・`--format` choices を argparse に宣言し、使い方エラーは argparse 組み込みの stderr + exit 2 に完全委譲する。
**When to use:** REQ-01/REQ-02/REQ-03 の exit 2 系すべて。
**Example:**
```python
# Source: ローカル CPython 3.14.9 stdlib ソース read 検証
# (lib/python3.14/argparse.py:2774-2785, error() は最後に self.exit(2, ...) を呼ぶ)
import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wordfreq")
    p.add_argument("filename")                                  # ちょうど1個（0個なら exit 2）
    p.add_argument("--top", type=int, default=10)               # 整数でなければ exit 2
    p.add_argument("--format", choices=["text", "json"], default="text")  # 不正形式 exit 2
    return p

args = build_parser().parse_args()
if args.top < 1:                       # D-C: 1 未満のみ明示検証（argparse 型検査の後）
    parser.error("--top must be >= 1") # → stderr + exit 2
```
検証済み verbatim 抜粋（CPython 3.14.9 `argparse.py`、`def exit` 直後）:
```python
    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        ...
        """
        self.print_usage(_sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _('%(prog)s: error: %(message)s\n') % args)
```
`parse_args()` は内部でこの `error()` を呼ぶため、引数個数不正・`type=int` 失敗・`choices` 失敗は例外なく「stderr + exit 2」になる [VERIFIED: lib/python3.14/argparse.py:2769-2785（本セッションで sed による範囲 read）]。

### Pattern 2: TextSource プロトコルによる入力取得境界（D-A / D-B）

**What:** `typing.Protocol` で `read_text() -> str` を宣言し、ファイル I/O とデコードは `FileSource` の中に閉じ込める。環境エラーは `InputError` へ正規化して `__main__` 側で exit 1 に写像する。
**When to use:** REQ-06。標準入力・URL 追加時は `sources.py` に実装を足すだけで、tokenizer/aggregator/formatter は触らない。
**Example:**
```python
# Source: design.md D-A/D-B + stdlib typing.Protocol（typing — docs.python.org/3/library/typing.html#typing.Protocol）
from typing import Protocol

class InputError(Exception):
    """入力取得境界で発生した環境エラー（__main__ が exit 1 に変換する）"""

class TextSource(Protocol):
    def read_text(self) -> str: ...

class FileSource:
    def __init__(self, path: str) -> None:
        self._path = path
    def read_text(self) -> str:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError) as e:
            raise InputError(f"{self._path}: {e}") from e
```
`__main__.py` 側: `except InputError as e: print(e, file=sys.stderr); sys.exit(1)`。`UnicodeDecodeError` は `ValueError` のサブクラスだが、`open().read()` の途中で出ることがあるため境界内で捕捉する [CITED: docs.python.org/3/library/exceptions.html#UnicodeDecodeError]。

### Anti-Patterns to Avoid
- **exit code 分岐を部品に散らす:** `tokenizer`/`aggregator`/`formatters` が `sys.exit` を持つと D-C 違反。分岐は `__main__.py` のみ（STATE.md 決定にも「exit code 0/1/2 分岐は `__main__.py` のみ（D-C）」と記録済み）。
- **aggregator にファイルパスを渡す:** 集計関数が `str` 以外を受け取った瞬間に REQ-06 の境界試験が落ちる。`FileSource` 非経由で合成テキストを直接渡す試験を aggregator 側に置く（D-B）。
- **`parse_args` の返り値を自分で再検証しすぎる:** 委譲できる検査（int 化・choices・個数）を自前に書き分けると exit 2 の文面・経路が分裂する。自前はいちばん小さい `top < 1` だけ。

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 使いエラー（usage 表示 + stderr + exit 2） | 自前の引数長チェック・メッセージ出力 | `argparse.ArgumentParser`（`type=` / `choices=` / 位置引数） | exit(2) まで組み込み。0 個・2 個以上の両方と不正値を同一経路で処理（argparse.py 検証済み） |
| 語の切り出し（Unicode 単語境界） | 自前の isalnum ループ | `re.findall(r"\w+", text)` | `\w` は既定で完全 Unicode マッチ（re.A 時のみ ASCII 制限）。ASCII/非 ASCII 境界や結合文字の扱いを自作すると決定論が壊れやすい [CITED: docs.python.org/3/library/re.html#re.A] |
| 大文字小文字の同一視 | `lower()` | `str.casefold()` | D-3/FR-5 が casefold を明記。lower より強い正規化（ß→ss 等）|
| JSON 出力 | 手組み文字列 | `json.dumps(pairs_as_dicts, ensure_ascii=True)` | D-E 固定。`json.loads` 可読性を自動保証、キー名 `word`/`count` |
| ソート | `Counter.most_common` に同数順を期待 | `sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))` | most_common は同数の順序を保証しない（下記 Pitfall 4） |

**Key insight:** この CLI の価値そのものが「stdlib の既定挙動の正確な選択」にある。自作するのは (a) 注入点としての関数引数、(b) `top < 1` チェック、(c) `InputError` への正規化の 3 点だけで足りないくらいに委譲できる。

## Common Pitfalls

### Pitfall 1: 「pyproject.toml がないと `python -m wordfreq` が動かない」と思い込む
**What goes wrong:** 危険なパス `pyproject.toml` を先に作らないと実行できないと誤解し、インストール・egg-info 等の余計な状態を持ち込む。
**Why it happens:** 実行とパッケージングが結びつけられがち。
**How to avoid:** `-m` は標準 import 機構でモジュールを探し、**cwd を sys.path の先頭に追加する** [CITED: docs.python.org/3/using/cmdline.html#cmdoption-m: "As with the `-c` option, the current directory will be added to the start of `sys.path`"]。repo 直下に `wordfreq/__main__.py` があればインストールなしで動く。task 3.2 の確認（repo 直下で `python -m wordfreq <file>`）もこの経路。
**Warning signs:** `pip install -e .` 後の egg-info が git status に出始める。

### Pitfall 2: `nargs="+"` などで「ちょうど 1 個」を緩める
**What goes wrong:** 2 個以上で exit 2 にならず、黙って先頭だけ使う／全件読む。
**Why it happens:** positional に `nargs='*'`/`'+'` をつけると argparse は 2 個目を許す。
**How to avoid:** 位置引数 `filename` はデフォルト（ちょうど 1 個）のまま。2 個以上の超過引数は argparse が `unrecognized arguments` として exit 2 [CITED: docs.python.org/3/library/argparse.html#nargs]。試験は「ファイル 2 個 → exit 2」を spec 通り必ず持つ。
**Warning signs:** CLI 試験に 2 個ケースが無い。

### Pitfall 3: `--top -1` と `--top 0` を同じ経路で壊す
**What goes wrong:** `--top -1` がオプションフラグ扱いで予期しないエラー文になる、または `0` が素通りする。
**Why it happens:** argparse は「負数に見えるトークン」を、パーサに負数風のオプションが 1 つも無ければ**値として**扱う（`-1` は `--top` の値として int('-1')=-1 になる）。
**How to avoid:** 本 CLI は負数風オプション（`-1` 等）を持たないので `--top -1` は値として通り、`type=int` → 1 未満チェック → exit 2 の同一経路に乗る。`--top 0` も同経路。`--top=-1` と `--top -1` 両方の試験ケースを持つと安全 [ASSUMED（動作自体は argparse の既知挙動だが、本セッションで実機実行はしていない）]。
**Warning signs:** 試験が `--top abc` しか持たない。

### Pitfall 4: `Counter.most_common` に FR-4 の同数タイブレークを任せる
**What goes wrong:** 同回数語の並びが CPython の実装依存（挿入順）になり、spec の「正規化後単語の昇順」が壊れる。
**Why it happens:** `Counter.most_common()` のドキュメントは「要素間の順序は不定（equal counts are ordered arbitrarily）」と明記。
**How to avoid:** `top_words` は `sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]` を使用 [CITED: docs.python.org/3/library/collections.html#collections.Counter.most_common]。試験は `apple`/`zoo` が 5 回のときに `apple` 先頭を固定（spec シナリオ）。
**Warning signs:** ソート試験が「回数の順序」しか見ていない。

### Pitfall 5: `SystemExit` を `except Exception` で握りつぶして exit 2 を壊す
**What goes wrong:** argparse の exit(2)（`SystemExit`）や自分の `sys.exit(1)` を合成側の try/except で拾い、exit code が 0/1 に化ける。
**Why it happens:** `__main__` のエラーハンドラを広く書きすぎる。
**How to avoid:** 捕捉は `InputError`（→exit 1）に限定。`SystemExit` は `Exception` のサブクラスではないため通常は安全だが、`except BaseException` は禁止。
**Warning signs:** CLI 試験で exit code を `subprocess`/`pytest.raises(SystemExit)` の両方ではなく stdout だけ見ている。

### Pitfall 6: 空ファイルを異常扱い、または `--top` 超過をエラーにする
**What goes wrong:** 空ファイルで exit 1、語種 < N で例外。
**How to avoid:** 空ファイルは結果 0 件で exit 0（text 出力なし / json `[]`）[VERIFIED: spec.md「空ファイルは 0 件で正常終了」シナリオを本セッションで read]。`[:n]` スライスは件数不足時に自然に全件を返す。
**Warning signs:** formatter が 0 件時に `None` を返している。

### Pitfall 7: 出力ストリームの取り違え
**What goes wrong:** エラーが stdout に出て「stdout に結果が出力されない」シナリオに違反、または結果の一部が stderr 混在で `json.loads(stdout)` が失敗。
**How to avoid:** 結果は stdout、エラーは stderr に完全分離。JSON 出力は D-E 通り `json.dumps(...) + "\n"` の 1 行のみを stdout へ。
**Warning signs:** CLI 試験が stdout/stderr をマージして検査している。

### Pitfall 8: 「CI の pytest ジョブ」が存在しないことを計画に入れ忘れる
**What goes wrong:** REQ-07/FR-7 の検証が CI で走る前提の計画になり、最後に検証不能で止まる。
**Why it happens:** proposal は「CI に pytest ジョブが必要になる**可能性がある**」と書いていたが、実測では workflow 自体が皆無。
**How to avoid:** 本リポジトリの git 直下には `.github/`（および GitLab 等の CI ディレクトリ）が**存在しない**ことを確認済み（`ls` 直下一覧に CI 設定なし）[VERIFIED: リポジトリルート一覧 read（.git, .planning, .compound-engineering, _bmad, _bmad-output, docs, openspec, README.md）]。task 3.3 は「無 → workflow 変更（人対応）として block 判定」の準備が確実に出番する。ローカル検証（`python -m pytest`）は Builder/品質が実行可能だが、REQ-07 の充足自体は CI ジョブ新設（人）に依存する。
**Warning signs:** 計画に「CI で緑」を検証手順として書き、block 経路が無い。

### Pitfall 9: `\w` の undersc­ore・数字混在を後で直そうとする
**What goes wrong:** `snake_case` が 1 語、`abc123` が 1 語になる挙動を「バグ」として途中で仕様変更し、既存試験と決定的仕様が割れる。
**How to avoid:** design D-D は「underscore を語に含める副作用は受け入れ、試験で固定」と明示 [VERIFIED: design.md D-D を本セッションで read]。task 1.1 の「underscore 語の固定」試験がこれ。日本語テキストも `\w` ルールの結果で決定的なら可。
**Warning signs:** tokenizer 試験に underscore ケースが無い。

## Code Examples

### aggregator の決定論ソート（REQ-04 / D-2）
```python
# Source: docs.python.org/3/library/collections.html（Counter.most_common の同数順序不定）+ design D-2
from collections import Counter
from typing import Iterable

def count_words(tokens: Iterable[str]) -> Counter:
    return Counter(tokens)

def top_words(counts: Counter, n: int) -> list[tuple[str, int]]:
    # 回数降順 → 正規化後単語の昇順。n 件未満なら全件（[:n] が自然に全件を返す）
    return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]
```

### tokenizer（REQ-05 / D-D、注入点）
```python
# Source: docs.python.org/3/library/re.html#re.findall + D-D
import re
from typing import Callable, Iterator

_WORD_RE = re.compile(r"\w+", re.UNICODE)

def default_tokenizer(text: str) -> list[str]:
    return _WORD_RE.findall(text)

def iter_tokens(text: str, tokenizer: Callable[[str], list[str]] = default_tokenizer) -> Iterator[str]:
    return (tok.casefold() for tok in tokenizer(text))
```

### formatters（REQ-03 / D-A / D-E）
```python
# Source: design.md D-A（<count>\t<word>）と D-E（ensure_ascii=True + 改行1つ・0件は []）
import json

def format_text(pairs: list[tuple[str, int]]) -> str:
    return "".join(f"{count}\t{word}\n" for word, count in pairs)

def format_json(pairs: list[tuple[str, int]]) -> str:
    items = [{"word": word, "count": count} for word, count in pairs]
    return json.dumps(items, ensure_ascii=True) + "\n"
```

### CLI 合成（REQ-01 / D-C）
```python
# Source: design.md D-C + ローカル argparse.py exit(2) 検証
import sys
from .aggregator import count_words, top_words
from .formatters import format_json, format_text
from .sources import FileSource, InputError
from .tokenizer import iter_tokens

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()          # Pattern 1
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")   # exit 2
    try:
        text = FileSource(args.filename).read_text()
    except InputError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    pairs = top_words(count_words(iter_tokens(text)), args.top)
    out = format_json(pairs) if args.format == "json" else format_text(pairs)
    sys.stdout.write(out)            # 0 件なら text="" / json="[]\n"
    sys.exit(0)
```

### 境界越し試験（REQ-06 / task 2.3 / D-B）
```python
# aggregator 系試験は合成テキストを直接渡す（FileSource 非経由）ことを構造的に示す
def test_aggregator_never_touches_files(tmp_path):
    import wordfreq.sources as sources
    from wordfreq.aggregator import count_words
    from wordfreq.tokenizer import iter_tokens
    calls = []
    orig = sources.FileSource.read_text
    def spy(self):
        calls.append(1); return orig(self)
    sources.FileSource.read_text = spy
    try:
        counts = count_words(iter_tokens("a b a"))   # 境界を一切通らない
        assert counts["a"] == 2 and calls == []
    finally:
        sources.FileSource.read_text = orig

class FakeSource:                    # TextSource 互換のテスト用二重化
    def read_text(self): return "hi hi there"
# 合成経路: count_words(iter_tokens(FakeSource().read_text())) が期待値になる
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `str.lower()` で大文字小文字同一視 | `str.casefold()`（3.3 以降） | Python 3.3 | spec が casefold 固定。lower とは結果が変わり得る（例: ß） |
| `re.U` を明示して Unicode を有効化 | str パターンは既定で Unicode マッチ（`re.A` で ASCII に制限） | Python 3 系全般（現行 docs 確認）[CITED: docs.python.org/3/library/re.html#re.A] | `re.UNICODE` を書いても書かなくても同じ。spec が `re.UNICODE` 参照なので明示で可 |
| `setup.py` 中心のパッケージ定義 | `pyproject.toml`（PEP 621）一択 | 2022 頃（setuptools 61+）| 新設は pyproject.toml のみ。setup.py を追加しない |

**Deprecated/outdated:**
- `pip install -e .` を `python -m` 実行のために前提にすること — `-m` の cwd 追加で不要（Pitfall 1）。

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `--top -1` は argparse の負数トークン解決で「値」として通り exit 2 経路に乗る（本セッションで実機未実行） | Pitfall 3 | 試験ケース設計の微修正で済む。`--top=-1` を併記すれば無害化 |
| A2 | pytest 9.2.0 を uv で対象 venv に導入すれば `python -m pytest` がその場で動く | Standard Stack / Wave 0 | 低。CI 側は人対応の job 定義次第 |
| A3 | 「CI ジョブの CPython 3 の版」は CI 新設時に人が決める（本マシンでは 3.14.9 と 3.12.15 が併存） | Open Question 1 | バージョン横断互換コードを書かない方針のため、実コードの分岐は発生しない。試験の import 可否のみ確認点 |
| A4 | pytest の SUS 判定は最新版 publish 日（2026-10-27）と download 取得不能による見かけ上の疑わしさで、pytest-dev/pytest 自体は実績プロジェクト | Package Legitimacy Audit | 誤判定なら checkpoint 1 回が無駄になるだけ。見逃しなら壊れた dev 導入 |

**If this table is empty:** All claims in this research were verified or cited — no user confirmation needed.

## Open Questions (RESOLVED)

1. **CI の pytest ジョブが存在しない。REQ-07 の「CI で通る」をどう充足するか？**
   - RESOLVED: CONTEXT.md「試験と実行環境（FR-7・FR-8）」の確定判断「CI に pytest ジョブが無ければ workflow 変更は人の対応扱い（Bot の権限外）。task 3.3 で有無を確認し、無ければ block 判定の準備をする」により、CI ジョブ新設は人対応と確定。PLAN 01-04 の `user_setup` として pytest ジョブ追加を人に依頼する経路で充足する（design.md Risks「CI に pytest ジョブが無い場合…block して人に委ねる（proposal Impact 済み）」と整合）。
   - What we know: リポジトリ直下に CI workflow 設定は無し [VERIFIED: ルート一覧 read]。workflow ファイル変更は Bot 権限外（承認済み制約）。tasks.md 3.3 は「無ければ block 判定の準備」を要求。
   - What's unclear: workflow を人に新設させるのか（依頼の一環として人対応で OK）、それとも「CI 追加は範囲外」なのかの確定。
   - Recommendation: 計画では task 3.3 を「CI 不在の確認済み → block 判定（人対応: pytest ジョブ 1 本の追加依頼）の準備」として必ず含め、Bot 実装部分は `python -m pytest` のローカル緑で検証完了扱いにする。
2. **対象 Python の正確な版数（「CI ジョブの CPython 3 の版」が未定義）**
   - RESOLVED: CONTEXT.md「試験と実行環境（FR-7・FR-8）」の「対象 Python は CI ジョブの CPython 3 の版。バージョン横断互換コードを書かない」により確定。design.md D-F「Python バージョンは CI ジョブの現行 CPython 3 に合わせ、互換分岐を書かない」と同じく、版数の未定義は横断互換コードを書かない方針で解消され、実装判断への影響は無い（ローカル検証の正は `python3` = 3.14.9）。
   - What we know: ローカルは CPython 3.14.9（`python3`）と 3.12.15（`/usr/bin/python3`）の併存。CI 不在のため CI 版は未確定。
   - What's unclear: 人が workflow を追加する際のランナー版。
   - Recommendation: 実装は両者で成立する stdlib 最小表記に留め（型注釈は `list[tuple[...]]` 等の 3.9+ 記法、3.14 専用機能は使わない）、バージョン横断互換コード（try/except import 等）は書かない。ローカル検証の正は `python3`（3.14.9）。
3. **pyproject.toml の最小形（ビルドバックエンド選択は Discretion）**
   - RESOLVED: CONTEXT.md「Claude's Discretion」の「`pyproject.toml` の最小限の設定内容（ビルドバックエンド選択等）は仕様『最低限のパッケージ設定は許容』の範囲で決定してよい」により決定権は実装側に委譲済み。design.md D-F「`pyproject.toml`（setuptools or hatchling の minimum）…ランタイム依存ゼロ。pytest は開発依存」を受け、PLAN 01-03 Task 3 が setuptools バックエンド最小形（[project] name/version・dependencies = []・pytest は dev 依存のみ・pythonpath 設定不要・1 ファイル集約）として確定済み。
   - What we know: 実行には不要（Pitfall 1）。必要になるのはメタデータ + dev 依存宣言 + 任意の `[tool.pytest.ini_options]`。危険なパスで人の承認対象になり得る。
   - What's unclear: 人が受け入れる最小差分の具体形。
   - Recommendation: setuptools バックエンド + `[project] name/version + dependencies = []` + pytest を dev 依存、の設定 1 ファイルに集約。`pythonpath` 設定も不要（repo 直下実行のため）。差分最小を明示して承認に出す。

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 (CPython) | 実行時（REQ-01〜08） | ✓ | 3.14.9（`python3`）/ 3.12.15（`/usr/bin/python3`） | — |
| pytest | 試験（REQ-07） | ✗（`python3 -m pytest` 不可。`~/.local/bin/pytest` はモジュール欠落の壊れたシム） | — | `uv pip install pytest`（uv 0.13.5 系が利用可 [VERIFIED: command -v uv]） |
| pip | — | 部分可 | venv の python3 には pip モジュール無し [VERIFIED: python3 -m pip → "No module named pip"]。`/usr/bin/pip3` は 3.12 用 23.3.2 | dev 依存導入は uv |
| uv | pytest 導入 | ✓ | `/home/Yuki/.local/bin/uv` [VERIFIED: command -v uv] | — |
| CI workflow（pytest ジョブ） | REQ-07 検証の正 | ✗ | `.github/` 等の CI 設定なし [VERIFIED: リポジトリルート一覧 read] | ローカル `python -m pytest`（Builder/品質の検証用。REQ-07 充足自体は人対応） |
| 外部パッケージ（ランタイム） | — | 不要 | stdlib only（REQ-08） | — |

**Missing dependencies with no fallback:**
- CI の pytest ジョブ（Bot 権限外。task 3.3 の block 判定ルートで人の対応へ）

**Missing dependencies with fallback:**
- pytest（→ `uv pip install pytest`。インストールは dev 依存のみ・Wave 0）

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.2.0（PyPI 最新 [VERIFIED: pip index versions pytest]。未インストール → Wave 0） |
| Config file | none — pyproject.toml の `[tool.pytest.ini_options]` は任意（repo 直下実行なら設定無しでも成立） |
| Quick run command | `python -m pytest tests/test_tokenizer.py -x`（対象ファイル単位） |
| Full suite command | `python -m pytest`（repo 直下で実行。cwd が sys.path に入り `wordfreq` を import 可能 [CITED: docs.python.org/3/using/cmdline.html#cmdoption-m]） |

注意: `pytest` 素のコマンドは既存シムが壊れており使わない。常に `python -m pytest`（対象インタープリタのモジュール解決に従う）。PLAN の検証コマンドは Builder・品質が実在する検証ファイルから実行する（未作成時点の試験ファイルを事前実行しない）。

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-01 | 正常実行/不存在 exit 1/UTF-8 不可 exit 1/引数個数 exit 2/空ファイル exit 0 | CLI 試験（subprocess または main() + SystemExit 検証） | `python -m pytest tests/test_cli.py -x` | ❌ Wave 0（task 3.1） |
| REQ-02 | `--top` 既定 10/指定/全件/不正値 exit 2 | CLI 試験 | `python -m pytest tests/test_cli.py -x`（top 系テスト） | ❌ Wave 0（task 3.1） |
| REQ-03 | text 行書式 `<count>\t<word>`/json 配列 `json.loads` 可読/0 件 `[]` | 単体（formatters）+ CLI | `python -m pytest tests/test_formatters.py tests/test_cli.py -x` | ❌ Wave 0（task 2.2） |
| REQ-04 | 回数降順→単語昇順・決定論 | 単体（aggregator） | `python -m pytest tests/test_aggregator.py -x` | ❌ Wave 0（task 1.2） |
| REQ-05 | 切り出し・casefold・句読点・underscore 固定・日本語決定的 | 単体（tokenizer） | `python -m pytest tests/test_tokenizer.py -x` | ❌ Wave 0（task 1.1） |
| REQ-06 | TextSource 境界越し検証・FileSource 非経由・FileSource 単体（正常/不存在/デコード失敗/空） | 単体 + 境界試験 | `python -m pytest tests/test_sources.py tests/test_sources_boundary.py -x` | ❌ Wave 0（task 2.1 / 2.3） |
| REQ-07 | pytest 一式が通る（CI 本番） | 全 suite | `python -m pytest` | ❌ Wave 0（フレームワーク未導入） |
| REQ-08 | ランタイム依存ゼロ宣言 | 構造検証（pyproject に dependencies 空） | `python -m pytest tests/test_cli.py -x` 経由 + pyproject 読取り確認 | ❌ Wave 0（task 3.2） |

### Sampling Rate
- **Per task commit:** 該当 task の試験ファイル 1 本（例 task 1.1 後は `python -m pytest tests/test_tokenizer.py -x`）
- **Per wave merge:** `python -m pytest`（全 suite。tasks.md の「各 task 時点で pytest 緑」約束と一致）
- **Phase gate:** Full suite green + task 3.3 の CI block 判定結果の記録 before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] pytest 導入 — `uv pip install pytest`（対象インタープリタは Open Question 1/2 の方針により `python3` = 3.14.9。dev 依存のみ・REQ-08 違反なし）
- [ ] `tests/` ディレクトリと `__init__` 無し試験ファイル一式 — 上表 6 ファイル（tasks.md 1.1〜3.1 が作成。conftest.py は現状不要 — 共有 fixture が無い。tmp_path 組み込みで足りる）
- [ ] CI pytest ジョブ — 存在せず。Bot 権限外のため task 3.3 で block 判定の準備（人対応）[VERIFIED: リポジトリに CI 設定なし]

## Security Domain

（config.json `security_enforcement: true`、ASVS level 1、block_on: high に対応）

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | ローカル CLI。認証対象なし |
| V3 Session Management | no | ステートレス |
| V4 Access Control | yes（軽微） | 読み取り対象はユーザーが明示した 1 ファイルのみ。OS のパーミッションが境界（`OSError` → InputError → exit 1） |
| V5 Input Validation | yes | argparse `type=` / `choices=` + `top >= 1`（Pattern 1）。UTF-8 デコード失敗は例外で捕捉（Pattern 2）。自前パースなし |
| V6 Cryptography | no | なし |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| 巨大ファイル読込みでメモリ枯渇 | DoS | design Non-Goal（ストリーミング無し）として受け入れ。CLI でユーザーが選択する入力のため実害低。A-5 範囲 |
| 非 ASCII 語の stdout 注入（端末エスケープ等） | Tampering | text 形式は仕様固定（D-A）。json 側は `ensure_ascii=True`（D-E）で非 ASCII をエスケープし機械可読性を保護 |
| 不正バイト列によるクラッシュ未捕捉 | DoS / Denial | `UnicodeDecodeError` を境界の try/except で `InputError` に正規化（Pattern 2）。traceback を素出ししない |
| トレースバックが exit 1 を偽装（意図しない例外） | Repudiation | `__main__` 側の捕捉は `InputError` 限定。pytest で exit code を直接検証（Pitfall 5） |

## Sources

### Primary (HIGH confidence)
- ローカル CPython 3.14.9 stdlib ソース（`lib/python3.14/argparse.py:2769-2785`、`sed` で範囲 read）— argparse exit(2) の verbatim 検証
- `docs.python.org/3/library/re.html` — `\w` の既定 Unicode / `re.A`、`findall` の左→右最大長（web で page 取得済み）
- `docs.python.org/3/using/cmdline.html#cmdoption-m` — `-m` は cwd を sys.path 先頭に追加（verbatim: "As with the `-c` option, the current directory will be added to the start of `sys.path`"）
- リポジトリ実測（本セッション）: `python3 --version`=3.14.9、`python3 -m pip`=モジュール無し、`pip index versions pytest`=9.2.0、ルート一覧に CI 設定無し、`ls .github` 不在
- 承認済み原本の全文 read（本セッション）: `openspec/changes/r-5a3b8a3f-wordfreq/{proposal,design,tasks}.md`、`specs/wordfreq-cli/spec.md`、`.planning/{REQUIREMENTS,STATE}.md`、`01-CONTEXT.md`、`.planning/argonauts/r-5a3b8a3f-learnings.md`（学習 0 件確認済み）
- GSD 公式 CLI（本セッション）: `init.phase-op 1`（phase_dir/has_research=false 確認）、`graphify status`（disabled → graph コンテキスト無し）、`research-plan` / `research-store put`（4 ダイジェスト cached）、`package-legitimacy check --ecosystem pypi pytest`（SUS）、`classify-confidence`（provider tier）

### Secondary (MEDIUM confidence)
- `docs.python.org/3/library/collections.html#collections.Counter.most_common` — 同数順序不定の記載（CITED。most_common 非使用判断の根拠）
- pytest 最小構成（docs.pytest.org 系統 + websearch digest）— 設定必須なし・`python -m pytest` 運用

### Tertiary (LOW confidence)
- argparse の負数オプション語彙が無いパーサでの `--top -1` 値解釈（既知挙動だが本セッションで実機未実行 → Assumptions A1）

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stdlib 標準機能のみ。exit(2) はローカルソースで verbatim 検証。pytest 版数は PyPI 実測
- Architecture: HIGH — 承認済み design.md D-A〜F がそのまま実装仕様に近い（部品 4+1 分割はCONTEXT・STATE でロック済み）。追加判断は argparse/Counter の既定挙動の選択のみ
- Pitfalls: HIGH（大半は spec×実測の交差）／A1 のみ LOW
- Validation: HIGH（Wave 0 ギャップは実測に基づき列挙済み）

**Research date:** 2026-11-17
**Valid until:** 2026-12-17（stable な stdlib 知識ベース。ただし CI 状況は変更の可能性が高く、task 3.3 実行時に再確認）
