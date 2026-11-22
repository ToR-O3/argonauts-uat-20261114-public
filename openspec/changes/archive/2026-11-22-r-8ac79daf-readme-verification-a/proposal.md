# Proposal

## Why

依頼者が指定した検証Aの文言をREADME.mdの末尾へ正確に掲載する。実施結果を新たに証明する依頼ではなく、指定文書の1行追記である。

## What Changes

- README.mdの末尾に独立した1行 `検証A: v1.12 の通しの確かめ（2026-11-22）` を追加する。かぎ括弧や句点は追加しない。
- 既存READMEの内容を削除・書換えせず、不要な空行も加えない。
- コード・試験を変更しない。工程の仕様・計画・検証文書は利用者向け変更と区別する。

## Capabilities

### New Capabilities

- `readme-verification-note`: READMEの指定検証文言と、その掲載範囲の契約。新しい実行時機能は導入せず、依頼された文書内容の受入要件だけを記述する。

### Modified Capabilities

なし。既存の`wordfreq-cli`の要件は変更しない。

## Impact

利用者向け変更はREADME.mdの1行追加のみ。API・依存・認証・権限・データ・外部送信・費用の変更なし。別件の句点追加は混ぜない。入力は `_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.md` と `_bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md`。この工程ではREADME自体を変更しない。
