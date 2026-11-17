# Requirements (intel)

MODE: merge。今回のPRD分類2文書の抽出。proposalの5項目とBMAD PRDのFR-1〜FR-4を出典別の9エントリで保持する。同一scopeの要約と具体化は同時に満たせるため競合variantではない。機能契約の正は承認済みdelta SPEC（constraints.md）。A-01〜A-04 / Q-01 / Q-02は要件に昇格させずcontext.mdへ残す。以下は受入条件の抽出であり、実行結果・合格宣言ではない。

DATA_363c7166_START

## REQ-min-count-option-proposal
- source: openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:9
- description: 最小出現回数オプションを追加する。
- acceptance: --min-count N、既定1、1以上の整数のみ。不正値・値欠落は使い方エラーexit2。
- scope: CLI引数、MC-1、AC3

## REQ-min-count-selection-proposal
- source: openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:10
- description: 正規化後集計から表示対象を選択する。
- acceptance: casefold後の集計からN未満を除外し、その後既存topを適用。両値は独立。同数初出順は不変。
- scope: 全形式の選択、MC-1、AC1/AC4

## REQ-min-count-empty-proposal
- source: openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:11
- description: 全形式で同じ対象と既存空形式を使う。
- acceptance: text/json/htmlで同じ表示対象。空入力・全件除外も既存の空形式を維持する。
- scope: 空結果、MC-2、AC1/AC2

## REQ-min-count-total-proposal
- source: openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:12
- description: HTML元総数と表示契約を維持する。
- acceptance: HTML総数はmin-count/top前の全出現回数。CSS・構造・既存文言は変更しない。
- scope: HTML総数、MC-2、AC5/AC7

## REQ-min-count-evidence-proposal
- source: openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:13,25-29
- description: 追加試験・利用説明と独立品質証拠を残す。
- acceptance: 正常・境界・異常・互換・併用のpytest、README説明、品質による実CLI生成HTMLの独立ブラウザ証拠。引数解析・必要最小限の集計選択・pytest・READMEに限定し、formatter公開契約・入力境界・Unicode抽出/casefold・同数初出順・静的安全性は維持。CI追加変更・依存追加・見た目変更・入力元追加・外部送信・権限・課金・削除は対象外。
- scope: 検証・説明・変更範囲、MC-3、AC6/AC7

## REQ-min-count-argument-prd
- source: _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:55-57,95,116,120,133
- description: FR-1 閾値指定と検証。
- acceptance: 既定1、1以上の整数。0/負数/1.5/abc/値欠落を各形式で入力読込より先にexit2、stderr通知、stdout空、Traceback/エラーHTMLなし。不存在パスでも引数エラーが優先。有効N>1では不存在・ディレクトリ・開けない・不正UTF-8はexit1のまま。既存topと同じargparse/int規則を継承し独自字句制約・上限・変換制限解除なし。重複指定は有効値の最後を採用、途中の整数変換エラーはexit2。権限試験不能は未検証と区別する。
- scope: CLI引数・既存入力エラー、MC-1、AC3/AC7

## REQ-min-count-common-selection-prd
- source: _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:59-61,71-75,94,96,101,112,114-115,127
- description: FR-2 共通の表示対象と既定互換。
- acceptance: 全形式でN未満を除外、Nちょうど/超を保持後top。大小相互制約なし、指定順によらず回数降順・同数正規化後初出順。元集計・入力非変更、既存top_words(counts, n)利用を壊さない。未指定/明示1/変更前stdoutを同数と10種類超の同一入力・argv・環境で比較し既定text/top10と構造を維持。着手前branch headと変更前原本を保存し変更後同士だけで代用しない。出力だけでなく品質が除外→topのファイル・行またはdiffを確認。Straße STRASSEをN=2でstrasse 2として全形式に残す。Zoo apple APPLE zoo bananaはN=2/top10でzoo2,apple2、N=2/top1でzoo2。
- scope: 共通選択・互換性・Unicode・top、MC-1/MC-2、AC1/AC2/AC4

## REQ-min-count-empty-total-prd
- source: _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:63-65,93,97,101,115,118
- description: FR-3 空結果とHTML総数。
- acceptance: 空ファイル/空白のみ/句読点のみ/全件除外はexit0。text空文字、jsonは[]と末尾改行1つ、htmlは既存メタ情報・3列見出し・0データ行・空状態文言・basenameのみを保持。総数は両フィルタ前の回数和で、抽出0語なら0、語あり全除外でも元の正数。Zoo apple APPLE zoo bananaをN=3なら0表示/総数5。閾値は入力・元集計を変更しない。
- scope: 空結果・HTML元総数、MC-2、AC1/AC5/AC7

## REQ-min-count-verification-readme-prd
- source: _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:67-69,77-83,98-118,124-137
- description: FR-4 試験と説明、および品質・範囲制約。
- acceptance: 正常/境界/異常/既定/併用の追加pytestと既存全試験を実行し、実コマンド・環境・収集件数・exit・結果・全形式CLI原本をAC対応で残す。0件収集/未実施は成功でない。品質は対象headでCLI HTMLを独立再生成し既定/部分表示/top併用/全除外/空を1280×900と320×900 CSS px・DPR1で実閲覧。変更前headのHTML/画像と入力・basename・ブラウザ版・フォント・viewport・DPRを揃え、環境差を記録。head/diff/argv/入力/exit/stdout/stderr/HTML/画像/閲覧結果を保存しcaptureやDOM/CSS一致だけで合格にしない。以前の証拠形式は参考のみで固定head/scope/AC/合格を流用しない。既存CIは対象headの必須contextとActions/statusを有限回確認、未報告/pending/不調を成功にせずCI待機処理・新CIを追加しない。CI・依存・見た目/CSS/テーマ/既存文言・新形式/入力源/形態素解析/抽出変更・全体リファクタなし。stdlibのみ、UTF-8/escape/静的性/プライバシー/入力境界/formatter公開契約と純粋性/既存試験を維持、pyproject.tomlは変更しない。READMEは指定法・既定1・先min後top・元総数・不正値exit2・全除外時は閾値を下げることのみ付随最小更新。
- scope: pytest・独立品質・README・範囲、MC-3、AC2/AC6/AC7

DATA_363c7166_END
