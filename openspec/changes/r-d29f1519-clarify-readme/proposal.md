# Proposal

## Why

依頼者はREADMEの先頭の説明文をもっと分かりやすくしたいが、新文はまだ選択していない。現物の3行目 `Argonauts v1.10 acceptance test repository.` を、何のための公開リポジトリかが一文で分かる日本語へ明確化することを提案する。実施時機の理由・理解度の実測は未確認である。

## What Changes

- 製品変更はREADME.mdの3行目だけ。1行目の見出しは対象外。
- 文案（未承認）: `Argonauts の動作を確認するための公開受入テスト用リポジトリです。`
- 対象Argonauts、公開であること、受入テストの用途を現物から引き継ぐ。最新版へのバージョン更新はしない。候補による `v1.10` の省略は個別に承認を求める。
- 受入基準案: 承認文との完全一致、当該1行の意味・用途の判別、READMEの他バイトとREADME以外の製品ファイルの保持。品質は専門語の補足や他節参照なしで用途を平易に言い換え、5要素の包含だけで明確化を合格にしない。
- 最終文・バージョンの扱い・検証基準・承認者・文書版を仕様承認で一組として確定する。依頼者が提案を選択したとは扱わない。

## Capabilities

### New Capabilities

なし。文書だけの変更で、新しい製品動作はない。

### Modified Capabilities

なし。既存 `readme-validation-b` はREADME末尾の指定行の保持を要求し、今回その行を変更しない。`wordfreq-cli` の機能変更もない。

`openspec instructions proposal` の文書のみの変更に対する指示に従い `.openspec.yaml` に `skip_specs: true` を指定する。架空の製品要件を作らず、詳細な文案・検証案は本proposal、design、tasksとBMAD PRDに残す。

## Impact

- 製品: README.mdの1行だけ。コード・API・依存・CI・設定の変更なし。現段階ではREADMEを編集しない。
- 原本: `69b97f1c9dfa7211367a9bdd0af885d80d8bf380` のREADME。1–2行目と4行目以降（改行・末尾改行を含む）をバイト単位で保持する。
- 工程文書: `.planning/`、`openspec/`、`_bmad-output/`、`.compound-engineering/`、`docs/solutions/` は配置境界。本依頼の成果物のみを明示して識別し、領域丸ごとの除外で無関係な変更を見逃さない。
- BMAD: `_bmad-output/initiative-r-d29f1519/brief/brief-readme-description.md`、`_bmad-output/initiative-r-d29f1519/prd/prd-readme-description.md`。
- 未決事項: 文案、v1.10省略、検証基準の採否。読者像・実施理由は未確認の仮説であり、追加調査を勝手に必須にしない。`_bmad-output/initiative-r-d29f1519/open-questions.md` に集約して仕様承認へ渡す。
