# r-c4894aff README冒頭説明の書き換え（light）

## 目的・受入条件
判断日時: 2026-11-26T09:49:05.681334+00:00
依頼者原文: ①にしてください。冒頭の説明文を「テキストの単語を数えて、多い順に並べるコマンドです。」に書き換えてください。変えるのは README.md だけです。
- README.mdの1行目の見出しの次の段落を指定文と完全一致させる。
- 対象段落以外はバイト単位で保持する。公開の動き・設定・データ形式・依存を変更しない。
- 製品変更はREADME.mdだけ。工程文書はPRに含める。full工程は実行しない。

## 変えるファイルと順序
1. 実装: README.mdの3行目だけを置換する（改行・空行・その他の内容は維持）。
2. 確認: .planning/argonauts/r-c4894aff/VERIFICATION.mdに条件別の実行結果を記録する。
計画ファイルは本PLAN.mdのみ。新規工程文書はこの2ファイル以外に作らない。
起点は初期化済みcommit `607e10053db2973a65ce3f95c86e58b62bb25a7c`。

## 実行可能な直接検証
実装担当は次のPythonブロックを標準write_fileで `$TMPDIR/r-c4894aff-check.py` に保存する。
リポジトリ直下で `python3 "$TMPDIR/r-c4894aff-check.py" --before` を実行し、置換前全文と対象位置を確認する。
編集前に `python3 "$TMPDIR/r-c4894aff-check.py"` が完全一致のassertで失敗することを確認（RED）。
置換後に同じ引数なしコマンドを実行して成功を確認（GREEN）。品質も独立に保存・実行する。
検証スクリプトは一時領域だけに置き、PRへ追加しない。

```python
from pathlib import Path
import subprocess
import sys

BASE = "607e10053db2973a65ce3f95c86e58b62bb25a7c"
def git(*args):
    return subprocess.check_output(["git", *args])
old = "テキストファイルの単語の出現回数を数えて、text・json・html の形式で出力する小さなコマンドラインツールです。".encode()
new = "テキストの単語を数えて、多い順に並べるコマンドです。".encode()
before = git("show", BASE + ":README.md")
lines = before.splitlines(keepends=True)
assert lines[0] == b"# argonauts-uat public\n" and lines[1] == b"\n"
assert lines[2] == old + b"\n" and lines[3] == b"\n", "置換前の対象段落が異なる"
actual = Path("README.md").read_bytes()
if sys.argv[1:] == ["--before"]:
    assert actual == before, "置換前のREADME全文が異なる"
    print("PASS: 置換前全文・対象段落")
else:
    assert not sys.argv[1:], "引数は --before のみ"
    expected = b"".join(lines[:2]) + new + b"\n" + b"".join(lines[3:])
    assert actual == expected, "指定文の完全一致または対象外の内容保持が未達"
    allowed = {b"README.md", b".planning/argonauts/r-c4894aff/PLAN.md", b".planning/argonauts/r-c4894aff/VERIFICATION.md"}
    changed = set(git("diff", "--name-only", "-z", BASE).split(b"\0")) - {b""}
    untracked = set(git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0")) - {b""}
    assert b"README.md" in changed and (changed | untracked) <= allowed, "変更範囲外のファイルあり"
    print("PASS: 指定文完全一致・対象外バイト保持・製品変更READMEのみ・工程文書範囲")
```

## 品質と引継ぎ
`git diff --check` と全差分の目視で、READMEは1行置換だけであることも確認する。
品質はVERIFICATION.mdに対象head、判断日時と原文、各コマンド・終了コード・実出力、条件別判定を文字で記録してpush・原本添付する。
画面変更はなく画像確認は不要（0枚）。PMに画像・圧縮ファイルを開かせない。
実装は検証後commit・依頼branchへpushし、draft PRを作成または確認して同じカードを品質レビューへ渡す。
確認工程の予約があっても実装カードはcompleteしない。実装レビューでは品質の印を付けない。
