---
title: "wordfreq HTMLの表示語種類数 — PRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-26"
updated: "2026-11-26"
request: r-6ae2cbf2
persona: John
source_brief: ../brief/brief-wordfreq-displayed-types.md
---

# wordfreq HTMLの表示語種類数 — PRD

## Table of Contents

- [Document purpose — 読者・入力・粒度](#document-purpose)
- [Vision — 今回の到達点](#vision)
- [Users and journeys — 対象利用](#users-and-journeys)
- [Glossary — 総出現回数と表示語種類数](#glossary)
- [Features and requirements — 機能と受入対象](#features-and-requirements)
- [Rules — 維持する契約](#rules)
- [Non-goals — 増やさないもの](#non-goals)
- [MVP scope — 変更範囲](#mvp-scope)
- [Success metrics — 判定と対抗指標](#success-metrics)
- [Quality and constraints — 既存品質の維持](#quality-and-constraints)
- [Change boundary — 差分と検証上の注意](#change-boundary)
- [API contract and versioning — CLI互換性](#api-contract-and-versioning)
- [Developer experience — READMEの1行](#developer-experience)
- [Stories — 小変更の受入](#stories)
- [Decisions — Architecture・省略・引継ぎ](#decisions)
- [Assumptions — 非重大な推定](#assumptions)
- [Open questions — 未決事項](#open-questions)

## Document purpose

Builder・品質担当・依頼者が r-6ae2cbf2 の範囲と受入条件を同じ意味で読めるようにする。指定は full、成果物は Brief と本 PRD の文書のみ。本書は initiative の単一機能を扱い、集計やレンダリング方式の再設計・実装計画には踏み込まない。

入力は依頼原文と [Brief 原本](../brief/brief-wordfreq-displayed-types.md)。既存 `_bmad-output/initiative-r-6ae2cbf2/initiative-r-6ae2cbf2.md` は frontmatter のみなので、存在しない Requirements を既決仕様として補完せず、依頼原文を要求の根拠とする。現状根拠は `wordfreq/formatters.py:22–38,108–124`、`wordfreq/__main__.py:35–55`、`README.md:19–29,55`、`tests/test_formatters.py`、`tests/test_cli.py`、`pyproject.toml`。

## Vision

wordfreq の HTML を読む人が、表を手で数えずに表示語種類数を把握できるようにする。表の上の総出現回数の横へ `表示 N 種類` を出す。これは依頼者が指定した小変更であり、利用者調査や利用規模に関する推定を製品要求に置き換えない。

総出現回数と表示語種類数は異なる情報である。前者の契約は維持し、後者だけを追加する。text/json を使う人への出力変更はない。

## Users and journeys

対象は HTML 出力を読む人。既存のコマンドで生成した HTML の表を見るとき、総出現回数の横で実際の表示語種類数を確認する。新しい操作や入力は増やさない。この単一 CLI 機能では実在しない人物の物語を作らず、Brief の利用ニーズを FR-1 の根拠とする。

## Glossary

- **総出現回数:** 全入力を正規化・集計した出現回数の合計。min-count / max-count / top 前の値。表示行の和でも語の種類数でもない。
- **表示対象:** min-count 以上かつ指定時の max-count 以下の語を既存順で並べ、top で制限した最終結果。現状では HTML 整形部品へ渡す `pairs`。
- **表示語種類数 N:** 表示対象の件数、すなわち表のデータ行数。見出し行は含めない。表示する語は正規化後の種類であり、元入力の表記ゆれを別種類として数えない。
- **表示文言:** `表示 N 種類`。N は実際の件数を表す非負の整数であり、例の3を固定しない。

## Features and requirements

### HTML の表示範囲を確認する

- **FR-1:** HTML 読者は、表より上の既存総出現回数の横で表示文言を読める。N は実際の表示語種類数と一致する。空入力、語なし入力、絞込みで全件除外された結果では `表示 0 種類` を示す。Brief の B1・B2 の実現であり、受入は表示テキスト・位置・表データ行数の照合で行う。
- **FR-2:** Builder・品質担当は追加された自動テストで FR-1 と RULE-1〜RULE-3 を検証できる。通常の入力、表示語種類数が3以外の場合、top による件数制限、候補数が top の指定値未満の場合、min/max 絞込み、既定 top、空入力、空白・記号のみの語なし入力、絞込み後0件を扱い、固定3・top指定値・絞込み前件数・出現回数合計を表示する誤りを検出する。Brief の B4・B5・B6 に対応する。
- **FR-3:** CLI 利用者は README.md の HTML 説明に追加された1行で、総数横の表示文言と N の意味を確認できる。1行は「表示した語の種類数」であること、絞込み/top 後であること、空なら0であることを説明する。既存説明や他形式の契約は書き換えない。Brief の B6 に対応する。

FR-2 の具体的な照合例は、既存 `tests/test_cli.py:858–908` の入力と期待行を再利用できる。`beta beta beta alpha gamma alpha delta` に `--max-count 2` を指定すると、表示対象は alpha / gamma / delta、表示は3種類で総出現回数は従来の7。さらに `--top 1` なら表示1種類、`--top 99` でも候補数の3種類である。`--max-count 0` では表示0種類だが総出現回数は7を維持する。空入力では表示0種類かつ総出現回数0。既存の12候補を残す入力（`tests/test_cli.py:872–874`）では、top省略で表示10種類、top99で表示12種類となることを照合する。これらは受入仕様例であり、本作業で実行した試験結果ではない。

## Rules

- **RULE-1:** 既存の総出現回数、表の語・回数・順位・並び順、空結果メッセージを維持する。N の追加のために入力を再読込みしたり集計や選択条件を変えたりしない。
- **RULE-2:** text/json の標準出力は文字列・バイト・末尾改行・順序を含め従来どおり。CLI の引数、正常／エラー時の終了コード、stderr、エラー時の空 stdout を維持する。
- **RULE-3:** HTML は引き続き静的な UTF-8 文書とし、既存のテキストエスケープ・basename のみの表示を維持する。依存・権限・外部送信・データ移行は追加しない。

## Non-goals

全入力の総種類数の新表示、表示行の回数合計、新しい集計・ソート・トークン化、新しい CLI 引数、JSON のメタデータ、text の見出し、HTML の対話操作・全体再デザインは対象外。新しい利用分析、性能予算、権限や移行の仕組みも作らない。

## MVP scope

FR-1 の HTML メタデータ小変更、FR-2 のテスト追加と必要な既存 HTML 期待値の整合、FR-3 の README 1行を含む。要求は既に最小のため分割・削減候補はない。将来機能を約束しない。

この文書作成では製品コード・テスト・README を変更せず、commit/push/kanban 操作をしない。実装・品質確認・受入は親が管理する後続工程である。

## Success metrics

- **SM-1:** 現状は表示語種類数の表示なし。受入目標は FR-2 の全対象ケースで FR-1 の N と実データ行数が一致し、総数の横かつ表の上に表示されること。対抗指標は RULE-1 の総数・行内容・順序・空結果の不変で、件数だけ合って表が変わる実装を合格にしない。
- **SM-2:** 現状の text/json 出力を基準として変更0、対象の既存回帰と追加テストに失敗0。FR-2 を検証する。対抗指標は HTML に必要な期待値更新を text/json に波及させないことと、検証対象を削除・緩和して緑にしないこと。
- **SM-3:** README の既存 HTML 説明に意味の分かる追加1行があり、FR-3 を満たす。対抗指標は既存コマンド例と総出現回数の説明が維持されること。

試験合格や実装済みの実測値は本書では主張しない。

## Quality and constraints

RULE-3 は既存契約の維持であり、新しい NFR を導入しない。追加表示が通常幅・狭幅で読め、総出現回数や表を隠さないことを、変更箇所に絞って実表示で確認する。総出現回数の横という位置関係は DOM 順序だけを証拠にせず、描画結果を確認する。既存の検証方法を再利用し、文書作成中にブラウザや検証サービスを起動しない。

## Change boundary

変更するのは HTML の総数横の表示と、その追加を説明・検証する箇所のみ。`format_html(pairs, basename, total)` の引数、純粋整形の責務、CLI の共有選択処理は維持可能であり、変更する必要はない。DOM class や CSS の具体的実装はここで増やして規定しない。

既存 `tests/test_formatters.py:94–134,218–262` は class と CSS を厳密に検査し、`tests/test_cli.py:201–260,425–441` はメタデータ辞書を比較する。さらに `tests/test_cli.py:796–817,1017–1029` は以前の HTML を含むバイト期待値を参照するため、新しい表示と衝突しうる。後続実装では HTML 変更の正当な差分のみを期待値へ反映し、text/json の保存済み期待値や安全性検査を緩めない。古い HTML バイト一致をそのまま要求することも、テストを丸ごと除外することも誤りである。封印済みの過去 baseline 原本は上書きせず、今回用の期待値またはテスト内の明示的な期待値変換で差分を扱う。過去依頼の製品 snapshot 固定による scope gate は今回の合否と区別し、その gate を無断で緩めない。

検証は既存の `tests/test_formatters.py` と `tests/test_cli.py` へ追加し、Builder・品質担当が実在する検証ファイルから実行する。未作成の検証コマンドやテスト関数名は本書に書かず、本作業では製品テストを実行しない。既存テストの読取りと BMAD 文書 CLI の検査を、製品の合格証拠にしない。

## API contract and versioning

公開 CLI の引数と text/json は不変。HTML のメタデータに表示文言が加わることだけが意図する出力差分である。版番号変更、新しい公開 API、廃止・移行手順は要求しない。

## Developer experience

FR-3 の追加行は既存 README の HTML 説明に置く。既存の起動方法・UTF-8 の説明・総出現回数の意味は維持し、別のガイドや検証ツールは要求しない。

## Stories

HTML 読者として、総出現回数の横で実表示種類数を確認したい。受入条件は FR-1〜FR-3 と RULE-1〜RULE-3。正常例・絞込み・top・空結果を FR-2 で検証し、README の追加行も確認する。ストーリーの登録や次工程への実行はこの文書作成に含めない。

## Decisions

- 明示指定の `prd` テンプレートを使用。小変更に合わせて能力中心の構成とし、実在しないペルソナの物語や工程表は作らない。
- **Architecture は不要。** 既存 HTML 整形内には最終 `pairs` と `total` が既に渡され、表より前にメタデータを出している。件数を表示するために部品境界、API、依存、権限、送信、データ形式を新設する判断はない。根拠は `wordfreq/formatters.py:22–38,108–124` と `wordfreq/__main__.py:35–46`。新設計の引継ぎは不要。
- AI behavior、consumer/branded Experience、複数チームの Stakeholders/rollout、Integrations/operations、Data/compliance、SLO/performance、Consumer migration、Hardware は適用条件がないため省略する。確認したリスクは旧 HTML 期待値との衝突であり、Change boundary で扱う。
- 次工程候補は Sofia による initiative Requirements への反映。ただし本作業では記録のみとし、呼出し・チケット変更・工程進行をしない。PRD は各 epic 完了後に学びに応じて Update し、推定・未決を見直す。

## Assumptions

- [ASSUMPTION: Users and journeys] 主な読者はローカルブラウザで HTML を読む既存 CLI 利用者。Brief から引き継いだ非重大な利用者像であり、機能の受入条件を左右しない。
- [ASSUMPTION: Document purpose] 文書の深さは小規模な既存機能改善に合わせる。規制・契約など追加条件は提示されていない。新しい品質基準は推測で追加しない。

## Open questions

なし。依頼に未決事項はなく、機能入力を推測で補っていない。DOM の細部は未決要求ではなく後続実装の裁量である。
