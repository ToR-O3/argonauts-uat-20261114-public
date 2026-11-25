# wordfreq --max-count：独立品質確認の手順

対象 r-d4bcda40、Phase 7。これは手順であって合格報告ではない。
OpenSpec2.2は未完了。Builder captureはpending-reviewのみで独立品質を代行しない。

## 最新判断と実施範囲

判断日時: 2026-11-25 21:22 JST。出典はt_87068596の人defaultコメント1795609328。

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

古いPLAN/UI-SPEC/VALIDATIONの画像・ブラウザーgateよりこの判断を優先する。
画像取得0枚、閲覧0枚、views0。画像・Range・実通信観測・canaryは未実施であり成功とは書かない。
従ってlive browser ownerや全full/tileの台帳は作らない。品質の独立CLI/HTML内容/全suite/ソース確認は維持する。
UI01..14のうち視覚的な横収まり/clip/重複/書体/折返し/UI01..04,10,12..14は未実施と明記。
UI05..09,11の空/静的完成文書/三出口/共通pairs/top/0,1,複数行は内容試験で確認する。
E01..E15の対応原本は07-VALIDATION.md。E12は非0/0件/ERROR/skip拒否、E13はhead/argv/件数/原本照合で確認。
新依存、CI、CSS、formatter、既存driver、製品コードの追加変更なし。

## 開始前

品質本人の実profile `argonauts-uat-quality` とそのHERMES_HOMEを使う。`--role quality`だけでは代用できない。
Builder環境変数を書き換えて品質として起動しない。profileの値は秘密でない出典情報であり認証の代替ではない。
自分のkanban_showのtask/runを文字記録へ明記する（terminalにtask環境変数が渡らない環境でも推測しない）。
依頼branch `argonauts/r-d4bcda40` のPRとoriginを確認しfetch、対象HEAD/PR head/originを一致させる。
実行面の未commit変更・shadowが無いことを確かめ、実行後にも同じheadと製品/tools/tests/設定のhashを照合する。
head変更時は文書のみでもfresh rootで全面再実行。過去の原本のheadや絶対pathを書き換えない。
変更前基点は8efbfaa1907ace272a4f685e2659144a4085d303、baselineは`.planning/argonauts/r-d4bcda40/baseline`。
これは固定bytesの参照であり現在の品質合格ではない。baseline modeを再実行しない。

## 実在するCLI

repo root、既設CPython3.12とpytestを使う。新installしない。
quality/final-01が既に存在すればfinal-02等の新番号を選ぶ。既存rootは上書き・再開しない。
通常のcaptureは有限600秒（個別CLI最大20秒）でCLI全形式、HTML原本、全suiteを実行する。
`review-session`は最新判断に従う同期CLI/HTML内容採取でありlive browserではない。CI待機ループを追加しない。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode review-session --role quality --output-dir .planning/argonauts/r-d4bcda40/quality/final-01 --baseline-dir .planning/argonauts/r-d4bcda40/baseline
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode validate --output-dir .planning/argonauts/r-d4bcda40/quality/final-01 --baseline-dir .planning/argonauts/r-d4bcda40/baseline
```

Builderの採取は同じCLIの`--mode capture --role builder`、固定rootはbuilder/07-03/capture。
採取はpending-review、independent_acceptance=falseのみ。CLI/suite途中失敗やtimeoutはpartial原本を残し停止する。
saved_builder_captureはread-only。採取ownerの直下pytestだけがsealed collectionを読み、実行中自身のsuite完了を要求しない。
採取終了後はsuite原本・非空件数・exit0・failures/errors/skipped0を必須として最終封印を照合する。
外側のフラグだけで未完了を許容しない。CIの浅いcheckoutでは保存済み原本照合に過去Git履歴を要求しない。

## 原本と内容確認

manifest.json/manifest.sha256、provenance.json、scope.jsonに実head/profile、実行面hash、環境、cwd、interpreter、入力、正確argv、exitを残す。
case配下のinput、stdout.bin、stderr.bin、HTMLのstdout.htmlを実読。manifest.artifactsは全原本path/SHA-256。
再配置はvalidatorの相対参照だけで、元絶対root/argvを書き直さない。
省略互換と大上限は同じ変更前固定bytesへ照合する。新コード2呼出し同士の比較だけで済ませない。
max1/2、min2max2/3と順交換、max2top1、三条件のzoo3/元12、max0/負数/逆転、空/空白/記号、Unicode、初出tie、選択後12種類で既定10/明示99、長語/長basename/CR/注入候補を確認する。
textはcount TAB word LF、jsonは固定配列+LF、HTMLは元total/basename/3列/連番とliteral pairsを確認。
正常空はexit0、入力失敗exit1、usageは入力前exit2。非整数/欠落/既存不正min/topとmax0/負数、読込拒否/decodeをpytestでも独立確認する。
stdout内容一致だけでは内部順序の証明にならない。

現headの`wordfreq/__main__.py`をread_fileし、35行元Counter、36行元total、37..39行包含AND、40行top、46..50行共有pairsを確認する。
`original-Counter/total -> AND -> top -> shared-pairs`の順、元Counter不変、元total保持、casefold後の初出順をsource hash/行/具体notesとともに記す。

## 品質台帳とfinalize

採取原本を読んだ後だけ、capture rootの外にreviews.jsonを作る。画像可読性やCI成功を自動記入しない。
必須keys: head、profile、capture_sha256（manifest.json）、source_sha256（現__main__.py）、source_order（上の文字列）、source_notes、ac_reviews（AC1..AC6各具体結果の文字列）。
各ac_reviewsに下表のREQ/原本path/入力/正確argv/exit/stdout/stderr/期待値/HTML/結論を列挙する。

```sh
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode finalize --role quality --output-dir .planning/argonauts/r-d4bcda40/quality/final-01 --baseline-dir .planning/argonauts/r-d4bcda40/baseline --review-ledger .planning/argonauts/r-d4bcda40/quality/reviews-01.json
```

finalizeは現head/hashと台帳の完備性を検査するだけで、品質本人の読取りを機械的に証明しない。
quality-content-reviewedでも独立受入完了ではなく、以下の文字証拠配送と品質判断が残る。
Builderのcaptureからquality受入へ昇格しない。未閲覧/欠落/改変/偽head/未完了suiteは拒否する。

## AC/REQ別の記録

| AC | REQ | 判断と原本 |
|---|---|---|
| AC1 整数・省略 | REQ-23,REQ-26 | parser/help/整数表記/変更前39case固定bytes、default/large/explicit-min |
| AC2 包含 | REQ-24,REQ-25 | max1/max2/zero/negative、全3形式pairsと三出口 |
| AC3 min併用 | REQ-24,REQ-25,REQ-26 | min2max2/3順交換/inverted/top1/triple元12、内部spy |
| AC4 全試験 | REQ-27 | 先行RED/GREEN原本、追加/全suite argv・実数・環境・exit・時間、suite.xmlとログ |
| AC5 README1例 | REQ-28 | test_max_count_readme_example、掲載入力/実CLI beta3 alpha2 JSON+LF |
| AC6 scope | REQ-26,REQ-27 | scope.json全path/内容、既存試験保持、製品2箇所/README関連だけ、依存/CI/formatter不変 |

品質は`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q`を自分でも実施する（review-session内も同じ標準command+JUnit）。
0 collected/非0/ERROR/skipを成功にせず、追加と全suiteの実数を区別する。30秒超はlatencyとして記録し高速としない。
RED/GREENはbuilder/07-01,07-02,07-03のstage別原本。実装後変異の失敗を先行REDへ付替えない。
Git scopeは今回STARTからの全path/内容。製品/READMEの承認hash、既存tests/test_cli.pyのappend-only、他製品/依存/CI不変を確認。

## CIと配送の3gate

CIは対象headでActions/statusを有限1回読み、正確なcontext/run/状態/結論/取得headをcli-ci-proof.mdへ保存。
Checks APIや待機ループを使わない。未報告CIは未確認でありローカル成功をCI成功へ置換しない。

1. 保存: 品質本人が`.planning/phases/07-wordfreq-max-count/07-VERIFICATION.md`とquality/final-01に隣接する`cli-ci-proof.md`を作る。
   全AC/REQ別に自分の実行結果と原本索引、head/profile/task/run、画像0枚/ブラウザー未実施の判断出典を明記する。
2. 標準添付: 品質本人のカードでVERIFICATION.mdとCLI/CI文字証拠原本をkanban_attachする。
   content_base64にargonauts:worktree:<相対path>を指定し、kanban_attachmentsで最新添付ID/保存名/絶対pathを読み戻す。
   原本と保存先のSHA-256を照合して配送記録へ残す。拒否を圧縮/改名/外部送信で迂回しない。
3. PM読取り: 受取PM本人が標準添付の文字原本をread_fileで読み、照合hashと結果を自分のカードへ記録する。
   PMに画像や圧縮物の閲覧を求めない。標準添付成功とPM原本読取りは別gateで、未読は未完了。

OpenSpec2.2の完了は独立品質のフェーズ検証とPMへの配送で判断する。Builderは2.2をチェックしない。
headが変われば新rootで独立採取をやり直す。過去の合格・CI・報告commitを現在の対象headへ付替えない。
