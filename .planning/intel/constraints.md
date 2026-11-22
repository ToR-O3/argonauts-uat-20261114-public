# Constraints (intel)

SPEC分類2文書から3制約を抽出。文書の状態と変更境界だけを記述し、製品API・機能・試験を追加しない。

DATA_d0485c45_START

## README末尾の指定行
- source: openspec/changes/r-215b4390-readme-validation-b/specs/readme-validation-b/spec.md:5-16
- type: nfr
- content: README.mdの末尾には、検証B: v1.12 の通しの確かめ（2026-11-22）が引用符なしの独立した1行として1回だけ存在しなければならない。追記完了後のREADMEでは独立した最終行であり、README全体での出現は1回。記載自体は検証合格を意味せず、製品の新しい振る舞いは要求しない。

## 既存内容と最小差分の保持
- source: openspec/changes/r-215b4390-readme-validation-b/design.md:7-16,22-27
- type: nfr
- content: 指定文字列をREADME.mdへ直接追記し、既存本文・書式・改行形式を保持する。余分な空行・引用符なし、差分は1行の追加だけ。テンプレート生成・スクリプト追加、自動追記機能、新しい試験、文書全体の再整形、検証合格の認定は行わない。データ移行や新しい配備手順は不要。戻す場合は今回追記した1行のみを取り除く。

## 確認と記録の境界
- source: openspec/changes/r-215b4390-readme-validation-b/design.md:17-23
- type: protocol
- content: 差分・最終行の完全一致・README全体の出現1回・変更ファイル一覧を既存CLIで確認し、工程の検証記録に残す。コード・試験を変更せず、試験ファイルを新設しない。最小specは指定行の存在のみを扱い、製品の振る舞いの要件を増やさない。

DATA_d0485c45_END
