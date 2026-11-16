# Design

## Context

新規追加の単一 Python パッケージ。既存コードへの影響はない。制約は PRD r-5a3b8a3f（FR-1〜FR-8）と、Bot ワークフロー側の制約（標準ライブラリ中心、`pyproject.toml` 等の危険なパスは人の承認対象になり得る、CI workflow ファイル変更は Bot の権限外）。本 file が受入条件 2 の「設計文書（ADR に相当するもの）」を兼ねる。

## Goals / Non-Goals

**Goals:**
- FR-1〜FR-8 の挙動を、テストで固定できる形に落とす。
- 入力元拡張（標準入力・URL）とトークナイザ差し替えの境界を、実装より先に見える形にする。
- 部品の境界ごとに単体試験を置けるようにする。

**Non-Goals:**
- 標準入力・URL 入力の実装（境界の確保まで）。
- 日本語形態素解析（D-1）。
- 性能最適化・ストリーミング・並列化。
- PyPI 公開（パッケージ設定は repo 内実行に必要最小限）。

## Decisions

### D-A: 部品の4分割と依存方向

`wordfreq/` パッケージを4つの部品に分割する。依存方向は一方向（外側が内側に依存する）:

- `tokenizer.py` — `iter_tokens(text) -> Iterator[str]`: 抽出（Unicode `\w` 連続最大長）+ `str.casefold()` 正規化。他部品の知識を持たない。
- `aggregator.py` — `count_words(tokens) -> Counter` と `top_words(counts, n) -> list[(word, count)]`（FR-4 のソート規則）。テキストの得方にも出力形式にも依存しない。
- `sources.py` — 入力取得境界。`TextSource` プロトコル（`read_text() -> str`）と、v1 の実装 `FileSource`（UTF-8 デコード、開けなさは `InputError`）。標準入力・URL は将来このプロトコルの実装として追加する。
- `formatters.py` — `format_text(pairs)` / `format_json(pairs)`。text 列書式は `<count>\t<word>` 1 行（タブ区切りで人可読・機械分割可。行頭が回数で語の長さと無関係に揃う）。
- `__main__.py` — 引数解析と合成のみ。exit code の分岐はここだけ。

代替案: 1 モジュール関数群（小さすぎる分離は試験しにくさより管理コストが勝つ場合もあるが、依頼が部品分離を明示的に要求しているため退ける）。クラス階層の過剰設計（プロトコル1つに実装1つで足りる）。

### D-B: 入力元拡張の構成判断（受入条件 2 の主眼）

「入力元を足す」変化に対して、変更箇所を `sources.py` の実装追加 + `__main__.py` の引数分岐だけに収める。解析・集計は `str` だけを受け取り、ファイルパスもストリームも知らない。標準入力を足す場合、`FileSource("-")` 相当ではなく専用 `StdinSource` を足すだけで、tokenizer・aggregator・formatter は触らない（この性質は試験で担保する: aggregator 系試験は合成テキストを直接渡し、FileSource を経由しない）。URL は「取得して str にする」責任も同じ境界に寄せる。

### D-C: エラーと exit code（D-4 と対応）

- 0: 正常終了（結果 0 件を含む）。
- 1: 環境エラー（`OSError` と `UnicodeDecodeError` を `InputError` に変換し stderr へ1行）。
- 2: 使い方エラー（argparse が `SystemExit(2)`。ファイル引数個数、`--top` 不正、`--format` 不正）。argparse の `type=` と `choices=` を使い、独自チェックは N の 1 未満のみ明示検証する。

### D-D: トークナイザ定義（D-3 と同一）

`re.findall(r"\w+", text, re.UNICODE)` → 各語に `casefold()`。underscore を語に含める副作用は受け入れ、試験で固定する。トークナイザは差し替え点: `count_words(iter_tokens(text, tokenizer=...))` 相当の注入か、tokenizer 関数引数（実装選択は tasks で決めるが、注入点の存在を spec の境界試験が要求する）。

### D-E: JSON 出力

`json.dumps([{"word": w, "count": c}, ...], ensure_ascii=True)` + 改行1つ。順序は FR-4。0 件は `[]`。key 名は `word` / `count`（spec 固定）。

### D-F: パッケージ形態

`pyproject.toml`（setuptools or hatchling の minimum）で `wordfreq` を定義し、repo 直下 `python -m wordfreq` で実行可能にする。ランタイム依存ゼロ。pytest は開発依存。CI に pytest ジョブが無ければ workflow 変更が必要になり得る（Bot 権限外 → 必要なら人の対応として proposal の Impact 済み）。Python バージョンは CI ジョブの現行 CPython 3 に合わせ、互換分岐を書かない。

## Risks / Trade-offs

- `\w` + underscore の語定義は利用者の期待とズレ得る → 試験で固定し、仕様書（spec.md の scenario）に明記して受入で確認する。
- `pyproject.toml` 追加が smart 方針で人の承認を要する → 変更は1ファイルに集約し、差分を最小にする。
- CI に pytest ジョブが無い場合、workflow 変更が Bot でできず依頼が止まる → 実装段階で既存 CI を確認し、必要なら block して人に委ねる（proposal Impact 済み）。
- text 列書式を design で固定したため、後続で JSON 派生ツールが増えるとき区切り変更が破壊的になり得る → 機械可読は JSON 側に寄せ、text は人向けと割り切る。
