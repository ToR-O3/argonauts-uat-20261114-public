# Revision review — input reconciliation

## Verdict

**PASS：指定3入力との実質的な矛盾・採用決定の落ち・AD ID改変なし。** PRDの試験証拠条件はPRDに残されており、spine内の参照を強めるlowの改善だけをrubric報告のRG-L1へ集約する。これは仕様承認でも全Reviewer Gate完了宣言でもない。

## Inputs

- `../../prd/prd-wordfreq-exclude.md` 全文（FR-1〜FR-7、Rules、Change boundary、Developer experienceを含む）。
- `../../decision-update.md` 全文。判断日時 `2026-11-28T14:45:42.849521+00:00`、依頼者原文「提案のまま進めてください（1〜5 すべて提案どおり）。」。
- `../.memlog.md` 全文。旧Create時点の保留と更新追記:19–20を時系列で照合。
- Target: `../architecture.md` 全文。補助のsource-context/open-questionsと既存実装も照合。履歴の未承認文言を現在の決定より優先しない。

## 採用決定5件の反映

| 決定 | spineの対応 | 判定 |
| --- | --- | --- |
| 1 HTML総数は元入力全体、ランキングだけ除外 | AD-4:60、seed diagram:85。除外/min-count/top前の元Counterを保護し、全語除外/0行でも総数から引かない。 | 完全反映 |
| 2 trim後に空行/#開始行判定、LF/CRLF/最終改行なし | AD-2:48。処理順と全行終端を明示。 | 完全反映 |
| 3 UTF-8、全読込み失敗は理由付きstderr/exit2、結果/HTML/Tracebackなし、本文exit1維持 | AD-3:54。FILE識別、失敗causeと入力役割の保持、結果stdout空も明示。 | 完全反映 |
| 4 既存Unicode `\w+` に行全体一致後casefold、数字/underscore可、全不正例とファイル名/行番号 | AD-2:48とAD-3:54。複数語/句読点/hyphen/単独結合文字/末尾#注記/先頭BOMを不正とし、部分抽出/BOM除去による受理も禁止。本文抽出は変更しない。 | 完全反映 |
| 5 引数構文/数値→除外取得と全行検証→本文、除外失敗なら本文未読 | AD-3:54。単なる存在確認でなく全行検証までを本文より先に置く。 | 完全反映 |

## PRD reconciliation

| 要求 | spineの対応・残存先 | 判定 |
| --- | --- | --- |
| FR-1 任意--exclude、全出現除外、未指定互換 | AD-2:48、Public surface:67、AD-4:60。 | 反映 |
| FR-2 行形式・全境界例 | AD-2:48、AD-3不正行診断。 | 反映 |
| FR-3 casefold、lowerへ変えない | AD-2:46–48。 | 反映 |
| FR-4 全読込み失敗・不正行、出力抑止、優先順位 | AD-3:50–54。引数優先、除外の全検証、本文未読まで固定。 | 反映 |
| FR-5 共通pairs、min-count/top、安定順位、空/全除外、元HTML総数 | AD-2/AD-4。空text/json/htmlは「既存」形式を維持。具体的な空形式は現行formattersと一致。 | 反映 |
| FR-6 help/README | AD-1のBinds、Deferred:94がPRD説明要求の実装を直接指定。説明の全項目をspineへ再掲しないことは要求削除ではない。 | 参照委譲 |
| FR-7 試験と互換の証拠 | AD-1〜AD-4のBindsと互換/境界/順位規則。基準版 `79d83ba14dd59d289d2ecd3e33c85e8de437972e`、バイト一致、全異常例、本文未読検査、README例実行の具体条件はPRD:102–106/:139に存続。spineでの委譲明記は弱い。 | 参照委譲・low改善RG-L1 |
| RULE-1/2 | AD-1/2/4。既存抽出/正規化/順序/既定公開面を維持し、CLIのみexit判断。 | 反映 |
| RULE-3、新依存/通信/CI禁止、HTML安全性 | Conventions:68–69、Structural Seed:73。UTF-8/escape/basename/静的CSS/見た目と既存構成を維持。 | 反映 |
| RULE-4、承認の代用禁止/未決推測禁止 | 冒頭:19、Deferred:92、Assumptions:99。後続承認を先取りせず、5件は採用入力に限って確定。 | 整合 |
| Non-goals / MVP / Change boundary | Public surface:67、状態/環境:88、Deferred:93–95、AD-1/4。ファイル書換え禁止は:69。機能を広げるADはない。 | 整合 |

## Memlog reconciliation / stable AD audit

| ID | 旧記録 | 更新記録:19–20 → 現spine | 結果 |
| --- | --- | --- | --- |
| AD-1 | :10 取得境界/CLI組立/純粋処理 | 境界不変。:42がcount_words/top_words/formattersのI/O/argv/exit混入を禁止。 | ID維持、弱体化なし |
| AD-2 | :11 casefoldと初出順 | :19で採用済みtrim/行終端/full-line検証を追記 → :48へ反映。 | ID維持、追加決定落ちなし |
| AD-3 | :12 除外欠落exit2、本文exit1、他失敗は未承認 | :19で全除外失敗/診断/入力順を明示採用 → :54へ反映。旧保留を勝手に採用したのではなく、新承認で解消。 | ID維持、権限衝突なし |
| AD-4 | :13 共通pairs/非破壊Counter、HTML意味はOQ-1 | :19で元HTML総数維持を採用 → :60へ反映。 | ID維持、OQ解消を反映 |

- memlog:14のOQ-1〜OQ-5は:19の更新で解消。spine:19/:92と共通open-questionsの「なし」は整合する。
- memlog:15のfeature/build-substrate推定とインフラ非追加はspineのfrontmatter/:88/:99に残っている。
- memlog:16の旧ゲート実施履歴を今回の更新承認へ流用していない。:19–20とspine:19/:99は親による再reconciliation/Reviewer Gate未了を明示する。
- 現spineの決定見出しはAD-1、AD-2、AD-3、AD-4をそれぞれ一度ずつ使用。改番・ID再利用・退役IDの復活・新IDへの置換は見当たらない。
- 原本の過去リビジョン自体はこの担当で履歴取得していない。ID維持の結論は指定されたappend-only memlogの旧/新記録との照合に基づく。

## Findings / disposition

- Critical / High / Medium: なし。
- Low: rubricの **RG-L1**（FR-7/Developer experienceへの明示委譲）。独立の製品未決ではなく、PRDの義務を削除したという判定でもない。推奨は任意の1行参照追加、原本修正は親担当の判断。
- `conflicts_with_prior_decisions: []`
- `open_questions: []`（本reconciliationで新たな製品問いは発見しなかった）。

## Boundaries

作成したのはこの報告と `review-revision-rubric.md` のみ。architecture/PRD/decision-update/memlog/コードの編集、git操作、Kanban操作、製品実装は行っていない。親がlintと残りのconfigured reviewersを集約し、後続仕様承認は別工程として扱う。
