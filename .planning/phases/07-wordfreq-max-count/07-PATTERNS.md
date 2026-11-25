# Phase 7: wordfreq max-count - Pattern Map

**Mapped:** 2026-11-25
**Files analyzed:** 3 concrete modification targets + 3 implied support artifact groups (names pending planner)
**Analogs found:** 6 / 6 targets/groups; 5 primary analog files
**Source HEAD:** `e627dfb4fb57298b65012c07c8e7e9147b695a45`

本書は既存コードの類例対応であり、PLAN・実装・試験結果・独立品質合格ではない。CONTEXT D-01〜08、RESEARCHのminimal touch surface / Wave 0 gaps、承認原本 `.planning/argonauts/r-d4bcda40-prd.md:198–210` から対象を抽出した。support artifactの具体名は未決であり、存在する検証CLIとして扱わない。

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `wordfreq/__main__.py`（変更） | controller / composition | argv → file-I/O → transform → stdout/exit | 同ファイルのmin-count登録・共通選択 | exact |
| `tests/test_cli.py`（追加のみを基本） | test | subprocess request-response / bytes file-I/O / monkeypatch | 同ファイルのmin-count試験・保存bytes試験 | exact |
| `README.md`（直接関連更新と新例1つ） | documentation | command → input/output contract | 同ファイルのmin-count例と説明 | exact |
| max専用採取・検証ファイル（新規、具体pathはplannerが決定） | utility | batch CLI → bytes/JSON → browser evidence | `tools/verify_wordfreq_min_count.py` | role-match; lifecycle参考、依頼契約は不一致 |
| max専用品質手順・文字証拠文書（新規、具体pathはplannerが決定） | documentation / verification | head/CLI/browser evidence → AC/REQ report | `docs/wordfreq-min-count-verification.md` | role-match; 今回の仕様へ再対応が必要 |
| 今回の固定oracle・入力fixture・証拠索引（新規、具体pathはplannerが決定） | test fixture / evidence | literal input → captured bytes/exit/env → read-only comparison | `tools/verify_wordfreq_min_count.py:23–114,191–260` の採取形式 | role-match; 旧原本は不変参照のみ |

「exact」は同じ責務とデータフローへの局所拡張を指し、maxが実装済みという意味ではない。追加の支援試験が必要なら同一test責務として既存CLI試験型へ対応させ、具体path・作成taskをPLANで確定する。`VERIFICATION.md` とCLI/CI文字証拠はフェーズ検証への引継ぎ対象である。

上表のprimary analogはすべて `git ls-files -- <path>` の非空出力を確認済み。install/runtime mirrorは類例に採用しない。

## Pattern Assignments

### `wordfreq/__main__.py` (controller, file-I/O → transform)

**Analog:** 同ファイル（58行）。stdlibと相対部品importを継承する（2–10行）。新依存・新部品APIは不要。

**Imports pattern** (`wordfreq/__main__.py:2–10`):
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

**Parser pattern** (`wordfreq/__main__.py:14–19`):
```python
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-count", type=int, default=1)
    parser.add_argument("--format", choices=["text", "json", "html"], default="text")
    return parser
```

コピーするのは `type=int` / argparse既定helpの方式。maxだけは承認design:21の `default=None` と整数全域受理であり、既存min/topの正値制約をコピーしない。

**Error handling / pre-I/O validation** (`wordfreq/__main__.py:23–33`):
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

非整数/欠落はargparseのexit2、既存min/top不正値も読込み前exit2。max0/負数/逆転から入力取得を短絡せず、入力失敗exit1を保持する。

**Core transform pattern** (`wordfreq/__main__.py:34–38`):
```python
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count})
    pairs = top_words(selected_counts, args.top)
```

既存の別Counter生成位置だけへ包含AND上限を追加する。`counts.items()`の順序、元Counter、元totalを保持し、全formatter分岐より前に一度だけ選択する。条件の原文は `openspec/changes/r-d4bcda40-max-count/design.md:22` の `count >= min_count` かつ `max_count is None or count <= max_count`。この文は将来差分の契約であって現行コード引用ではない。

**Output boundary:** 同ファイル39–53行。HTMLはbasenameをfilesystem encodingで表示用復号し `format_html(pairs, basename, total)`、JSON/textも同じpairsを受ける。HTMLだけUTF-8 bytesをbufferへ書く既存分岐を変更しない。Auth/guardは該当なし（ローカルCLI、認証境界を追加しない）。

### `tests/test_cli.py` (test, subprocess / file-I/O)

**Analog:** 同ファイル（819行）。既存期待値を上書きせずmaxケースを追加する。importは2–11行のjson/HTMLParser/Path/subprocess/sys/pytestを再利用する。

**Bytes subprocess pattern** (`tests/test_cli.py:418–422`):
```python
def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
```

`run_cli`（16–20行）はtextモード、bytes/newline/UTF-8の契約には上記を使う。`assert_output_bytes`（425–441行）は固定expected pairsをtext/JSON/HTMLへ照合し、HTMLは `CLIHTML`（201–239行）で見出し3列・行・basename・元total・表より前のmetadataを確認する。

**Pre-I/O spy pattern** (`tests/test_cli.py:631–641`):
```python
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

max用へ名称/メッセージassertだけ適応し、642–644行の実subprocess確認も併用する。整数表記は611–616行の `build_parser().parse_args(...)` 型を継承するが、maxでは0/負数もvalid。min0/top0とmax0/負数の組合せもpre-I/Oを検証する。

**Internal order / identity pattern** (`tests/test_cli.py:771–783`):
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

759–793行のsetup/monkeypatch/元Counterの値と項目順不変assertまでを一組で継承する。上限超過・下限未満・topで落ちる語を別々に持つ入力に適応し、元total12とzoo3の三条件ケースも区別する。出力一致だけでfilter-before-topを立証しない。

**Empty/error matrix:** 686–741行の全形式parametrize・literal expected pairs・元total・固定空copyを継承。max0/負数/逆転/全除外/空/空白/記号を正常exit0とする。647–669行の入力失敗matrixはmissing/directory/decode/permissionを実CLIで確認し、permissionは同実効ユーザーで `pytest.raises(PermissionError)` を確認してfinallyでchmodを戻す。mockやskipだけに置換しない。

**Fixed-byte oracle pattern** (`tests/test_cli.py:798–804`):
```python
    root = ROOT / ".planning/argonauts/r-e476c11d/baseline"
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    case = index["cases"][case_index]
    capture_root = Path(index["root"])
    path = root / Path(case["input"]).relative_to(capture_root)
    expected = (root / Path(case["stdout"]).relative_to(capture_root)).read_bytes()
    assert path.read_bytes() == case["body"].encode("utf-8")
```

805–817行のargv/env復元と `(returncode, stderr) == (0, b"")` / stdout固定bytes比較まで継承する。履歴絶対pathはメモリ上だけ移す。旧root/head/index/保存bytesは書き換えない。今回不足するmin>1や空text/json等のoracleは製品編集前に固定し、省略・大上限・明示min1をその原本と比較する。変更後2呼出しの比較だけではREQ-26を満たさない。

### `README.md` (documentation, reproducible command contract)

**Analog:** `README.md:9–17,21–28,32–36` と、それを実行する `tests/test_cli.py:672–682`。

**Existing example-test excerpt** (`tests/test_cli.py:676–682`):
```python
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python -m wordfreq input.txt --min-count 2 --top 1 --format json" in readme
    path = tmp_path / "input.txt"
    path.write_text("beta beta beta alpha gamma alpha delta", encoding="utf-8")
    result = run_cli_bytes(path, "--min-count", "2", "--top", "1", "--format", "json")
    assert (result.returncode, result.stdout, result.stderr) == (
        0, b'[{"word": "beta", "count": 3}]\n', b"")
```

新しい1例は `python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`、同じ入力、固定stdout `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]` + LF、exit0/stderr空へ適応する。掲載コマンド・入力・期待結果と実CLIを確認する。既存min例は残す。直接関連する整数全域/省略None/包含/併用/正常空/上限を上げるか省略する案内/元総数説明のみを整える。末尾の検証B行は無関係変更しない。

### max専用採取・検証ファイル / oracle・fixture (utility + evidence, batch file-I/O)

**Analog:** `tools/verify_wordfreq_min_count.py`。責務はliteral oracle、実subprocess、原本保存、head/env帰属。巨大driver全体をmaxへ複製/一般化することは要求しない。

**Literal oracle + capture seam** (`tools/verify_wordfreq_min_count.py:30–35,97–104`、非連続の引用):
```python
    body = "Zoo APPLE apple zoo Hello hello HELLO one, two. one b c d e f g h"
    pairs = [("hello", 3), ("zoo", 2), ("apple", 2), ("one", 2),
             ("two", 1), ("b", 1), ("c", 1), ("d", 1), ("e", 1), ("f", 1)]
    add("default-text", "input.txt", body, pairs, 17, "text", explicit=False)
    for fmt in ("text", "json", "html"):
        add("baseline-" + fmt, "input.txt", body, pairs, 17, fmt)
```
```python
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)
        stdout, stderr = folder / "stdout.bin", folder / "stderr.bin"
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        record = dict(case, input=str(source), input_sha256=parts.digest(source), argv=argv,
                      cwd=str(ROOT), executable=sys.executable, environment={k: env.get(k) for k in
                      ("PYTHONIOENCODING", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "LANG", "LC_ALL")},
                      exit=result.returncode, stdout=str(stdout), stderr=str(stderr), views=[])
```

入力作成は84–96行、HTML原本は105–108行のstdout bytesそのまま保存。49–81行のoracle validatorは製品の出力を期待値として再生成しない。191–211行はfresh root・実profile/run・head・`independent_acceptance=False` の境界を示す。524–550行はpytest argv/cwd/head/件数/exitとstdout/stderr/JUnit保存、非0/空/必須skip拒否の類例。

**Reuse limits:** 18–20行のREQUEST/BASE/WIDTHS、145–177行の旧task commit preflight、444–450行のmin/topのみargv、490–502行の旧依頼/Phase4 scope、586–587行のREQ-15以降AC対応は今回に不一致。旧driverのCLIをmax受入コマンドとして呼ばない。collectorの機構を参照する場合も、依存先を実読しtracked originを確認してから具体的な再利用を決める。本mappingはその依存先のAPI互換まで確認していない。

### max専用品質手順・文字証拠文書 (verification, evidence → report)

**Analog:** `docs/wordfreq-min-count-verification.md`（手順であって合格報告ではない）。

**Concrete procedure excerpt** (`docs/wordfreq-min-count-verification.md:63–65`):
> 品質は1280×900と320×900 CSS px、DPR1、zoom100%、fresh contextの**全full/全tileおよび同環境baseline全画像**を実際に開く。fullが縮小されれば実寸以上/全域panも行い全tileを省略しない。scrollbarはcollectorのEmulation.setScrollbarsHidden条件をrawと画像で統一する。自然な縦scroll可、横scroll依存・clip・隣接重複は不可。存在/PNG寸法/DOM一致/scrollWidth単独では可読性合格でない。
>
> raw.jsonの全文字Range（UTF16 offset/全codepoint/空白・ゼロ面積含む）、全祖先のoverflow/box、隣接列・前後行・metadata非重複、computed書体/CDP実font、全数値を画像に対応付ける。横収まり・clipなしを検査し、自身elementの厳格縦包含だけは要求しない。rawをclamp/丸め/削除しない。

9–15行の実profile分離/能力gate、84–86行の失敗含む通信試行/現headソース順序確認、90–100行の実閲覧後台帳/owner終了/最終原本照合、122–124行のhead変更時再検証/未報告CI未確認を引き継ぐ。旧件数・旧AC/REQ・旧headや39–43行の過去依頼限定一時path許可は移植しない。

今回の権威はCONTEXT D-07とPRD:210。PM向けは `VERIFICATION.md` とCLI/CIの**文字証拠**を添付し、AC/REQ別結果・実画像閲覧枚数/内容/結果を明記する。旧runbookのPM画像原本閲覧要求（118行）をそのままコピーして今回の「PMに画像/圧縮物閲覧を求めない」契約を上書きしない。品質本人の画像閲覧義務とは区別する。

## Shared Patterns

### 共通データフローと保護境界

`argv/argparse → 既存usage検証 → FileSource → casefold済tokens/元Counter → 元total → 別Counterのmin AND optional max → 既存top → shared pairs → formatter → stdout/exit`。

- 対象: CLI・内部spy・実CLI・品質ソース確認。元totalを選択Counterや表示行から再計算しない。
- `wordfreq/aggregator.py:11–17` の安定ソートは回数だけをkeyにする。初出順をset/語昇順で破壊しない（参照のみ、変更対象外）。
- `wordfreq/formatters.py:6–14,17–37,45–127` のAPI/escape/CR保護/empty/CSSを維持。formatter別のfilterやmax用HTMLを増やさない（参照のみ、変更対象外）。

### 固定期待値と証拠帰属

- 対象: regression/fixture/verification。期待pairsは仕様からliteralに固定し、互換bytesは変更前原本を使う。旧baseline index:3–15はrequest `r-e476c11d` / head `789cc17267fb4cfeea24111797c3d934c542ce6a` / `independent_acceptance=false` であり、今回品質合格ではない。
- 旧indexのjq抽出ではdefault text、全3形式、空/空白/記号HTML、long既定/12/99、injection、CR basenameを確認。不足する今回oracleを製品編集前に別fresh rootへ固定する。
- 入力/argv/cwd/interpreter/version/env/対象head/exit/stdout/stderr/HTML/raw/network/画像とAC/REQ索引を結ぶ。REDは未実装機能の狙った失敗のみ、pytest欠落/import error/0 collectedをRED/GREENとしない。
- 品質は対象headから自ら再生成し実画像を読む。Builder capture・hash一致・構造試験・画像の存在だけで独立受入にしない。

### 標準実行方法と存在gate

`docs/wordfreq-min-count-verification.md:17–22` とRESEARCH:179–207に従う既存環境の標準形（本mappingでは未実行）:
```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q
```

既存ファイルの実在を確認して提示しただけで、maxケースやpytest合格の主張ではない。新selector・新採取CLIは作成taskを同じtaskまたは先行taskへ明記し、Builder/品質が実在後に実行する。PLANのautomatedに外側cd/grepや未作成コマンドを足さない。inline実行/ヒアドキュメントで検証手順を代替しない。

## No Analog Found

上表の責務/データフローにはすべて類例がある。ただし、**max専用の完成済み検証CLI・ケース集合・今回変更前oracle不足分・独立品質原本は存在すると確認していない**。既存min-count driverで代替合格にしない。plannerはRESEARCH Wave 0 gapsと承認全scenarioを参照して具体path/作成順/検証契約を決める。これは部品類例不足ではなく、今回依頼固有の実行可能artifactの未作成gapである。

## Metadata

- **Analog search scope:** CONTEXT/RESEARCHの明示参照と `wordfreq/`, `tests/test_cli.py`, `README.md`, `tools/verify_wordfreq_min_count.py`, `docs/wordfreq-min-count-verification.md`, 旧baseline index。強いprimary analog 5ファイルで探索を停止。
- **Files scanned:** primary analog 5ファイルを全文読了。補助参照はaggregator/formatters/CONCEPTS/config/承認PRD/design/必読文書。大きい旧indexは1–90行だけread_file、項目抽出はjq。
- **Pattern extraction date:** 2026-11-25（terminal `date -I`）。
- **Official GSD discovery:** 指定launcherを同一terminalでsource後、`query init.phase-op 7` はphase_found=true / phase_number=07 / has_plans=false / plan_count=0。`query agent-skills gsd-pattern-mapper --skills-only` は出力なし。
- **Project instructions:** `HERMES.md` はnot found、`.hermes/skills/` / `.agents/skills/` はpath not found。未発見の規約は創作しない。
- **Workflow retained:** `.planning/config.json:21–25,43,49–50` のpattern_mapper / plan_check / nyquist_validation / security_enforcementはtrueのまま、設定変更なし。
- **Execution boundary:** 書込みは本PATTERNSのみ。ソース編集・PLAN・試験/未作成検証実行・baseline採取・browser・品質受入・commit/push・Kanbanは実施しない。開始時点の未追跡研究/UI関連成果は他工程のものとして保持する。
