## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済みのREADME末尾1行追記をGSDで計画するため、既存学習から制約・検証上の注意を抽出する。指定行は `検証A: v1.12 の通しの確かめ（2026-11-22）`。かぎ括弧・句点を加えず、既存内容・改行を保持し、コードと試験ファイルは変更しない。
- **Keywords Used**: README, documentation-only, exact-match, CLI, verification, evidence, git, scope classification, workflow, conventions, head, 検証, 証跡, 差分, 末尾, 追記, 計画。
- **Files Scanned**: 5 total files（`docs/solutions`配下のMarkdown全5件を検索し、候補5件のfrontmatterを確認。関連3件を全文読了。`.gitkeep`とディレクトリは件数に含めない）。
- **Relevant Matches**: 3 files（いずれも隣接知見。READMEの完全一致・末尾追記、GSDのscope分類、既存CLI限定を直接定める学習は見つからなかった）。

検索手順・範囲:
- 先にrepoルートの `CONCEPTS.md` を全文読み、検証対象head・独立検証証跡・試験の判別力の用語を確認した。
- 学習の検索範囲は指定どおりこのrepoの `docs/solutions` のみ。発見した分類は `workflow-issues/` と `best-practices/`。知見が工程と検証を横断するため全体を対象にした。
- 大文字小文字を区別しないfrontmatter検索を並列実施した。使用パターンは `(title|tags|module|problem_type):.*(readme|documentation|workflow|convention|verification|evidence|git|scope|検証|証跡|差分)` と `^\s*- .*(CLI|exact|documentation|head|検証|末尾|追記|計画|README)`。各検索で5件が一致し、統合候補は5件だった。候補3件未満・25件超の条件には該当しない。
- `attachment-refusal-git-original-and-human-standard-reattachment.md` と `pm-readable-evidence-delivery.md` は添付経路・原本配送に関する知見であり、今回は保存のみで添付操作がないため弱一致として除外した。
- `docs/solutions/patterns/critical-patterns.md` はファイル探索結果に存在しなかった。

### Relevant Learnings

#### 1. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 中程度。README追記にCI必須という要件を追加する根拠ではないが、工程文書の更新と利用者変更を伴う工程で、検証証跡の対象を取り違えないために有効。
- **Key Insight**: 「証拠の『量』ではなく『対象』で判定する」（Guidance 5）。検証対象headと報告commitを別に記録し、判定直前に対象を照合する。計画ファイルの存在やCLIによる計画形式の合格は、READMEの文字列・末尾・差分の充足証拠にはならない。
- **Severity**: high

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 中程度。README追記の差分確認に対し、状態一覧だけで内容保持を証明しないという注意が適用できる。scratch回帰試験の新設・変異注入・ステージ操作そのものは今回の作業には適用しない。
- **Key Insight**: 未追跡ファイルでは「git status がパス名だけを報告するため内容変更が不可視」（Context）。ファイル一覧・状態確認と、README内容の差分確認を分ける。工程文書を含む全体の状態と、利用者変更であるREADMEの差分を区別して記録し、statusだけで既存内容保持や1行のみの追記を合格にしない。
- **Severity**: medium

#### 3. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 中程度の隣接知見。今回に使うのは、テキストの表示上の一致とバイト不変・改行方針は別という部分のみ。アプリのトークナイズ・順位付け・決定論試験は対象外。
- **Key Insight**: 「読み取り層は『読み取り専用』と『改行方針』を明示して固定する」（Guidance 4）。READMEの既存内容・改行を保持する要求は、追記文字列が見えることだけでは満たせない。追記前の改行状態を把握した上で、既存部分を変えず末尾に指定の1行だけが追加されたことを別に確認する。
- **Severity**: medium

現行資料との衝突: 上記3は2026-11-17の学習であり、本文の同率順位「語のコードポイント昇順」は、現在の `CONCEPTS.md` の「決定論的順位」（同一頻度では正規化後の初出順、旧Phase1契約を意図して置換）と異なる。旧順位契約を現行指針として採用しない。抽出した改行・バイト保持の注意とは別論点であり、今回コード変更には転用しない。3件ともfrontmatterに `status: stale` の指定はないが、それだけで本文全体の現行性を保証しない。

### Recommendations
- 実装担当が事前に読む優先箇所は、知見1のGuidance 4–5、知見2のContextの未追跡基底に関する説明、知見3のGuidance 4。全文の試験新設手順を今回へ機械的に持ち込まない。
- 計画では、利用者変更はREADMEへの指定行 `検証A: v1.12 の通しの確かめ（2026-11-22）` の末尾追記のみと明示する。コード・試験ファイルの変更禁止、かぎ括弧・句点を加えないこと、既存内容・改行の保持は呼出元の制約であり、既存学習から発見した規則とは区別する。
- 工程文書の生成・変更は利用者変更と別に列挙する。差分確認は全体の変更範囲とREADME内容の両方を扱い、工程文書があることを理由にREADME以外の製品変更を許容しない。
- 検証条件を「指定行の完全一致」「ファイル末尾」「追記以外の既存内容・改行不変」「コード・試験ファイルの変更なし」に分ける。部分一致検索、状態一覧、計画形式の合格のいずれか一つで全条件を満たしたとしない。
- 呼出元指定に従い、GSDの判定は公式CLI、ファイル・JSON確認は `read_file`、項目抽出は利用可能なら `jq` とする。既存CLIを用い、インライン実行・ヒアドキュメントスクリプト・新規試験の追加で制約を迂回しない。PLANに検証ファイルの実行を書く場合は、実在するファイルを読んで確認してからBuilder・品質へ渡す。
- 本調査は学習の検索と保存のみ。GSDの判定やREADMEの実装・検証コマンドは実行しておらず、具体的な検証ファイルの存在・CLIの利用可否・READMEの現状を確認済みとは主張しない。該当する直接知見がないREADME追記・scope分類の運用は、完了後に実証に基づく学習化の候補となる。
