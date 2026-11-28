# Spec Delta

## ADDED Requirements

### Requirement: 最小文字数オプション（ML-1）
システムは（SHALL）`--min-length N`で集計結果に含める単語の最小文字数を指定できるようにする。既存規則で抽出・casefoldした後の語の文字数がN未満なら除外し、NちょうどとN超は文字数によって除外しない。text/json/htmlに共通で適用し、既存の頻度上下限で絞ってからtopを適用する働きと同頻度初出順を維持しなければならない（MUST）。

#### Scenario: N未満と境界値と超過
- **WHEN** 入力 `a bb ccc bb` を各形式で `--min-length 2` として実行する
- **THEN** `bb` 2回、`ccc` 1回の順で残り、`a` は結果に含まれず、exit0となる

#### Scenario: 正規化後の文字数
- **WHEN** 入力 `ß ss a` を各形式で `--min-length 2` として実行する
- **THEN** casefold後の `ss` を2回として残し、`a` を除外する。casefold前の長さで `ß` を除外しない

#### Scenario: 頻度上下限とtopとの併用
- **WHEN** 入力 `a a a bb cc bb cc dddd` を各形式で `--min-length 2 --min-count 2 --max-count 2 --top 1` として実行する
- **THEN** `bb` 2回だけを表示する。文字長・頻度条件を満たす語の同頻度初出順を維持してtopで制限する

### Requirement: 最小文字数の既定互換と空結果（ML-2）
システムは（SHALL）min-lengthの既定値を1とし、省略と明示1で従来の出力・終了コードを維持する。抽出・casefold・既存の引数と入力エラー・出力構造・HTMLの見た目を変えてはならない（MUST）。HTMLの入力全体の元総数は長さ選択で減らさない。長さ条件で全件除外された場合も既存形式の空結果で正常終了する。

#### Scenario: 省略と明示1の互換
- **WHEN** 同じ既存入力・引数で、min-length省略および明示 `--min-length 1` を各形式で実行する
- **THEN** stdout・stderr・終了コードが変更前の保存済み出力または固定期待値と一致する。変更後の2呼出し同士の比較だけで互換確認済みとしない

#### Scenario: 全件除外でも正常終了
- **WHEN** 入力 `a bb` を各形式で `--min-length 3` として実行する
- **THEN** exit0となり、textは空文字、jsonは `[]` と末尾改行、htmlは既存の空状態と0データ行になり、HTML元総数は2のままである

#### Scenario: 表示から除いてもHTML元総数を保つ
- **WHEN** 入力 `a a a bb cc bb cc dddd` をhtml形式で `--min-length 2 --min-count 2 --max-count 2 --top 1` として実行する
- **THEN** `bb` 2回の行と元総数8を表示し、短い語の除外や頻度条件やtopにより元総数を減らさない

### Requirement: 最小文字数の説明と試験（ML-3）
システムは（SHALL）`--help`に最小文字数の選択肢、N文字未満を除く動作、既定値1を説明する。追加動作・N境界・既定互換のpytestを追加し、既存全試験とともに成功しなければならない（MUST）。README.mdは変更しない。

#### Scenario: helpで動作を確認できる
- **WHEN** ファイル引数なしで `python -m wordfreq --help` を実行する
- **THEN** exit0・stderr空で、stdoutに `--min-length` と値の指定、N文字未満の除外と既定値1の説明がある

#### Scenario: 試験と変更範囲を確認できる
- **WHEN** 品質が対象headの追加pytestと既存全pytestおよび差分を確認する
- **THEN** 動作・境界・既定互換の試験があり、実行した環境・コマンド・件数・exitと受入条件の対応を文字の証拠で確認でき、README.mdに差分がない。未実施を合格扱いしない
