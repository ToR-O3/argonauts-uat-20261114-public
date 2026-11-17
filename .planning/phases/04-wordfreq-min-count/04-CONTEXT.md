# Phase 4: wordfreq min-count - Context

**Gathered:** 2026-11-18
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-e476c11d-prd.md)
**Approval:** t_a438e6b2 run140; request r-e476c11d; OpenSpec r-e476c11d-wordfreq-min-count

<domain>
## Phase Boundary
既存wordfreqに--min-count Nだけを追加する。text/json/html共通の表示対象を絞り、既定互換・初出順・HTML元総数を保持する。REQ-15〜REQ-21（AC1〜AC7）の全体をこのphaseで計画する。製品実装と実際の受入はBuilder・品質の後工程。新サービス・依存・CI・見た目の変更はない。
</domain>

<decisions>
## Implementation Decisions (locked)

### 引数・入力境界
- **D-01:** min-countは既定1、1以上の整数のみ。既存argparse/int規則を維持し、0/負数/非整数/非数値/欠落は入力取得より先にexit2、stderr通知、stdout空、Traceback/エラーHTMLなし。topとの大小相互制約を追加しない（MC-1、AC3、task1.2）。
- **D-02:** 有効N>1でも不存在/ディレクトリ/開けない/不正UTF-8は既存exit1、stderr通知、stdout空を維持する。既存のファイル入力境界・抽出/casefold・formatter公開契約を変えない。

### 選択順序と全形式
- **D-03:** casefold後のcountsからN未満だけを除外し、回数降順・同数時正規化後初出順で選び、その後topを適用する。text/json/htmlは同じpairsを使う。旧単語昇順への復帰は禁止。top/min-count値は独立で指定順によらない（MC-1/FR-2/FR-4、AC1/AC4、task1.3）。
- **D-04:** 閾値ちょうど/超を保持。Straße STRASSE→strasse2、Zoo apple APPLE zoo banana→N2/top10でzoo2,apple2、N2/top1でzoo2。出力比較だけで除外→topの内部順序を証明したことにせず、品質が該当ソース箇所を記録する。

### 元集計・空結果・見た目
- **D-05:** 元countsを破壊しない。HTML総数はmin-count/top前の回数和、表示行の和や種類数ではない。語あり全除外でも元正数を保持し、抽出0語は0（HTML-2、AC5、task1.4）。
- **D-06:** 空ファイル/空白のみ/句読点のみ/全除外は正常exit0。text空文字、json[]+末尾改行1つ、HTML既存メタ情報・3列見出し・0データ行・空文言を保持。basename限定/UTF-8/escape/静的安全性/formatter/CSS/文言/見た目は変えない（MC-2、AC1/AC5/AC7）。

### 既定互換と試験順序
- **D-07:** 最初の製品変更前にtask1.1を実施する。着手前head/環境/入力/argvと全3形式のstdout、HTML原本、1280×900・320×900 DPR1画像を保存。同数語と10種類超の入力を含める。後の未指定/明示1を同条件で比較し、既定text/top10と既存構造・初出順を維持する。変更後同士の比較で代用しない（MC-2、AC2、tasks1.1/2.1）。
- **D-08:** tasks1.2/1.3/1.4は対応するpytestを先に追加しRED確認→最小実装→GREEN。全3形式、境界/正常/異常/Unicode/独立top/空/抽出0語/全除外/既定互換と既存全pytestを実行する。環境/収集件数/実コマンド/exit/結果を保存し、0件収集・未実施を成功にしない（MC-3、AC6、task2.1）。

### 独立品質と配送
- **D-09:** task2.2の実行主体は品質。対象headで自らCLIを再実行し、既定/閾値部分表示/top併用/全除外/空のHTMLを1280×900と320×900 CSS px・DPR1で開き実閲覧。同環境のbaseline画像と比較し、対象head/argv/入力/stdout/stderr/exit/HTML/画像/閲覧結果/ソース順序をAC1/2/4/5/6/7へ対応付ける。既存文字範囲・安全性の証拠契約を維持。Builder証拠や自動captureを独立閲覧へ代用しない。未検証はgaps。
- **D-10:** 証拠原本の保存・標準添付・受取PMの読取りは別gate。索引とAC対応、head/run/root/path/SHAを残し、PMが読める原本を渡す。拒否や能力不足を迂回せず停止して理由を報告する。過去の証拠のscope/head/合格を流用しない。

### 説明・範囲・工程
- **D-11:** READMEの指定法/既定1/不正値exit2/先min後top/元HTML総数/全除外時の閾値調整のみ最小更新。新サービス・依存・CI追加変更・新入力元・抽出変更・全体リファクタ・テーマ/対話/サーバー・外部送信/権限/課金/削除は対象外（MC-3、AC7）。
- **D-12:** 有限回の既存CI確認・draft PR・レビュー・phase検証・OpenSpec verify・受入・sync/archiveはチームの該当カードで扱い、CI待機ループを導入しない。既存CI未報告/pending/不調を成功と呼ばない。Q-01背景/Q-02期限とA-01〜04は未提示/未承認のまま非要件。旧phase1/3のstaleは表示しても今回計画へ混ぜない。

### Claude's Discretion
既存コードを調べた最小の関数境界、試験ファイルの分け方、PLAN分割。各PLANは3task以内、同じ依頼branchへ順に積み上げる。baseline保存を製品変更より先に置く。検証コマンドと入力は当該task終了時点で存在し、他PLANの成果の有無にかかわらない独立PLAN検証を確保する。品質専用の確認はBuilderの自己承認タスクにしない。
</decisions>

<canonical_refs>
## Canonical References
- .planning/argonauts/r-e476c11d-prd.md — proposal→全spec→tasksの結合PRD。
- openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md — 目的と対象範囲。
- openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md — MC-1/MC-2/MC-3/FR-2/FR-4/HTML-2と全scenario。
- openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md — 1.1〜2.2の順序/対応。
- openspec/changes/r-e476c11d-wordfreq-min-count/design.md — 最小設計。
- _bmad-output/initiative-r-e476c11d/brief/brief-wordfreq-min-count.md — 背景未提示。
- _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md — FRとAC、仮定と未決事項の非要件境界。
- .planning/REQUIREMENTS.md — REQ-15〜21と既存REQ-11の有効初出順。
- .planning/ROADMAP.md — phase4目標。
- .planning/argonauts/r-e476c11d-learnings.md — 学習、旧昇順の注意、証拠配送。
- .planning/phases/03-wordfreq-html-output/03-CONTEXT.md — 現行HTMLと初出順。
</canonical_refs>

<specifics>
## Specific Ideas
beta beta beta alpha gamma alpha deltaをN2/top1でbeta3だけ/HTML総数7、N4なら0行/総数7。Zoo apple APPLE zoo bananaをN3で0表示/HTML総数5。既定互換は同数+10種類超を含む同一入力で全形式比較。
</specifics>

<deferred>
## Deferred Ideas
新たな利用背景や期限・効果を創作しない。依存/CI/見た目/入力元/形態素解析/全体リファクタは対象外。マージは人または品質が許可された予約のみ。今回のカードは計画まで。
</deferred>
