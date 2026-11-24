# Design

## Context

動機と対象はproposal.mdを参照。製品の設計変更はない。同じ例の検証であること、README限定と工程証拠の区別を、実装前に明確にするための作業設計だけを記す。BMAD Architectureは不要。

## Goals / Non-Goals

**Goals:** 1つのREADME例とREADME.mdだけの最終PR全差分を、独立品質の文字原本からPM本人が判定できるようにする。

最新判断（旧記述より優先）: 2026-11-24T21:20+09:00「(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。」。例外判断2026-11-24T13:39:57.048159+00:00「Aを選ぶ。この依頼に限り、原本の保全→最終化→品質の最終確認→受入の判断、の順を許可する。」。根拠 `.planning/argonauts/r-5f8197e8-fix-1.md`。

**Non-Goals:** 新機能、新しい試験・検証ツール、既存HTML全般の再設計、過去依頼の全条件の再実装。

## Decisions

- READMEの既存起動表記に合わせ `python -m wordfreq input.txt --min-count 3` を1つ追加する。3つの例の掲載は選ばない。既存説明と末尾行は維持する。
- 旧設計の同一UTF-8入力・3形式実行・語/回数/順序/構造の照合・実入力/出力/ログ・pytestは、依頼者の判断により対象外（2026-11-24T21:20+09:00）。新試験・fixture・quality runbookを作らず、実行済みとはしない。
- 必要な工程原本と変更後資料を標準添付ID/保存名/path/SHA-256で保全し、その後に最終化担当のみが既存工程文書を基準branchの内容へ戻し、今回新規の工程文書を最終treeから外す。保全前の除外・無差別削除は禁止。
- 最終品質は実PRのbase/head/merge-base、filterなし全name-status、README patch/全文で2条件を判定し、文字原本を非commit標準添付する。PM本人がread_fileで読んでから受入判断する。画像0枚（文字のみ）、zip不要。
- 現在は条件2未達、OpenSpec2.1未完、品質run37 gaps_foundを保持する。今回だけ最終化前にphase passed/受入approvedを要求しない。受入前自動マージ予約は禁止、手動待ち。skip_specs:trueを維持する。

## Risks / Trade-offs

- [旧実行義務の復活] → 最新縮小判断を優先し、対象外を合格と混同しない。
- [工程filterによる誤合格] → README以外が1件でもあれば条件2未達。補完レビューと最終受入を区別する。
- [原本の喪失・主体の混同] → 添付実体hashを照合し、独立品質とPM本人の判断までpendingを保持する。

移行は不要。READMEの局所追加を戻せば文書変更を取り消せる。未決事項はなし。ここに実行結果は含めない。
