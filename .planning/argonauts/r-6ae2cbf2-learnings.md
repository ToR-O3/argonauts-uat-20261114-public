## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み r-6ae2cbf2。`wordfreq --format html` の総出現回数の横に「表示 N 種類」を追加するGSD計画前調査。Nはmin/max/top適用後の最終pairs行数。変更はHTML表示と必要最小限のレイアウトに限定する。
- **Keywords Used**: wordfreq、HTML、pairs、min/max/top、Unicode、正規化、baseline、snapshot、scope gate、バイト不変、320px、独立検証、試験の判別力、証拠配送、検証対象head。
- **Files Scanned**: `docs/solutions` のMarkdown文書5件を内容検索し、候補5件の先頭30行を確認。適合4件を全文読取り。動的探索で見つかった分類は `best-practices/` と `workflow-issues/`。`.gitkeep` とディレクトリ自体は文書件数に含めない。
- **Relevant Matches**: 4件。添付拒否の文書はfrontmatterで隣接論点と判定し、今回の上位結果から除外した。
- **Grounding**: repo rootの `CONCEPTS.md` を全文読取り。検索対象の学習コーパスは `docs/solutions` のみ。Compound Packなし。`docs/solutions/patterns/critical-patterns.md` は存在しない。
- **調査境界**: 学習文書とCONCEPTSの調査であり、現行実装、承認本文、封印baseline、検証スクリプトの実在や動作を確認したものではない。GSD状態判定、未作成コマンドの試行、Kanban操作、commit/pushは行っていない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 表示種類数を追加する際、正規化前の語数やフィルタ前の集計件数を使わず、既存パイプラインの責務境界を保つ必要がある。text/jsonの並び順やバイト列も変更対象ではない。
- **Key Insight**: トークナイザの境界、差し替え境界、CJKの既定粒度を分けて検証する。正規化・集計をHTML層でやり直さない。決定論は単一シードでの再実行一致だけでは証明できず、複数の `PYTHONHASHSEED` で試験と実CLIの一致を確認する。
- **Severity**: medium
- **現行用語との不一致**: 2026-11-17の本文34行とコード例は同率時の「語コードポイント昇順」を推奨している。一方、`CONCEPTS.md` の「決定論的順位」は r-50053edc でこれを意図的に置換し、頻度降順・同率は正規化後の初出順・その後top制限と定義している。旧ソート例を復活させない。frontmatterに `status: stale` はないが、この旧順位部分は現在の契約として採用しない。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: HTML以外の互換性や入力・作業ツリー不変を「テストが通った」だけで判断しないための試験設計指針。
- **Key Insight**: 過去には未追跡ファイルの内容改変を `git status` が見逃し、偽合格した。状態比較を使う場合、使い捨てscratch内でcold copyを用意し、`git init` → `git add -A` 後に比較基底を取る。追跡内容変更と想定外の未追跡生成物は別々の変異で判別力を示す。変異を製品作業ツリーへ入れない。
- **Severity**: medium
- **適用の限定**: ここでいうstaged baselineは一時Gitリポジトリの状態比較基底であり、今回の封印済HTML baselineではない。この記事を根拠に封印原本を作り直したり上書きしたりしない。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 今回の独立品質判定を、過去snapshotのscope gateや旧headの成功記録で代替しないために直接関係する。
- **Key Insight**: 証拠の量ではなく、対象要求・証拠種・検証対象headを一致させる。CI設定の存在、過去headの人の成功報告、ローカル成功は、現在headの独立CI証拠とは別物。判定・報告直前にheadを再照合し、検証対象headと報告commitを分記する。
- **Severity**: high
- **適用の限定**: CI実行結果を充足条件とする要求には独立CI読取りが必要という教訓であり、全てのローカル機能試験を無効にする意味ではない。今回のCI要否そのものはこの調査では判定していない。

#### 4. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md`
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: HTML安全性、狭幅320px、独立品質の原本を別担当へ渡す計画に有効。コード変更自体への直接の実装指針ではなく、受入工程の隣接論点。
- **Key Insight**: 保存済み・標準添付済み・受取側で読取り済みを分ける。品質profileの絶対パスやJSON索引だけでは原本配送完了にならない。対象head/run/rootと相対pathを保ち、CLI入出力・raw・derived・画像を受取側の能力で開ける形にする。SHA一致は可読性や試験合格の証明ではない。
- **Severity**: high
- **例外の限定**: 過去のPM本人PNG閲覧の代替は、人の明示承認により特定対象へ限定されたもの。今回の品質本人の画像実閲覧や新headの再検証を省略する恒久的免除ではない（本文68–81行）。

### Recommendations

#### 制約として計画へ渡すこと
- **Nの責務を固定する**: 今回の入力条件に基づき、Nはmin/max/topの全制限後にHTMLへ渡す最終pairsの行数とする。入力全体の異なり語数、top前の件数、総出現回数から推測しない。総出現回数の既存意味も変えない。
- **HTMLを純粋な整形に留める**: `CONCEPTS.md` の「純粋なHTML整形」に従い、既存pairsの順序を維持し、再読込み・再集計・I/Oを追加しない。Unicode正規化・casefold・トークナイザ境界は既存パイプラインに任せる。今回のために新しい正規化方式を導入しない。
- **互換例外を狭くする**: ユーザー指定のHTML表示追加と最小レイアウトのみを例外とし、text/jsonは同一入力・同一オプションでバイト不変を期待する。既存の頻度降順・同率初出順を保持する。
- **封印baselineを保全する**: 封印原本は上書きしない。今回用の期待値を別途持つか、許容する表示追加・レイアウト差分を明示した変換で比較する。広い差分無視で他の退行を隠さない。封印baselineの取扱いは今回の指定であり、検索した学習文書に直接の手順はなかった。
- **履歴と今回判定を分離する**: 過去snapshotのscope gate結果は当時の対象に帰属させて保持し、今回の検証対象head・要求・許容差分に対する判定を新しく記録する。

#### 試験設計への助言
- 最終pairs行数と表示Nの一致を、通常例、空入力、フィルタで全件除外、min/max境界、topで切詰め、候補より大きいtop、min/max/top併用で確認する。top前件数や無制限件数を誤表示すると失敗するケースを含める。
- Unicode・casefoldで同一化される入力とCJKの既定境界を含め、正規化前の見かけの語数をNとして使う誤実装を捕らえる。期待値は既存契約から導き、旧文書のコードポイント順は採用しない。
- text/jsonのバイト比較とHTMLの限定差分比較を別の主張として試験化する。状態不変試験を改修するならscratchでの変異注入を用い、試験設計エラーではなく対象アサーションで落ちることを示す。
- HTML動的値の標準escape一回・独立テキストノード・固定属性/CSS/URLというCONCEPTSの境界を維持する。空pairsでもメタ情報と表見出しを保つ。HTML構造試験だけで安全性・ブラウザ可読性・通信観測・品質合格をまとめて主張しない。
- 320pxでの新しいメタ情報の折返し・重なり・横方向のはみ出しは、今回のブラウザ証跡と品質本人の確認対象にする。検索コーパスに320pxの具体的レイアウト解法はなく、過去の画像閲覧代替承認を流用しない。
- 複数の `PYTHONHASHSEED` で既存順位と各形式の再現性を確かめる工程を必要に応じて配置する。単一実行成功を判別力や決定論の証明にしない。

#### 推奨する順序と引継ぎ
1. 計画担当が承認条件、最終pairsを得る境界、現行検証ファイル、封印原本と比較手順を別途読取り確認する。この調査はそれらの実在確認を代行していない。
2. Builderが表示Nと互換性の判別力を持つ試験を用意してから、HTML表示・最小レイアウトを実装する。PLANに記載する検証コマンドは、Builder・品質が実在する検証ファイルを確認して実行できるものへ結び付ける。計画段階で未作成コマンドを試さない。
3. 機能・バイト互換・HTML限定差分の証跡と、ブラウザ/320px/安全性の証跡を分けて生成する。baseline原本と今回生成物の保存先を分離する。
4. 品質担当が今回の検証対象headへ独立検証を行い、必要なCI証拠は当該headの実行基盤から直接確認する。head更新後へ旧成功を付け替えない。
5. 受入担当が必要原本を読める形で引き継ぎ、保存・配送・読取り・画像実閲覧・再実行の実施者と未実施事項を区別する。

実装前に優先して読む文書は上記1（境界・旧順位の注意）と2（試験の判別力）。品質・受入前には3と4を読む。今回の封印baseline、具体的なmin/max/top検証ファイル、320pxのCSS解法については直接適合する学習がなく、実装後に判別力のある知見が得られれば今回の学習として追加する余地がある。
