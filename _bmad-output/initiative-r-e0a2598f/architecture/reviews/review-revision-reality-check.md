# Architecture revision review — reality-check

## 対象と判定

- 対象: `../architecture.md` と `../.memlog.md`（本レビューからの相対パス）。
- 適用レンズ: 指定された公式 resolved lens `reality-check` のみ。採用済み判断がweb・現行プロジェクト・現行starterのいずれかで現実確認されているかを検査した。
- **判定: 指摘なし。** 今回の採用判断について、学習済み知識だけで断定された技術選択、確認されていない最新版の主張、存在しない構成部品、starter既定値への未検証依存は見つからなかった。
- brownfieldであり、新ライブラリ・framework・starter・version固定を採用していない。既存プロジェクトを直接読むことで確認できるため、web検索は行っていない。「最新」「全環境で動作」「実装済み」の証明ではない。

## 現実根拠との対応

以下のコード・設定パスはリポジトリ相対。行番号は今回実読したファイルに対応する。

| 採用判断／主張 | 実読した現実根拠 | 確認結果 |
| --- | --- | --- |
| AD-1: CLI合成、取得境界、純粋なtokenizer/aggregator/formatterを維持 | `wordfreq/__main__.py:7-10,22-54`; `wordfreq/sources.py:9-22`; `wordfreq/tokenizer.py:9-18`; `wordfreq/aggregator.py:6-17`; `wordfreq/formatters.py:6-27`; `tests/test_sources_boundary.py:7-42` | 記載された部品と依存方向は実在する。FileSourceが取得、CLIが終了判断、末端部品が変換を担う。新関数名・分割を既存APIとして捏造していない。 |
| AD-2: Unicode抽出とcasefold、安定順位を維持 | `wordfreq/tokenizer.py:6-18`; `wordfreq/aggregator.py:11-17`; `tests/test_tokenizer.py:6-38`; `tests/test_aggregator.py:17-46` | 本文は実際にUnicode `\\w+` 抽出後のcasefold。順位は回数降順の安定sortで、Counter挿入順を保持する前提もコードに明示されている。ASCII lowerや集合反復順に依存する設計ではない。 |
| AD-2: 除外のtrim、コメント、行全体検証、行終端、BOM等の扱い | `../decision-update.md:10,12` および `../prd/prd-wordfreq-exclude.md:72-82` | 既存本文parserから推測して確定した規約ではなく、明示された採用決定を反映している。既存正規表現による部分抽出と、新規の行全体検証を区別している。 |
| AD-3: UTF-8、cause保持、本文exit1、引数検査先行を維持 | `wordfreq/sources.py:17-22`; `wordfreq/__main__.py:22-33`; `tests/test_cli.py:41-46,64-70,120-135,624-644` | UTF-8取得と例外causeは現存する。本文InputErrorはCLIでexit1、top/min-count検査は取得前。除外入力の役割を残す必要性も既存の一律exit1処理から説明できる。 |
| AD-3: 除外の全読込み失敗・不正行exit2、除外先行で本文未読 | `../decision-update.md:11-13` および `../prd/prd-wordfreq-exclude.md:84-90` | 新しい除外固有の方針は採用決定に由来し、既存FileSourceに既に実装されているとは主張していない。CLIだけが終了コードを決める境界とも整合する。 |
| AD-4: 元Counter/HTML総数保持、共通pairs、min-count→順位→top | `wordfreq/__main__.py:34-48`; `wordfreq/aggregator.py:11-17`; `wordfreq/formatters.py:22-27,109-115`; `tests/test_cli.py:686-741,759-793`; `../decision-update.md:9` | 元総数は実際に選択前に算出され、候補Counterは別に作られる。HTMLは呼出し側のtotalを表示する。除外追加後にもこの契約を維持する方針は既存構造に適合する。 |
| 既存のtext/json空結果、HTMLのUTF-8/escape/basename/静的CSS/空状態を維持 | `wordfreq/formatters.py:6-19,22-46,101-127`; `wordfreq/__main__.py:39-53`; `tests/test_cli.py:138-143,711-741` | 宣言された表示契約は実装上存在する。新rendererや外部CSS、通信を前提にしていない。 |
| Structural Seed: 標準ライブラリ構成継承、新技術・starter・版固定なし | `wordfreq/` の各実装ファイル; `pyproject.toml:1-15`; `.github/workflows/pytest.yml:11-18` | runtime dependenciesは空。既存build backendはsetuptools、dev依存はpytest。CIはPython 3.12を指定する。spineはこれらを最新と称さず、ローカル版でCIや依存版を上書きしないとしている。新規stack選定に必要なweb確認は発生していない。 |

## 判断記録の扱い

`.memlog.md:9-18` はCreate時点の判断・保留・レビュー履歴であり、`:19-20` が今回の採用決定による更新を明示している。旧OQ保留を現在の未決として読み替えたり、旧レビュー実施記録を今回のレビュー完了と取り違えたりしていない。現在のarchitectureも `:19,97-99` で親のreconciliation／Reviewer Gate未了とdraft維持を明示している。

採用判断の内容は `decision-update.md:9-15` と照合した。製品方針の根拠はこの明示決定であり、webが製品承認を代替するものではない。

## 限界・非実施

- 実装と試験のソースを読んだレビューであり、pytest・CLI・新規除外parserの実行結果は取得していない。新機能の受入、未指定時のバイト互換、全異常系の合格は宣言しない。
- CI指定Python 3.12での実行、およびUnicodeデータベース差を含む版横断の動作保証は本レビューの成果ではない。architectureにもそのような保証はない。
- 既存のsetuptools/pytest/GitHub Actionsが最新版であるかは調べていない。これらの更新・新規採用・最新版への適合を判断した文書ではないため、未確認の最新版主張には該当しない。
- 原本、memlog、製品コードは編集せず、gitおよびKanban操作は行っていない。本報告書のみを作成した。

## Findings

```json
[]
```
