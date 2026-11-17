# r-50053edc gap=1 — Phase 3追加計画入力

入力: t_db3e2cfc、PM t_e8b9b8a9、品質 t_9de84d5f completed run106。検証対象995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c、報告commit c26d9d963b5983e539b675b767fbd3d1c0572e7aを区別する。

## 公式分岐と範囲

init.progress: project_exists/requirements_exists/roadmap_exists/state_existsは全true、初期化不要。roadmap.analyze.current_phase=1（旧phaseのsource変更によるstale）、STATE.current_phase=3。固定入力対象3のinit.plan-phaseはExecuted、verification_status=gaps_foundなので閉じていないPhase3へ--gaps追加。新規ingestやPhase2流用、既存03-01〜04の上書きは禁止。phase_count=2（ROADMAPの1,3）。--gapsが公式§5でresearchをskipするため新researchは起動せず、既存RESEARCH/PATTERNSを参考とし今回のgap原本を優先する。init.plan-phase CLIは--gapsを受け取らない導入版なので通常引数3で照会し、workflow/planner Mode=gap_closureに反映する。

## G1 必須 — 最終証拠の内部整合性

tools/verify_wordfreq_html.pyのlive finalize成功後top-level acceptedでも全22 viewsがpending-review、reviewed_images=[]、derived.jsonもpending。validated ledgerを画像path/sha256/viewed_atごとに各viewへ正確に投影し、manifest/derived/ledgerを一致させる。失敗は未検証扱い。accepted/builder-reviewedにpendingを残さず各viewの画像集合とledgerが完全一致するfail-closed検査。欠落/余計/重複/改変/空/中途保存/失敗時の誤合格を回帰試験する。top-levelのみ成功、過去証拠の手修正は禁止。docs/wordfreq-html-verification.mdに最終照合を明記する。

## G2 必須 — 既存CI環境での全試験成功

旧headの必須pytest:5 failed/279 passed。tests/test_cli.pyのISO-8859-15 locale前提2件、tests/test_html_verifier.pyのscope3件（shallow checkoutにbaseline 5a7659b949dc118b59cea5ef3eb40bcd94337d8d / approved snapshot ed7e6cc…がなくdiff exit128）。tests/tools修正のみ（runbook記録更新は許可）。byte-level/filesystem/stdout encoding契約、exact baseline/approved snapshot、dirty/untracked拒否を保つ。locale非導入CIでも実行可能なtest-provided前提でバイト契約を検証し、対応環境でのcharmap実測義務を消さない。scopeテストは自己完結test-controlled repo等で行えるが実scopeの参照欠落はfail-closedで成功を偽装しない。CI workflow/依存追加変更、skipや条件削除で義務を隠すことは禁止。

関連非阻害警告も同じ証拠境界の箇所に限り扱う: tests/外untracked test_*.py/conftest.py/root pytest.py等の実pytest収集/実行影響とprovenance dirty検査を整合。別actor manifest拒否と--actor省略時profile記録の回帰試験。無関係な汎用化・リファクタなし。

## 新head再検証とOpenSpec完了記録の責任

G1/G2修正をpushした新headで独立品質がfresh quality rootに実CLIを独立再生成。空/通常/top/長文/注入、Chromium1280x900/320x900 CSS px、DPR1、zoom100%。全full画像/全tilesを実閲覧しrawRange全原本を監査。open前から閲覧/live finalize/flush完了まで失敗試行も含めた通信観測とcanaryを保持。AC1〜AC6別証拠と最終manifest/derived/ledger一致/pending無しを確認する。全suite、新headの既存CIも記録。CIは有限1回の読取り、未報告は未報告で成功とせず待ちループ禁止。旧証拠流用・手修正禁止。

OpenSpec tasks3.1/3.2/4.1/4.2は未完了。担当Builderが独立品質の新headの根拠に基づいて完了記録を整える具体的工程・handoffをPLANに記す。品質は製品コードやOpenSpecを書き換えない。未実施4.1の事前完了禁止。最終OpenSpec verifyにcritical未完了を残さない。品質の手順後に必要な完了記録の更新はPMによる適切なBuilder工程への割当を明示し、計画自身や事前のBuilder自己検証を独立品質証拠と取り違えない。

## 固定仕様と禁止

自己完結静的HTML3列（順位/単語/回数）、表上basenameのみ・top前総数。全形式回数降順/同数時正規化後初出順（旧語昇順の置換は承認済）。明るい背景のみ・切替なし・1始まり表示行連番。横収まり・切取り祖先内収まり・隣接非重複・全画像可読性で判断しrawRangeを補正しない。要素自身への厳格な縦包含は不要。HTML escape・外部参照通信なし・ディレクトリ非埋込み。同数順以外の入力/エラー/抽出/casefold/text/json構造維持。

CI/依存追加変更、生成日時、テーマ切替、対話操作、Webサーバー、入力元拡張は禁止。製品仕様変更なし。新PLANは各3task以下、同じ依頼branchに番号順直列、先行PLAN成果を前提とする検証は前提を明示。独立PLANは後続未実装でも自己完結して検証可能にする。automatedは実在/同task作成のtestファイルを使い、各直後にobservable fails_whenを置く。既存承認済コマンド python -m pytest 等を維持し、環境prefixは既存CPython3.12用実績に限る。計画中に製品テストや未作成コマンドを実行しない。

## 原本

.planning/phases/03-wordfreq-html-output/03-VERIFICATION.md、03-VALIDATION.md、03-SECURITY.md、03-REVIEW.md、03-UI-REVIEW.md。
.planning/argonauts/t_9de84d5f/openspec-verify.md、ci-evidence.md、ac-evidence.md、quality-evidence.tar.gz、quality-sha256.txt（実在名は検索して原本を確認）。承認済変更openspec/changes/r-50053edc-wordfreq-html/。
今回の学習は .planning/argonauts/r-50053edc-learnings.md（--prd入力には混ぜない）。
