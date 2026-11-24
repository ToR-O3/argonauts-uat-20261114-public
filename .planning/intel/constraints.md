# Constraints (intel)

SPEC分類3文書から7制約を抽出。schema 2 / nfr 1 / protocol 4。下記は承認済み仕様の検証契約であり、この取込みで製品編集・検証スクリプト実行・品質受入を行う指示ではない。

DATA_b3a5ac1c_START

## descriptionの固定完成値
- source: openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md:9-19; openspec/changes/r-774f3cd6-pyproject-uat/design.md:15-18
- type: schema
- content: [project].descriptionを新設し、文字列 `argonauts-uat public (UAT)` と完全一致させる。依頼者指定 `argonauts-uat public` にASCII ` (UAT)` を1回連結した値。正規化・重複追加・空文字補完は禁止。必要な1行だけを追加し、全体再シリアライズを行わない。

## 指定入力・基準・承認の区別と直前照合
- source: openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md:21-31; openspec/changes/r-774f3cd6-pyproject-uat/design.md:16,24; openspec/changes/r-774f3cd6-pyproject-uat/tasks.md:7
- type: protocol
- content: 不変比較基準はcommit `b34cba0d008923e7f5267ce52d5403492ea53925` のpyproject.toml（description欠落）。指定連結元を現物の旧値と記録しない。新設許可と指定値は受付t_78c8849eの2026-11-24T13:00:38.567271+00:00の依頼者判断による。OQ-1は回答済み。改訂仕様のPM承認を文書commitまたはSHA-256で特定し、旧仕様承認と新設許可の組合せで代用しない。実装前にrepo・branch・パス・基準・description欠落・指定値・新設許可を再照合する。対象や基準が異なる、description既存、TOML解析不能なら推測せず編集せずPMへ返す。

## 他項目・既存バイト列・他製品ファイルの不変
- source: openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md:33-39; openspec/changes/r-774f3cd6-pyproject-uat/design.md:17-19,25-26
- type: nfr
- content: 製品変更はpyproject.tomlのdescription新設1行だけ。他のTOML項目・依存・他製品ファイル・無関係な書式を保持する。変更後からdescriptionだけを除いた解析済み構造は変更前と完全一致し、追加1行を除いた編集後バイト列も編集前と一致する（空白・改行・末尾改行を含む）。比較元treeは基準commit、比較先は製品commitへ固定する。追跡済み追加/削除/改名/mode、index、作業ツリー、未追跡一覧も確認する。工程成果物の除外パスと用途は全件記録し、工程ディレクトリ内という理由だけで任意コードを除外しない。製品試験ファイル・CIを追加変更しない。

## TOML全体の有効性と構造比較
- source: openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md:41-47; openspec/changes/r-774f3cd6-pyproject-uat/design.md:18
- type: schema
- content: Python標準tomllibで前後のファイル全体を解析する。編集後は構文エラーなし。固定完成値との一致、description除外後の構造一致、不変条件を個別に確認する。変更前に存在しないキーへアクセスして連結しない。解析成功だけで他の受入条件を代替しない。

## 検証スクリプトの成功・負例・実行エラー
- source: openspec/changes/r-774f3cd6-pyproject-uat/design.md:19,27-28; openspec/changes/r-774f3cd6-pyproject-uat/tasks.md:8
- type: protocol
- content: スクリプトは工程管理領域に置き、具体的コマンドと基準取得方法を計画で確定する。正しい値で成功し、工程管理領域の負例（欠落、接尾辞重複、異なる値、他項目変更、不正TOML）を拒否することを確認する。負例を製品へ書かない。要件不一致と実行エラーを区別する。編集前の期待失敗はTOML解析と基準取得が成功し固定完成値条件のみ不一致の場合に限る。欠落キーの無条件アクセスによる異常終了だけでは試験にならない。

## 同一製品commitと独立品質の文字証拠
- source: openspec/changes/r-774f3cd6-pyproject-uat/design.md:20,25,28; openspec/changes/r-774f3cd6-pyproject-uat/tasks.md:9,13
- type: protocol
- content: 品質は同じ製品commitと対象ファイルSHA-256を照合して独立検証する。製品commitのblobから算出したSHA-256と検証ファイルのSHA-256の一致も確認する。head・製品commit・ファイルSHA-256・基準commit・コマンド・終了コード・条件別結果を文字の検証文書へ記録して添付し、PMに画像や圧縮ファイルを開かせない。必須条件失敗・実行不能は未完了で停止し、残存差分と理由をPMへ返す。無関係な変更で修復せず、他者差分を一括復元しない。

## タスク順序・full工程・最終化境界
- source: openspec/changes/r-774f3cd6-pyproject-uat/tasks.md:3-15; openspec/changes/r-774f3cd6-pyproject-uat/design.md:36
- type: protocol
- content: task1.1承認・前提照合→1.2工程領域スクリプトと編集前期待失敗→1.3直前照合・description1行新設・全条件検証・証拠記録の順。1.3は直前照合/新設、全条件検証、証拠記録を別substepとして進捗表示する。全タスク完了、同一製品commitの独立品質合格、全受入条件成立、PM受入の後に最終化工程でOpenSpec sync/archiveし品質最終確認へ渡す。文書finalやOQ-1回答済みだけで実行しない。危険パスpyproject.tomlのため受付lightよりfullを優先した理由を最終報告まで引き継ぐ。

DATA_b3a5ac1c_END
