## Institutional Learnings Search Results

### Search Context
- **Feature/Task**: 承認済み `r-50053edc-wordfreq-html` の計画入力。Python wordfreq CLI に自己完結した静的HTMLを追加し、既存のトークナイザ・casefold・エラー契約を維持する。依存追加・CI変更はしない。
- **Keywords Used**: wordfreq, CLI, HTML, escaping, basename privacy, pre-top totals, stable ordering, first occurrence, determinism, tokenizer, input-boundary, testing, evidence, independent-verification, head-resolution。Activity／Concepts／Decisions／Domainsから抽出し、関連語の input/boundary/order/test/CI/検証/入力/順位も使用。
- **Files Scanned**: `docs/solutions/` のMarkdown 4ファイルをネイティブ内容検索で走査。候補4件の先頭30行を確認し、強・中関連の3件だけを全文読了。別途、用語の根拠としてルート `CONCEPTS.md` を全文確認した。
- **Relevant Matches**: 3 files（直接関連2件、証拠運用の隣接関連1件）。添付拒否の1件は今回の作業条件との重なりが弱いため本文精読・採用を見送った。
- **Search Scope / Method**: 検出した実在カテゴリは `best-practices/` と `workflow-issues/`。コード実装とワークフローの両方にまたがるため `docs/solutions/` 全体を対象に、case-insensitiveの title/tags/module と problem_type/applies_when条件の複数検索を並列実行し、パスのみ取得した。候補数は4件のため追加の拡大・絞込み条件には該当しない。Packs指定なし。`patterns/critical-patterns.md` は存在しない。

### Relevant Learnings

#### 1. 入力の境界は3層で検証し、出力の決定論は全順序と PYTHONHASHSEED を変えた再実行で示す
- **File**: `docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md`
- **Module**: `wordfreq CLI (sources/tokenizer/aggregator/formatters)`
- **Problem Type**: `best_practice`
- **Relevance**: 強。HTMLを既存集計パイプラインに追加する際の責務分離、既存入力契約の維持、全出力の同率順位に直接関係する。
- **Key Insight**: 既定のUnicode単語文字の最長列、トークナイザ差し替え、CJK境界を混同せず、casefoldはトークン化後段に残す。出力追加を理由にこれらを変更しない。決定論は単一実行の一致ではなく複数 `PYTHONHASHSEED` の実CLI出力で確認する。入力ファイルの不変性も回帰対象にする（本文31–36行）。
- **Severity**: medium
- **Date / Conflict**: 2026-11-17。文書は同率をコードポイント昇順にする旧契約を推奨し、`CONCEPTS.md` の「決定論的順位」も同じ定義である。一方、今回の承認済みwork-contextは「頻度降順、同率は初出順」をtext/json/html共通に要求する。**旧タイブレークをそのまま転用してはならない**。現在のコードは今回の検索範囲外なので未確認であり、学習文書内のコード引用を現行コードの実測とは扱わない。
- **Planning Input**: 順位契約の更新と、それに依存する仕様・用語・期待値の整合をHTML整形前に解決する。初出順は入力から得た順序を保持し、setの反復順やHTML専用の再ソートで失わない。複数seedの一致は補助証拠であり、初出順そのものの期待値試験も必要。

#### 2. 状態検証試験は scratch コピーへの変異注入で判別力を示し、比較基底は git add -A 後に固定する
- **File**: `docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md`
- **Module**: `wordfreq CLI（tests/test_cli.py の読み取り専用リグレッション試験）`
- **Problem Type**: `best_practice`
- **Relevance**: 強。HTML生成後も入力・リポジトリ不変を保つ回帰検証と、UI検証の判別力を設計する際に適用できる。
- **Key Insight**: 成功した試験だけでは欠陥の検出能力は示せない。状態比較ではcold copy、`git init` → `git add -A` → before取得、キャッシュと継承環境の分離が重要。未追跡の既存ファイルは内容が変わってもstatusに現れず偽合格し、準備不備は偽陽性を起こす。変異注入は本作業ツリーでなく独立scratchで、欠陥種ごとに期待するアサーションで落ちることを確認する（本文31–44行）。
- **Severity**: medium
- **Date / Conflict**: 2026-11-17。今回のwork-contextとの矛盾は見当たらない。ただし本文の既存試験位置・過去実測は履歴記述であり、今回の実行結果ではない。
- **Planning Input**: HTMLの安全性・レスポンシブ試験にも「何を検出するか」を明記する。escaping欠落、フルパス漏出、top適用後の誤った総数、同率順序の逆転、横はみ出し、外部通信の試行は別々の失敗として扱う。これは本文の判別力原則からの今回向け提案であり、既存学習がHTML・ブラウザの具体手法を実証しているわけではない。

#### 3. CI依存の要求は検証者の独立した最新head証跡のみで充足を確定し、報告直前に検証対象headを再解決する
- **File**: `docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md`
- **Module**: `フェーズ検証・要求充足判定（REQ-07 CI pytest job）`
- **Problem Type**: `workflow_issue`
- **Relevance**: 中・隣接関連。今回の独立ブラウザ証拠にも「要求に適合する証拠の種類」と「検証対象head」を区別する原則が有用。ただしCI実行要求そのものは今回新設しない。
- **Key Insight**: 設定の存在、他人による過去headの報告、ローカルテスト成功、検証者による対象headの独立読取りは相互代替ではない。証拠は量でなく要求との対応で評価し、検証対象headと報告commitを分け、報告直前に対象を照合する（本文22–37行）。
- **Severity**: high
- **Date / Conflict**: 2026-11-17。本文のCI限定の判定基準をローカルブラウザ検証へそのまま移すのは不適切。学習を理由にCI変更・依存追加を計画へ混入させない。今回へ移せるのは証拠の帰属・独立性の原則である。
- **Planning Input**: Builderの要約やスクリーンショットだけを独立ブラウザ証拠の代替にしない。品質側が対象headから生成したHTMLを自ら検証し、viewport、生成手順、実行結果、rawな文字Range geometry、失敗も含むnetwork attemptを証拠に残す。これは今回のwork-contextに沿った適用であり、学習文書の既成ブラウザ手順ではない。

### Recommendations

1. **先に契約の衝突を処理する**: 旧学習・`CONCEPTS.md`のコードポイント昇順と今回の初出順は両立しない。今回の承認済み契約に従い、実装前のコード・試験確認で更新箇所を明らかにする。text/json/htmlの順位を一つの集計経路で確定し、HTMLだけ別順序にしない。
2. **実装順序**: (a) 同率順位と既存回帰の期待値を整合、(b) top適用前の総語数・異なり語数を保持する境界を確定、(c) basenameだけを受け取り表示値をescapeする自己完結HTML整形、(d) CLI連携、(e) 独立ブラウザ検証。順序・総数をHTML側で推測し直す設計は避ける。これは学習の責務分離原則と今回要件を組み合わせた計画上の提案。
3. **試験の含意**: tokenizer/casefold/CJK/既存エラーを維持し、全形式の頻度降順・同率初出順を固定する。HTMLでは特殊文字、入力basenameと親ディレクトリ非露出、空入力、top切捨て前総数、長い語を含む表を対象にする。判別力の証明を行う場合は欠陥種別ごとにscratchで実施し、本ツリーへ故意の欠陥を入れない。
4. **UI判定の制約**: lightな表を通常幅と320 CSS pxで確認する。raw character Range geometryを保存し、可読性・横方向のはみ出しを判定する一方、文字を自身の要素の高さへ厳密に縦包含させる独自条件は追加しない。外部通信は成功requestだけでなく失敗した試行も確認する。これらは今回の承認済みwork-contextに由来し、`docs/solutions/`に専用の実証済み手順は見つからなかった。
5. **証拠と完了判定**: 機能テスト、実CLI、独立ブラウザ、必要な場合の既存CI証拠をそれぞれ対応する要求へ紐付ける。検証対象headと報告commitを区別し、古い結果を未検証headへ継承しない。計画段階では未作成の検証コマンドを試さず、Builder・品質が実在する検証ファイルから実行する。今回の調査ではコードや検証コマンドを実行していない。
6. **Implementer required-reading**: 上記1・2の2ファイルを着手前必読とする。独立品質証拠の担当者は上記3も読む。HTML escaping、basename privacy、pre-top totals、Range geometry、network attemptsの専用学習は今回の対象文書では見つからないため、実装・検証後に新しい耐久的学習として記録する価値がある。
