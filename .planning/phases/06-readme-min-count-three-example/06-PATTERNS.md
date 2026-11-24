# Phase 06: README min-count three example - Pattern Map

**Mapped:** 2026-11-24（terminal `date -I`）
**Files analyzed:** 4対象（製品1ファイル、工程文書・原本3分類。可変run内の原本はファイル群として集約）
**Analogs found:** 4 / 4（内容・役割の照合。tracked-source gateは未確認、後述）

## Scope and Discovery

公式 `gsd-pattern-mapper.md` 全文、06-CONTEXT.md、06-RESEARCH.mdを最初に読んだ。公式launcherをsourceした `gsd_run query init.phase-op 6` はphase_found=true、phase_number="06"、has_context=true、has_research=true、has_plans=false、has_verification=falseを返した。計画の存在や受入成功は主張しない。

HERMES.mdはファイル検索で発見なし。`.hermes/skills/` と `.agents/skills/` は検索時にPath not found。追加project-local skillは発見していない。

**Tracked-source gateの制約:** 公式役割はanalogごとの `git ls-files` を要求するが、本依頼はgit操作を禁止しているため実行していない。以下はリポジトリ直下の実在ファイルをread_fileで確認した内容上のanalogであり、git追跡済みとの認定ではない。install/runtime mirrorは採用していない。追跡状態は未確認として引き継ぎ、許可された後続工程で確認する。製品CLI、pytest、kanban操作も未実行。

## File Classification

工程ファイル名のうち `<actor>` / `<run>` は後続で選定する提案値で、存在確認済みのファイル名ではない。Roleは公式分類のutilityを文書・証拠に適用し、括弧に実際の責務を記す。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `README.md`（既存を局所変更） | utility（利用者向け文書） | file-I/O | `README.md:5-26,35` | exact（同一ファイル・同一用途） |
| `_bmad-output/initiative-r-5f8197e8/verification/<actor>/<run>/` 内の入力コピー・各stdout/stderr/exit・既存試験結果・差分原本（新規工程文字証拠群） | utility（実行原本、非fixture・非ツール） | file-I/O | `docs/wordfreq-min-count-verification.md:9,22,61,104-118` | role-match（旧工程の原本追跡責務だけ継承） |
| 同run配下のCLI証拠文書・索引Markdown（新規工程文書、名称は後続決定） | utility（証拠索引・照合記録） | file-I/O | `docs/wordfreq-min-count-verification.md:102-118` | role-match（文字索引と配送gate） |
| `VERIFICATION.md` 等の品質判定文書（正確な配置は後続決定。phase配下またはinitiative配下の工程文書） | utility（独立品質の判定） | file-I/O | `docs/wordfreq-min-count-verification.md:4,9,99-100,118` | role-match（主体分離・未実施拒否） |

**除外する変更:** `wordfreq/`、`tests/`、`tools/`、設定・依存・CI・HTML/CSSの製品変更なし。既存spec・runbook・試験は参照専用。新fixture、新試験、補助script、validatorを作らない。repo rootの一時 `input.txt` は後続の実行準備物であり製品ファイルではない。既存なら上書きしない。PLAN/SUMMARY/VALIDATION等の標準工程文書は製品と別管理し、本mapperが作るのはこのPATTERNS.mdだけ。

## Pattern Assignments

### `README.md` (utility/documentation, file-I/O)

**Analog:** `README.md`（同一ファイル）

**Imports / Auth:** 該当なし。文書変更のため依存・認証を導入しない。

**Core pattern — 既存sh fenceへ1行だけ追加** (`README.md:9-15`):

```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
python -m wordfreq input.txt --format html > result.html
```

現行全文に指定の `python -m wordfreq input.txt --min-count 3` は存在しない。最初の通常実行行の直後へ指定行を1つだけ挿入するのがclosest pattern。閾値2例の置換、検証用json/htmlの2行追加、末尾への追記はしない。

**Preservation / validation** (`README.md:19,23-24,35`):

```text
- `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
```

既存23行は回数降順・同数初出順、24行はmin-count/top前総数を説明済み。原則説明を重複追加しない。末尾は次の原文を保持する。

```text
検証A: v1.12 の通しの確かめ（2026-11-22）
```

既存内容・順番・改行byte・末尾改行を保持し、単に指定文字列があるだけで合格にしない。今回mapperではbyte検査を実施していない（LFの観測は06-RESEARCH.md:88の上流記録）。後続で変更前後原本と差分を照合する。

**Testing analog — 既存例は残す必要がある** (`tests/test_cli.py:672-682`):

```python
def test_min_count_help_and_readme_example(tmp_path):
    help_result = run_cli_bytes("--help")
    assert help_result.returncode == 0 and help_result.stderr == b""
    assert b"--min-count MIN_COUNT" in help_result.stdout
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python -m wordfreq input.txt --min-count 2 --top 1 --format json" in readme
    path = tmp_path / "input.txt"
    path.write_text("beta beta beta alpha gamma alpha delta", encoding="utf-8")
    result = run_cli_bytes(path, "--min-count", "2", "--top", "1", "--format", "json")
    assert (result.returncode, result.stdout, result.stderr) == (
        0, b'[{"word": "beta", "count": 3}]\n', b"")
```

この既存testはmin-count3新例を検査しない。試験の追加・改変で補わず、掲載1回と保存内容の直接照合を別途計画する。

### 実行主体別の文字原本群 (utility/evidence, file-I/O)

**Analog:** `docs/wordfreq-min-count-verification.md`（旧Phase4の工程責務のみ）

**Core pattern — 実行記録は成功報告と区別** (`docs/wordfreq-min-count-verification.md:22`):

```text
非0/0 collected/必須skipは失敗。高速feedbackを独立品質と呼ばない。全pytestは次のdriverも自ら実行しsuite.json/xml/stdout/stderrへ実argv/cwd/head/環境/件数/exitを保存する。各stageの開始・終了・所要時間を別記し、未測定を30秒以内としない。
```

コピーするのは実argv/cwd/head/環境/件数/exitを保存し、未測定や未実行を成功にしない規律だけ。旧driver、旧baseline、旧head、画像matrix、tar配送はコピーしない。

**具体的な出力契約の根拠** (`wordfreq/formatters.py:6-14`、参照専用):

```python
def format_text(pairs: list[tuple[str, int]]) -> str:
    """Format count-first tab-separated lines, or nothing for no pairs."""
    return "".join(f"{count}\t{word}\n" for word, count in pairs)


def format_json(pairs: list[tuple[str, int]]) -> str:
    """Format ordered word/count objects as one ASCII-safe JSON line."""
    items = [{"word": word, "count": count} for word, count in pairs]
    return json.dumps(items, ensure_ascii=True) + "\n"
```

実際の各形式のstdoutを独立保存し、他形式から合成しない。textのTAB/LF、JSON配列word/count・整数・順序・末尾改行を照合する。空stderrも原本を残す。

**既存実CLI試験の照合パターン** (`tests/test_cli.py:698-708`、既存testを読む/実行するだけ):

```python
def test_min_count_selection(tmp_path, output_format, content, minimum, expected, total, top, reverse):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    options = ["--min-count", str(minimum)]
    if top is not None:
        top_options = ["--top", str(top)]
        options = top_options + options if reverse else options + top_options
    result = run_cli_bytes(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format,
                        expected[:10 if top is None else top], path.name, total)
```

今回はこのtest内のfixture生成コードを新試験へコピーしない。後続は同一UTF-8実input.txtで既定textの指定例と `--format json` / `--format html` だけを加えた3実行を行う。top等は足さない。直接リダイレクト後、直ちに実exitを記録する捕捉手順は06-RESEARCH.md:122-160の提案であり、既存helperまたは実行済み結果とは扱わない。

入力提案は06-RESEARCH.md:94-98の原文を利用する。計画期待と実測を分離し、実測欄は後続の実CLI原本からのみ埋める。入力を保存する場所・名前とrun名は後続で確定し、未作成pathを検証コマンドとして今実行しない。

### CLI証拠文書・索引 (utility/evidence-index, file-I/O)

**Analog:** `docs/wordfreq-min-count-verification.md:102-118`

**Core pattern — 原本と判断の対応付け** (同:104):

```text
manifest.ac_indexの全原本参照に、下表の判断内容と先行RED/GREENを結ぶ。原本request/head/run/actor/root/path/SHAを欠かさない。
```

今phaseでは旧manifest/先行RED-GREENを新規に作るのではなく、REQ-25/26/27・OpenSpec1.1/1.2/2.1に対して、実行主体、cwd、検証head、実入力pathと全文、完全コマンド、実exit/stdout/stderr、独立期待、比較結果、原本pathを文字で対応付ける。検証が実行されて初めて実測と書く。

**Delivery / error handling pattern** (`docs/wordfreq-min-count-verification.md:118`):

```text
3. **PM原本読取りgate**：受取PM本人が配送された実入力/argv/exit/stdout/stderr/HTML/raw/画像/閲覧台帳/AC索引を実際に読み、照合hashと読取り結果を自分のカードへ記録する。ローカルpath通知や添付成功だけでは読取り済みでない。PM未読は未達gateのまま渡す。品質実閲覧台帳をBuilderが署名しない。
```

適用するのは保存・標準添付・PMの実原本読取りを混同しない部分だけ。今phaseは画像・圧縮物の閲覧をPMへ要求せず、CLI原本とVERIFICATION.mdを文字で渡す。画像不要なら0枚と理由を明記。標準添付は後続担当が行い、このmapperはkanban操作しない。

### `VERIFICATION.md` 等 (utility/independent-verification, file-I/O)

**Analog:** `docs/wordfreq-min-count-verification.md:4,9,99-100,118`

**Independent actor / guard pattern** (同:4):

```text
本書は実行手順であり合格報告ではない。Builder自己承認不可。OpenSpec task 2.2、画像実閲覧、PM原本読取り、現head CIは実証までpending。
```

今回のOpenSpec番号は2.1であり旧番号を転記しない。同:9は実profile・別run/別rootを要求し、role引数だけの変更を独立性の証明にしない。Builderは自分の実行結果だけを報告し、独立品質未実施を明記する。品質本人が同入力・閾値・3形式を独立実行し、別rootの原本と照合を記録する。

品質は依頼基点から対象headまでと作業中の全差分を後続の許可されたgit工程で確認し、README以外の製品変更と工程文書を分類する。未確認・不一致・原本欠落・実行環境blockは未達として記録する。コード変更へ無断拡張しない。

## Shared Patterns

### 既存データフローを変えず検証する

**Source:** `wordfreq/__main__.py:34-38,44-54`（参照専用）
**Apply to:** 3形式原本・索引・品質判定。

```python
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count})
    pairs = top_words(selected_counts, args.top)
```

FileSource→iter_tokens/casefold→count_words→元total→閾値→top→形式分岐→stdout。元totalは表示回数和や種類数でない。`openspec/specs/wordfreq-cli/spec.md:81-90` は同数時の正規化後初出順を規定し、旧シナリオ名「昇順」は現在の期待値を意味しない。ソースは変更しない。

### HTMLは新UIでなく実stdout原本を確認する

**Sources:** `wordfreq/formatters.py:28-32,39-43,108-122`、`tests/test_formatters.py:94-133`。
**Apply to:** HTML原本・REQ-26照合表。

```python
    rows = "".join(
        f'<tr><td class="rank">{_html_text(str(rank))}</td>'
        f'<td class="word">{_html_text(word)}</td>'
        f'<td class="count">{_html_text(str(count))}</td></tr>\n'
        for rank, (word, count) in enumerate(pairs, 1)
    )
```

既存静的性検査の抜粋 (`tests/test_formatters.py:127-133`):

```python
    table_position = document.nodes.index(document.tagged("table")[0])
    for name in ["filename-value", "total-value"]:
        assert len(document.classified(name)) == 1
        assert document.nodes.index(document.classified(name)[0]) < table_position
    css = document.tagged("style")[0]["text"]
    assert not re.search(r"url\s*\(|@import|expression\s*\(|javascript:|https?:|//", css, re.I)
    assert "\\" not in css  # No escaped CSS identifiers hiding resource paths.
```

3列見出し、1始まり順位、語/回数/順序、basenameのみ、表前の元total、UTF-8宣言、内包style、script/外部参照なしを既存契約と照合する。既存HTML全文の検査は必須だが、CSS/DOM/見た目変更、新UI-SPEC、browser driver増設はしない。今回の画像0枚方針は新phaseのD-05/D-06に基づき、旧phaseの画像・browser合格を継承したとは書かない。

### 検証コマンドは既存ファイルから、実行は後続のみ

**Sources:** `tests/test_cli.py:672-708`、`tests/test_formatters.py:9-48,94-175`、`docs/wordfreq-min-count-verification.md:14-22`。

後続PLANに使える既存ファイルの確認済み参照例（**mapperでは未実行、成否・所要時間未確認**）:

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k 'min_count_selection or min_count_help_and_readme_example' -x
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -x
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest
```

3.12用経路は既存runbookの環境パターン。現在の実行可否は後続で確認する。06-RESEARCH.md:79-82はPATH上pytestのimport失敗を記録しており、単なる `pytest` を成功前提で採用しない。失敗時はblock報告とし、新依存・新試験・新ツールで救済しない。既存試験の成功だけで指定例そのものの3形式実行と独立品質を代用しない。

## No Analog Found

ファイル責務の内容上のno-analogはなし。ただし新しい依頼専用の文字だけの原本構成に完全一致する既存実行済みfixture/validatorは確認していないため、原本群・索引・品質文書はrole-matchとした。正確なファイル名や新入力の実出力を既存実績として扱わない。

| File / Concern | Role | Data Flow | Reason |
|----------------|------|-----------|--------|
| 全analogのgit追跡状態 | source provenance gate | read-only metadata | git操作禁止により未確認。read_file成功をtrackedの証明にしない。 |

## Metadata

- **Analog search scope:** repo root README、docsの既存min-count runbook、tests/test_cli.py、tests/test_formatters.py。処理・契約の裏取りとしてwordfreq/__main__.py、wordfreq/formatters.py、openspec/specs/wordfreq-cli/spec.md、当依頼tasks.mdも読んだ。
- **Strong analogs:** README、既存runbook、既存CLI試験、既存formatter試験の4ファイルで探索を停止。
- **Pattern extraction date:** 2026-11-24。
- **Evidence status:** read_fileと公式GSD queryによる計画資料。製品CLI/pytest/独立品質/差分scope検証は未実行。git/kanban操作なし。
- **Writes in this task:** `06-PATTERNS.md` のみ。製品変更・試験/fixture/検証ツール・設定/依存追加なし。
- **Planning handoff:** 各PLAN最大3tasks、番号順直列、task終了時点で存在する入力・検証対象を使う。開始時gate値維持。後続Builder・品質の実証と標準添付、PM読取りはpending。
