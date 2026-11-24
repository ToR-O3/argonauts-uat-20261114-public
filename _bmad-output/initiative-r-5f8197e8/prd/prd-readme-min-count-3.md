---
title: "README --min-count 3 実行例のPRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-24"
updated: "2026-11-24"
---

# README --min-count 3 実行例のPRD

## Table of Contents

- [Document purpose — 入力と読者](#document-purpose)
- [Vision — 説明改善の目的](#vision)
- [Users and journeys — 読者と作業上のneed](#users-and-journeys)
- [Glossary — 例・入力・証拠原本](#glossary)
- [Features and requirements — FR-1〜FR-3](#features-and-requirements)
- [Rules — RULE-1〜RULE-4](#rules)
- [Non-goals — 対象外](#non-goals)
- [MVP scope — 今回の範囲](#mvp-scope)
- [Success metrics — SM-1〜SM-3と対抗指標](#success-metrics)
- [Change boundary — 変えるものと維持するもの](#change-boundary)
- [API contract and versioning — CLI契約の維持](#api-contract-and-versioning)
- [Developer experience — READMEの実行導線](#developer-experience)
- [Stories — 作業単位と受入条件](#stories)
- [Decisions — 確定事項と理由](#decisions)
- [Open questions — 未決なし](#open-questions)
- [Assumptions — 非重要な作業上の具体化](#assumptions)

## Document purpose

実装担当、品質担当、PMが、READMEへの例追加と後続検証の範囲を共有するためのinitiative PRD。例は1つだけ追加し、同じ入力と閾値で3形式を実際に動かして裏付ける。PMが文字の証拠原本から実行の事実と出力確認結果を追えることを受入の前提とする。

本書は仕様工程の成果物。READMEの変更やCLIの実行はまだ行っておらず、以下のコマンドと確認条件は後続工程への指定であって実行結果ではない。

入力は [Brief](../brief/brief-readme-min-count-3.md)、利用者の依頼・確定事項、`_bmad-output/initiative-r-5f8197e8/initiative-r-5f8197e8.md`、`README.md` と既存CLIの `wordfreq/__main__.py`、`wordfreq/aggregator.py`、`wordfreq/formatters.py`。initiativeファイルはメタデータのみで、要件の出典は依頼とBriefである。

## Vision

READMEを参照する人が、既存の最小出現回数フィルタを `--min-count 3` で指定する方法を具体例から理解できるようにする。READMEには閾値2の例があるが3の例はなく、利用者が今回の追加を依頼した。機能の追加や改善効果の数値推定は行わない。

## Users and journeys

- READMEの読者: 閾値3の例を見つけ、UTF-8実ファイルで実行する（FR-1）。
- 実装担当・品質担当: 同じ入力・閾値で3形式の語・回数と形式固有の表示を確かめる（FR-2）。
- PM: コマンド・終了コード・出力の文字原本を `read_file` で読み、成功主張の根拠を確認する（FR-3）。

## Glossary

- **追加例**: READMEの使い方に1つ加える `--min-count 3` のCLI実行例。
- **同じ入力**: 追加例の実行と3形式の検証で共通に使うUTF-8実ファイルの同一内容。各形式の前に内容を変えない。
- **閾値3**: 出現回数が3以上の語を残す既存フィルタの指定。3未満は表示対象にしない。
- **3形式**: `text`、`json`、`html`。語と回数は共通で、出力の表現は異なる。
- **文字の証拠原本**: 実際の実行コマンド、終了コード、出力と確認結果を保存した工程上の文字ファイル。画像や口頭報告だけで代用しない。
- **利用者向け変更**: 今回はREADME.mdのみ。Brief、PRD、レビュー、実行証拠などの工程文書とは区別する。

## Features and requirements

### READMEの例追加

**FR-1.** READMEの読者が「wordfreq の実行」の説明内で、`--min-count 3` を明示した実行例を1つ参照できる。既存の例と説明は保ち、追加例は次のコマンドを使う。

```sh
python -m wordfreq input.txt --min-count 3
```

`input.txt` は既存のREADMEと同様に、利用者が用意するUTF-8実ファイル。新しいfixtureをリポジトリに追加する要求ではない。

### 同じ例の3形式確認

**FR-2.** 実装担当・品質担当が追加例と同じ入力・閾値で3形式を実行し、各形式が終了コード0となり、表示対象の語と回数が一致することを確認できる。textは追加例そのもの（既定形式）、他の2形式では `--format json` または `--format html` だけを加える。`--top` 等の追加条件で結果を変えない。

後続検証では、閾値以上の語が残ることと閾値未満の語が除かれることの両方が観察できる入力を用意し、実際の内容と期待する語・回数を証拠に記す。これは検証入力の条件であり、入力ファイルや自動試験ファイルの追加を要求しない。具体的な準備方法は後続担当の作業裁量とする。

### 読める実行証拠

**FR-3.** PMが `read_file` で文字の証拠原本を読み、3形式それぞれの実行と出力確認を判定できる。原本には作業ディレクトリ、同じ入力のパスと内容、実行した完全なコマンド、実際の終了コード、標準出力・標準エラー、期待値との照合結果を記録する。CLI出力を要約だけに置き換えず、HTMLもテキストとして読める原本を残し、分離保存した場合はそのパスを示す。

記録先は当該initiative配下の工程証拠とし、PMへの結果報告には実在する原本パスを含める。未実行や出力未確認を成功として記録しない。

## Rules

- **RULE-1.** 利用者向け変更はREADME.mdだけ。工程文書・実行証拠は別扱いとし、コード・設定・依存・公開入出力・試験ファイルを追加変更しない。
- **RULE-2.** flowはfull固定。Architecture文書、HTML view、外部引継ぎは不要。検証対象のhtml出力はHTML viewとは別物であり、省略しない。
- **RULE-3.** 同じ入力・閾値3を3形式で維持し、3形式の実行と確認がそろう前に受入完了としない。
- **RULE-4.** 仕様段階では実装・実行済みを主張しない。実行の成功主張は後続の文字の証拠原本に基づく。

## Non-goals

RULE-1の変更禁止事項に加え、READMEの全面改稿、既存説明の互換性変更、新しい検証ツールの追加、既存HTMLの視覚品質全般の再設計は行わない。

AI動作、ブランド体験、外部連携・運用SLA、個人情報・規制対応、性能予算、利用者移行、ハードウェアは今回の変更対象でないため専用節を設けない。製品横断の新しい品質目標も追加せず、変更禁止事項と証拠要件をRulesにまとめる。

## MVP scope

今回の範囲はFR-1からFR-3まで。例1つの追加と、その例の3形式の後続実行・文字証拠だけであり、さらに削減すると明示依頼を満たさなくなる。将来リリースへ延期する機能はない。

主なリスクは、READMEと別の入力を検証すること、空結果だけでフィルタを確認したとすること、結果を文字で追えないこと。FR-2の入力条件とFR-3の記録でこれを防ぐ。担当の実行作業に必要な入力・出力の一時データは、利用者向けの追加ファイルとして残さず工程証拠と区別する。

## Success metrics

- **SM-1.** FR-1を評価する。現在のREADMEに閾値3の例は0、目標は追加例1つ。対抗指標は、既存例の削除・改変とREADME以外の利用者向け変更を0に保つこと。
- **SM-2.** FR-2を評価する。現時点では本依頼の3形式実行は未実施。目標は3形式すべてで終了コード0と内容照合の成功。対抗指標は、入力・閾値の不一致、閾値未満の語の誤表示、形式間の語・回数の差異を0にすること。
- **SM-3.** FR-3を評価する。現時点では本依頼の実行証拠は未作成。目標は3形式すべてのコマンド・実終了コード・出力確認が原本パスから読めること。対抗指標は、出力未保存や自己申告だけでの成功判定を0にすること。

これらは受入条件であり、利用者数や事業効果の測定値ではない。

## Change boundary

変えるのはREADMEの使い方に足す例と、その理解に必要な局所的説明だけ。既存の例・注意書き・説明の意味は維持する。

既存の集計、正規化、同数時の初出順、topの既定値、各形式とエラー処理は変更しない。textは `count`、タブ、`word`、改行。JSONは、`word` と整数の `count` を持つ要素の配列で、末尾に改行を付ける。HTMLはUTF-8静的文書で、表の順位・単語・回数、basenameとmin-count/top前の総出現回数を持つ。後続確認はこれら既存契約に対して行う。HTML総数を表示行の和と取り違えない。

## API contract and versioning

公開CLIはRULE-1とChange boundaryのとおり維持する。新APIや互換性移行は不要。起動表記 `python -m wordfreq` も既存のままとする。

## Developer experience

READMEはリポジトリ直下でUTF-8実ファイルを指定する既存の案内を保つ。新しいセットアップ、インストール、Webサーバーを要求しない。text例は既定形式のまま1つ追加する。3形式の検証コマンドを、READMEにも3例として追加する必要はない。

## Stories

作業単位は「READMEの閾値3の例を補い、同じ例の動作を証拠で示す」。受入条件はFR-1の例1つ、FR-2の3形式の成功と内容一致、FR-3の読める原本、RULE-1の差分境界をすべて満たすこと。実装担当が例追加と実行証拠を用意し、品質担当が同じ条件で独立に確かめ、PMが文字証拠を読む。未実行・証拠欠落・不一致があれば受入を止め、コード修正へ無断で広げない。

## Decisions

FR-1のコマンドは既存の入力名・起動表記を維持し、不要なtop指定を加えない。既定textを使うのは例そのものを検証するためである。

Brief→PRDとRULE-2は利用者指定。Architectureは既存CLIの説明だけなので不要とした。各epic完了後にPRDを見直し、学びによる変更はUpdateするが未承認の拡張は加えない。Briefで省略したVisionは将来構想を指し、本PRDのVisionは今回の目的だけを要約する。

## Open questions

なし。承認を要する未決の事業判断はない。後続担当が検証入力と証拠ファイルの具体的な準備方法を選ぶことは、要件の未決ではなく作業裁量である。

## Assumptions

- [ASSUMPTION: FR-1のinput.txtと既定textの採用は既存READMEに合わせた文書作成側の具体化であり、利用者が指定した入力名・形式ではない。後続担当が例と同じ入力を使う要件は変わらない。]
- [ASSUMPTION: FR-3の作業ディレクトリ・入力内容・標準出力/標準エラーの記録は、利用者指定の文字証拠を追跡可能にするための作業上の具体化。追加の事業判断や重要入力の推定ではない。]
