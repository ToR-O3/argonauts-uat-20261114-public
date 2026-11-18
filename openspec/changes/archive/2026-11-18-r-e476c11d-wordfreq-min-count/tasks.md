# Tasks

この一覧は仕様承認後の実装・検証対象。本要求・仕様工程では未着手とする。対応: MC-1→AC1/3/4、MC-2→AC1/2/5/7、MC-3→AC6/7。GSDの具体PLAN分割は後工程。

## 1. 引数と共通選択、対応する試験と説明

- [x] 1.1 実装着手前head・環境・入力・argvを固定し、既定text/json/htmlの変更前stdoutとHTML比較原本・画像を保存する。後の同条件比較で辿れることを確認する（AC2、見た目不変）。
  - 04-01: 製品未変更の正式task commit `789cc17267fb4cfeea24111797c3d934c542ce6a` から一度採取。`.planning/argonauts/r-e476c11d/baseline/index.json`（SHA-256 `d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089`）、12 CLI/18実browser view/32画像、saved原本16試験と全392試験がexit0。事前採取gateと正確なコマンドは `.planning/argonauts/t_337d3562/BASELINE-GATE.md`。実画像閲覧・変更後比較・独立品質合格を意味しない（2.1/2.2は未完）。
- [x] 1.2 min-countの正数・既定・異常値/欠落・入力読込み前のexit2を各形式で検査するpytestを先に追加しREDを確認してから、既存argparse方式で引数を実装する。有効N>1の入力取得失敗exit1も確認する。READMEに指定法・既定1・不正値とexit2を説明し、対象pytestの成功とヘルプ/記載例の実CLI結果で検証する（AC3、AC7）。
- [x] 1.3 全形式の閾値未満/ちょうど/超、casefold合算、同数初出順、topとの独立値・指定順・共通選択経路を検査するpytestを先に追加しREDを確認してから、元countsを保持し閾値除外→既存top選択の順に実装する。READMEに順序と例を追記し、対象pytestと全形式実CLIの期待pairs、ソース順序の確認で検証する（AC1、AC2、AC4）。
- [x] 1.4 空ファイル/空白のみ/句読点のみ/全件除外とHTML総数の新規pytestを先に追加しREDを確認し、必要な修正後に成功を確認する。HTMLには元totalを渡し、formatter/CSS/文言を維持する。READMEに全件除外時は閾値を下げる案内を追加し、総数0と語あり全除外の正の総数、各形式の空出力を実CLIと試験で検証する（AC1、AC5）。

## 2. 統合確認と独立品質の証拠

- [x] 2.1 既存全件と新規pytestを実行し環境・収集件数・結果・終了値を保存する。変更前原本/未指定/明示1の全形式比較（同数と10種類超を含む）、CI・依存・見た目の差分なしを確認し、各ACへ証拠を対応付ける（AC2、AC6、AC7）。
  - 04-03: clean head `d6dcbef0295f2052324188a24f32d1698c3e1d60`、Builder run149 の許可済み一度限り再採取 `.planning/argonauts/r-e476c11d/builder/04-03-capture-retry-run149/manifest.json`。全683試験exit0、62 CLI/68 view/110画像、24既定比較、saved_capture 25試験exit0を2回。scope/環境/bytes/raw/画像の機械比較とAC1〜7索引を保存。pending-review/independent_acceptance=false。失敗原本・baseline不変。独立品質の画像実閲覧と見た目の最終受入は2.2に残す。
  - 04-04: clean head `904e95b8b1e9910f95d5832cfe9620370feb5ff9`、Builder run154。人の許可で失敗run153原本を保持し新root `builder/04-04-integration-retry-run154/` へ一度再採取。全685試験exit0、62 CLI/68 view/110画像・24比較・errors空、saved_capture 27試験exit0（112.85s）。採取283.092s、pending-review/independent_acceptance=false。品質2.2・PM原本読取り・現head CIは未実施。
- [x] 2.2 品質が検証headで自らCLIを再実行し、既定・閾値部分表示・top併用・全件除外・空結果のHTMLを通常幅1280×900/狭幅320×900・DPR1で開いて閲覧する。比較元と同環境の画像、入力/argv/exit/stdout/stderr/HTML原本、対象head、文字範囲と安全性の既存契約を含む検証証拠を保存・添付し、AC1/2/4/5/6/7と照合する。フィルタ→topのソース箇所も記録し、未検証を合格にしない。

  - 最終化 t_68f21475/run162で既に満たしたgateを記録・終結。品質 t_419e62f7/run157、final-01 accepted（製品head `afaa56fc022c895ee2243b8f67a239c7c0096086`、報告head `421a65cb024c848ec8a0b9ff2ff5aec1538abfde`）。標準添付197 VERIFICATION/198 UATと188/189/191〜196が根拠。品質694/694 pass exit0、110 current＋32 baseline画像実閲覧、filter→top/original-totalソース確認は品質の実施記録でありBuilder/PMの実施ではない。
  - PM gate: t_a60abb2e/run160 添付199 `PM-READ-DECISION.md`、受入 t_9f464654/run161 添付220 `ACCEPTANCE-DECISION.md`（approved、AC1〜7充足）。人default 13:03承認に基づきPMのPNG閲覧を品質142画像実閲覧記録＋PM HTML/raw/CLI原本確認で代替。PM自身はPNG未閲覧、618件SHA一致は人の照合結果を採用。REQ17/P6は単発CLI以上の保証不要。
  - 添付191のCRITICAL1件は当時の未チェックtask2.2の履歴として保持。上記技術/PM gateを照合し本記録で未チェックを解消し、archive前に公式applyの6/6完了とvalidateを確認する。過去verify/VERIFICATION本文の古いhuman_neededを改変せず最新run/UAT/PM判断と併読する。
  - これは旧headで完了したgateの記録で、新headの合格ではない。最終品質は `docs/wordfreq-min-count-verification.md` §6どおり新head/fresh rootで独立CLI・全画像実閲覧・source-order・owner exit0・全derived整合・標準添付を全面再確認し、CI未報告を成功としない。

## Workflow follow-up

- 既存CI状態の有限回確認・PR・レビュー・OpenSpec verify・受入・sync/archiveはチームの担当カードで扱う。CIの追加変更や待機ループは導入しない。
- マージは人または品質が方針に従って予約したGitHub自動マージに委ねる。
