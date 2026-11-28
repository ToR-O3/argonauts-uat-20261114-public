## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み `wordfreq --exclude FILE` 追加のGSD計画に向けた学習検索。製品判断は再審議せず、実装はしない。
- **Keywords Used**: wordfreq、argparse、exclude、UTF-8/UTF-8-sig、casefold、空行、コメント、除外、min-count、top、初出順、HTML、終了コード、stderr、input-boundary、determinism、test-discrimination、read-only、CI、検証、証拠配送、code-implementation、workflow、test-failures。
- **Files Scanned**: `docs/solutions/` 内のMarkdown文書6件。全6件をfrontmatter検索の候補として冒頭30行確認し、関連4件を全文読了した。`.gitkeep` とディレクトリは文書数に含めない。
- **Relevant Matches**: 4件（直接関係する入力・順序の学習1件、検証・無人品質証拠の隣接学習3件）。
- **調査範囲・方法**: 指定された公式 `learnings-researcher.md` を最初に全文読了。repo直下 `CONCEPTS.md` を語彙の根拠として読了。検索rootは `docs/solutions/` のみ、packsなし。実在カテゴリは `best-practices/` と `workflow-issues/`。複数領域にまたがるため全体を対象に、title/tags/module/component/problem_typeおよびapplies_whenのリスト行を大文字小文字を区別せず並列検索した。補助的に全文キーワード検索も行った。`patterns/critical-patterns.md` はファイル探索結果に存在しない。
- **対象外**: 限定PRの工程原本保全、添付拒否の正規解消の2件はfrontmatterから今回の主題への適合が弱いと判断し、全文読了・採用していない。引用先の旧カード、リンク先runbook、製品コード、試験ファイルは今回の検索root外なので追跡していない。GSD状態判定、未作成検証コマンドの試行、実装、commit、Kanban操作は行っていない。
- **不足する直接学習**: `--exclude` 専用、除外ファイルの最後指定のみ読取り、UTF-8-sig、空行・コメント処理、既存引数→除外→本文の優先順位、除外エラー2/本文エラー1を直接規定する既存学習は見つからなかった。これらは今回の承認済み入力として計画に渡し、過去学習が保証した仕様とは扱わない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: wordfreq CLI (sources/tokenizer/aggregator/formatters)
- **Problem Type**: best_practice
- **Relevance**: 除外語の読込み・正規化という新しい入力境界と、全形式の集計・順位の既存互換に直接関係する。
- **Key Insight**: 入力方針、トークナイザ差し替え、正規化を混同しない。本文の既定トークナイザはUnicode単語文字の最長列であり、casefoldは後段の共通処理。CJKを文字単位と誤認しない。読取り専用性は入力バイト不変まで試験し、決定論は複数の `PYTHONHASHSEED` で試験と実CLI出力を比較する（同文書31–36行）。除外リストに本文用トークナイズ規則を無条件に流用する根拠にはならない。
- **Severity**: medium
- **現行語彙との衝突**: 文書は2026-11-17のPhase1を記録し、34行・55–57行で同率時の語コードポイント昇順を推奨する。しかし現在の `CONCEPTS.md`「決定論的順位」（49–51行）は頻度降順・正規化後の初出順・その後topで、旧規約を意図的に置換したと明記する。旧ソート例をコピーしない。現在の語彙文書を優先し、初出順を保持する安定ソートと除外後の順序を検証する。frontmatterに `status: stale` の指定はないが、この順序規則は明示的に旧規約である。製品コードとの独立照合は今回の範囲外。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）
- **Problem Type**: best_practice
- **Relevance**: 隣接学習。除外ファイルを追加で読むCLIで、入力や作業ツリーを変更しないという既存互換を試験するときに適用する。全機能試験へGit準備を強制するものではない。
- **Key Insight**: Git状態比較で未追跡ファイルの内容変更は見えず、偽合格になり得る。使い捨てscratchのcold copyで `git init` → `git add -A` → before/after比較とし、既存内容変更と想定外未追跡生成物の検出を別々に証明する。継承された `PYTHONDONTWRITEBYTECODE` や温まったキャッシュによる偶然の合格を避ける（37–44行）。本体worktreeには変異を注入しない。
- **Severity**: medium

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`
- **Module**: フェーズ検証・要求充足判定（REQ-07 CI pytest job）
- **Problem Type**: workflow_issue
- **Relevance**: 無人品質証拠に直接適用する横断学習。CI依存の受入条件がある場合に限り、その条件を満たす証拠の種類を規定する。
- **Key Insight**: CI設定の存在、人による旧headの成功報告、ローカル試験成功、検証者による対象headの独立CI読取りは別物。CI実行結果を条件とする要求は最後の証拠でのみ充足する。判定・報告直前に検証対象headを再解決し、報告commitとは別記録にする（33–37行）。旧headの件数や成功を今回へ転用しない。
- **Severity**: high

#### 4. 証拠の配送は添付成功ではなく受取PMの原本読取りまで確認する
- **File**: `docs/solutions/workflow-issues/pm-readable-evidence-delivery.md`
- **Module**: wordfreq HTML受入の証拠配送
- **Problem Type**: workflow_issue
- **Relevance**: 隣接する無人運用学習。HTMLを含む全形式の証拠を別profileへ引き渡す計画で、品質完了後の読取り不能を防ぐ。
- **Key Insight**: 保存済み・標準添付済み・受取側読取り済みを区別し、CLI入出力など原本の相対pathと対象headを保持する。archiveや品質profileの絶対pathだけでは配送完了にならない（33–45行）。HTML構造試験、画像実閲覧、原本同一性の確認は別の主張。既往のPM画像閲覧の代替承認は案件限定であり、今回に自動適用しない（68–81行）。
- **Severity**: high

### Recommendations
- **実装前に読む順序**: 入力境界・決定論の学習を読み、上記の旧順序規約の注意を必ず添える。次に証拠種とhead照合の学習を読む。Git不変性を試験する担当は状態検証の学習、別profileへ証拠を渡す担当は配送の学習も読む。
- **承認済み制約を検証可能な単位へ分ける**: 除外ファイルは最後指定のみ読む、既存引数→除外→本文の処理順、除外の失敗は終了コード2で本文の失敗は1、stderr、依存追加なしを変更しない。多重障害の組合せにより、結果だけでなくどの段階が先に扱われたかを試験する。古い無効パス・最後の有効パスの組合せは「最後だけ読む」の判別に使える。これは今回の確定仕様からの試験提案であり既存学習の実測結果ではない。
- **読取り境界を独立試験する**: UTF-8-sig、casefold、空行・コメントの承認済み定義をフィクスチャ化し、本文用トークナイザと除外リストの解釈を混同しない。本文・除外ファイルのバイト不変も確認する。コメント解釈などの細部を学習文書から勝手に補わない。
- **処理順と全形式を一緒に固定する**: 除外をmin-count/topより前に適用し、初出順を壊さず、text/json/htmlの同じ集計から出す。全除外・除外なし・同率・再出現・top境界を含める。HTML総数は `CONCEPTS.md` の純粋なHTML整形契約（top前総数、呼出し側で計算、formatterは再集計しない）を尊重し、除外後・min-countとの関係は今回の承認済み仕様の明示値で固定する。ここを過去学習だけで推定しない。
- **決定論と互換を別々に示す**: `--exclude` 未指定時の既存出力・エラー互換と、指定時の除外後の初出順を試験する。複数ハッシュシードで全形式の実CLI出力を比較する。setは所属判定に使っても、出力列の再構築元にして初出履歴を失わない。
- **検証ファイル→実行→品質証拠の順を計画に記す**: 計画段階では未作成の検証コマンドを試さない。Builder・品質は実在する検証ファイルを確認して実行し、argv、入力フィクスチャ、stdout、stderr、終了コード、対象head、試験結果、各原本のpathを残す。CI条件がある場合は品質が対象headのCIを独立確認し、不足はgapとして残す。原本配送を品質試験そのものの代わりにしない。
- **学習の今後の候補**: 専用学習がないUTF-8-sig除外リストと多重障害の優先順位について、実装・独立品質で得た判別力のある例を、完了後にdurable learningとして記録する価値がある。今回の調査では学習追加や製品変更は行わない。
