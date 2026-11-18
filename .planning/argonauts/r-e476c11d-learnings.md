## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済みOpenSpec `r-e476c11d-wordfreq-min-count` をGSDへ取り込み、実装せずに計画するため、min-count変更に適用できる既存学習を調査する。
- **Keywords Used**: wordfreq、argparse、min-count、正整数、入力境界、Unicode casefold、top、決定論的順位、同数初出順、HTML総数、静的安全性、既定互換、baseline、test-discrimination、PYTHONHASHSEED、独立検証証跡、検証対象head、PM-readable、evidence-handoff、標準添付、原本同一性。title/tags/moduleの技術軸とtitle/tags/problem_typeのworkflow・evidence軸を大文字小文字無視で並列検索した。
- **Files Scanned**: 5 total files（`docs/solutions/` 配下の学習Markdown全5件を内容検索し、候補5件のfrontmatterと本文を読了。.gitkeep・ディレクトリは件数から除外）。
- **Relevant Matches**: 5 files（入力・順位1件、試験判別力1件、独立証跡1件、配送2件）。

根拠の用語は先に読んだrepo rootの `CONCEPTS.md` に従う。検索rootは当該repoの `docs/solutions/` のみ。実在した分類は `best-practices/` と `workflow-issues/` であり、技術と工程をまたぐため両方を検索した。Compound Packは対象外。

`docs/solutions/patterns/critical-patterns.md` は存在しない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: min-countを正規化前の個別表記に適用するとcasefold合算後の閾値契約を壊す。閾値除外・top追加後も、既定トークナイザと決定論的順位を維持する必要がある。
- **Key Insight**: トークン境界、差し替え境界、正規化を分離し、Unicode・数字・下線・CJKを既存契約のまま扱う。計画ではcasefoldで合算したcountsへ閾値を適用し、その後topで制限する。複数のPYTHONHASHSEEDによる試験・実CLIの一致は決定論の確認として引き継ぐ。ただし本文34行・55–57行の「同数はコードポイント昇順」は2026-11-17のPhase1契約であり、現在の `CONCEPTS.md:49–51` の「頻度降順、同数は正規化後の初出順」と衝突する。旧ソートキーをコピーしてはならない。Counterの初出挿入順を保つ安定ソートの現行契約を優先する。
- **Severity**: medium

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 既定互換・入力不変を回帰試験にしても、比較対象と判別力が不十分なら偽合格する。新しいmin-count試験でも「通った」だけでなく、要求違反を見分けられる設計が必要。
- **Key Insight**: 状態比較を使う場合はcold scratchコピーを作り、scratch内でgit init→git add -A→比較基底保存の順にする。未追跡ファイルのパスだけの比較では内容改変を検出できない。既存内容変更と想定外生成物は別々の変異として判別力を示す。この教訓のstaged baselineは状態試験内部の基底であり、今回必要な「最初の製品変更前に保存する出力・画像baseline」とは別物。後者を実装後に取り直して代用しない。変異注入は将来の担当がscratchだけで行い、製品worktreeを変異状態にしない。
- **Severity**: medium

#### 3. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 本件は独立品質のCLI・ブラウザ証拠と変更前後の画像をPMへ渡すため、品質profileに原本があることやJSON索引だけでは受入の完了にならない。
- **Key Insight**: 「保存済み」「標準添付済み」「受取側で読取り済み」を別々のgateとして計画する。raw・derived・CLI入出力・通信原本・画像の相対path対応、対象head/run/root、SHA一覧を保つ。PMのread_file等で原本を読める形式を先に確認し、archiveのみで展開不能なら許可された個別配送または人の安全展開を求める。品質の画像実閲覧、PMの文書照合、人のSHA照合は実施者を区別する。SHA一致だけでPNG可読性や品質合格を主張しない。
- **Severity**: high

#### 4. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 独立品質CLI・ソース順序・ブラウザ観測をBuilderの要約や過去の成功で代用しないための工程設計に適用する。CIそのものを要求する場合にだけCI固有の充足条件も適用し、今回CI変更を追加する理由にはしない。
- **Key Insight**: 証拠の量ではなく要求との対応と検証対象headで判定する。CI定義、歴史的headの人の成功報告、ローカル合格は最新headの独立CI成功ではない。同様に構造試験は独立ブラウザ証拠へ転用できない。品質担当自身の読取り・実行結果を要求別に残し、判定・報告前にheadを照合する。報告用文書更新でheadが動いた場合、旧証拠を新headへ黙って流用しない。本文のREQ-07や旧head/runは歴史的事例で、本件を充足済みとする証拠ではない。
- **Severity**: high

#### 5. 検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す
- **File**: docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md
- **Module**: 検証証拠の受け渡し（Argonauts カード添付・検証成果物の原本）
- **Problem Type**: workflow_issue
- **Relevance**: PM向け添付原本の引継ぎでフック拒否・保存path誤記が起きた場合の停止条件を事前に定義できる。拒否発生時に適用する条件付き学習。
- **Key Insight**: 拒否を圧縮・リネーム・形式変更・URL化で迂回しない。具体的な拒否理由と原本所在地を記録し、人に正規の提供を求める。原本同一性は名前でなくバイト列・SHAで確認し、拒否と後続の解消は別記録にする。2026-11-17の本文31行はGit原本のpushを推奨するが、2026-11-18の配送学習と `CONCEPTS.md:35–39` では原本はGit管理の有無を問わない。本件の大型raw/画像をすべてGitへ入れる必須条件にはせず、許可された原本保管・標準配送を計画する。本調査に対するcommit/push禁止は維持する。
- **Severity**: high

### Recommendations

以下は既存学習からの計画上の含意と、呼出し元が与えた承認済み制約を分けて組み合わせた提言であり、現在の実装や検証成功を確認したものではない。

1. **baseline保存を最初の製品変更の前提gateにする（呼出し元の決定）。** 変更前head・入力・CLI引数・環境を記録し、全3形式text/json/htmlの既定出力とDPR1の1280x900／320x900画像を保存してから製品変更へ進む。変更後は同条件で比較する。保存担当、保存先、比較方法、品質側の独立読取り、PM配送までの順序をPLANで明示する。学習2の状態試験用基底と混同しない。
2. **入力取得前の失敗と処理順序を別々の受入観点にする（呼出し元の決定＋学習1・2）。** min-count既定1、正整数のみ、異常値は入力取得前exit2とする。異常値の結果だけでなく入力取得が呼ばれていないことを検出する試験と、品質によるソース順序確認を計画する。正規化counts→閾値未満除外→順位付け・topという順序を固定し、casefold合算で境界を越える例、閾値ちょうど、全件除外、同数初出順、topとの併用、既定省略と明示1を区別する。未作成試験を本調査で実行しない。
3. **HTMLの集計値と表示行の責務を分ける（呼出し元の決定＋CONCEPTS）。** 総数はフィルタ・top適用前の元countsから算出し、format_htmlには既に選別されたpairsと元総数を渡す。既存の純粋なHTML整形契約を維持し、再集計・I/O・並べ替えを持ち込まない。全件除外時も元総数・メタ情報・見出しを保つ観点を含める。静的安全性はCLI出力やDOM構造だけで満たしたことにせず、独立ブラウザの通信等の必要原本を品質が残す。見た目・CI・依存は変更しない。
4. **要件ごとの証拠と担当をPLANで分離する（学習3・4）。** Builderの回帰試験、品質の独立CLI、品質のソース順序確認、品質のブラウザ実閲覧・通信観測、既定出力・画像比較、PMの原本照合は相互代用しない。品質が確認する対象headと原本を結び付け、報告前のhead照合を含める。要求の証拠が不足すればPending/gapsを維持し、何の原本が欠けるかを書く。
5. **検証ファイル作成と実行の依存関係を明記する（呼出し元の制約）。** PLANに記す検証コマンドは、Builder・品質が実在する検証ファイルから実行する流れにする。未作成コマンドの試走、インラインスクリプトやヒアドキュメントによる代用を計画確認に使わない。GSD状態を判断する場合は公式CLIで確認し、ファイルの存在や過去のSUMMARYだけで完了と推定しない。本調査はGSD状態の判定を行っていない。
6. **PM配送を完了条件に含める（学習3・5）。** 原本manifestに要求との対応・相対path・対象head/run/root・SHAを含める。標準添付後の読取り確認と、PMが利用できる形式での原本照合を別工程にする。配送不能なら具体的な能力不足・拒否理由を記録し、迂回や原本の手修正で解消しない。

実装前の優先読書は学習1（旧同率ソートの注意込み）・学習2、品質と引継ぎ前の優先読書は学習3・4・5。検索した学習にはmin-count機能自体の専用事例はなく、既存の入力・決定論・試験・配送の原則を本件へ適用した。ソース・承認済みOpenSpec本文・GSD状態は本調査の検索対象外であり、呼出し元の決定との実装整合や実行結果は未検証。

本作業は本報告ファイルの保存のみ。製品実装、検証コマンド実行、Git commit/push、Kanban操作は行っていない。
