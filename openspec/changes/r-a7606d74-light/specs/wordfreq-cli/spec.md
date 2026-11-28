# Spec Delta

## ADDED Requirements

### Requirement: 最小文字数オプション（LEN-1）
システムは（SHALL）`--min-length N` を提供し、既存の単語抽出とcasefold後のUnicodeコードポイント数がN未満の語を全出力形式で除外し、Nちょうど以上の語を残す。既定は1、Nは1以上の整数のみとする。書記素数・UTF-8バイト数・casefold前の長さで判定してはならない（MUST）。

#### Scenario: 未満・境界・超過
- **WHEN** `a bb ccc bb` をtext/json/htmlで `--min-length 2` として実行する
- **THEN** bb2、ccc1の順だけを表示し、aは除外する。exit0・stderr空である

#### Scenario: 正規化後に長さを数える
- **WHEN** `ß SS a 日本語 12 __` を各形式で最小文字数2および3として実行する
- **THEN** 2ではss2、日本語1、121、__1の順で残る。3では日本語1だけが残る。CJK連続語を文字ごとに分割しない

### Requirement: 最小文字数の入力検証（LEN-2）
システムは（SHALL）0・負数・非整数・オプション指定時の値欠落を、入力取得前の使い方エラーとしてexit2、stderrへ通知、stdout空で拒否する。有効なNでは入力取得を省略せず、既存の入力失敗exit1を保つ。

#### Scenario: 不正値を先に拒否する
- **WHEN** 各形式でNを0・-1・abc・1.5または値欠落とし、不存在ファイルまたは入力未完了のstdinを与える
- **THEN** 入力を取得せずexit2・stdout空・stderrに使い方エラーとなる。Tracebackや結果HTMLは出さない

#### Scenario: 有効な閾値で入力失敗を隠さない
- **WHEN** 有効な大きいNと、不存在・ディレクトリ・読込み不能・不正UTF-8の入力を与える
- **THEN** 各形式ともexit1・stdout空・stderrへ通知し、正常な空結果へ変換しない

### Requirement: 文字数と既存選択条件の合成（LEN-3）
システムは（SHALL）文字数と既存min-countおよび指定されたmax-countの条件をANDで適用し、その後に頻度降順・同数初出順とtop制限を適用する。指定順で結果は変わらず、text/json/htmlの語・回数・順序は一致する。HTML総数は文字数・頻度・topの全選択前の入力全体の出現回数を保たなければならない（MUST）。

#### Scenario: 短い高頻度語がtopの枠を奪わない
- **WHEN** `a a a Zoo apple APPLE zoo banana` を各形式でmin-length3/min-count2/max-count2/top1として実行し、指定順も交換する
- **THEN** zoo2だけを表示する。top2ではzoo2、apple2の順。HTML元総数は8で、表示順位は1から付く

#### Scenario: 全除外・空入力でも既存の空表現を保つ
- **WHEN** `a bb` をmin-length3で実行する、または空・空白のみ・記号のみの入力を有効なNで各形式に出力する
- **THEN** exit0・stderr空、textは空、jsonは`[]`と改行1つ、htmlはbasename・3列見出し・0データ行・既存空状態を保つ。HTML総数は前者2、後者0である

### Requirement: 最小文字数の互換性・説明・試験（LEN-4）
システムは（SHALL）省略と明示1で従来の出力・終了コード・stderrを維持する（help追加説明を除く）。helpは最小文字数の指定・casefold後の文字数・正整数・N未満除外と境界包含・既定1を説明する。追加pytestと既存全pytestは成功しなければならない（MUST）。README.md、依存、CI、抽出・正規化、HTML見た目・安全性は変更しない。

#### Scenario: 変更前の固定期待値で互換を確認
- **WHEN** 1文字語・同数語・10種類超を含む入力で、各形式の省略と明示1を変更前の固定期待値と比較する
- **THEN** stdoutバイト列・exit・stderrが一致する。変更後同士の比較だけで互換確認済みとしない

#### Scenario: ファイルなしでhelpを表示
- **WHEN** ファイル引数なしで `--help` を実行する
- **THEN** exit0・stderr空で、LEN-4の指定方法と文字数規則・既定値の説明がstdoutに出る

#### Scenario: 実施した証拠と変更範囲を読む
- **WHEN** Builderと品質が追加および全既存試験を実施して受入を確認する
- **THEN** 対象head、環境、コマンド、件数、終了結果とCLIの入力・argv・exit/stdout/stderrを文字の検証原本に対応付ける。README差分なしを確認する。HTMLは既存の独立ブラウザ確認義務を保ち、省略互換・絞込み・全除外・元総数を確認する。画像の確認内容と結果も文字で残し、未実施を合格としない
