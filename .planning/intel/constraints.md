# Constraints (intel)

SPEC分類のtasks.mdから3制約を抽出。nfr 3件。新しいAPI/schema/protocol契約はない。以下は後続工程の制約であり、本synthesisで実行する指示ではない。

DATA_932ab4e6_START

## 指定例1つの追加と既存内容の維持
- source: openspec/changes/r-d78495de-readme-min-count/tasks.md:5
- type: nfr
- content: README.md の使い方に `python -m wordfreq input.txt --min-count 3` を1つ追加し、既存例・説明・末尾行を維持する。README原本と差分を読んで追加例1件を確認し、文字証拠をカードへ添付する。実装・試験・ツール・依存・設定・公開入出力は変えない。

## 独立確認と最終PR全差分の文字証拠
- source: openspec/changes/r-d78495de-readme-min-count/tasks.md:9
- type: nfr
- content: qualityがREADME原本と差分で例1つの追加を独立確認し、チームD.5整備後の最終PR `base...head` 全変更一覧がREADME.mdだけであることを確認する。base/head・全一覧・2条件の判定を文字証拠とVERIFICATION.mdに記録してカードへ添付し、PMがread_fileで読む。工程文書をpath除外して判定しない。最終PR整備前の確認は暫定とし、残る工程ファイルを明示する。

## 最新判断の検証範囲と工程原本の境界
- source: openspec/changes/r-d78495de-readme-min-count/tasks.md:13-15
- type: nfr
- content: 最新判断2026-11-25T06:53+09:00の確認対象は例1つと変更ファイルREADME.mdのみ。text・json・htmlの実行確認、検証入力・出力・終了コードと実行証拠は対象外。旧タスク1.2は撤去済みで未完了に残さない。full工程、工程原本のGit保存・push・カード添付を維持し、後続のD.5で最終PRから工程文書を外した後に品質が最終全差分を再確認する。仕様承認・計画・実装・品質確認・受入・最終化は既存カードで行う。振る舞い不変の文書変更としてspecsはskip_specsで省略する。

DATA_932ab4e6_END
