# 学習調査結果 — request r-5a3b8a3f / task t_0d6af354

## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: wordfreq CLI の phase 1、REQ-07（リポジトリ CI pytest job）の gap 計画。既存 01-01..04 を再実装せず、人による workflow push と品質担当の独立再検証を分離して、Executed 状態の phase 1 に gap plan を追加する。本報告は前計画カード t_fcdaa629 の報告を今回カード向けに更新したもの。
- **Keywords Used**: GitHub Actions, CI, pytest, workflow, permission, gap, verification, test, CPython 3.12, Python, stdlib, GIT_, UTF, 検証, 権限, 学習。Activity・Concepts・Decisions・Domains（workflow / code-implementation / testing）から抽出。
- **Search Roots**: `docs/solutions/` のみ。Compound Pack の指定なし。
- **Files Scanned**: 検索ルートの全ファイル探索で 1 ファイル（`docs/solutions/.gitkeep`）を検出。学習文書は 0 件。発見された下位ディレクトリはなし。
- **Relevant Matches**: 0 files。候補がないため frontmatter の採点・関連文書の全文読取りは対象なし。
- **CONCEPTS.md**: リポジトリ内ファイル探索で該当なし。共通語彙の読取りを省略。
- **Critical Patterns**: `docs/solutions/patterns/critical-patterns.md` は全ファイル探索に存在せず、省略。

### Search Evidence
1. `docs/solutions/` を `**/*` で探索し、`.gitkeep` のみを検出した。
2. 大文字小文字を区別しない frontmatter プリフィルタ `(title|tags|module|problem_type):.*(github|actions|ci|pytest|workflow|permission|gap|verification|test|CPython|標準|検証|権限)` は 0 件。
3. `applies_when` 等のリスト条件を拾う `^\s*- .*(github|actions|ci|pytest|workflow|permission|gap|verification|test|CPython|検証|権限)` も 0 件。
4. 候補が 3 件未満のため、frontmatter に限定しない全文フォールバック `(github|actions|ci|pytest|workflow|permission|gap|verification|test|python|stdlib|GIT_|UTF|検証|権限|学習)` を大文字小文字を区別せず検索し、0 件。

### Relevant Learnings

該当する既存学習は 0 件。`docs/solutions/` はプレースホルダーのみであり、CI 証跡、人の Workflows 権限境界、gap closure の順序、CPython 選択について採用・回避すべき既存パターンは発見できなかった。以下は過去学習からの発見ではなく、今回提供された作業コンテキストに基づく計画上の注意点である。

### Recommendations
- **要件とスコープを維持する**: phase 1 の gap plan として REQ-07 の残余検証に限定する。新規 ingest、既存 01-01..04 の再実装、CI 要件の緩和、権限変更、CI polling loop の追加は行わない。
- **人の操作と独立検証を区別する**: 作業コンテキストでは、人が `.github/workflows/pytest.yml` を commit `5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2` に追加済みで、CPython 3.12 を選択した。人の workflow push は既に行われた前提入力として扱い、品質担当による対象 commit・workflow・イベント・実行結果の独立再確認を別の検証段階にする。
- **報告された CI 証跡を検証対象として渡す**: push run `44017344584` と pull_request run `44017344659` はともに completed/success・43 passed と報告されている。ただし本調査は学習コーパス検索のみであり、GitHub や workflow 内容、実行ログを独立確認していない。これらを本調査の検証済み結果や REQ-07 完了判定に置き換えない。
- **検証の実在性を保つ**: PLAN に記載する検証コマンドは Builder・品質が実在する検証ファイルから実行できるものに限定する。計画中に未作成の検証コマンドは試さない。標準ライブラリのみの runtime 要件を維持し、継承された GIT_* 隔離と非 UTF-8 stdout の警告は今回も非 blocking として扱う。
- **完了後の学習候補**: 人の Workflows 権限境界、push / pull_request 両イベントの証跡、品質担当の独立再検証を順序立てて gap closure する手順は、実証後に `docs/solutions/` へ永続化する価値がある。今回の検索結果だけから一般化済みの学習として断定しない。
