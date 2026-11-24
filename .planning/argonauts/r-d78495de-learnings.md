## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: r-d78495de の README 使い方に `python -m wordfreq input.txt --min-count 3` を1例追加する計画。README限定、既存末尾行保持、原本文字差分、最終PR全変更一覧、工程文書カード添付、GSD full を扱う。
- **Keywords Used**: README, wordfreq, --min-count, workflow, documentation, evidence, git, head, attachment, 原本, 添付, 工程, 検証, 変更, 差分。
- **Files Scanned**: 5 total files（docs/solutions/ のMarkdown全5件を内容検索し、候補5件のfrontmatterを読取り。関連3件を全文読取り。.gitkeepとディレクトリは件数外）。
- **Relevant Matches**: 3 files（工程への強い関連1件、隣接・条件付き2件）。
- **Grounding**: repo root の CONCEPTS.md を全文読取り。「検証対象head」「標準添付」「原本同一性」の定義を採用。検索rootは docs/solutions/ のみ。実在する分類は workflow-issues/ と best-practices/ で、領域横断のため全ツリーを検索した。Compound Packは指定なし。
- **Decision boundary**: 2026-11-25T06:53+09:00 の判断を優先する。受入は指定例1つの追加と、最終PR全変更が README.md のみであること。text/json/html実行と証拠作成は対象外。過去学習からこれらを復活させない。

Critical Patterns: docs/solutions/patterns/critical-patterns.md は存在しない。

### Relevant Learnings

#### 1. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: docs/solutions/workflow-issues/pm-readable-evidence-delivery.md
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 強い工程上の関連。工程文書をカード添付で渡す際、「保存」「添付」「受取側で読取り」を混同しないために適用する。HTMLの大型証拠生成・画像確認という元事例の製品検証範囲は今回に移さない。
- **Key Insight**: 保存先の絶対pathや添付成功だけでは配送完了ではない。受取側が必要文書を利用可能なツールで開けることまで確認し、読取り・照合の実施者と未実施事項を区別する。参照箇所は33–45行、70–81行。人の明示承認は対象・範囲限定であり、別依頼へ一般化しない。
- **Severity**: high
- **Date**: 2026-11-18（last_updatedも同日）。今回の明示判断により、raw・derived・PNG・CLI出力等の生成要求は採用しない。

#### 2. 検証証拠の添付拒否は迂回せず Git 原本と人の標準添付で成立させ、拒否と解消は別記録に残す
- **File**: docs/solutions/workflow-issues/attachment-refusal-git-original-and-human-standard-reattachment.md
- **Module**: 検証証拠の受け渡し（Argonauts カード添付・検証成果物の原本）
- **Problem Type**: workflow_issue
- **Relevance**: 条件付きの隣接学習。工程文書の標準添付が拒否された場合と、原本の所在を後続担当へ渡す場合に有用。今回の調査では添付操作も拒否発生も確認していない。
- **Key Insight**: フック拒否を圧縮・リネーム・形式変更で迂回せず、具体的理由を人へ渡す。拒否と後続の解消を別記録にする。表示名の一致は原本同一性の証明ではない。参照箇所は30–35行。
- **Severity**: high
- **Date**: 2026-11-17。
- **Conflict / limitation**: 元学習31行の「原本をGit管理下へpushする」は今回の「最終PR全変更 README.md のみ」と衝突するため採用しない。工程文書を最終PRへ混入させず、指定されたカード添付経路で扱う。原本同一性の考え方は配送時の条件であり、対象外の製品実行証拠を新規作成する根拠にはしない。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 隣接学習。今回に適用するのは、検証した対象と最終PRの対象を一致させ、要求に合う確認だけを充足根拠にする原則。CI実行結果そのものを今回の追加受入条件にはしない。
- **Key Insight**: 過去headの報告や別種の確認を現在の対象へ転用しない。判定・報告直前に検証対象headを照合し、報告commitと区別する。参照箇所は33–37行。READMEの確認後に工程文書のcommit等が追加されると対象や全変更一覧が変わるため、最終対象で確認し直す必要がある。
- **Severity**: high
- **Date**: 2026-11-17。旧REQ-07のCI義務を今回へ流用しない。

### Recommendations
- 計画の受入条件を、指定コマンド例の追加1つ、既存末尾行保持、原本文字差分の一致、最終PR全変更一覧が README.md のみ、に固定する。これは今回の指示に由来する条件であり、学習に同一のREADME変更事例が見つかったという意味ではない。
- Builder・品質は、最終PR対象の全変更一覧とREADME原本文字差分を照合する。直前の作業ツリーや単一commitの変更一覧だけで最終PRの限定を主張せず、判定対象の更新があれば対象を照合し直す。
- 工程文書は指定のカード添付で引き渡し、最終PRの追跡変更へ含めない。後続工程では保存済み・標準添付済み・受取側読取り済みを別に記録する。添付拒否時は迂回せず、人への具体的な引継ぎと拒否／解消の区別を守る。本調査ではcommit/push/Kanban操作を行わない。
- text/json/htmlの実行、raw・画像・CLI出力等の証拠作成、CI要件の追加を計画へ持ち込まない。採用する学習は対象帰属・引渡し・範囲統制に限る。
- GSD full という前提を維持する。本調査はGSD判定を行わず、既存ファイルや学習からGSD状態を推測しない。後続で判定が必要なら公式CLIを使う。
- 計画中に未作成の検証コマンドを試さない。PLANの検証コマンドは、Builder・品質が実在する検証ファイルを根拠に実行する。
- 実装前に上記3文書の限定箇所を読む。特に添付の旧Git原本方針を今回へそのまま転用しない。

### Excluded Candidates and Limits
- docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md：frontmatterの適用条件はGit状態比較試験・変異注入・scratch基底。今回は試験追加もCLI読取り専用性の再証明も対象でなく、弱い関連として除外。`git add -A` を今回の手順へ取り込まない。
- docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md：frontmatterの適用条件はトークナイザ・決定論・出力順。README例1つ追加に該当せず除外。CONCEPTS.mdは現行順位を初出順と定義しているため、旧学習のcodepoint-order関連語を現行契約として扱わない。
- READMEの原本文字差分、既存末尾行保持、最終PRをREADME.mdだけにすることへ直接一致する専用学習は見つからなかった。今回の明示条件として扱う。
- この調査は学習文書の検索・読取りと本結果の保存のみ。README実装、製品実行、検証合格、最終PR限定の実証、添付完了を主張するものではない。
