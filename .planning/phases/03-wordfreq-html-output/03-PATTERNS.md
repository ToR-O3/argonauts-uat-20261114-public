# Phase 3: wordfreq HTML output - Pattern Map

**Mapped:** 2026-11-17 (JST)
**Files analyzed:** 15 targets (13 create/modify candidates + 2 unchanged regression targets)
**Analogs found:** 14 / 15 (exact 10, role-match 3, partial/data-flow-match 1, no analog 1)

## Scope and Authority

- 対象は r-50053edc / Phase 03 のみ。03-CONTEXT.md、03-RESEARCH.md から対象を抽出し、承認済み OpenSpec proposal/design/tasks/spec、同依頼 BMAD Brief/PRD、learnings、INGEST-CONFLICTS、03-UI-SPEC.md を読んで境界を照合した。
- 公式 CLI `node /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/gsd-core/bin/gsd-tools.cjs query init.phase-op 3` は phase_found=true、phase_number=03、phase_slug=wordfreq-html-output、has_context=true、has_research=true、has_plans=false を返した。
- ルート HERMES.md は探索で未検出、プロジェクト `.hermes/skills` / `.agents/skills` は存在しない。独自規約を補わない。
- 以下の既存 analog はすべて、この worktree の `git ls-files` 出力に含まれる追跡済みファイル。インストールミラー、他依頼の Phase 2、過去 PLAN は analog としない。
- exact は同一責務・同一データフローの既存ファイルを指し、要求された新機能が既に実装済みという意味ではない。NEW パスは研究で提案された名称であり、作成済みと扱わない。

## File Classification

| New/Modified File | Disposition | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|---|
| `wordfreq/aggregator.py` | modify | service | batch / transform | 同ファイル :6-13 | exact |
| `wordfreq/formatters.py` | modify | utility | transform | 同ファイル :5-13 | exact |
| `wordfreq/__main__.py` | modify | controller | file-I/O / request-response | 同ファイル :11-32 | exact |
| `tests/test_aggregator.py` | modify | test | batch / transform | 同ファイル :17-42 | exact |
| `tests/test_formatters.py` | modify | test | transform | 同ファイル :7-46 | exact |
| `tests/test_cli.py` | modify | test | subprocess / file-I/O | 同ファイル :15-19,63-180 | exact |
| `tests/test_sources.py` | modify if permission coverage needed | test | file-I/O | 同ファイル :21-52 | exact |
| `tests/test_tokenizer.py` | regression-only; preserve | test | transform | 同ファイル :6-60 | exact |
| `tests/test_sources_boundary.py` | regression-only; preserve | test | file-I/O / transform | 同ファイル :7-42 | exact |
| `README.md` | modify | utility (documentation) | static reference | `CONCEPTS.md` :45-51 | role-match |
| `CONCEPTS.md` | modify current ranking entry | utility (documentation) | static reference | 同ファイル :37-51 | exact |
| `tools/verify_wordfreq_html.py` | proposed NEW | utility | subprocess / file-I/O / event-driven | `tests/test_cli.py` :15-19,152-180 | partial/data-flow-match |
| `tools/wordfreq_html_geometry.js` | proposed NEW | utility | DOM measurement / transform | none | none |
| `tests/test_html_verifier.py` | proposed NEW | test | transform / evidence validation | `tests/test_formatters.py` :18-46 | role-match |
| `docs/wordfreq-html-verification.md` | proposed NEW | utility (documentation) | static reference | `CONCEPTS.md` :5-19,49-51 | role-match |

`wordfreq/sources.py` は変更対象ではなく、入力例外境界の読み取り参照。tokenizer/source boundary の 2 試験は実行対象として分類したもので、製品変更を要求しない。

## Pattern Assignments

### `wordfreq/aggregator.py` — shared counting/ranking

**Analog:** `wordfreq/aggregator.py:1-13`。標準ライブラリ、型付き純粋関数、入力取得なし。

```python
from collections import Counter
from collections.abc import Iterable


def count_words(tokens: Iterable[str]) -> Counter[str]:
    """Count a token iterable without acquiring text."""
    return Counter(tokens)
```

既存の変更箇所（:11-13）:

```python
def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    """Return up to n pairs by descending count, then ascending word."""
    return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]
```

**Copy / change:** Counter と sort-then-slice の責務は保持。ただし語昇順キーと docstring はコピー禁止の旧契約。承認 design.md:11 に従い回数のみの安定ソートへ変更し、counts 挿入順が正規化後初出順である前提を記録する。HTML 専用ソート、集合経由再構築、後の出現で初出位置を更新する処理を追加しない。

### `wordfreq/formatters.py` — pure HTML string renderer

**Analog / concrete core:** `wordfreq/formatters.py:1-13`。

```python
"""Pure output formatting; callers own writing and exit decisions."""
import json


def format_text(pairs: list[tuple[str, int]]) -> str:
    """Format count-first tab-separated lines, or nothing for no pairs."""
    return "".join(f"{count}\t{word}\n" for word, count in pairs)
```

既存 JSON の :12-13 は `items = [{"word": word, "count": count} for word, count in pairs]` → `return json.dumps(items, ensure_ascii=True) + "\n"`。受け取った順を維持して文字列だけ返す方式をコピーする。新 HTML は pairs/basename/total を受け取り、再読込み・再集計・再ソート・stdout/exit を行わない。既存 text/json シグネチャと空形式は変えない。

**New concern, not existing code:** `html.escape(..., quote=True)` による動的テキストの一度だけの escape。既存 HTML/CSS renderer はない。固定タグ・CSS・タイトル、独立した basename 値ノード、意味的 table、3 見出し、空 tbody は 03-UI-SPEC.md:36-54,108-126 を規範とする。CSS 寸法・色・書体は同書の値を使い、別デザインを発明しない。

### `wordfreq/__main__.py` — composition, validation and output ownership

**Imports analog:** `wordfreq/__main__.py:2-8` は標準ライブラリの後に `.aggregator` / `.formatters` / `.sources` / `.tokenizer` の相対 import。

**Validation / errors / core** (`wordfreq/__main__.py:21-32`):

```python
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    try:
        text = FileSource(args.filename).read_text()
    except InputError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
    pairs = top_words(count_words(iter_tokens(text)), args.top)
    output = format_json(pairs) if args.format == "json" else format_text(pairs)
    sys.stdout.write(output)
    sys.exit(0)
```

`build_parser` :11-16 の argparse choices/default を拡張する。単一読込みと exit/stderr 境界をコピーし、counts を保持→top前 total→共通 top_words→形式 dispatch とする。basename は CLI でホスト規則に従って取得し HTML にだけ渡す。上記一行合成・二分岐は拡張点であり、そのまま維持する指定ではない。

### `tests/test_aggregator.py` — ordered-pair contracts

**Analog** `tests/test_aggregator.py:20-23`:

```python
    counts = Counter({"zoo": 5, "rare": 1, "middle": 3, "apple": 5})
    original = counts.copy()
    assert aggregator.top_words(counts, 3) == [("apple", 5), ("zoo", 5), ("middle", 3)]
    assert counts == original
```

fixture→明示した順序付き pairs→非破壊検査の形をコピーするが、上記期待値は旧語昇順なので更新必須。:26-33 の top1/2/oversized/empty、:36-42 の巨大整数を残す。Counter 等値だけでは順序を検査できないため keys/items の順も確認し、正規化入力経路、後の再出現、異なる頻度を加える。

### `tests/test_formatters.py` — exact output, roundtrip, nonmutation

**Analog** `tests/test_formatters.py:21-28`:

```python
    pairs = [("hello", 10**100), ("world", 1)]
    output = formatters.format_json(pairs)
    assert json.loads(output) == [
        {"word": "hello", "count": 10**100}, {"word": "world", "count": 1}
    ]
    assert output.endswith("\n")
    assert output.count("\n") == 1
    assert pairs == [("hello", 10**100), ("world", 1)]
```

標準 parser で意味を戻して比較する方式を HTMLParser ベースへ拡張する。既存 text の :11-15 と JSON の :31-46 はそのまま回帰対象。HTML parser/static allow-list は新規設計であり既存にはない。直接 `& < > " '` とタグ/イベント候補を与え、元テキスト一致、余分なタグ/属性/実行・外部経路なし、empty0行を検査する。escape 文字列が含まれることだけでは合格にしない。

### `tests/test_cli.py` — real subprocess and cold-copy regression

**Analog / helper** `tests/test_cli.py:15-19`:

```python
def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, timeout=10,
    )
```

argv 配列・明示 cwd・分離した streams・timeout をコピーする。HTML の保存 bytes/strict UTF-8 は text=True だけでは検証できないため bytes 経路を加える。:22-60 の lexical 期待値は初出順へ置換する。:63-134 の exit1/2・空 stdout・Traceback不在、:137-149 の空 text/json と明示 text は維持し、html を含むケースへ拡張する。

**Cold-copy baseline** `tests/test_cli.py:160-162`:

```python
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    # Track the baseline so content changes show up, not just new paths.
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
```

:152-180 の cold package / 独立 repo / before-after status / 元 bytes 検査を HTML にも使う。これは試験内の隔離 repo の方式であり、計画担当に本 worktree の stage/commit を許可するものではない。:183-189 の依存宣言検査を壊さず CI/依存を変更しない。

### `tests/test_sources.py` — permission error coverage candidate

**Analog** `tests/test_sources.py:39-43`:

```python
    with pytest.raises(InputError) as caught:
        FileSource(str(path)).read_text()
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)
    assert str(path) in str(caught.value)
    assert path.read_bytes() == data
```

例外型・cause・入力非破壊を検査する形を PermissionError に使う。既存 :46-52 は directory/OSError であり permission denial の証拠ではない。monkeypatch 単体と実効権限での CLI 拒否を区別し、chmod が効かない環境で実拒否を合格としない。製品側の analog `wordfreq/sources.py:17-22` は OSError/UnicodeDecodeError を InputError へ chaining し、exit を所有しない。

### `tests/test_tokenizer.py`, `tests/test_sources_boundary.py` — preserve and execute

**Analogs:** 同ファイル。tokenizer :10-12 は casefold と入力順、:18-29 は句読点/underscore/digit、:35-38 は CJK、:48-60 は差替え後 casefold。これらは HTML 追加のため緩めない。

**Boundary concrete guard** `tests/test_sources_boundary.py:15-17`:

```python
    monkeypatch.setattr(FileSource, "read_text", spy)
    assert count_words(iter_tokens("Hello hello WORLD")) == {"hello": 2, "world": 1}
    assert calls == []
```

同 :29-42 は source の単一 read を検査する。新 formatter/aggregator に I/O を混ぜない根拠として使う。

### `README.md`, `CONCEPTS.md`, `docs/wordfreq-html-verification.md`

**Analog:** `CONCEPTS.md:45-51` の `## 決定論的順位` / `## 決定論的再実行` と、:5-19 の head・独立証跡・verdict・判別力という見出し＋短い契約本文の形式。

既存 :47 の「頻度の降順、同一頻度では語のコードポイントの昇順」は更新対象でありコピーする仕様ではない。:51 の `PYTHONHASHSEED` を変えた再実行の原則は維持する。README は現在 :1-3 のタイトル/説明しかなく使用例の analog はないため、標準 Markdown の役割だけを参考にする。HTML 出力/保存例、意図した全形式の互換性変更を追記する。

新 verification guide には実在する検証ファイルの正確な起動法、環境、固定 fixture、両幅、raw geometry、独立再生成、画像閲覧台帳、通信観測の開始/終了と review/finalization 境界、未実施時の扱いを記録する。既存 glossary はブラウザ手順の実装 analog ではない。

### `tools/verify_wordfreq_html.py` — partial analog only

**Analog:** 上記 `tests/test_cli.py:15-19` と :152-180。実 CLI を argv 配列で起動し exit/stdout/stderr と原本を保存する部分だけコピー可能。pytest helper の text=True・固定10秒・テスト ROOT を無検討に流用しない。

**No existing browser collector:** Python ソースの `playwright|HTMLParser|getClientRects` 検索は該当なし。ブラウザイベント、CDP、raw geometry、manifest、review待機/最終検査、環境不足の fail-closed は新規責務。03-RESEARCH.md:268-280 と UI-SPEC :134-183 を設計規範にし、既存成功済み仕組みと表現しない。Playwright は実行環境側のみ、通常 pytest collection で import 必須にしない。

### `tests/test_html_verifier.py` — test role-match only

**Analog:** 上記 `tests/test_formatters.py:21-28,38-46` の明示データ→構造/値/完全性 assertion。ブラウザ不要の deterministic records で predicate/manifest の欠損・空ケース・横 overflow・clip・隣接 overlap・失敗通信試行を検出する。own element の縦を越えるが clip/重複しない valid record は誤拒否しない。browser unavailable や未閲覧画像を pass にしない。既存 suite に geometry/manifest 専用の判別試験はない。

## Shared Patterns

- **責務と I/O:** `wordfreq/formatters.py:1,5-13` と `tests/test_sources_boundary.py:7-42`。取得は source、集計/整形は pure、書込み/終了は CLI。検証 tool の evidence I/O と製品の無書込みを混同しない。
- **Validation/error:** `wordfreq/__main__.py:11-28` の argparse positive top/choices と source exception mapping。`wordfreq/sources.py:21-22` の `raise InputError(...) from error`。HTMLエラー画面を追加しない。
- **順序:** `wordfreq/aggregator.py:6-13` の共有パイプラインを全形式で使う。ただし lexical key は承認変更のため削除対象。歴史的 Phase 1 記録を新仕様に改変しない。
- **安全性:** 既存 auth/session/web middleware は不要。新しい保護は HTML text escape、basename-only privacy、静的外部経路検査、文書起因の失敗を含む通信試行観測。標準 escape/API を使い独自 encoding を作らない。
- **試験形式:** 標準 imports、pytest 関数、tmp_path/monkeypatch、明示期待値、subprocess argv 配列。文字列/構造/exit と streams をそれぞれ検査し、空 manifest や skipped browser を成功にしない。
- **UI/evidence:** UI-SPEC の 1280×900 / 320×900、DPR1、固定 long/whitespace/multi-digit fixtures を使う。原本 float/空 Range/全祖先を保持し、判定結果を別記する。画像の実閲覧は自動存在確認で代用しない。観測は開く前から実際の確認終了まで継続する。
- **Sequencing:** NEW ファイルは作成後に Builder/品質が repo root から実行する。計画段階では未作成コマンド・製品試験・ブラウザ受入を実行しない。各 PLAN は順次積み上げ、前の検証も含め、後の未作成 artifact に依存しない。

## No Analog Found

| File | Role | Data Flow | Reason / fallback |
|---|---|---|---|
| `tools/wordfreq_html_geometry.js` | utility | read-only DOM measurement / transform | geometry filename 探索と Python 内容検索に該当なし。既存 DOM/Range collector なし。UI-SPEC :165-172 と RESEARCH :274-276 の raw Element/Range・文字位置・全祖先・computed overflow 契約に従い新設する。検証側から実ファイルを読む方式で、製品HTMLへ script を挿入しない。 |

partial/role-match は不足を隠さない。HTML renderer の escape/semantic CSS、HTML parser、browser/network collector、manifest/review finalization も既存コードからそのまま得られる実装ではなく、承認仕様と研究から補う必要がある。

## Metadata

**Analog search scope:** tracked `wordfreq/`, `tests/`, root Markdown; repository filename/content discovery. Existing first-party Python source があるため framework 不在を理由に mapping を skip しない。
**Primary concrete analogs:** `wordfreq/aggregator.py`, `wordfreq/formatters.py`, `wordfreq/__main__.py`, `tests/test_cli.py`, `tests/test_formatters.py` (5 strong sources; その他は対象自身の regression/documentation/source-boundary grounding)。
**Target files read:** 11 existing targets; 4 proposed NEW targets remain uncreated. Supporting source `wordfreq/sources.py` and approved scope/UI documents also read.
**Verification performed:** tracked-file gate via `git ls-files`; official Phase 3 query; file reads and analog searches. PATTERNS.md のみを新規作成。製品/試験編集、test/browser実行、commit/push、Phase 2 再利用なし。
**Execution risks carried forward:** default Python の package discovery、Chromium互換性/観測能力、実 permission denial、全画像閲覧と observation window は研究で未検証。mapping 完了は製品受入合格ではない。
