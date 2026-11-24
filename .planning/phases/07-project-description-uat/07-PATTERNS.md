# Phase 7: Project description UAT - Pattern Map

**Mapped:** 2026-11-25 (`date -I`)
**Files analyzed:** 6 target files (うち工程ファイル名5件は提案、製品対象1件は確定)
**Analogs found:** 6 / 6 (exact: 1, role-match: 5; 完全な検証器の既存実装を意味しない)
**Inspection head:** `24a32e75c63c8d7dc41255487c47a63706263e7d`
**Fixed implementation baseline:** `c572613dc626160db2eb3bf4a41c95fc8283b828` (inspection headで置換しない)

## Scope and Input Extraction

- `07-CONTEXT.md:14-21` と `07-RESEARCH.md:178-222,225-240` から対象を抽出した。製品変更は `pyproject.toml` の新規description 1行のみ。工程検証器・判別力試験・文字証拠は `.planning/argonauts/r-cf2eeaab/` 内。
- `verify_description.py` / `test_verify_description.py` はRESEARCHの予定名。`builder-evidence.md` / `VERIFICATION.md` / `cli-evidence.txt` は今回の責任分類用の提案名であり、未作成。品質の独立実行・添付は後続品質担当の責任。Builderが品質済みの記録を先に作らない。
- canonical design/tasksは `openspec/changes/r-cf2eeaab-project-description-uat/design.md:15-19` と `tasks.md:7-13` を直接確認した。旧phase成果は修復・再実行・受入根拠への流用をしない。既存ファイルの引用は実装様式の読取りだけ。
- 今回のmapperが書くのは本PATTERNS.mdのみ。製品変更、検証器作成、既存/新規試験実行、commit/push/Kanban操作はしていない。

## File Classification

以下の `P/` は説明上の略記で `.planning/argonauts/r-cf2eeaab/` を表す。実際のPLANには完全な相対pathを書く。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pyproject.toml` (modify) | config | file-I/O | `pyproject.toml:5-11` (既存projectテーブルの自己analog) | exact |
| `P/verify_description.py` (new) | utility / verification | file-I/O + batch + transform | `tools/verify_wordfreq_html.py:265-284`; TOMLは `tests/test_cli.py:185-191` | role-match |
| `P/test_verify_description.py` (new) | test | file-I/O + isolated Git request-response | `tests/test_min_count_verifier.py:51-77,165-178,190-230` | role-match |
| `P/builder-evidence.md` (new, proposed name) | config / process evidence | batch → file-I/O | `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33-45,66` | role-match |
| `P/VERIFICATION.md` (new, quality follow-up) | config / quality evidence | independent execution → file-I/O | `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33-45,74-81` | role-match |
| `P/cli-evidence.txt` (new, proposed name; role-separated originals) | utility output / evidence | subprocess streams → file-I/O | `tools/verify_wordfreq_html.py:118-134` | role-match |

工程Markdownは製品configではない。role列のconfigはmapper分類語彙への対応であり、運用記録を指す。CLI原本はBuilder/品質/RED/GREENごとに別ファイルまたは追記禁止の別保存先へ分けてよい。上表6件は論理対象数で、実行後の原本ファイル総数ではない。

## Pattern Assignments

### `pyproject.toml` (config, file-I/O)

**Analog:** 同ファイル `5-11`、追跡済み。既存project直下の単純なスカラー設定の様式を踏襲する。

```toml
[project]
name = "wordfreq"
version = "0.1.0"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]
```

**Apply:** version直後・dependencies直前を候補に `description = "argonauts-uat public (UAT)"` の1行だけを追加する。次のoptional-dependenciesテーブルへ入れない。import/auth/error handlingは静的設定なので該当しない。既存行・改行・末尾状態を保ち、serializerで全体を再生成しない。この段階では追加しない。

### `P/verify_description.py` (utility, file-I/O + batch)

**Primary analog:** `tools/verify_wordfreq_html.py:265-284`。標準ライブラリのsubprocess argv、明示cwd、Git失敗の伝播、NUL区切り未追跡列挙、対象headの記録を再利用する。

**Imports/root pattern:** 同ファイル `14,17-19,24` の `Path` / `subprocess` / `sys` / `tempfile` と `Path(__file__).resolve()` による位置確定。配置の深さが異なるため既存の `.parents[1]` はコピーしない。新配置からrepo rootを決定して全Git呼出しのcwdに渡す。TOML用に `tomllib`、比較用に `copy` を標準ライブラリから追加する。

**Core Git excerpt** (`265-284`、抜粋):

```python
def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8", errors="strict")
```

```python
    for name in filter(None, git("ls-files", "--others", "--exclude-standard", "-z", "--", *paths).split("\0")):
        content = (ROOT / name).read_bytes()
        untracked.append(dict(path=name, sha256=hashlib.sha256(content).hexdigest(),
                              content_utf8=content.decode("utf-8", errors="backslashreplace")))
    return dict(head=git("rev-parse", "HEAD").strip(), status=status, untracked_product=untracked,
                product_status=dirty, product_diff=git("diff", "HEAD", "--", *paths))
```

**TOML validation excerpt:** `tests/test_cli.py:185-191`:

```python
def test_package_declares_only_development_dependencies():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["name"] == "wordfreq"
    assert config["project"]["dependencies"] == []
    assert config["project"]["optional-dependencies"] == {"dev": ["pytest"]}
    assert config["build-system"]["build-backend"] == "setuptools.build_meta"
    assert config["tool"]["setuptools"]["packages"] == ["wordfreq"]
```

**Adaptation / do not copy unchanged:**

1. 既存provenanceは限定pathsとHEAD diffであり今回には不足する。全パスを取得し、固定起点→HEAD/index/worktreeと未追跡を別々に分類する。既存のexclude pathspecや製品パス一覧を流用しない。mode変更・削除・renameの旧新パスを取りこぼさない。
2. `git show <fixed-base>:pyproject.toml` のstdoutはdecode前のbytesを保持する。作業側もread_bytesを原本にし、tomllibで両方を解析する。完成値完全一致、descriptionだけ除いた全体構造一致、追加行をちょうど1行だけ除いたbytes一致を独立判定する。既存testは依存宣言だけの検査なので、そのままではREQ-25/26/27を満たさない。
3. 工程パスは `.planning/`、`openspec/`、`_bmad-output/`、`.compound-engineering/`、`docs/solutions/` のディレクトリ境界で判定。それ以外は未知パスを含め製品と扱い、許可製品は `pyproject.toml` のみ。
4. Git失敗、OSError、UnicodeError、TOMLDecodeErrorを条件別に示して非zero終了。description欠落と区別する。既存のcheck=Trueを例外握り潰しへ変えない。本番検証器はassertのみで判定しない。認証/権限/APIの追加は不要。
5. 具体的な完成値・baseline・bytesの比較方式は `07-RESEARCH.md:95-118,155-172` を併用する。これらの全条件を統合した既存実装は今回の探索では確認できない。

### `P/test_verify_description.py` (test, isolated Git + file-I/O)

**Analog:** `tests/test_min_count_verifier.py`。pytest構文やbrowserの仕組みではなく「追跡基準を先に作る」「同じ検証器で正常対照を通してから変異を拒否する」部分を移植する。

**Fixture Git excerpt** (`65-73`):

```python
    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True).stdout.decode().strip()
    git("init", "-q")
    git("config", "user.name", "Synthetic baseline fixture")
    git("config", "user.email", "fixture@example.invalid")
    git("add", ".")
    git("commit", "-qm", "feat(04-01): synthetic fixture formal task")
    monkeypatch.setattr(v, "ROOT", repo)
    monkeypatch.setattr(v, "BASE", git("rev-parse", "HEAD"))
```

これは既存ソースの引用であり今回の実行指示ではない。本repoでcommitはしない。将来のisolated fixtureがcommit比較を試す場合だけscratch内に独立基準を作る。元ファイルの古いtask名、ROOT/BASEの値、環境role設定、browser pipelineは持ち込まない。

**Positive control → mutation excerpt** (`171-178`):

```python
    index = json.loads((output / "index.json").read_text())
    assert v.baseline_errors(index, output, allow_synthetic=True) == []
    wrong = copy.deepcopy(index)
    wrong["cases"][0]["argv"] += ["--min-count", "1"]
    assert v.baseline_errors(wrong, output, allow_synthetic=True), "baseline argv must forbid min-count"
    wrong = copy.deepcopy(index)
    wrong["provenance"]["changed_paths"] = ["wordfreq/__main__.py"]
    assert v.baseline_errors(wrong, output, allow_synthetic=True), "scope must be derived, not trusted"
```

**Adaptation:** 標準 `unittest.TestCase` / `subTest` / `tempfile.TemporaryDirectory` 等へ置換する。pytestを新ファイルでimportしない。TMPDIR配下の独立fixtureで正常な1行追加を先に通し、欠落・誤値・別テーブル・重複・破損・既存metadata/bytes変更・他製品committed/staged/unstaged/未追跡/削除/mode・工程prefix偽装を別々に試す。単なる非zeroでなく、狙った判定の失敗を確認する。環境/import/Git失敗を欠落RED認定しない。固定起点のproduction定数をfixtureの都合で変更せず、内部検証関数へfixture root/baseを渡すなどの局所設計を採る。

補助根拠: `tests/test_cli.py:158-164,172-182` はcold copy→git add→before/after比較を実装済み。`docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:37-43` は変異種別ごとの分離と基準追跡の理由を明記する。単なるstatus比較だけでは今回の固定commit間検証の代わりにならない。

### `P/builder-evidence.md` and `P/VERIFICATION.md` (process evidence, file-I/O)

**Analog:** `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md:33-39`:

```markdown
証拠受渡しでは次の三段階を別々に記録する。

|段階|確認すること|まだ言えないこと|
|---|---|---|
|保存済み|原本の保管先、対象head、run/root、保持期間を特定できる|別profileから読める、標準添付された|
|標準添付済み|添付IDと実際の保存ファイルを一覧で読み戻せる|受取側に展開手段がある、中身を照合済み|
|受取側で読取り済み|必要な原本をその担当の利用可能ツールで開き、要求と照合できる|その担当自身が製品試験や画像実閲覧を再実施した|
```

**Apply:** Builderは実測RED/GREENのコマンド・exit・stdout/stderr原本path、固定起点、検証対象head、dirty状態、完成値、構造/bytes/全差分、AC-1/2/3とREQ-25/26/27の対応を記録する。品質は自身の独立再実行結果を別のVERIFICATION.mdに残す。検証headと後の報告headを区別する（同analog `66,74-81`）。標準添付・PM原本読取りは未実施なら未実施と書く。画像は0枚、メタデータのみで視覚変更なしという理由を記す。画像/アーカイブの読解をPMへ要求しない。旧phaseの数値・画像件数・成功headは転用しない。

### `P/cli-evidence.txt` (evidence output, streams → file-I/O)

**Analog:** `tools/verify_wordfreq_html.py:122-130`:

```python
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)
        stdout = folder / ("stdout.html" if case["format"] == "html" else "stdout.txt")
        stderr = folder / "stderr.bin"
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        record = dict(case, input=str(source), basename_repr=repr(case["basename"]),
                      argv=argv, cwd=str(ROOT), executable=sys.executable,
                      environment={key: env[key] for key in ("PYTHONIOENCODING", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
                      exit=result.returncode, stdout=str(stdout), stderr=str(stderr), views=[])
```

**Apply:** 実argv、cwd、exitと出力原本を判定要約から分離して保持する。CLI原本の値を手で成功値へ修正しない。今回はHTML/browser出力ではなく文字原本を渡す。Builderと品質の実行原本を区別し、同じファイルへ上書きしない。上記コード自体の取り込みや製品toolsの修正は不要。

## Shared Patterns

- **Read-only inputs / minimal write:** 検証器は固定blobと作業設定を読む。製品TOMLは1行挿入だけ。fixture以外に欠陥を注入せず、Git index/worktreeを検証の副作用で修復しない。
- **Independent oracle:** 完成値と固定起点は承認値を使用し、現物を正解として生成しない。意味一致とbytes一致は別gate。
- **Fail closed:** subprocess argv + cwd + check、NUL区切りパス、未知パス拒否、例外の条件別非zero。shell=Trueや外側grep、否定pathspecへ依存しない。認証・DB・HTTP・UI・新規外部依存は該当なし。
- **Evidence attribution:** 欠落固有RED→同じ検証器GREEN、Builder自己検証と品質独立検証、保存と添付とPM原本照合、対象headと報告headを混同しない。
- **Direct automated commands (作成後のみ):** `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` と `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py`。計画中は実行しない。実在ファイル作成後、各taskの入力実在条件を満たして直接実行する。各PLAN最大3tasks・同branch直列積上げはCONTEXT D-08を保持。

## No Analog Found

完全にanalogがないtarget fileはないが、以下は既存ソースのコピーだけでは成立しない。

| Gap | Related target | Planner action |
|---|---|---|
| 固定起点TOML構造＋追加行除去後bytes＋HEAD/index/worktree/未追跡/modeを統合する検証器 | `P/verify_description.py` | RESEARCHの比較条件を局所実装し、作成後に判別力を実測。既存provenanceを完全実装と誤記しない |
| 同要件を直接扱う標準unittestスイート | `P/test_verify_description.py` | 既存pytestのfixture/変異様式だけ参考に標準ライブラリで新設。製品testsを変更しない |
| 本依頼の独立品質結果・文字原本・添付実績 | evidence files | 後続の実行事実だけ記録する。今回未実施の結果は作らない |

## Metadata

- **Analog search scope:** root metadata、`tests/`、`tools/`、`docs/solutions/`。TOML/未追跡Gitパターンはrepo全体の `*.py` 内容検索でも確認。工程配下の新検証器はRESEARCH上も未作成。
- **Primary analog files:** 5 (`pyproject.toml`, `tests/test_cli.py`, `tests/test_min_count_verifier.py`, `tools/verify_wordfreq_html.py`, `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md`)。別に基準追跡の補助学習文書1件を直接確認。
- **Tracked-source gate:** 上記5件と補助学習文書は、同worktreeの `git ls-files -- <明示path列>` が各pathを出力した。runtime/install mirrorをanalogにしていない。
- **Project instructions:** root `HERMES.md` はread_fileで不存在。`.hermes/skills/` と `.agents/skills/` はsearch_filesで探索先不存在。追加project skillを仮定しない。
- **Initial worktree state:** `git status --short` は既存 `.planning/state.json` modified とphase `.gitkeep` untrackedを表示。これらを変更・修復しない。
- **Verification boundary:** 調査と文書保存のみ。新旧の製品試験・検証器実行、品質判定、commit/push、添付・Kanban更新はなし。GSD phase判定は追加不要で、stale STATEからphaseを推定していない。
- **Pattern extraction date:** 2026-11-25。
