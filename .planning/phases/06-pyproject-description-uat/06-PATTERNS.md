# Phase 06: pyproject description UAT — Pattern Map

**Mapped:** 2026-11-24（`date -I`で確認）
**Status:** 読取り調査完了。類似コード候補の具体的抜粋あり。Git追跡gate・最終更新順は未確認。
**Certified analogs:** 未認定（Git操作禁止のため）。以下の候補を追跡済みanalogと誤認しない。

## Scope and Extraction

- CONTEXT:9,18–29,36、RESEARCH:118–131,227–285から製品・工程ファイルを抽出。製品変更は `pyproject.toml` の `[project].description` 新設1行のみ。完成値は `argonauts-uat public (UAT)`。CLI/API/画面/依存/CI/製品試験は変更しない。
- **検証器の正しい配置はVALIDATION:43–44の `.planning/argonauts/r-774f3cd6/verify_description.py` と `.planning/argonauts/r-774f3cd6/test_verify_description.py`。** RESEARCH:124–125,239–248のphase配下 `verification/` は旧候補であり採用しない。PLANは引数・終了契約を実装taskに明記し、実在後にBuilder・品質が実行する。本調査はPLANも検証器も実装しない。
- process-pathsと証拠はRESEARCHの候補を以下へ記載する。検証器以外の保存先は未固定であり、Plannerが確定する。正本参照一覧は変更許可一覧ではない。既存CONTEXT/RESEARCH、承認OpenSpec、Brief/PRD、過去phaseを一括変更しない。
- `.planning/config.json` の `workflow.pattern_mapper=true`、`nyquist_validation=true`、`plan_check=true` をread_fileとjqで確認。設定変更なし。
- mapper役割のtracked-source gateは `git ls-files` を要求するが、この依頼はGit操作禁止。禁止を優先してGitを実行せず、**候補の認定を留保**する。本文のパスは実在を読んだ参考候補・入力であり、認定済みanalog割当ではない。mirrorからのコピーや追跡元の推測はしない。

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pyproject.toml`（変更） | config / package metadata | file-I/O: 既存bytes → 1行局所挿入 → TOML読取 | 同一ファイル:1–14を入力として確認 | 同一対象の書式参照。新設descriptionの前例なし、追跡未認定 |
| `.planning/argonauts/r-774f3cd6/verify_description.py`（新規・固定） | utility / 工程専用検証CLI | file-I/O + batch/transform: 基準/候補bytes・Git状態 → 条件別結果/exit/hash | 未認定。下記A・C・Dが部分候補 | 役割/データフロー部分一致。description検証の完全一致なし |
| `.planning/argonauts/r-774f3cd6/test_verify_description.py`（新規・固定） | test / 工程自己テスト | batch: 隔離正負例 → 条件名/exit/副作用判定 | 未認定。下記B・Cが部分候補 | 既存はpytest。stdlib unittestの同役割例なし |
| `.planning/phases/06-pyproject-description-uat/verification/process-paths.json`（RESEARCH候補、未固定） | config / exact-path用途台帳 | file-I/O: 全差分の個別分類 → 境界層へ入力 | 未認定。下記Eの用途表が概念上の部分候補 | 同じJSONスキーマの実在例は未発見 |
| `.planning/phases/06-pyproject-description-uat/evidence/builder-cli.md`（候補） | process-record / Builder一次証拠 | batch/file-I/O: 承認・RED/GREEN・argv/exit/hash → 文字原本 | 未認定。下記E | role/dataflow候補。旧結果をコピーしない |
| `.planning/phases/06-pyproject-description-uat/evidence/quality-cli.md`（候補） | process-record / 独立品質一次証拠 | batch/file-I/O: 独立blob取得/検証 → 文字原本 | 未認定。下記E | role/dataflow候補。主体と製品commitを独立固定 |
| `.planning/phases/06-pyproject-description-uat/06-VERIFICATION.md`（新規候補） | process-record / 要件判定索引 | transform: REQ-23・同一製品commit証拠 → 判定/引継ぎ | 未認定。下記E | role-match候補。合格値の流用禁止 |
| `.planning/phases/06-pyproject-description-uat/06-VALIDATION.md`（既存draft、将来の実測後更新） | process-record / 検証戦略 | transform: 実行証拠 → sampling/sign-off | 現行ファイル:1–8,56–65を入力として確認 | 現在draft/false/pending。計画中に合格へ変更しない |

fixtureは工程領域の隔離データで、現時点で具体的ファイル名未固定。工程内であっても未知コードをprefix免除しない。SUMMARY名・PLAN数も未固定であり、本マッピングで新しい実装taskを増やさない。

## Pattern Assignments

以下は**認定前の参考候補の抜粋**。追跡済みanalogとしての直接割当は留保する。最近の工程はPhase 5（文書上2026-11-22）を優先し、スクリプトはPhase 4の実在候補を使用した。Git log/mtime比較はしていないので「最新更新コード」とは断定しない。

### A. 工程検証CLI — argv、bytes、指紋、対象帰属

候補 `tools/verify_wordfreq_min_count.py`。imports:2–11にargparse/json/pathlib/subprocess/sys等。中核の実例（169–171行）:

```python
        blob = subprocess.run(["git", "show", f"{formal}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout
        if hashlib.sha256(blob).hexdigest() != parts.digest(ROOT / path):
            raise ValueError("working driver/tests differ from formal commit")
```

実argv・cwd・exitと出力を保存する例（472–478行）:

```python
        record = dict(oracle, input=str(source), input_sha256=parts.digest(source), executable=sys.executable,
                      environment=recorded, cwd=str(ROOT), stdout=str(folder / "stdout.bin"), stderr=str(folder / "stderr.bin"), views=[])
        record["argv"] = case_argv(record, sys.executable)
        result = subprocess.run(record["argv"], cwd=ROOT, env=env, capture_output=True, timeout=20)
        record["exit"] = result.returncode
        Path(record["stdout"]).write_bytes(result.stdout)
        Path(record["stderr"]).write_bytes(result.stderr)
```

参照可能な要素: argv配列（shell未使用）、binary stdout、固定commit blobと入力の照合、実行記録。ROOTの`parents[1]`はtools配置専用なので新配置へ直コピーしない。旧BASE/REQUEST/環境・役割値も今回用に確定する。

**継承しない箇所:** 同ファイル138–142,153–155,490–502には `.planning/**` 除外やprefix許可がある。本件D-06はexact-path/用途全件列挙なのでこの方式は不適合。1013–1015はエラーをexit1へまとめており、今回の要件不一致/実行エラー分離にもそのまま使えない。ブラウザ、画像、製品pytest、待機セッションも不要。importで旧driverを実行/依存させず、必要な小さなパターンだけを新しいstdlib検証器へ適用する。

### B. 自己テスト — 正常fixtureを先に通し、1条件を壊す

候補 `tests/test_min_count_verifier.py`。imports:2–8はimportlib/json/os/pathlib/sys + pytest。実在ファイルからmoduleを読む例（13–19行）:

```python
def driver():
    path = ROOT / "tools/verify_wordfreq_min_count.py"
    assert path.is_file(), "baseline driver implementation is missing"
    spec = importlib.util.spec_from_file_location("min_count_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

負例の前に同じ正例を検証する例（169–175行）:

```python
    assert v.main(["--mode", "baseline", "--role", "builder", "--output-dir", str(output)],
                  collector=synthetic_collect) == 0
    index = json.loads((root / "index.json").read_text())
    assert v.baseline_errors(index, output, allow_synthetic=True) == []
    wrong = copy.deepcopy(index)
    wrong["cases"][0]["argv"] += ["--min-count", "1"]
    assert v.baseline_errors(wrong, output, allow_synthetic=True), "baseline argv must forbid min-count"
```

567–568行にも原本を先に通す形がある。構造だけ再利用し、今回のテストは**stdlib unittest**へ置換、工程領域の隔離bytes/fixtureのみを壊す。pytest依存・既存製品tests編集・synthetic acceptanceの導入は不要。上例は単にエラー集合が非空かを確認しているが、今回は条件名/exitを照合し、欠落REDが完成値条件だけのFAILであることまで要求する。

### C. メタデータの既存読取りと既存製品書式

`pyproject.toml`:5–11（現物入力）:

```toml
[project]
name = "wordfreq"
version = "0.1.0"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]
```

この表示にdescriptionはない。改行種別・末尾改行・baseline blob一致・解析成功は表示だけから断定しない。新設行は次のtableより前の `[project]` 内で、既存bytesを保持する局所挿入だけ。新設内容の正本は承認入力であり、既存nameから生成しない。

読取り候補 `tests/test_cli.py`:185–191:

```python
def test_package_declares_only_development_dependencies():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["name"] == "wordfreq"
    assert config["project"]["dependencies"] == []
    assert config["project"]["optional-dependencies"] == {"dev": ["pytest"]}
    assert config["build-system"]["build-backend"] == "setuptools.build_meta"
    assert config["tool"]["setuptools"]["packages"] == ["wordfreq"]
```

imports:5–11にはPath/subprocess/sys/tomllib/pytest。既存メタデータの全体TOML解析の部分候補だが、description・全構造差分・生bytes保持の検証例ではない。この製品試験自体は変更せず、新CLIはbinary取得から解析し、構造比較とbytes比較を別条件とする。

### D. TOMLの局所編集と解析エラー境界（補助コード候補）

`_bmad/scripts/stamp_release.py`:73–86:

```python
def read_toml(path: Path, rel: str) -> tuple[str, dict[str, object]]:
    try:
        text = path.read_bytes().decode("utf-8")
        return text, tomllib.loads(text)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise StampError(f"{rel}: cannot read bmod file: {error}") from error


def verify_stamp(root: Path, records: list[Path], expected: dict[str, dict[str, object]]) -> None:
    for record in records:
        rel = record.relative_to(root).as_posix()
        _, data = read_toml(record, rel)
        if data != expected[rel]:
            raise StampError(f"{rel}: stamping changed something other than the version")
```

imports:30–38はfuture annotations、argparse/importlib/sys/tomllib/Path、bytecode抑止。これはbmodのversionを編集するツールで、製品metadata verifierではない。binary→strict UTF-8→tomllibと全構造比較の参考に限定する。45–57行のvalidator動的importと90–112行の書込みpipelineは使わず、実行もしない。上例の統合エラーを今回へコピーせず、候補TOML不正（不適合）とbaseline/取得失敗（実行エラー）を分離する。tracked origin未確認なので、この補助ツールを認定済みsourceや依存元と扱わない。

### E. 最近の工程文書候補 — Builder/品質/判定索引

候補 `.planning/argonauts/r-215b4390/builder-cli-evidence.md`:14–15:

```markdown
| Actual argv | exit | stdout / observation |
|---|---:|---|
```

同文書5–8行はfixed baseline / start head / product commit / later reporting HEADを別欄にし、78–84行は全変更を残してパスと用途を分類する。RESEARCH候補のprocess-paths.jsonには、この**個別用途の考え方**だけを適用する。今回の実差分を取得してから確定し、過去の用途一覧や工程prefixをコピーしない。

候補 `.planning/argonauts/r-215b4390/quality-cli-evidence.md`:14–17:

```markdown
## 1. 実行したコマンドと結果（実argv / exit / stdout / stderr）

| # | 実argv | exit | stdout | stderr |
|---|---|---|---|---|
```

候補 `.planning/phases/05-readme-validation-b/05-VERIFICATION.md`:14–16:

```yaml
baseline_sha: 127143c20b95518585663f176ed767aa4cbfc158
target_head_sha: f3bac6032db66fa6508a5225a8f447d8b4e08b03
evidence: .planning/argonauts/r-215b4390/quality-cli-evidence.md
```

ここで引用したSHAは**過去書式の実例**で、Phase 6の値ではない。今回の固定基準は `b34cba0d008923e7f5267ce52d5403492ea53925`。製品commit・検証開始/終了HEAD・報告commit、blob/入力/検証器SHA-256は後続で実測する。REQ-23の値/構造/bytes/Git状態/独立品質を別行にする。既存05-VERIFICATIONはfrontmatter passedと本文42行human_neededが異なるので判定を複製しない。旧全pytest/画像/CI判定も今回へ持ち込まない。VALIDATIONは現行draftの実測後更新だけであり、ここでsign-offしない。

## Shared Patterns

1. **内容と境界を分離:** baseline/candidate raw bytesの純粋検証とGit取得/状態分類を別責務にする。TOML解析、完成値完全一致、description除去後の全構造一致、許可追加行除去後の全bytes一致を個別判定する。description欠落へ無条件キー参照しない。
2. **REDの判別力:** 基準取得・双方解析・基準欠落・元内容一致が成功し、完成値条件だけがFAILの場合に限る。正例成功と必須負例（欠落/suffix重複/異値/他項目変更/不正TOML）の狙った拒否を工程自己テストで検証。旧capture_red.pyは実exitを記録する実例だが、意味判定文が固定であり今回のoracleには使えない（`.planning/argonauts/t_61fb0c48/capture_red.py`:14–21を読了）。
3. **エラーを区別:** RESEARCH:141–147の0=全条件成功、1=要件不一致、2=取得/実行エラーは未実装の契約案。PLAN/Builderが具体化し、候補不正TOMLと基準不正/読取り不能を区別する。既存例のexit1への一括変換を継承しない。
4. **差分の全件分類:** 固定基準→固定製品commit、index、worktree、未追跡を別々に観測し、追加/削除/改名/modeとstaged/unstaged相殺も捕捉する。正確な工程パスと用途のみを分離し、未知パスは停止。ignoredの扱いも証拠化する。
5. **主体と対象を分離:** Builder GREENは独立品質ではない。品質が同一製品commit blobを独立取得し、blob SHA-256と実検証入力の一致、検証器の一致を再確認。文字原本/VERIFICATIONを標準添付しPMがread_fileで判断可能にする。sync/archiveはPM受入後の最終化のみ。
6. **認証機構は追加しない:** auth/sessionパターンは非該当。守る境界は対象repo/branch/承認head/基準/入力path、subprocess argv、工程内fixture、証拠完全性。hash一致は承認の代替ではない。

## No Analog Found

- description新設の全契約（固定値・全構造・生bytes・全Git状態・RED識別・独立品質）を実装した同役割の既存CLIは、今回探索した範囲で見つからない。
- `.planning/` Python探索と `tomllib|unittest` 検索では該当なし。rootのPython検索にはtomllib例があるが、専用stdlib unittest自己テストの実例は見つからない。既存pytestを工程unittestへ置換する必要がある。
- 用途付きexact-path JSONの同一スキーマは発見していない。人の用途表は参考候補であってJSON実装ではない。
- 上記すべてのコード/文書候補はGit追跡確認未実施。mapperの追跡済みanalog要件を満たしたとは主張せず、認定留保をPlannerへ引き継ぐ。Git禁止が続く限り、候補を自動的に認定済みへ昇格させない。

## Metadata

- 読取り対象: 必須mapper役割、06-CONTEXT、06-RESEARCH、06-VALIDATION、config、現物pyproject、OpenSpec design、既存検証driver/自己テスト、test_cli該当範囲、補助TOMLツール該当範囲、Phase 5のPATTERNS/証拠/VERIFICATION、head帰属のsolution文書。
- 探索範囲: rootのPythonファイル、`.planning/` Python、`tools/`、`tests/`、`_bmad/scripts/`、工程文書。部分読取りは必要箇所のみで重複範囲の再読なし。全repositoryの不存在を一般証明したものではない。
- root HERMES.mdは検索一致なし。`.hermes/skills/` と `.agents/skills/` はPath not found。追加project skillを推測しない。
- 公式launcherをsourceした同じshellで `gsd_run query init.phase-op 6` を実行し、phase_found=true、phase_number=06、has_context=true、has_research=true、has_plans=false、plan_count=0を確認。GSDの判定は独自parserで代替しない。
- 未実施: Git/Kanban操作、追跡確認/履歴調査、基準blob取得、TOML実解析、hash計算、検証器作成/試験、製品編集、PLAN作成、品質/受入判定。未作成の検証コマンドを試していない。候補コードの引用は実行結果ではない。
- 本作業の唯一の書込みは本 `06-PATTERNS.md`。製品/設定/過去phaseは変更しない。
