# pyproject keywords — light PLAN

## 目的・範囲
- 受付: r-96e0448e。製品変更は `pyproject.toml` の説明用メタデータ1行のみ。
- 起点: `20f706e61ba87746a7da1b3adc09c5fbe74731c9`（初期化済み依頼branch）。
- 工程文書は本PLANと `.planning/argonauts/r-96e0448e/VERIFICATION.md` のみ。
- 公開入出力・実行設定・データ形式・依存・既存試験を変更しない。フレームワーク導入なし。

## 受入条件（依頼本文の原文）
1. pyproject.toml の [project] に keywords = ["wordfreq"] の1行を足す。
2. 変えるのは pyproject.toml だけ。
3. 未決事項は無い。

## 実装手順
1. 下記検証コードを標準 `write_file` で `$TMPDIR` 内の `verify_keywords.py` に保存する（Gitには加えない）。
2. `python3 <保存した絶対パス>` を編集前に実行し、keywords欠落のassertionで失敗することを記録する。
3. `[project]` の `version` の直後へ `keywords = ["wordfreq"]` を1行追加する。他の既存バイトは保持する。
4. 同じ検証を再実行しexit 0を確認する。`python3 -m pytest -q` で既存試験も実行する。
5. commit・依頼branchへpushしremote headを照合する。PRを確認し、無ければdraftで作成する。
6. 後続の品質が同じ検証と差分を独立確認し、VERIFICATION.mdをpush・原本添付する。

## 条件ごとの直接検証
- 条件1: `tomllib`で実ファイルをparseし、`project.keywords == ["wordfreq"]` と文字どおりの1行追加を確認。
- 条件2: 起点のバイト列へ1行追加した結果との完全一致、他のTOML値の一致、全変更pathの許可リスト一致を確認。
- 条件3: 受付と最新の人の判断を再読し未決事項なしを確認する。新たな判断が必要ならPMへ返す。
- コードはリポジトリ直下で実行する。assert失敗・TOML parse失敗・Git失敗はいずれも不合格。

```python
from pathlib import Path
import subprocess
import tomllib
base = "20f706e61ba87746a7da1b3adc09c5fbe74731c9"
def git(*args):
    return subprocess.check_output(["git", *args])
old = git("show", f"{base}:pyproject.toml")
new = Path("pyproject.toml").read_bytes()
before, after = tomllib.loads(old.decode()), tomllib.loads(new.decode())
assert after["project"].get("keywords") == ["wordfreq"], "project.keywords missing/wrong"
assert new == old.replace(b'version = "0.1.0"\n', b'version = "0.1.0"\nkeywords = ["wordfreq"]\n', 1), "not exactly one prescribed line added"
del after["project"]["keywords"]
assert after == before, "other TOML values changed"
allowed = {"pyproject.toml", ".planning/argonauts/r-96e0448e/PLAN.md", ".planning/argonauts/r-96e0448e/VERIFICATION.md"}
changed = set(git("diff", "--name-only", base, "--").decode().splitlines())
untracked = set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
assert "pyproject.toml" in changed and changed | untracked <= allowed, "unexpected paths"
print("PASS: valid TOML, exact keywords line, other values and product files unchanged")
```

## 品質の証拠・マージ
- VERIFICATION.mdに対象head、比較起点、条件別判定、実コマンド・exit code・出力、既存試験、全差分pathを文字で残す。
- PMは標準read_fileで判断できること。画面変更なしのため画像・圧縮ファイルは不要。
- `pyproject.toml` は危険なパス。smartでも自動マージを予約せず、人がマージする案内へ渡す。
