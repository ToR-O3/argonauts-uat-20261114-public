---
title: "wordfreq 最小文字数指定"
template: agent-spec
version: 1.1.0
status: final
created: "2026-11-28"
updated: "2026-11-28"
---

# wordfreq 最小文字数指定

## Table of Contents

- [Problem — 短い語の除外](#problem)
- [User stories — 境界・互換・help](#user-stories)
- [Edge cases — 空結果と不正値](#edge-cases)
- [Requirements — FR-1〜FR-5](#requirements)
- [Success criteria — SC-1〜SC-5](#success-criteria)
- [Out of scope — 変更禁止範囲](#out-of-scope)
- [Assumptions — 未承認事項なし](#assumptions)
- [Implementation context — 既存契約との整合](#implementation-context)

## Problem

文字数はcasefold後のUnicodeコードポイント数（`len(word)`）、Nは1以上の整数と確定した。未決事項なし。これは要求の確定であり、実装・試験の完了を示さない。

CLI利用者が、短い単語を除いて頻度を調べられるようにする。追加は `--min-length N` の1機能だけとし、指定しない利用者の結果を変えない。

## User stories

**P1：短い語を除外する。** 主目的そのもの。独立試験：入力 `a bb ccc bb` に `--min-length 2` を指定する。
- Given この入力、When 各出力形式で実行、Then `bb` が2回、`ccc` が1回の順になり、`a` は出ない。境界の2文字は含む。

**P1：既存の呼出しを保つ。** オプション追加による回帰を防ぐ。独立試験：保存済みの変更前期待値との比較。
- Given 1文字語・同数語・10種類超を含む既存入力、When 新オプションを省略または1を指定、Then 結果のstdout・exit・stderrは変更前と一致する（helpの追加説明を除く）。

**P1：helpだけで指定方法を理解する。** READMEを変えずに使えるようにする。独立試験：ファイル引数なしの `--help`。
- Given ファイル未指定、When helpを表示、Then exit0・stderr空で、オプション名、最小文字数、N未満除外・境界包含、既定1を説明する。

## Edge cases

- 空ファイル、抽出0語、全語がN未満：exit0。textは空、jsonは `[]` と末尾改行、htmlは既存の空表示・見出し・basename・元総数を維持する。
- 頻度の下限・上限と文字数条件をすべて満たす語だけを順位付けし、その後topを適用する。オプションの指定順で結果を変えない。
- 大きなNで全除外しても、正常な入力取得を省略しない。不存在・読込み不能・不正UTF-8は既存のexit1・stderr通知・stdout空を保つ。
- casefold後に数えるため、`ß` は `ss` の2文字となり、N=2で残り、N=3で除外される。書記素数・UTF-8バイト数・casefold前の長さではない。既存のUnicode単語抽出自体は変えない。
- Nが0・負数・非整数、またはオプション指定時に値が欠落する場合は、入力取得前にexit2、stderrに使い方エラー、stdout空とする。入力が存在しなくてもこの引数エラーを優先し、stdinも読み始めない。

## Requirements

- **FR-1:** システムは `--min-length N` を追加し、casefold後の語のUnicodeコードポイント数（`len(word)`）がN未満なら除外し、Nちょうど以上なら含まなければならない（MUST）。Nは1以上の整数のみ許容し、0・負数・非整数・指定時値欠落は入力取得前にexit2、stderrに使い方エラー、stdout空としなければならない（MUST）。
- **FR-2:** システムは既定値を1とし、省略と明示1で既存の結果・終了コード・出力構造を維持しなければならない（MUST）。
- **FR-3:** システムは既存のUnicode単語抽出・casefold・頻度合算・回数降順・同数初出順を変えず、文字数条件を頻度条件と併用し、topより前に適用しなければならない（MUST）。text/json/htmlの語・回数・順序は一致し、HTML総数は文字数・頻度・topの全選択前の入力総出現回数を保つ。
- **FR-4:** システムは `--help` にFR-1の文字数定義・正整数規則・N未満除外と境界包含、および既定1の説明を追加しなければならない（MUST）。
- **FR-5:** 追加pytestと既存全pytestは成功し、READMEは変更しないこと（MUST）。未実施の試験を成功扱いしない。

## Success criteria

- **SC-1:** 境界未満・ちょうど・超過をtext/json/htmlで検証し、FR-1の結果になる。`ß` がcasefold後に `ss` としてN=2で残りN=3で消えることを各形式で試験し、casefold前の長さ判定を検出する。既存抽出に従うCJK連続語・数字・下線のコードポイント境界も含める。
- **SC-2:** 省略・明示1の出力を変更前の固定期待値と比較し、FR-2を満たす。変更後同士の比較だけでは互換性の証拠にしない。
- **SC-3:** 頻度上下限・同数初出順・top併用・全除外・空入力を検証し、FR-3と既存HTML契約を満たす。長さで除外される高頻度語を含め、top先行の誤りを検出する。
- **SC-4:** helpの説明と正常終了を試験する。0・負数・非整数・指定時値欠落の各入力でexit2・stdout空・stderrエラーを確認し、不存在ファイルおよび未完了stdinでも入力取得前に拒否することを検証する。正常なNでの入力失敗は既存のexit1契約を保つ。
- **SC-5:** Builder・品質が実在する試験ファイルから追加・全既存pytestを実行し、対象head・環境・コマンド・件数・終了結果を記録する。READMEの変更前後差分がない。

## Out of scope

README編集、依存追加、CI変更、UI・HTML見た目変更、新しい入力元、抽出・正規化規則の変更、無関係な改修は行わない。

## Assumptions

未承認の仮定はない。旧OQ-1・OQ-2と引数規則の仮定は、要求者の2026-11-28T13:23:21.058370+00:00の回答および今回の明示決定で解決した。

## Implementation context

既存CLIはUnicodeの単語構成文字の最大連続を抽出し、casefold後に頻度を合算する。頻度選択前の総数を保持し、頻度選択、安定した順位付け、top、各形式への整形を行う。最高位の試験境界は実CLIのサブプロセスとし、既存の部品単体・境界試験も維持する。

既存仕様のREADME説明義務は過去のmin-count/max-count機能に対するもの。今回は既存記述を残したままREADMEを変更しない。既存のHTML独立確認・安全性義務も免除しない。新規データモデルは不要のためKey entitiesは省略した。


