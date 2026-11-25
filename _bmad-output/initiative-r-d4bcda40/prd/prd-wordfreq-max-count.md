---
title: "wordfreq --max-count PRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
request: r-d4bcda40
sources:
  - ../brief/brief-wordfreq-max-count.md
---

# wordfreq --max-count PRD

## Table of Contents

- [Document purpose](#document-purpose) — 入力と読者
- [Vision](#vision) — 頻度上限の追加
- [Users and journeys](#users-and-journeys) — CLI利用
- [Glossary](#glossary) — 選択と総数
- [Features and requirements](#features-and-requirements) — FR-1〜FR-6
- [Rules](#rules) — 共通契約
- [Non-goals](#non-goals) — 範囲外
- [MVP scope](#mvp-scope) — 最小変更
- [Success metrics](#success-metrics) — 受入と逆指標
- [Quality and constraints](#quality-and-constraints) — 回帰保護
- [Change boundary](#change-boundary) — 変更箇所
- [API contract and versioning](#api-contract-and-versioning) — CLI互換
- [Developer experience](#developer-experience) — README例
- [Stories](#stories) — 実装・検証スライス
- [Decisions](#decisions) — 導出とArchitecture
- [Assumptions](#assumptions) — 非阻害推定
- [Open questions](#open-questions) — 未決事項

## Document purpose

依頼 r-d4bcda40 の実装・品質担当向け。入力Brief: `_bmad-output/initiative-r-d4bcda40/brief/brief-wordfreq-max-count.md`。ユーザー原文と固定受入を正とする。initiativeは管理情報のみ。単一機能のepic相当の仕様である。

現状は指定のCLI・aggregator・formatters・README・OpenSpec・tests/test_cli.py・pyproject.tomlを全文確認した（パスはBrief参照）。

## Vision

整数オプション `--max-count N` で頻度N以下の語を出す。省略時は上限なしで既存互換、min-count併用で両端を含む頻度帯を選べる。

## Users and journeys

単一CLIのため利用手順のみ示す。利用者はUTF-8ファイルと閾値を指定して結果を読む（FR-1〜FR-4）。実在人物は未提示。利用者像はAssumptions参照。

## Glossary

**count:** Unicode抽出とcasefold後の語ごとの正の出現回数。**min-count:** 既存の下限、既定1・1以上の整数。**max-count:** 今回の上限、整数・省略時上限なし。**選択:** 両閾値を満たす語の集合。**top:** 選択を並べた後の表示種類数、既定10・1以上。**総数:** 入力全体のcountの和、閾値とtopの適用前。

## Features and requirements

### 上限指定と共通選択

- **FR-1:** CLIは `--max-count N` を既存の `type=int` と同じ整数解釈で受理する。省略は上限なし。0・負整数も受理し、正値限定を追加しない。非整数 `abc`・`1.5` と値欠落は入力読込み前に stderr へ使い方エラー、exit2、stdout空、Tracebackなし。`--help` に新オプションが現れる。
- **FR-2:** 全形式で、指定時は `count >= min_count AND count <= max_count`、省略時は下限のみで選択する。境界を含み、CLIオプションの指定順に依存しない。選択後に回数降順・同数初出順で並べ、その後topを適用する。
- **FR-3:** 入力が正常に読み込めた場合、上限0・負数、`min_count > max_count`、全語除外、空ファイル、抽出0語はいずれも exit0、stderr空。textは空、jsonは `[]` と改行1つ、htmlは既存の3列見出し・データ0行・空状態・basename・元総数を維持する。有効整数でも不存在・読込み/UTF-8失敗は exit1・stdout空であり、空結果への早期終了にしない。
- **FR-4:** max-countを指定しない場合、既存引数を使った呼出しの出力・順序・終了コード・各形式構造を維持する。HTML総数はmin/max/topのすべての前。抽出・casefold・同数初出順・UTF-8・escape・静的安全性・既存min/topの正値検証を変更しない。

### 検証と説明

- **FR-5:** 追加pytestと既存全試験が成功する。
- **FR-6:** README.md に実行例1つと、整数指定（0・負数含む）・省略時は上限なし・上限値と同じ出現回数の語も含むこと・min-count併用の説明を追加する。上下限逆転は正常な空結果となること、上限で全件除外されたらmax-countを上げるか省略することも説明し、既存の「min-countを下げる」だけの案内を修正する。例は Developer experience 参照。

### 検証設計

以下は未実行の試験設計。全ケースをtext/json/htmlで検証する。総数の期待値はHTMLのみに適用し、text/jsonにメタ情報を追加しない。

| 入力・オプション | 期待結果 |
|---|---|
| `beta beta beta alpha gamma alpha delta`、max2 | alpha2、gamma1、delta1。beta3除外、HTML総数7 |
| 同じ入力、max1 | gamma1、delta1のみ。最小の有用な正の上限を含む |
| 同じ入力、min2/max2 | alpha2のみ。上下限一致を含む |
| 同じ入力、min2/max3 | beta3、alpha2。両境界を含む |
| 同じ入力、max2/top1 | alpha2。上限除外がtopより先 |
| 同じ入力、max0、max-1、min3/max2 | それぞれ空結果exit0、HTML総数7 |
| `Zoo apple APPLE zoo banana`、min2/max2でtop1とtop2をそれぞれ指定 | top1ではzoo2のみ。top2ではzoo2→apple2。同数初出順 |
| `Straße STRASSE 日本語 日本語`、max1とmin2/max2 | 前者は空、後者はstrasse2→日本語2。正規化合算後に判定 |
| 空・空白のみ・記号のみ、有効max | 空結果exit0、stderr空。HTMLの場合のみ総数0。text/jsonはFR-3の空出力 |
| 正常入力、上限省略と十分大きい整数 | 同じstdout。省略時は変更前の既存期待値とも一致 |
| 不存在入力、非整数/欠落max | exit2、stderrあり、stdout空。読込みspyでも未呼出し |
| 不存在・ディレクトリ・権限失敗・不正UTF-8、有効max0/負数 | exit1、stderrあり、stdout空。空集合でも入力失敗を隠さない |

整数受理は0、負数、`+2`、`02`、通常の大きな整数と `--max-count=-1` も含める。min/max/topの指定順交換、min-countの既存不正値検証を保つ。共通選択をtopへ渡す前の内部spyで確認し、元Counterを変更せず各formatterへ同じ選択結果を渡すことも検証する。

追加の直接確認:
- 上限適用後に11種類以上残る入力で、top省略は10件、大きいtopは残った全件となること。
- `beta`4回・`zoo`3回・`apple`2回・`pear`2回・`single`1回の入力でmin2/max3/top1を指定し、zoo3のみ・HTML元総数12を確認する。min/max/topがそれぞれ実際に除外する条件とする。
- max0または負数とmin-count0/top0をそれぞれ組み合わせ、不存在入力でも読込み前exit2・stdout空となること。
- ファイル名なしの`--help`はexit0・stderr空、stdoutに`--max-count MAX_COUNT`が現れること。
- 未指定互換は既存の保存済み出力または変更前に固定した期待バイト列と比較し、上限省略・十分大きい上限についてstdoutバイト列・exit・stderrの一致を確認する。変更後の2呼出し同士の比較だけで済ませず、既存の文字コード検証も再利用する。

## Rules

- **RULE-1:** 全形式で同じ選択と順序を使う。HTMLだけで再集計・別フィルタをしない。
- **RULE-2:** min-countとtopの既存制約は変更せず、max-countに正値限定・min/max大小エラーを追加しない。

## Non-goals

依存追加/更新、CI追加/変更、HTMLの見た目/CSS/空文言変更、入力元追加、Unicode規則変更、並び順変更、部品API再設計、性能目標追加、無関係な整理は行わない。

## MVP scope

製品変更の対象は上限引数・共通選択・追加試験・README例1つのみ。既に最小で延期候補なし。今回の作業は文書作成のみで、製品変更は実装時に行う。

## Success metrics

- **SM-1:** FR-1〜FR-3の追加試験は失敗0。逆指標はFR-4の既存互換破壊0。
- **SM-2:** FR-5の全既存試験と追加試験が成功。逆指標は既存試験の削除・回避0、未実施を成功扱いする報告0。
- **SM-3:** FR-6の新使用例1つが実CLIで成功。逆指標は範囲外差分0。

新機能・新試験は未実装、実測結果なし。

## Quality and constraints

- **RULE-3:** HTML安全性・basename限定・元総数・text/json構造の回帰0。既存検証義務を省略しない。
- **RULE-4:** 範囲外差分0。試験環境・コマンド・件数・exitを記録し、未実施・未報告CIを成功と呼ばない。

## Change boundary

予定箇所は `wordfreq/__main__.py` の引数・選択、`tests/test_cli.py` の追加試験、READMEの関連説明。その他の製品部品は維持する。

## API contract and versioning

任意CLI引数の追加のみ。旧呼出し・部品API・出力schema・既定top10/textは不変。移行・版番号更新は不要。

## Developer experience

新例: `python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`。試験表の入力 `beta beta beta alpha gamma alpha delta` と期待JSON `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]` をREADMEの同じ例に併記し、配列＋改行・exit0を実装後に検証する。READMEの総数説明にもmax-count前を反映する。

## Stories

1スライス: 頻度帯を選べる。受入はFR-1〜FR-6とRULE-1〜RULE-4すべて。未実施があれば製品受入は未完了。

## Decisions

上限0・負数・下限が上限を超える場合の扱いは、既存定義ではなく「整数」「値以下」「両条件」からの導出。正のcountと上限0以下、またはmin>maxの共通部分は空集合なので、正常な全除外のexit0を適用する。

新Architectureは不要。既存CLI共通filterへの局所変更で境界/API不変。境界変更が必要なら再判断する。

AI/UI/多チーム展開/外部連携/SLA/規制/性能/移行/ハードウェアは非該当で任意節を除外。完了後の学びをPRD Updateへ反映する。

## Assumptions

- [ASSUMPTION: Users and journeys] 低頻度語・頻度帯を抽出する既存CLI利用者を想定する。実利用者の同定は未提供で、機能受入に影響しない。所有者: 要求担当。利用者向け説明が必要な時に再確認する。

## Open questions

なし。製品試験・受入は実装後であり文書完成と別である。
