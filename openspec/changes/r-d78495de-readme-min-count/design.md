# Design

## Context

動機はproposal.md参照。最新判断（2026-11-25T06:53+09:00）で確認は2点に縮小された。full維持、skip_specsでspecsは省略、designはtasksの前提として記録する。Architecture不要。

## Goals / Non-Goals

**Goals:** README例1つの追加と、最終PR全変更がREADME.mdだけであることを文字で確認する。

**Non-Goals:** text・json・htmlの実行確認とその入力・出力・終了コード等の証拠作成。CLI・試験・依存・設定・公開契約・HTML表示は変更しない。

## Decisions

- 既存使用例に `python -m wordfreq input.txt --min-count 3` を1つ追加する。例の置換や3コマンド追加はしない。既存の任意UTF-8ファイルを指定する説明は維持する。
- 検証はREADME原本と追加差分、最終PR base/headを特定した `base...head` 全変更一覧を文字で確認する。工程文書を除外した一覧ではファイル限定を証明できない。
- full工程原本はGit保存・push・カード添付する。最終PRは後続のチームD.5指定ファイル限定手順で工程文書を外して整える。原本を失わず、最終PR変更はREADMEだけにする。文書の個別削除や比較対象からの隠蔽で代用しない。
- Builderとqualityは2条件の文字証拠を残し、PMがread_fileで読む。旧3形式実行要件は失効した。実行成功を主張する必要もない。

## Risks / Trade-offs

- [旧受入条件の残存] → 最新判断日時を引き継ぎ、3形式実行を対象外と明記する。
- [工程文書が最終PRに混入] → 添付原本保持とD.5整備後、PRの全変更一覧で判定する。途中branchの工程文書を最終受入済みと混同しない。
- [無関係な本文変更] → README差分を読み、既存例・説明・末尾行の保持を確認する。
