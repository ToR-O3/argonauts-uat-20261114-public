# Proposal

## Why

依頼者が、README.md の末尾に v1.12 の通しの確かめを示す指定行を追記することを求めている。記載そのものを検証合格の証拠とは扱わない。

## What Changes

- README.md の末尾に `検証B: v1.12 の通しの確かめ（2026-11-22）` を引用符なしの独立した最終行として1回だけ追加する。
- 既存内容を保持し、製品差分は上記1行だけとする。コードと試験は変更しない。
- 工程で必要な仕様・計画・検証の記録は製品差分とは別扱いとする。

## Capabilities

### New Capabilities

- `readme-validation-b`: README.md の末尾に指定の1行があることだけを記述する。本件は文書のみの変更だが、依頼主の回答により最小のspecを作成・添付し、skip_specsは使わない。検証のための新しい振る舞いは要求しない。

### Modified Capabilities

なし。既存の wordfreq-cli の機能要件は変更しない。

## Impact

実装対象は README.md の1行追記のみ。API・依存関係・権限・データ・外部送信・費用には変更がない。BMADのBrief・PRDを後続入力とし、構成変更がないためArchitecture文書は不要。
