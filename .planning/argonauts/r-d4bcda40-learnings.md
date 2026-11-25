## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み wordfreq `--max-count` のGSD計画向け調査。整数・省略None・包含上限、minとの積集合、filter-before-top、元Counter/HTML総数不変、引数exit2/入力exit1、0・負数・min>maxは空集合exit0、固定期待値RED/GREEN、独立CLI/HTMLブラウザ検証、README例を対象とする。既存API/抽出/casefold/同数初出順/安全性を維持し、依存・CIは変更しない。
- **Keywords Used**: wordfreq, CLI, Counter, filter, min-count, max-count, top, argparse, HTML, security, deterministic, PYTHONHASHSEED, input-boundary, verification, test-discrimination, workflow, 検証, 試験, 順位, 入力。
- **Files Scanned**: docs/solutions内のMarkdown学習文書5件（全件に対してcontent-search、5件のfrontmatter確認、採用4件を全文読了）。ディレクトリ2件と.gitkeepは文書件数に含めない。
- **Relevant Matches**: 4 files（実装・回帰への直接関連1件、試験判別力への応用1件、独立検証・証拠配送の隣接学習2件）。packs指定なし、探索なし。
- **Grounding**: `CONCEPTS.md` 全文を先に確認。「決定論的順位」「純粋なHTML整形」「試験の判別力」「検証対象head」「独立検証証跡」「決定論的再実行」の現行定義で解釈した。
- **Search Evidence**: 発見された `best-practices/` と `workflow-issues/` の両方を含む全ツリーを検索。大文字小文字を区別しない `(title|tags|module|problem_type):.*(wordfreq|cli|counter|filter|test|verification|security|deterministic|workflow|検証|試験|順位|入力)` と、YAMLリスト条件 `^\s*- .*(argparse|html|counter|top|count|入力|検証|試験|決定論)` の独立検索はそれぞれ同じ5文書を返した。候補は3件以上25件以下のため追加fallback不要。`patterns/critical-patterns.md` はファイル検索で不存在。
- **Excluded Candidate**: `docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md` はfrontmatterを確認したが、今回の計画調査では添付拒否/原本同一性の事故が発生しておらず弱関連として除外。配送一般の重複は下記3で扱う。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 共通選択の追加が抽出/casefold/同数順を壊さないこと、およびtext/json/htmlの決定論的再実行を計画する根拠になる。
- **Key Insight**: 入力境界・正規化・集計・整形を混ぜない。単一シードでの成功は決定論の証明にせず、複数PYTHONHASHSEEDで試験と実CLIの出力を照合する。
- **Severity**: medium
- **Current-evidence conflict**: 2026-11-17の記事34行および55–57行の「同数はコードポイント昇順」は旧契約。`CONCEPTS.md:49–51` はr-50053edcで正規化後の初出順へ置換済みと明記し、現行 `wordfreq/aggregator.py:11–17` も回数だけの安定ソートで確認できる。frontmatterにstale指定はないが、この箇所を現行指針として採用しない。順序を辞書順へ戻す実装/期待値は不可。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 固定期待値のRED/GREENを「実際に狙った回帰を検出する」試験へ落とすための応用学習。git状態試験の詳細は、それを新設/改修する場合のみ適用する。
- **Key Insight**: 試験自身の設計不良による失敗と、製品の狙った失敗を区別する。検出すべき失敗の種ごとに判別力を示し、1種のREDを別の種へ流用しない。変異を使うなら使い捨てコピーだけに置く。git状態比較を扱う場合はcold copy・環境汚染除去・ステージ済み基底が必要で、未追跡ファイルの内容変更をstatusだけで検出できると思わない。
- **Severity**: medium
- **Planning implication**: 「上限を適用しない」「包含を排他的にする」「top後にfilterする」「元Counter/総数を書換える」を異なる検出対象として固定期待値を設計する。今回この調査では試験の実行や変異注入はしていない。

#### 3. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 独立CLI/HTMLブラウザ検証を計画に含めるため、コード上の構造試験だけでなく画像・通信・原本の保存先と受渡しを先に設計する必要がある。製品のmax-countロジックそのものの学習ではない。
- **Key Insight**: 保存済み・標準添付済み・受取側で原本読取り済みは別gate。別profile内の絶対pathと要約だけでは受取側の確認は成立しない。画像閲覧・SHA照合・製品試験の実施者を分離して記録する。過去のmin-countで人が認めたPNG閲覧代替はその依頼限定で、今回への恒久的免除ではない。
- **Severity**: high
- **Current corroboration**: 現行 `docs/wordfreq-min-count-verification.md:102–124` は全AC索引、配送3gate、head更新時のfresh rootでの全品質gate再実行を明記している。これは先行min-countの現行文書であり、max-countの新しい受入条件を無条件に追加する根拠ではない。

#### 4. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 品質の独立性と検証対象headへの証拠帰属を計画する際の隣接学習。CI実行結果そのものが要求される場合にだけCI固有のgateを適用し、今回の「CI変更なし」を破らない。
- **Key Insight**: ローカル試験成功、workflowの存在、人の過去headの成功報告を、現在の対象headに対する独立CI証跡と混同しない。報告直前に検証対象headを再解決し、検証対象headと報告commitを分ける。過去原本のheadの付替えは不可。
- **Severity**: high

### Recommendations
- **実装前に読む資料**: 最優先は学習1・2と `CONCEPTS.md`。独立品質/証拠受渡し担当は学習3・4、および既存 `docs/wordfreq-min-count-verification.md` の対応する原本・head・配送規則を確認する。先行カードの件数/承認/headを今回の期待値に転用しない。
- **変更境界**: 現行 `wordfreq/__main__.py:34–44` は元counts→元total→min選択→top→HTMLの順。上限はminとの共通選択に組み込み、選択前の元Counter/totalは維持する。現行 `wordfreq/aggregator.py:11–17` と `wordfreq/formatters.py:22–33` のAPI、初出順、純粋整形は変えない。None判定を明示し、0を「未指定」とみなすtruthiness処理を避ける（これは今回の承認条件からの具体化であり、既存学習にmax-count実装例があるわけではない）。
- **固定期待値の試験計画**: 未指定/Noneと包含上限、minとの積集合、min=max、min>max、max=0/負数、全除外/抽出0語、同数初出順、text/json/html一致を表にする。高頻度語を上限で除いてからtop1に低頻度の適格語が繰り上がる入力を置き、top-before-filterの偽合格を防ぐ。空集合でもexit0、HTMLの元総数/メタ情報/見出し/安全な空表示を固定期待値にする。
- **エラーと安全性**: 非整数・非数値・値欠落は引数exit2、有効上限での入力失敗はexit1として分離する。既存min引数の制約を上限へ機械的にコピーして0/負数をexit2にしない。basename限定、動的値の一度だけのescape、固定属性/CSS、UTF-8出力と通信安全性は現行HTML契約を維持し、構造試験の成功をブラウザ実閲覧/通信観測の代わりにしない。
- **順序・実行責任**: Builderが実在する検証ファイルに固定期待値を作成し、狙ったアサーションのREDを記録してから最小実装しGREENへ進む。品質は同じファイルに加えて独立CLI/HTMLブラウザ確認を自ら行い、実施者・対象head・原本pathを残す。決定論を主張する範囲は複数シードで確認する。計画段階では未作成のコマンドを試さず、PLANの検証コマンドは実装された検証ファイルから実行可能なものとしてBuilder/品質へ渡す。
- **範囲と未実施**: この成果物は学習調査のみ。GSDの状態判定/計画作成/試験/CLI/ブラウザ/CI検証、commit/push/kanban操作は実施していない。GSD判定が後工程で必要な場合は公式CLIを用いる。本調査は検証合格や要求Completeを意味しない。製品差分は引数・共通選択・最小README例に留め、依存/CI/抽出/順位/見た目の変更を広げない。
