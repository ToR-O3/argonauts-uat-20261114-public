# Revision review — divergence

## 対象・判定

- 対象: `../architecture.md`、`../.memlog.md`（今回の採用決定反映後）。
- 範囲: wordfreq の任意 `--exclude FILE` のみ。
- 指定済み resolved lens: “Attack the spine as an adversary: construct two units one level down that each obey every AD to the letter yet still build incompatibly — clashing shared-data shapes, two owners of one entity, conflicting state-mutation paths. Every pair you find is a hole to close with a new or tightened AD.”
- **結果: 指摘なし。すべてのADに従いながら互換性を失う下位unit対は、今回確認した境界では成立しなかった。AD追加・強化の要求なし。**
- 文書レビューの結果であり、実装・試験の合格、spineのfinal化、後続仕様承認を意味しない。

## 照合根拠

主対象を全文読取りし、既存境界の確認に `wordfreq/sources.py`、`wordfreq/__main__.py`、`wordfreq/aggregator.py` を参照した。現行の承認済み意味は initiative直下の [採用決定](../../decision-update.md)、[入力照合](../../source-context.md) に照合した。リンクは本レポートの配置先 reviews ディレクトリを起点とする。

## 二つの下位unitによる攻撃

| 攻撃対象とunit対 | 意図的に作った非互換 | 全AD準拠の対として成立するか |
| --- | --- | --- |
| 行解釈unit / 照合unit | 前者はlower済み語を渡し、後者はcasefold済み本文キーと比較する。あるいは解釈側が本文tokenizerで部分抽出する。 | 不成立。AD-2（architecture.md:44–48）が全文一致の検証後casefold、本文の既存Unicode抽出維持を指定する。lower、部分抽出、BOM除去による受理は準拠しない。 |
| 行解釈unit / CLI合成unit | 前者は遅延iteratorで返し、後者は本文取得後に残りの不正行を検出する。 | 不成立。AD-3（50–54）が除外の全行検証完了を本文取得より先に要求する。遅延表現自体は可でも、CLIは本文取得前に検証を完了しなければならない。 |
| 除外取得unit / CLIエラーunit | 前者が既存InputErrorを返し、後者が本文と同じexit1へ変換する。 | 不成立。AD-3がcauseと入力役割の保持、除外読込み失敗のexit2、本文失敗のexit1、CLIのみの終了コード決定を指定する。既存FileSourceを再利用しても役割別のCLI制御が必要になる。 |
| 行解釈unit / CLI診断unit | 前者が空行・コメント削除後の行番号だけを返し、後者がそれをFILEの行番号として表示する。 | 不成立。AD-3が不正行のファイル名と行番号を要求する。整形後の位置では当該FILE内の不正行を識別できない。行番号情報の表現方法は自由だが診断の意味は自由ではない。 |
| 表示候補選択unit / 順位unit | 前者が除外語setの順序でCounterを再構成し、後者が既存stable sortに従う。あるいは前者がtop後に除外する。 | 不成立。AD-2が残存語の初出順保持と除外FILEの順序非依存、AD-4（56–60）が除外/min-count後の候補を順位/topへ渡すことを指定する。既存top_wordsも入力Counterに正規化済み初出順を要求する。 |
| 集計・選択unit / HTML整形unit | 前者が元Counterから除外語を削除し、後者が受け取ったCounterから総数を計算する。 | 不成立。AD-4が元Counter非破壊と除外/min-count/top前の総数を指定する。本文全体の集計は維持し、フィルタ済み候補を別に扱う必要がある。 |
| CLI共通選択unit / 各形式の整形unit | CLIは共通pairsを渡す一方、HTMLだけ別の除外判定や再選択を行う。 | 不成立。AD-1（38–42）の純粋整形境界、AD-4の同一結果pairs、既存空状態/元総数の維持に反する。形式側による独立した選択所有権は与えられていない。 |
| CLI取得unit / 集計unit | 両方が除外FILEを読み、別タイミングの内容を使う。または集計unitが終了コードを決める。 | 不成立。AD-1がcount_words/top_words/formattersへのファイルI/O・argv・exit判断追加を禁止し、AD-3が終了コードをCLIに限定する。取得と純粋処理の所有権は分離済み。 |

## 共有データ・所有権・状態経路

- **共有データ:** 本文の正規化語・回数・初出順は既存Counter契約、出力は既存pairs契約（architecture.md:64–68）。既存 `top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]` と整合する。除外語の集合型・補助関数名・ファイル配置は明示的にBuilder裁量（90–94）であり、別々の公開APIとして固定する要件はない。単にsetとfrozenset、独自例外と役割別catchを選べることだけでは、外部意味が衝突するAD欠落としない。
- **所有権:** CLIは取得/処理/整形の合成と終了コード、sourcesは取得、行解釈は検証/正規化、集計・選択は共通順位、formattersは表示を担う。除外FILEを複数unitが独立して取得する正当な経路はない。
- **状態変更:** 元入力Counterは保持し、選択候補のみを絞る。HTML総数と順位の情報源が混同される経路はAD-4で遮断されている。入力/除外FILEの書換えも禁止（69）。

## memlogの扱い

`.memlog.md:12–14` の「他読込み失敗は未採用」「HTML総数等は未決」は更新前の履歴である。後続の19行目が承認日時と変更後AD-2/3/4を明示し、20行目が更新原本への反映と親レビュー未了を記録する。architecture.md:19、92も製品未決解消を明示している。古い未決を現行の代替契約として選べる状態とは判定しなかった。

## Findings

```json
[]
```

原本architecture.md / .memlog.mdの編集、実装変更、git操作、Kanban操作は行っていない。
