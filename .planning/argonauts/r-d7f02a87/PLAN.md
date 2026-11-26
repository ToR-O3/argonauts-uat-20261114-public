# README参照の追加計画（r-d7f02a87 / light）

## 目的と範囲
- pyproject.toml の配布メタデータから既存 README.md を参照させる。
- 製品変更は pyproject.toml の [project] に指定の1行を追加するだけ。
- 工程文書はこの PLAN.md と同じディレクトリの VERIFICATION.md のみ。PRには工程文書も含める。
- README、依存、対応Python版、実行時の処理、workflowは変更しない。full用成果物・割振りは追加しない。
- 比較元：初期化済み依頼branchの 7d4e4d14397265858b22b40419cf2f51b4756432。

## 受入条件（依頼本文の原文）
1. pyproject.toml の [project] に readme = "README.md" の1行を足す。
2. 変えるのは pyproject.toml だけ。
3. 未決事項は無い。

## 実装と直接の確かめ方
1. 下記の試験を標準 write_file で `$TMPDIR/r-d7f02a87-check.py` に保存する（製品・Gitには追加しない）。
   リポジトリ直下で `python3 "$TMPDIR/r-d7f02a87-check.py"` を実行し、readme未指定による失敗を記録する。
2. pyproject.toml の [project] の description の次へ `readme = "README.md"` を1行だけ追加する。
   同じ試験を再実行して成功を確認し、`git diff --check` も実行する。
3. 試験はTOML構文、project.readmeの値、READMEの実在・読取り、readme以外の全TOML値不変、
   元のファイルに指定1行だけ追加したバイト差分、工程文書以外の変更パスを直接assertする。
   未決事項は受付本文と最新コメントを照合し、追加の判断が不要であることを記録する。

```python
from pathlib import Path
import subprocess
import tomllib
base = "7d4e4d14397265858b22b40419cf2f51b4756432"
original = subprocess.check_output(["git", "show", f"{base}:pyproject.toml"])
current = Path("pyproject.toml").read_bytes()
before = tomllib.loads(original.decode("utf-8"))
after = tomllib.loads(current.decode("utf-8"))
assert after["project"].get("readme") == "README.md", "project.readme must reference README.md"
assert Path(after["project"]["readme"]).is_file(), "README must exist"
Path("README.md").read_text(encoding="utf-8")
assert current.splitlines(keepends=True).count(b'readme = "README.md"\n') == 1
assert current.replace(b'readme = "README.md"\n', b'', 1) == original, "only the requested line may change"
del after["project"]["readme"]
assert after == before, "other TOML values, dependencies and Python support must not change"
paths = subprocess.check_output(["git", "diff", "--name-only", "-z", base, "--"]).decode().split("\0")
allowed = {"pyproject.toml", ".planning/argonauts/r-d7f02a87/PLAN.md", ".planning/argonauts/r-d7f02a87/VERIFICATION.md"}
assert set(filter(None, paths)) <= allowed, paths
assert not subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "-z"]), "untracked files must be reviewed"
print("PASS: TOML, README reference, exact one-line change and product scope")
```

## 証拠と引継ぎ
- 実装者は試験のRED/GREENの出力・終了コードと差分を記録し、品質も試験を独立して再実行する。
- 品質は条件別の判定、対象head、実行コマンド・出力・終了コード、製品差分と依存・Python版不変の根拠を
  `.planning/argonauts/r-d7f02a87/VERIFICATION.md` に文字で保存・添付する。画像・圧縮ファイルは不要。
- 文書を新規作成した場合は指定パスだけgit addしてから範囲試験を再実行し、未追跡ファイルを隠さない。
- 実装者はcommit・依頼branchへpush後にdraft PRを用意し、同じカードを品質レビューへ渡す。
- pyproject.toml は危険なパスのためsmartでも自動マージを予約せず、最終確認後に人がマージする。
- この計画工程では製品変更と試験実行は行わず、PLANだけcommit・push・原本添付して後続へ渡す。
