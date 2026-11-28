## 変わること

wordfreqで `--exclude FILE` を指定すると、ファイルに書いた単語を結果から外せます。大小の違いは既存と同じ扱いで、HTMLの総数は元の入力全体を保ちます。

UTF-8の1行1語を使い、前後空白を除いた空行・`#`開始行は無視します。除外ファイルが読めない場合や不正な行がある場合は原因を知らせ、本文を読まずに終了します。READMEの実行例を実際に動かし、除外を指定しない場合は変更前と同じ出力になることも確認しました。

**まだマージしないでください。** 実装側の動作確認と証拠の準備を終え、独立した品質確認を待っています。

## 作業の記録

- 依頼: r-e0a2598f
- OpenSpec変更: r-e0a2598f-wordfreq-exclude
- 実装計画: `.planning/phases/08-wordfreq-exclude/08-01-PLAN.md`、`08-02-PLAN.md`、`08-03-PLAN.md`。実測原本は同じ場所の `08-01-SUMMARY.md`、`08-02-SUMMARY.md`、`08-03-SUMMARY.md`。
- Builderの条件別原本・AC対応: `.planning/argonauts/r-e0a2598f/builder-evidence.md`
- 引渡しと後続品質の全義務: 同ディレクトリの `quality-handoff.md` / `quality-handoff.json`
- 検査と実package破損copyの結果: `task02-evidence.md` / `real-package-controls.json`

| 確認 | Builderが実際に実行した結果 |
|---|---|
| 指定語除外・Unicode行文法・help/README例 | 08-01追加71件成功、同カードで品質レビュー済み |
| 全読込み失敗・役割別exit・引数先行・本文未取得・元行番号 | 08-02の117件成功、同カードで品質レビュー済み |
| 全形式の除外→min-count→初出順→top、空/no-op/元総数、Counter/pairsと静的HTML | 08-02の最終190件成功、同カードで品質レビュー済み |
| 固定過去版との未指定互換 | exact Git `79d83ba14dd59d289d2ecd3e33c85e8de437972e` の隔離packageと64通りでstdout生bytes/status/stderr一致。同じinterpreter/絶対入力path/argv/env |
| 入力両役割の不変・完全な説明/実行例 | 新規9ケースと説明1ケースを含む追加74件成功 |
| 除外関連累積 | 最終452件成功、358 deselected、18.58秒 |
| 全既存を含む試験 | 最終1154件成功、188.74秒。既存1080件を保持し74件追加 |
| 互換試験の識別力 | default/top、辞書順tie、JSON末尾改行、HTML templateの隔離4変異を対象AssertionErrorで拒否 |
| 引渡し検査 | stdlib19 tests成功。実package検査も成功。実原本削除/古い対象head/Q6配送義務削除の隔離copyをそれぞれ名前付き診断で拒否 |
| 今回08-03の製品差分 | 回帰試験とREADMEの非目標説明のみ。wordfreq/・依存・CI・CSSは08-02から不変 |

完全な説明の欠落と引渡しcheckerは実RED→GREENを記録し、公式TDD証拠検査で確認しています。互換比較は既実装でGREENだったため架空のREDを作らず、隔離した誤実装で判別力を確認しました。JUnit・CLI生出力・入力bytes/argv/env/exitは原本のまま保存しています。

26edge（21explicit/5backstop）・14UI状態・2descriptor-less禁止は個別identityとpredicate/source/dispositionで引き継ぎます。5backstopはhuman_needed/insufficient_spec、2禁止はflagged-unverifiedを維持し、未確認を合格扱いにしません。画像閲覧0枚。静的ソースやバイト一致を、geometry・画像可読性・実通信の新規実測とはしていません。

引渡しの初期製品内容対象は `d30dd316ae6b73dcf10376ce9bd75cfc134b0c2c`。報告だけの後続commitと区別して、全19scopeファイルをGit bytesと現在bytesの両方で検査します。品質はレビュー時の実HEADを新たに解決して独立実行します。引渡しchecker成功は独立品質の成功ではありません。

公式状態はPhase8/Plan3/Total3、verifying、ROADMAP3/3実行済み・In Progress、独立VERIFICATIONはまだmissingです。全体Progress更新はunscoped警告で見送りのまま、過去の表示を合格率として使いません。OpenSpec1.1/2.1/2.2/3.1は実施済み、3.2の独立検証・文字原本添付は後続品質の担当として未完です。draftと途中品質の印なしを維持します。
