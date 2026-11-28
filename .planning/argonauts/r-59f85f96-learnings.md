## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: README.md「wordfreq の実行」の既存コードブロックへ `python -m wordfreq input.txt --top 5 --format text` を1行追加するlight計画。製品変更はREADME.mdのみ、既存記述を保持し、工程原本はPR含有可能。
- **Keywords Used**: README, documentation/doc, CLI, wordfreq, exact diff, test-first/test, workflow, 実行例, 既存記述。title/tags/module/problem_typeとapplies_when相当のリスト行を大文字小文字を区別せずsearch_filesで検索。
- **Files Scanned**: docs/solutions配下の学習Markdown 6ファイルを検索・frontmatter確認。うち関連原本2ファイルを全文確認。ディレクトリと.gitkeepは学習件数に含めない。
- **Relevant Matches**: 2ファイル（直接関連1件、試験設計の隣接関連1件）。
- **Search Scope**: このrepoのdocs/solutionsのみ。packsなし。実在カテゴリはworkflow-issuesとbest-practices。候補は6件で、候補不足の追加検索条件には該当しない。
- **Grounding**: repo直下CONCEPTS.mdを全文確認。「試験の判別力」「検証対象head」「原本同一性」を用語の基準とした。
- **Critical Patterns**: docs/solutions/patterns/critical-patterns.mdは探索結果に存在しない。

### Relevant Learnings

#### 1. 限定PRの整備は工程原本の保全を先行し、新headの全差分を独立確認する
- **File**: docs/solutions/workflow-issues/limited-pr-process-original-preservation.md
- **Module**: README限定PRと工程原本の保全
- **Problem Type**: workflow_issue
- **Relevance**: READMEへの1行追加、既存記述保持、製品変更範囲と工程原本の区別が直接一致する。ただし原本（2026-11-25）の過去依頼は「PR全体がREADMEだけ」を要求しており、今回の「工程原本はPR含有可能」とは条件が異なる。
- **Key Insight**: 保存対象の一覧と受入対象の全変更一覧を混同しない（27–31行）。過去の実例ではREADMEの全patchと両原本を確認して指定例1行・既存保持を別々に判定した（54行）。今回も製品差分と工程差分を区別して全体を把握するが、工程原本を含むだけで違反とはしない。過去事例のPR限定化・削除・履歴操作を今回に持ち込まない。
- **Severity**: high
- **Verification implication**: 製品pytestでは工程原本保全や文書差分の条件を証明できない（37行）。過去依頼で実行対象外だった事実を「README変更なら常にCLI実行不要」へ一般化しない（60行）。確認結果は確認した版に帰属させ、後の変更へ自動転用しない。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: test-firstとexact diff確認に対して「検査が実際に違反を検出するか」という原則が隣接関連。原本（2026-11-17）はGit状態検査の学習であり、README専用試験の既存実装や必須手順を述べるものではない。
- **Key Insight**: 試験が通るだけでは判別力の証拠にならない。期待する失敗を使い捨てscratchコピーへ注入し、期待する主張で失敗することを確認する。検出対象の失敗種ごとに証明し、作業ツリーや製品コードを変異状態にしない（37–44行）。
- **Severity**: medium
- **Verification implication**: READMEへの適用案は、対象行未追加の初期状態で検査が失敗し、追加後に通ることを確認すること。さらに既存行削除や別箇所への追加をscratch側で検出できれば、それぞれの保持・配置条件の判別力を示せる。これは学習からの適用案であり、今回それらを実行済みとは主張しない。原本のgit init/add手順は今回の調査では実行しない。

### Recommendations
- light計画では、対象見出し配下の既存コードブロック内に指定文字列をそのまま1行追加すること、既存内容を削除・変更しないこと、製品変更がREADME.mdだけであることを別々の受入条件にする。
- test-firstの確認は文書契約に合わせる。単なる全README内の文字列存在確認では配置・既存保持を証明できないため、対象ブロックと元内容との差分を確認対象にする。製品コードや恒久的なテストファイルの追加を前提にしない。
- 工程原本を含む全体と製品差分を明示的に分ける。今回許容された工程文書を除去して、過去依頼の「PR全体README限定」を再現しようとしない。
- 関連原本として上記2文書を実装前の参照先とする。README実行例追加に特化した既存の学習原本は見つからなかった。
- 残る4文書はfrontmatter等で選別した。CI依存要求、添付拒否、受取PMへの大型証拠配送、トークナイザ・出力順の学習は今回の1行追加の直接条件ではないため採用しない。CI要求や添付要件を新設せず、現行の順位契約へ過去のコードポイント順を持ち込まない。

### Research Boundaries
- 実施したのは学習探索と本調査文書の保存のみ。README本文・製品実装・参照先の歴史的工程原本は今回の探索範囲外であり、現状実装や実行例の動作を検証したものではない。
- Kanban操作・git操作・CLI実行・テスト実行は行っていない。学習原本の事例を今回の検証証拠として扱わない。
