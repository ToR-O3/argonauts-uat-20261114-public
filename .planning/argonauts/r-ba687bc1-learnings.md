## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: README.md「wordfreq の実行」の既存コード例へ `python -m wordfreq input.txt --top 5 --format text` を1行追加するlight計画。製品変更はREADMEのみとし、既存例・コード・設定・依存を維持する。OpenSpecのskip_specs利用は呼出し元の決定として扱う。
- **Keywords Used**: README, wordfreq, documentation, workflow, scope, preservation, 検証, 変更, 限定, 原本。title/tags/module/problem_typeを大文字小文字を区別せず検索。
- **Files Scanned**: docs/solutions配下のMarkdown 6ファイルを内容検索し、候補6ファイルのfrontmatterを確認。関連2ファイルを全文読取りした。ディレクトリ・.gitkeepは件数に含めない。
- **Relevant Matches**: 2ファイル（直接関連1件、条件付きの周辺知識1件）。
- **Search Roots**: docs/solutionsのみ。実在する分類はworkflow-issuesとbest-practices。根拠文書のRelatedリンク先へ探索を拡張していない。
- **Grounding**: CONCEPTS.mdの「検証対象head」「独立検証証跡」の定義を確認。
- **CE Config**: .compound-engineering/config.yaml:1は `docs_root: docs` のみ。pack宣言はなく、外部packは探索・読取りしていない。
- **Critical Patterns**: docs/solutions/patterns/critical-patterns.mdは探索一覧に存在しない。

### Relevant Learnings

#### 1. 限定PRの整備は工程原本の保全を先行し、新headの全差分を独立確認する
- **File**: docs/solutions/workflow-issues/limited-pr-process-original-preservation.md
- **Module**: README限定PRと工程原本の保全
- **Problem Type**: workflow_issue
- **Relevance**: 強い関連。READMEの1行追加と、成果物がREADMEだけという受入条件を直接扱う。2026-11-25の学習であり、full工程の事例を今回のlight計画へ無条件に移植しない。
- **Key Insight**: 工程資料を除外した差分一覧では「READMEだけ」を証明できない。最終受入は実際のbase/headに対する除外なし全一覧とREADME全patchで確認する（19、27、31行）。工程原本の保全と製品差分限定は独立の条件であり、原本を失う削除や無承認の履歴操作で解決しない（28–35行）。今回の調査報告も工程成果物であって製品変更ではないため、製品限定の評価対象と工程原本の扱いを計画で区別する必要がある。
- **Severity**: high
- **Verification Implication**: 既存例を保持して指定1行だけ追加したことと、他ファイルの製品変更がないことを別に確かめる。過去事例の実CLI実行免除は依頼者固有の判断であり、「README変更なら常に実行不要」という免除には使えない（54、60行）。

#### 2. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 条件付きの周辺知識。2026-11-17の学習。今回CI要件が明示されたわけではないため、新規CI要件や追加実装の根拠にはしない。後工程で検証結果を報告する場合の証拠帰属に関係する。
- **Key Insight**: CI設定の存在、他者による過去headの成功報告、ローカル実行成功、現対象headへの独立CI読取りは異なる証拠である（24–27、33–37行）。READMEや工程文書のcommit後にheadが変われば、以前の検証結果を新headへ付け替えない。検証対象headと報告commitを区別する。
- **Severity**: high
- **Verification Implication**: CI成功を条件・報告に含める場合だけ、その対象headの独立証跡を必要とする。計画段階で現在のCI成功を主張したり、過去の件数を今回の結果として使ったりしない。

### Recommendations
- 実装前に直接関連文書 `docs/solutions/workflow-issues/limited-pr-process-original-preservation.md` の19、27–37、54–60行を読む。成果物限定の確認はREADMEのみへ絞った一覧ではなく、受入対象全体の差分で行う方針を置く。
- 製品変更は指定コードブロックへの指定コマンド1行追加に限定し、既存例・コード・設定・依存を変更しない。工程報告の存在を製品差分限定と混同せず、原本を消す・隠すことで条件達成としない。
- OpenSpec skip_specsは呼出し元の前提として維持する。今回検索した学習にはskip_specsの操作方法・適否を裏付ける記述はなく、本調査からそのCLI手順を推測しない。
- 後工程の検証では指定行の正確性、追加位置、既存内容保持、他の製品変更なしを明示的に確認する。実行確認の要否は今回の受入条件に従い、過去事例の免除を流用しない。
- CI要求がある場合に限り2件目を適用する。今回のlight計画へCI新設・試験改修・追加依存を持ち込まない。

### Scope and Limitations
- 残る4候補は添付拒否、大型証拠配送、状態検証試験の変異注入、入力境界・決定論の試験を扱い、今回のREADME例1行追加との直接の関連が弱いため採用しなかった。
- 今回は学習調査のみ。README・製品コード・設定は変更せず、実CLI・検証スクリプトの実行、GSD判定、commit/push、kanban操作は行っていない。過去文書に記されたhead到達性やCI成功を今回独立確認したものではない。
