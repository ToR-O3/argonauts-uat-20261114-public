# Phase 08: wordfreq exclude-file — 既存コード再利用パターン

**Mapped:** 2026-11-28（terminal `date +%F`）
**Files analyzed:** 主要変更候補5ファイル＋工程原本2項目
**Analogs found:** 主要5 / 5、工程2 / 2（証拠文書の配置は未固定）

本書は実装前の対応表である。抜粋は実在する現行コードであり、除外機能の実装例・合格結果ではない。製品・試験・PLAN・設定・OpenSpecチェックは変更していない。

## File Classification

CONTEXT D-01〜08、およびRESEARCH「Component Responsibilities / 最小変更候補」（150〜157行）から抽出した主要候補。既存ファイル自身の最寄りの関数・試験をanalogにすることで、別方式の導入を避ける。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `wordfreq/__main__.py` | controller / CLI composition | argv → file-I/O → transform → stdout | 同ファイル `build_parser`, `main` | exact |
| `wordfreq/sources.py` | utility / 入力境界 | file-I/O → text、例外正規化 | 同ファイル `FileSource.read_text` | exact（取得境界）。除外行文法そのものは新規 |
| `README.md` | documentation | 利用者の入力 → 実CLI再現例 | 同ファイル min-count構文・契約説明 | exact |
| `tests/test_sources.py` | test | 実file-I/O / monkeypatch → 集合・例外・入力不変assert | 同ファイル UTF-8・原因連鎖試験 | exact |
| `tests/test_cli.py` | test | subprocess request-response / composition spy | 同ファイル min-count・全形式・順序・バイト検査 | exact |

CONTEXT D-05/D-07とRESEARCH Wave 0 Gaps / Planning Implicationsから抽出した工程項目は主要変更と区別する。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `openspec/changes/r-6442a149-exclude-file/tasks.md` | workflow / 完了記録 | 実装・証拠 → task状態 | 同ファイル 2.1 / 2.2 / 3.1 | exact |
| Phase08の `VERIFICATION.md` 等の文字証拠原本（配置未固定。慣例候補 `.planning/phases/08-wordfreq-exclude-file/08-VERIFICATION.md`） | verification / documentation | 対象head・argv・入出力・exit → 条件別結果 → 独立品質引渡し | `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md` の対象head・Truth/Evidence表 | role-match。旧受入内容・判定はコピー禁止 |

証拠原本の候補名は本書での配置案であって、CONTEXT/RESEARCHが固定した新ファイル名ではない。新検証ツール・fixture・conftest・依存設定を追加する必要は原本から導けない。

## Pattern Assignments

### `wordfreq/__main__.py`（controller、file-I/O / transform）

**Analog:** `wordfreq/__main__.py:2-19,22-54`。同じCLIでmin-countを組み込んだ現行処理が最も近い。

**Imports pattern**（2〜10行）:

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

標準ライブラリと相対importを維持し、除外取得も入力境界からimportする。新API名・型は本書では固定しない。

**Validation / I/O / error pattern**（23〜33行）:

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

ここでは本文失敗がexit1である。全引数検証の後、本文のtryより前へ採用除外FILEの取得を置く対応が適する。除外側だけ同じstderr出力形式でexit2にする。単一catchへ統合して本文までexit2にしない。`build_parser:15-18` の `add_argument` に文字列パスの保存を追加する候補とし、parse中に開くFileType・I/Oするtype・全FILEを読むappend方式は避ける。最後FILEのみ採用する具体処理は新実装として試験が必要。

**Core selection pattern**（34〜48行）:

```python
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count})
    pairs = top_words(selected_counts, args.top)
    if args.format == "html":
        # argv uses filesystem surrogateescape; HTML needs displayable Unicode.
        basename = os.fsencode(os.path.basename(args.filename)).decode(
            sys.getfilesystemencoding(), errors="replace"
        )
        output = format_html(pairs, basename, total)
    elif args.format == "json":
        output = format_json(pairs)
    else:
        output = format_text(pairs)
```

再利用点は共通counts→total→min-count→top→pairs。変更はcasefold済み列の所属判定フィルタを計数直前へ接続する。setは所属判定だけに使い、setから出力順を作らない。HTML総数は除外後のcountsから選択前に取得するため、formatterへ除外一覧や新引数を渡す必要はない。

**Output pattern**（49〜54行）:

```python
    if args.format == "html":
        # The document declares UTF-8, independently of the terminal locale.
        sys.stdout.buffer.write(output.encode("utf-8"))
    else:
        sys.stdout.write(output)
    sys.exit(0)
```

全取得・計算成功後に一度出力する既存境界を維持する。失敗前の部分stdoutを追加しない。

### `wordfreq/sources.py`（utility、file-I/O）

**Analog / core / errors:** `wordfreq/sources.py:13-22`:

```python
class FileSource:
    def __init__(self, path: str) -> None:
        self._path = path

    def read_text(self) -> str:
        try:
            with open(self._path, "r", encoding="utf-8") as source:
                return source.read()
        except (OSError, UnicodeDecodeError) as error:
            raise InputError(f"{self._path}: {error}") from error
```

`with open`で読取り、対象パスと原因を含むInputErrorへ `from error` で連鎖し、exit判断はしない構造を再利用する。既存 `InputError` は5〜6行、`TextSource` Protocolは9〜10行にある。Protocolを除外集合用に無理に変更しない。

**差分境界:** 本文 `FileSource` のUTF-8指定は保持する。除外専用の小さい読込関数等でUTF-8-sig→行strip→空/先頭#無視→行全体casefold集合を実装する候補。本文tokenizerの流用、途中#のコメント化、記号分割、全行のBOM除去は行わない。行文法に完全一致する既存関数はなく、下記「No Analog Found」に明記する。

### `README.md`（documentation、実CLI再現）

**Analog:** `README.md:9-23,27-40`。構文例→箇条書きの値・順序・空・エラー契約→部品契約、の並びを利用する。

**既存の実行例**（15〜17行）:

```sh
python -m wordfreq input.txt --min-count 3
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
```

**説明様式**（27〜28行）:

> - `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
> - `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。

同じ箇所へ `--exclude FILE` 構文と本文/一覧の具体内容を示し、実CLIで再現できる例を追加する。helpにも行規則・casefold・最後FILE・読込失敗exit2・空結果を反映する（CLI側の変更）。34行の既存「読込み失敗exit1」は本文と除外を区別する必要がある。32/40行の総数説明は除外後かつmin-count/top前と明確にし、未指定の総数契約は維持する。無関係な末尾注記やブラウザ手順を再設計しない。

### `tests/test_sources.py`（test、file-I/O / 原因連鎖）

**Analog:** `tests/test_sources.py:7-18,21-43,46-80`。module先頭は `import importlib.util` と `import pytest`、対象部品は各test内でimportする。

**入力バイト不変**（11〜18行）:

```python
    path = tmp_path / "input.txt"
    data = "Hello 日本語\nStraße\n".encode("utf-8")
    path.write_bytes(data)
    source: TextSource = FileSource(str(path))
    assert callable(source.read_text)
    assert source.read_text() == data.decode("utf-8")
    assert path.read_bytes() == data
    assert sorted(p.name for p in tmp_path.iterdir()) == ["input.txt"]
```

除外読込では返値を集合へ変更した新assertが必要。CLI結果だけで済ませず空文字・コメントが集合に入らないこと、行内の空白/記号が残ることを固定集合との比較で確認する。BOM・LF/CRLF・最終改行なし、Straße/STRASSE、重複について入力bytesを明示する。

**原因連鎖とopen呼出し**（67〜80行）:

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

原因例外のidentity確認と対象/原因の部分一致を再利用する。末尾のutf-8 assertは本文の既存契約であり変更しない。除外専用側には別のcodec期待値を置く。21〜52行の不存在・decode・ディレクトリ例も同じ例外分類の最寄りである。

### `tests/test_cli.py`（test、subprocess / composition spy）

**Analog:** `tests/test_cli.py`。新ツールではなく既存ヘルパーとパラメータ化を利用する。

**Imports / 実CLI**（2〜11行はjson、HTMLParser、os、Path、shutil、subprocess、sys、tomllib、pytest）。bytes helperは418〜422行:

```python
def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
```

**全形式共通assertの呼出し**（705〜708行）:

```python
    result = run_cli_bytes(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format,
                        expected[:10 if top is None else top], path.name, total)
```

`assert_output_bytes:425-441` はtext/JSON/HTMLの順序、strict UTF-8、改行、basename、総数を検査する。`CLIHTML:201-239` を再利用しHTMLを文字列splitしない。`test_min_count_selection:686-708` の全形式×入力×top等の構造を除外入力へ適用する。期待pairs/totalは要求の固定値を与え、製品関数で期待値を再計算しない。

**引数検証前I/O禁止**（629〜644行）:

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
    real = run_cli_bytes(tmp_path / "missing", "--format", output_format, *options)
    assert real.returncode == 2 and real.stdout == b""
    assert b"--min-count" in real.stderr and b"Traceback" not in real.stderr
```

除外と本文の両境界をspyし、パス付き呼出し履歴へ拡張する。CLIにimportされた関数の参照をpatchする先例は759〜786行。除外→本文の厳密な二入力順序、前FILE未読、count_wordsへ渡る列からの計数前除外は新assertで補う。既存例がそれを既に保証するとは扱わない。

**その他の再利用箇所（同ファイル）:**

- 503〜527行: 不存在/ディレクトリ/decode/permission×全形式。permissionは実効ユーザーで `pytest.raises(PermissionError)` を確認しfinallyでfixtureのmodeを戻す。除外版はexit2、本文版exit1を保つ。製品による権限変更は追加しない。
- 672〜682行: `--help`、README中のコマンド文字列、同じ入力での実CLI再現を一体で検査。
- 711〜741行: 全件なしのtext `b""`、JSON `b"[]\n"`、HTML空表と既存案内。除外版には総数0、min-countのみで全件なしには旧総数を期待する。
- 744〜756行: PYTHONHASHSEEDを変えたstdout bytes比較。set由来の出力順変動を検出する形として利用。
- 759〜793行: top/formatter spyで同じpairsとmetadataを検査。新count spyではiteratorを消費して除外済み列そのものを確認する必要がある。
- 796〜817行: 保存済み未指定bytes比較。既存baselineを上書き・再収集しない。
- 153〜189行: 入力/作業tree不変、製品依存なし。新入力は本文と除外一覧の両方のbytes不変を確認する。

### 工程原本（workflow / verification）

**Tasks analog:** `openspec/changes/r-6442a149-exclude-file/tasks.md:7,11-16`。現状は `1.1` のみ完了、`2.1`・`2.2`・`3.1` は未完。11行は正常・行・Unicode・総数・説明、12行は異常・順序、16行は統合回帰と文字証拠を条件にする。完了条件を変更せず、後続実行の事実と証拠が揃った項目だけ記録する。mapping工程では変更しない。

**証拠原本analog:** `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md:60-68,122-136,142-152`。既存の記録形は次の表ヘッダ（131〜132行）:

```markdown
| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
```

要求と証拠の対応は144〜145行:

```markdown
| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
```

形だけを再利用し、今回のhead/実行者/環境/本文・一覧入力/argv/stdout・stderr/exit/REQ-28〜35・EX-1〜6・HTML-2の条件別結果を実行後に記録する。旧frontmatterのpassedと本文human_neededの相違や、旧実測値・対象headを継承しない。未実施は未実施とし、Builderのgreenと独立品質の結果を分離する。今回PMへ画像・圧縮物の閲覧を要求しない。画像が生じた場合は品質本人の実閲覧内容・枚数・結果を文字原本へ記録する。

## Shared Patterns

### 順序保持の純粋部品をそのまま使う

**Source:** `wordfreq/tokenizer.py:14-18`、`wordfreq/aggregator.py:6-17`。**Apply to:** CLIの計数前フィルタと試験期待値の境界。

```python
# wordfreq/tokenizer.py:18
    return (token.casefold() for token in tokenizer(text))

# wordfreq/aggregator.py:6-8
def count_words(tokens: Iterable[str]) -> Counter[str]:
    """Count a token iterable without acquiring text."""
    return Counter(tokens)

# wordfreq/aggregator.py:17
    return sorted(counts.items(), key=lambda wc: -wc[1])[:n]
```

上記は独立抜粋で実行ファイルではない。本文tokenizerは `\w+`（同6行）を維持。casefoldをlowerへ変更せず、Counterの挿入順と回数だけの安定ソートを維持する。語昇順やset順を導入しない。tokenizer/aggregatorは原則変更対象外。

### formatterは取得・除外を知らない

**Source:** `wordfreq/formatters.py:6-27,34-38`。**Apply to:** CLI接続・README・全形式試験。

```python
# wordfreq/formatters.py:17-19
def _html_text(value: str) -> str:
    """Escape once, protecting CR from HTML's input newline normalization."""
    return escape(value, quote=True).replace("\r", "&#13;")
```

`format_html:22-27` はpairs/basename/totalだけを受け取りI/O・再集計・ソートなし。34〜38行は既存空案内を選択する。CLIのtotal接続だけを変更候補とし、CSS・明背景・escape・basename限定・空案内は維持する。formattersも原則変更不要。

### 診断と安全性

認証/guard/DB/ネットワークのanalogは不要（ローカルCLI）。OS既存権限でread-only取得し、取得境界で原因連鎖、CLIでstderrとexitを決める。本文のInputError→1と除外のInputError→2を分離する。追加依存・外部送信・製品chmodを導入しない。

### 検証の実在性と旧工程の非転用

Builder・品質は新assertを実ファイルへ追加してから実行する。本mappingでは機能試験・pytestを実行しない。既存検証対象は `tests/test_sources.py`、`tests/test_cli.py` と既存全suite。未作成node-id、専用検証scriptを実行前提にしない。

`docs/wordfreq-html-verification.md:16-24` の旧scopeは固定baselineと本文source変更禁止等を含み、今回のsources.py変更を伴う受入へそのまま転用できない。同文書52行の入力/argv/bytes/exit保全の考え方だけ参照可能。旧phase1/3/4/5/7を再検証・変更しない。

## No Analog Found

ファイル全体でanalogがない主要候補はない。ただし次の機能単位は新規であり、既存コードをそのままコピーするだけでは要求を満たさない。

| 対象 | Role | Data Flow | 不足と補完根拠 |
|---|---|---|---|
| sources.py内の除外一覧パーサ | utility | UTF-8-sig file → 行 → casefold集合 | 本文読込はあるがBOM/strip/先頭#のみ無視/行非分割の実装なし。CONTEXT D-02/D-03、設計AD-3、RESEARCH Pattern 2に従う |
| __main__.pyとCLI試験の二入力優先制御 | controller / test | argv → 最後除外FILE → 本文 → 計数 | 一入力の前検証はあるが二入力順序と最後FILE未読保証なし。CONTEXT D-01/D-04、AD-4を直接spy＋実CLIで追加 |

## Metadata

- **原本:** `08-CONTEXT.md`、`08-RESEARCH.md`全文、承認設計 `architecture.md`、同OpenSpec `tasks.md` を読了。
- **analog探索範囲:** `wordfreq/`、`tests/`、`README.md`、OpenSpecの同変更、既存phase検証原本、`docs/wordfreq-html-verification.md`。
- **追跡確認:** 本書でanalogとして採用した既存ファイルは `git ls-files -- ...` の出力で追跡済みと確認。gitignored install/runtime mirrorを採用していない。主要な強い一致はCLI/source/README/その2試験の5ファイルで探索を止めた。共有境界と工程文書は補助参照。
- **追加指示/skill:** repo直下 `HERMES.md` と `.hermes/HERMES.md` はread_fileでnot_found。`.hermes/skills/` と `.agents/skills/` も存在せず。追加agent skillsの公式query空という依頼結果を採用し再設定しない。
- **公式判定:** 指定runtime launcherをsourceした同一terminalの `gsd_run query init.phase-op 8` がphase08存在、has_context=true、has_research=true、has_plans=false、plan_count=0を返した。commit_docs=trueでも今回commit禁止を優先。
- **既存dirty:** 開始時点で既存planning文書・研究/UI/validation等に差分あり。それらを変更・復元しない。
- **本工程の書込:** この `08-PATTERNS.md` のみ。機能/既存試験実行、製品/試験/PLAN/設定変更、commit/push/Kanbanなし。
