# 著者指定の追加（r-85dae0a8 / light）

## 目的と受入条件（依頼本文の原文）
pyproject.toml の [project] に authors = [{ name = "Argonauts UAT" }] の1行を足す。変えるのは pyproject.toml だけ。未決事項は無い。

## 変更範囲
- 製品: `pyproject.toml` の `[project]` に指定行を追加するだけ。依存・対応Python版・既存項目は変更しない。
- 工程文書: 本PLANと `.planning/argonauts/r-85dae0a8/VERIFICATION.md` だけを新規作成可。既存文書は変更しない。
- PRの掲載範囲を製品だけに限定した依頼ではないため、工程文書は通常どおりcommit・push・原本添付する。
- 起点: `1fa71c3b934b4003d6d3f735d63e7a6e801fab3e`（初期化済み依頼branch）。

## 実装と直接試験
1. Builderは以下の試験を標準write_fileで `$TMPDIR` 内の `verify_authors.py` に保存する（repoに試験ファイルを追加しない）。
2. repo直下で `python3 "$TMPDIR/verify_authors.py"` を先に実行。著者未指定によるAssertionErrorと終了コード非0を確認する。
3. `[project]` 内に指定の1行を追加し、同じコマンドで終了コード0とPASSを確認する。
4. 品質は同じ試験を自分で再実行し、差分を独立にレビューする。画面変更は無く画像確認は不要。

```python
from pathlib import Path
import subprocess
import tomllib

BASE = "1fa71c3b934b4003d6d3f735d63e7a6e801fab3e"
def git(*args):
    return subprocess.check_output(["git", *args])

before = git("show", BASE + ":pyproject.toml")
after = Path("pyproject.toml").read_bytes()
old = tomllib.loads(before.decode())
new = tomllib.loads(after.decode())
assert new["project"].get("authors") == [{"name": "Argonauts UAT"}], "著者の指定値が不一致"
line = b'authors = [{ name = "Argonauts UAT" }]\n'
assert after.splitlines(keepends=True).count(line) == 1, "指定行はちょうど1行"
assert after.replace(line, b"", 1) == before, "指定1行以外の変更あり"
del new["project"]["authors"]
assert new == old, "依存・対応Python版を含む既存設定の変更あり"
allowed = {"pyproject.toml", ".planning/argonauts/r-85dae0a8/PLAN.md",
           ".planning/argonauts/r-85dae0a8/VERIFICATION.md"}
changed = git("diff", "--name-only", "-z", BASE).split(b"\0")
untracked = git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
paths = {p.decode() for p in changed + untracked if p}
assert paths <= allowed, f"範囲外の変更: {paths - allowed}"
assert "pyproject.toml" in paths, "製品差分がない"
print("PASS: TOML構文・著者指定・1行差分・既存設定不変・変更範囲")
```

## 条件ごとの証拠と引継ぎ
- TOML構文と指定値: `tomllib` と著者リストの完全一致を確認する。
- 製品差分が指定1行のみ: バイト列から指定行を1回だけ除去して起点と完全一致させる。範囲外変更も失敗にする。
- 依存・対応Python版の不変: authors除去後のTOML全体が起点と等しいことを確認する（requires-python未指定も維持）。
- 未決事項: 無し。仕様や範囲の判断が必要になれば実装せずPMへ返す。
- 品質はVERIFICATION.mdに実行コマンド・終了コード・出力・対象head・差分確認・各条件の判定を文字で記録し、push・原本添付する。PMに画像や圧縮ファイルを開かせない。
- Builderはpush後draft PRを作成／確認し、同じ実装カードで品質へrequest_reviewする。確認工程を飛ばさない。
- pyproject.tomlは危険なパス。smartでも自動マージを予約せず、最終案内で人のマージ操作を示す。
