## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: `wordfreq --exclude FILE` の承認仕様をGSD計画へ取り込む前の学習検索。実装・試験実行・GSD状態判定は行わず、計画への参考入力を整理する。
- **Keywords Used**: wordfreq, Python CLI, argparse, UTF-8, Unicode, `\w+`, fullmatch, casefold, exclude/exclusion/除外, 入力境界, 本文取得前, exit2, regression/baseline/回帰, HTML total, min-count/top, 初出, stable/determinism, test-first, code-implementation, workflow。決定事項は新依存なし・CI変更なし・HTML見た目変更なし。
- **Files Scanned**: 6 Markdown files。`docs/solutions/` 全木を探索し、6件とも検索候補としてfrontmatterを読取り、関連3件は全文を読んだ。`.gitkeep` とディレクトリは件数に含めない。
- **Relevant Matches**: 3 files（直接関連2件、証拠運用に条件付きで関連1件）。
- **Search Root**: このworkspaceの `docs/solutions/` のみ。追加pack、別workspace、製品コード、工程履歴への検索拡大なし。
- **Vocabulary Grounding**: repo直下の `CONCEPTS.md` を全文読取り。「既定トークナイザ」「トークナイザ差し替え境界」「決定論的順位」「純粋なHTML整形」「決定論的再実行」「試験の判別力」「検証対象head」の定義を使用。
- **Search Evidence**: 実在する分類は `best-practices/` と `workflow-issues/`。領域横断のため両方を検索。大文字小文字を無視して (1) title/tags/module/component の wordfreq・Python・CLI・Unicode・入力・順位・検証・baseline 類、(2) problem_type の best_practice/test_failure/logic_error/workflow_issue と applies_when相当のリスト項目、を並列検索した。候補はそれぞれ5件・6件、重複除去後6件。補足として全文の exclude/exclusion/除外/argparse/UTF-8/fullmatch/casefold/total/min-count/初出/exit2 を検索し5件が一致したが、新候補はなかった。
- **Critical Patterns**: `docs/solutions/patterns/critical-patterns.md` はファイル探索に存在しない。
- **Not Selected**: 添付拒否、PM可読配送、限定PRの工程原本保全の3件はfrontmatterの適用条件が今回の除外処理設計・回帰試験と一致しないため除外。Kanban操作・commit・pushは実施していない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 強い関連。Unicodeの入力境界、casefold、集計との責務分離、読み取り専用性、出力順の決定論が除外機能の影響範囲と重なる。
- **Key Insight**: 語の境界・正規化・集計を分けて試験し、CJK連続、数字、下線、句読点、空入力の認識違いを防ぐ。入力ファイルのバイト不変と改行方針も試験対象。決定論を主張する場合は単一シードの反復で済ませず、異なる `PYTHONHASHSEED` で試験と実CLIの一致を示す（本文31–36行）。
- **Severity**: medium
- **Currency / Conflict**: 2026-11-17の学習。本文34行および例は旧契約「同率は語コードポイント昇順」を推奨するが、現在の `CONCEPTS.md:49–51` と今回の承認コンテキストは「頻度降順、同率は正規化後の初出順を安定保持してからtop」を明示する。旧ソート例をコピーしてはならない。現行用語集ではCounter挿入順と回数だけの安定ソートが契約であり、set経由の再構築などで初出履歴を失わないことが重要。frontmatterに `status: stale` はないが、この部分は後続契約に置換されている。製品コードとの照合は検索範囲外のため行っていない。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 強い関連。除外ファイルと本文入力の不変性、既存CLI回帰基底、試験が不具合を本当に検出するかの計画に関係する。Git状態比較の具体手順は、その方式の試験を追加・変更する場合だけ適用。
- **Key Insight**: 単なる成功実行では試験の判別力を証明できない。状態比較には無変異時の成功と、失敗種ごとの隔離コピーでの期待アサーション失敗が必要。未追跡基底では既存ファイルの内容変更が見えず偽合格するため、使い捨てリポジトリの比較基底をステージ後に固定する。cold copyと継承環境の制御も重要（本文31–44行）。本workspaceへのステージ操作を求めるものではない。
- **Severity**: medium
- **Currency**: 2026-11-17。過去の試験path・行番号と実測件数は歴史的情報であり、今回の実在確認・実行結果として扱わない。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 条件付きの隣接学習。今回CI変更は対象外であり、この学習から新しいCI要求を追加しない。既存の受入条件にCI実行成功が含まれる場合の証拠区別と、品質への引継ぎに役立つ。
- **Key Insight**: ローカル試験成功、設定ファイルの存在、過去headの人からの報告、検証者による対象headの独立CI読取りは別の証拠。要求が必要とする証拠種に対応づけ、検証対象headと報告commitを区別する（本文22–37行）。
- **Severity**: high
- **Currency**: 2026-11-17。記載された43件成功等は過去の結果であり、今回の回帰基底件数や検証結果ではない。

### Recommendations
- **制約・実装パターン**: Builderはまず上の直接関連2件を読む。承認仕様の「Unicode `\w+` fullmatchによる検証、その後casefold」を、本文の最長一致トークナイズと混同しない。学習は境界の分離を裏付けるが、除外ファイルの文法そのものを定義してはいない。新依存・CI変更・HTML見た目変更は加えない。
- **順序リスク**: 除外集合の構築は本文取得より前という承認条件を独立した観測可能な試験にする。無効な除外入力と未取得本文を組み合わせて、単にexit2になるだけでなく本文取得が呼ばれなかったことを確認する設計が有効。これは今回の承認条件からの提案であり、過去学習に除外機能の実績があるという意味ではない。
- **test-firstの構成**: 除外ファイル読取り・文法/正規化、集計からの除外、実CLIのエラー優先順位/exit2、既存出力の非回帰を分ける。UTF-8異常、Unicode/CJK、数字・下線・句読点、casefoldの境界などを承認仕様へ対応づける。改行や空行等の詳細は承認仕様を優先し、過去文書から未承認の振舞いを補わない。
- **回帰基底と判別力**: 変更前の実在する回帰試験と実行結果をBuilderが記録し、変更後と比較する。入力不変の試験では除外ファイルと本文の双方を対象にする。Git状態比較を扱う場合に限り学習2の隔離基底・失敗種別の判別力を適用し、製品作業ツリーへ変異を入れない。
- **順位・絞込み**: 同率語を初出順と辞書順で逆にしたfixtureを用意し、casefold後の同一語の再出現・除外・min-count・topの組合せでも残存語の初出順が保たれることをtext/json/htmlで確認する。旧学習のコードポイント昇順に戻さない。決定論の証明には異なるハッシュシードでの実行を含める。
- **HTML**: `CONCEPTS.md:53–55` の純粋なHTML整形契約に従い、formatter内で除外ファイルを読んだり再集計したりしない。今回の承認条件であるHTML original total、min-count/topとの関係を期待値付きで固定する。過去学習には除外導入後のtotal計算位置の根拠がないため、詳細は承認仕様から直接転記し、ここで新定義を作らない。
- **検証コマンド**: この調査では未作成の検証コマンド・インラインスクリプト・テストを実行していない。PLANに記載する実行コマンドは、Builder・品質が実在する検証ファイルを確認して実行できるものへ結びつける。GSD状態判定が必要になった担当者は公式CLIを使用する。本調査はGSDの状態や計画の妥当性を判定していない。
- **学習の空白**: `--exclude FILE`、argparseの除外オプション、除外ファイルのfullmatch、本文取得前の検証、exit2、除外時のHTML original totalについて直接の既存学習は見つからなかった。実装・独立検証後に、承認仕様との対応と実際に起きた落とし穴を耐久的な学習として記録する候補になる。
