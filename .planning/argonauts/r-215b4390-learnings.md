## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済みr-215b4390の計画入力として、README.md最終行に「検証B: v1.12 の通しの確かめ（2026-11-22）」を1回だけ追加するdocs-only作業に関係する学習を調査する。既存内容保持、最終行完全一致、1行差分を守り、コード・試験・新しい試験ファイルは変更しない。工程記録は別に扱う。
- **Keywords Used**: README、docs-only、documentation、workflow、Git、verification、GSD、最終行、追記、既存内容、1行、差分、証拠、head、staged。CONCEPTS.mdを先に全文読み、「検証対象head」「独立検証証跡」「試験の判別力」「要求ステータス」の定義を参照した。
- **Files Scanned**: docs/solutions配下のMarkdown文書5件を内容検索し、候補5件のfrontmatterを確認。関連性を認めた2件のみ全文を読んだ。.gitkeepとディレクトリは文書件数に含めない。
- **Relevant Matches**: 2 files（いずれも隣接する検証・工程上の教訓。README末尾追記やGSD CLIの直接的な手順を示す学習は見つからなかった）。
- **Search Scope**: docs/solutions/のみ。実在する分類はworkflow-issues/とbest-practices/。添付関連2件、トークン化・決定論関連1件はfrontmatter上で今回の変更対象と適用条件が合わず除外した。Compound Packは指定されていない。

critical-patterns.mdはdocs/solutions/patterns/配下に存在しないため、Critical Patternsの内容は補わない。

### Relevant Learnings

#### 1. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 中程度・隣接。2026-11-17の教訓。docs変更や工程記録のcommitにより検証対象headがずれる危険と、工程判定と実行証跡を混同しない点が今回にも関係する。ただし今回にCI要件を追加する根拠ではない。
- **Key Insight**: Guidance 4は「検証対象headと報告commitは別のものとして扱い、記録にも両方を別々に残す」とする。Examples 1はSUMMARY存在判定・requirements.ready-ids判定をCI成功証跡と区別している。したがって公式GSD CLIの判定はその判定範囲に限って記録し、READMEの最終行一致・一度だけの追記・既存内容保持の実検証を代替させない。後続工程でheadが変わる場合は、過去の合格を無条件に転用しない。
- **Severity**: high

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 中程度・隣接。2026-11-17の教訓。既存内容保持・変更範囲の限定を確かめる際、ファイル名の状態表示だけでは内容差分を保証できないという点が参考になる。新しい回帰試験・scratch環境を作る作業自体は今回の範囲外。
- **Key Insight**: ContextとGuidance 3は、未追跡ファイルの内容変更はgit statusのパス表示だけでは見えず、偽合格になり得ると説明する。今回の計画ではstatusや既存試験の成功だけで「READMEに1行だけ追加」を証明せず、READMEの比較基底と実内容差分を直接照合する。記事のgit add -Aは一時試験リポジトリの基底固定手順であり、この作業ツリーを一括stageする指示ではない。
- **Severity**: medium

### Recommendations
- **変更範囲を固定する**: README.mdへの承認済み1行追加だけを製品側の変更とし、コード・既存試験・新しい試験ファイル・無関係な整形は触らない。学習調査やPLANなどの工程記録をREADMEの1行差分と混同しない。この制約は今回の依頼によるもので、過去学習から新しい試験追加要件を導かない。
- **内容検証と工程判定を分離する**: Builder・品質はREADMEについて、既存内容が保持されること、追加文字列が完全一致すること、対象行が1回だけ存在し最終行であること、追加1行・削除0行であることを個別に確認する。計画段階では未作成の検証コマンドを試さない。PLANには、実在を確認した検証ファイルに基づいてBuilder・品質が実行できるコマンドを記す。
- **公式CLIに基づく範囲限定の判定**: GSDの判定は公式CLIで行い、必要なJSONの確認はread_file、項目抽出は利用可能ならjqを使う。学習文書に今回使用すべきGSDコマンドの根拠はないため、構文を創作しない。本調査ではGSD判定やREADME実装検証は実施していない。
- **証拠の帰属を保つ**: 後続の判定・報告時は検証対象headと記録の対象を照合し、工程記録によるheadの変化を区別する。公式CLIの成功・既存試験の成功だけでREADMEの受入条件を充足したと報告しない。CIは今回の条件にある場合だけ独立した対象head証跡を要求し、過去のREQ-07を今回へ移植しない。
- **実装前に読む資料**: 上記2文書のGuidanceとExamples。歴史的な試験行番号・commit・CI runは本調査では現状と照合しておらず、今回の証跡として転用しない。frontmatterにstatus: staleの指定はないが、過去の記録と現在の検証結果は別扱いとする。

### Research Boundary
本調査はdocs/solutionsの学習抽出と本ファイルの保存のみ。README.mdの編集、検証ファイル作成・実行、GSD判定、commit、push、kanban操作は行っていない。README末尾への厳密な1行追記について直接の学習は見つからず、実装・品質完了後に固有の再利用可能な発見があれば学習化を検討できる。
