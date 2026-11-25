# 07-03 Builder実行記録・独立品質への引継ぎ

依頼r-d4bcda40 / task t_814e09b4 / run133 / 実profile argonauts-uat-builder。
これはBuilderの確認であり独立品質の合格報告ではない。OpenSpec2.1のみチェックし2.2は未完了。

## 最新の依頼者判断

判断日時: 2026-11-25 21:22 JST。原コメントt_87068596、default、created_at=1795609328を直接確認。受付t_bcdd7392の引継ぎとも一致。

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

画像取得/閲覧0枚、views0。ブラウザー/Range/実通信/canary未実施。旧PLANに書かれた実施済み状態を捏造せず、最新判断に沿うCLI/HTML内容採取へ変更。新依存/CI/製品/CSS/formatter変更なし。

## 実行環境と帰属

既設`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3`を使用。
各stage command.json/result.jsonにargv/cwd/env/実head/Python/製品SHA/開始終了/時間/件数/exit、stdout/stderr/JUnitの原本を保存。
terminalにtaskの環境変数が無いためstage原本のtask=nullを変更せず、上記の実カード/runを本文へ記録。

実装commit b4705e23baca58bda3de4e84b35b28e211915d14。
採取時headはe7bb32adafff85dcc13748218c71a26893028d44＋未commit実装差分。過去原本のheadを報告commitへ付替えない。
採取時provenance.runtimeに保存されたtools/testsのSHAが実装commitの同ファイルと一致する。製品は親d61dff3から不変。

## 実測

全rootは`.planning/argonauts/r-d4bcda40/builder/07-03/`。

| Stage | 結果 | wall秒 | 原本 |
|---|---|---|---|
| red-capture | 対象API不足1 assertion失敗、exit1 | 0.389641041 | stdout.txt/junit.xml/result.json |
| red-cases | max case/品質role API不足2 assertion失敗、exit1 | 0.364137453 | 同上 |
| red-contract | runbook/scope API不足2 assertion失敗、exit1 | 0.372995653 | 同上 |
| green-api | browser_free13成功、exit0 | 0.835454106 | 同上 |
| green-contract | 13成功/fixture ERROR1、成功ではない | 1.045136479 | scope許可に公式state.jsonが不足した初回原本 |
| green-contract-02 | browser_free/evidence_contract/scope_contract49成功、exit0 | 7.685593482 | stdout.txt/junit.xml/result.json |
| capture | CLI138、HTML46、画像0、pending-review | 204.521879617 | manifest/provenance/全case原本/scope/suite |
| capture内全suite | 1048成功、failures/errors/skipped0、exit0 | 200.617190704 | suite.json/xml/stdout/stderr/command |
| saved | 完了後read-only saved_builder_capture1成功、exit0 | 0.396841174 | stdout.txt/junit.xml/result.json |
| cli | tests/test_cli.py全650成功、exit0 | 62.024429242 | stdout.txt/junit.xml/result.json |
| validate CLI | 最終capture照合exit0 | 時間未測定 | validate.stdout.json |

capture収集部分3.904502914秒、全600秒deadline内。CLI/full/captureは30秒を超え高速とはしない。
全3 REDは公式classifierでRED_EVIDENCE_OK、出力は*-classifier.json。主capture APIのREDを分類確認・commit後に実装開始。
補助caseのclassifier保存は実装後になったが、元の未実装時RED/JUnitは保持しており、先行記録や判定時刻を捏造しない。
詳細拒否fixtureとscope否定fixtureは追加の判別力確認であり、07-01製品編集前の先行REDの代用ではない。

## 原本索引とAC対応

manifest.json SHA-256 `2c112163996e06658d71755fc286800c2f5906533f942b910b5ef6768a35c0df`。
全468 artifactをpath/SHAで列挙。138実CLIケースのinput/argv/exit/stdout.bin/stderr.bin、HTML46原本stdout.htmlを保存。
baseline39caseの省略と大上限78caseは同じ変更前固定bytesへ照合。再採取/改変なし。

| AC | REQ | 今回の確認・原本 |
|---|---|---|
| AC1 | REQ-23,26 | default/large/explicit-min、元39case固定bytes、既存parser/help/整数表記試験 |
| AC2 | REQ-24,25 | max1/max2/zero/negative、全形式、case literal pairs、exit0 |
| AC3 | REQ-24,25,26 | min2max2/3と順交換/top1/triple zoo3元12/inverted、Unicode/tie/選択後12種類 |
| AC4 | REQ-27 | 追加拒否群と全1048件、650CLI、先行RED/GREEN原本、suite成功実数 |
| AC5 | REQ-28 | test_max_count_readme_exampleを含むCLI650成功、READMEは親から不変 |
| AC6 | REQ-26,27 | 実Git scope.json（基点8efbfaa、採取前302path）、cold repoの無関係/依存/workflow/formatter/README/既存試験削除・緩和拒否。主製品2箇所の承認hash/READMEhash固定、他製品不変 |

現在のソースはread_fileで確認済み。__main__.py35元Counter、36元total、37..39包含AND、40top、46..50共有pairs。元Counter不変と共有pairsは既存spy試験でも確認。
`git diff --exit-code d61dff3 -- wordfreq tests/test_cli.py README.md .github pyproject.toml`はexit0。
今回のruntime差分はmax専用tool325追加/2削除、同試験205追加/既存削除0、runbook107行新規、OpenSpec2.1チェックと工程原本だけ。

## 品質担当へ

実装カードの同一カードレビューと、子t_dc0281b7のフェーズ検証は別。まず同カード品質へ渡す。
品質本人の現在head/profile/fresh rootで独立CLI/HTML内容と全suiteを再生成する。
runbookはdocs/wordfreq-max-count-verification.md。review-sessionは最新判断による同期内容採取でありlive browserではない。
品質のVERIFICATION.mdとcli-ci-proof.mdの標準添付/読戻しhash/PM本人の文字原本読取りまで未完了。
未報告CIをローカル成功で代替しない。品質実行前の2.2チェックなし。phase.completeは呼ばない。
