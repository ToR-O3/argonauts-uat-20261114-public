# Proposal

## Why

wordfreqは頻度の下限だけを指定でき、出現回数の上限や頻度帯をCLIで選べない。依頼r-d4bcda40に従い、省略時の既存動作を保つ任意の上限指定を追加する。

## What Changes

- 整数オプション`--max-count N`を追加し、省略時は上限なし、指定時は正規化後の出現回数N以下の語だけを残す。
- 既存`--min-count`と併用し、両条件で選択した後に既存の並び順とtopを適用する。text/json/htmlで共通とする。
- 整数全域（0・負数含む）を受理する。正常入力の上限0以下や下限>上限は空結果exit0であり、入力失敗を隠さない。これは「整数」「値以下」「両条件」からの導出であって既存の定義ではない。
- 境界・省略互換・併用・空結果・不正引数の追加試験を既存試験とともに通す。
- README.mdへ使用例を1つ追加し、直接関わるオプション・総数・空結果案内を更新する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 最大出現回数の整数指定、min/max共通選択、top前の選択、元総数と既存互換、試験と使用例。

## Impact

予定する製品差分は`wordfreq/__main__.py`、関連CLI試験、`README.md`。部品API・抽出とcasefold・同数初出順・出力構造・HTML見た目と静的安全性は変更しない。依存とCIの追加変更、無関係な機能は対象外。

要求の根拠は依頼本文とBMADのBrief・PRD（`_bmad-output/initiative-r-d4bcda40/`）。Architectureの新規作成は、既存共通選択への局所追加で境界変更がないため不要。製品実装・試験はまだ行っていない。
