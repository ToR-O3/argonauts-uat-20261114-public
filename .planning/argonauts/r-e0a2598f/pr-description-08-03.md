## 変わること

wordfreqで `--exclude FILE` を指定すると、ファイルに書いた単語を結果から外せます。大小の違いは既存と同じ扱いで、HTMLの総数は元の入力全体を保ちます。

UTF-8の1行1語を使い、前後空白を除いた空行・`#`開始行は無視します。除外ファイルが読めない場合や不正な行がある場合は原因を知らせ、本文を読まずに終了します。READMEの実行例を実際に動かし、除外を指定しない場合は変更前と同じ出力になることも確認しました。

**まだマージしないでください。** 実装側の動作確認と証拠の準備を終え、独立した品質確認を待っています。

## 作業の記録

- 依頼: r-e0a2598f
- OpenSpec変更: r-e0a2598f-wordfreq-exclude
- 実装計画・実測SUMMARY: `.planning/phases/08-wordfreq-exclude/08-01-PLAN.md`〜`08-03-PLAN.md` と対応SUMMARY
- Builder条件別原本: `.planning/argonauts/r-e0a2598f/builder-evidence.md`
- 後続品質の全義務: 同ディレクトリ `quality-handoff.md` / `quality-handoff.json`
- 差戻し修正の原本: `.planning/argonauts/t_354e296c/CI-REPAIR.md` と同ディレクトリのRED/GREEN/full-suite出力

| 確認 | 実際に実行した結果 |
|---|---|
| 指定語除外・Unicode行文法・help/README例 | 08-01追加71件成功、同カードで品質レビュー済み |
| 読込み失敗・役割別exit・引数先行・本文未取得・元行番号 | 08-02の117件成功、品質レビュー済み |
| 全形式の選別順序、空/no-op/元総数、Counter/pairs、静的HTML | 08-02の190件成功、品質レビュー済み |
| 固定過去版との未指定互換 | Git `79d83ba14dd59d289d2ecd3e33c85e8de437972e` の隔離packageと64通りでstdout生bytes/status/stderr一致。同一interpreter/絶対入力path/argv/env |
| 最新の互換・両入力不変・説明/実行例・浅い取得・基準破損 | 79件成功、736 deselected |
| 最新の除外関連選択 | 457件成功、358 deselected、21.95秒 |
| 浅い取得での既存CIコマンド | origin切断・depth1・固定commit欠落の隔離checkoutで `python -m pytest` が1159件成功、190.74秒。既存1154件を保持し5件追加 |
| 引渡し検査 | stdlib19件成功。実package成功、原本削除/古い対象/Q6義務削除copyをexit2と名前付き診断で拒否 |
| 08-03の製品差分 | 試験とREADMEのみ。製品コード・依存・CI・CSSは08-02から不変 |

### 品質の差戻しへの対応

初回head92ddd6cのGitHub Actionsでは、浅い取得に固定過去版がなく64件がsetup ERRORでした。新しい浅い取得回帰を先に追加し、同じexit128を再現してから修正しました。

固定commit/root tree/wordfreq tree/6blobの9objectを、実Gitから取得して `tests/fixtures/exclude-baseline-git-objects.json` に同梱。Git hash-objectで全IDを検査し、固定commitからtree/blobをたどって原本を抽出します。fetch・通信・候補自身を使うgolden・skipを追加していません。基準file欠落/blob欠落/blob改変/改変後再hashの4種を拒否。checkoutのGit databaseへは書きません。GitHub自身の新head CI成功は手元の浅い取得実測とは区別し、ここでは未主張です。

現在の製品・試験内容対象は `526b89cec8d6b7c440b5716ee6319aec2f68f479`、21scopeファイルをGit bytesと現在bytesで照合。報告だけの後続commitとは区別します。以前の64pair生出力等は当時の実測履歴として保持し、新しい対象の全件実行原本を追加しました。品質は実際のレビューHEADを新たに解決して独立実行してください。

記録のみのWR-01（形の崩れたhandoffのexit1/traceback）・WR-02（工程試験のprofile依存）・IN-01〜05は未変更。今回の必須修正はCIの基準欠落に限定しました。

26edge（21explicit/5backstop）・14UI状態・2descriptor-less禁止は個別identity/predicate/source/dispositionで引き継ぎます。5backstopはhuman_needed/insufficient_spec、2禁止はflagged-unverified。画像閲覧0枚、静的ソースやバイト一致を新しいgeometry/可読性/実通信の実測とはしません。

公式状態はPhase8/Plan3/Total3/status verifying、verification.status missing。新しいPLAN/Quickや重複の進捗更新は行っていません。OpenSpec3.2、独立フェーズ検証・PM受入は未完。draftと途中品質の印なしを維持します。
