# Independent reality review — wordfreq exclude architecture

## Verdict

**PASS（既存実装・技術実在性のfloor lens）**。確定判断AD-1・AD-2とStructural Seedを現行ソース、依存宣言、PRDに独立照合した。既存実装との矛盾、根拠のない新技術選定、未確認の最新版・starter defaultへの依存は検出しなかった。新機能の実装完了・試験合格・製品未決事項の解消を意味しない。

## Scope and method

- 対象：`_bmad-output/initiative-r-6442a149/architecture/architecture.md` 全文、`wordfreq/`の全Pythonソース。
- 補助根拠：同architectureの`.memlog.md`、PRD全文、`README.md`、`pyproject.toml`、既存試験の該当箇所。
- 観点：各確定判断が学習済み知識の断言ではなく、既存実装・明示要件・論理的帰結で裏づけられるか。技術実在性、用途適合、version/starterの未確認前提も確認。
- 確認はread_file/search_filesによる静的照合。コマンド、インラインコード、git、Kanban、テスト実行、設計編集、依存導入、外部送信は行っていない。
- 本レビューは親から委任された独立floor reviewerの成果物であり、全rubricや他lensを代行しない。

## Findings

### Blocking / high / medium

該当なし。

### 注意事項（非阻害・既に文書化済み）

1. **現行CLIにはまだ除外機能がない。** `wordfreq/__main__.py:13-19`のparserに`--exclude`はなく、`:29-38`も本文の読取り・直接集計のみ。spine:61が正しく現状と計画を区別している。ADの`[ADOPTED]`を「実装済み」と解釈してはならない。追加filterと除外FILE取得は後続実装の拘束である。
2. **未決の入力契約を既存本文仕様から埋めない。** 現行本文はUTF-8で読み、casefoldし、本文取得失敗はexit1になるが、新除外FILEのUnicode方式・strip・BOM・例外契約等はPRD OQ-1〜OQ-6に残る。spine:22,51,57,79-80がこの区別を保持する。これらの仕様・期待値確定前に要求担当による解消が必要。
3. **実行互換性の合格は本レビューの範囲外。** 既存試験は読み取りによる補強根拠だけで、実行していない。PRD:80と既存`tests/test_cli.py:154-177,504-527,648-669`からgit操作・権限変更を含む試験があることも確認した。禁止範囲下で一括実行していないことは検証漏れの隠蔽ではなく、明示的な制約である。

## Decision-by-decision evidence

| 対象／確定主張 | 確認根拠 | 判定 |
| --- | --- | --- |
| Paradigm：既存の単方向CLI／pipes-and-filtersをratifyする | `__main__.py:7-10,29-48`が取得→tokenizer→集計→選択→formatterを合成。`sources.py:17-22`がI/O担当、`aggregator.py:6-17`と`formatters.py:6-27`はデータを受け取る処理。新framework名ではなく実装構造へのラベル | 裏づけあり |
| AD-1：CLI側で取得を統括し、集計・formatterへ取得依存を入れない | `__main__.py:29-48`、`aggregator.py`全体、`formatters.py`全体。`tests/test_sources_boundary.py:7-17`にも集計がファイル取得しない契約がある。除外FILE取得そのものは新設計規則で、既存実装済みとは扱わない | 既存境界に適合 |
| AD-1：本文トークンを集計前に除外し全形式で共有 | `__main__.py:34-48`に共通集計と形式分岐が存在。`count_words`は`Iterable[str]`を受ける（`aggregator.py:3-8`）ため、トークン段階のfilterを接続できる。PRD FR-1、RULE-1（:58,84-86）が新規制約の直接根拠 | 要件由来・既存接続可能 |
| AD-1：min-count→top→formatterを維持 | `__main__.py:36-48`がmin-countによるCounter選択後にtop_words、続いてformatterを呼ぶ | 完全一致 |
| AD-1：HTML総数は除外後・min-count/top前 | 現行の総数計算は`__main__.py:34-38`、HTMLへの引渡しは`:44`。`formatters.py:22-27,113-115`は渡された総数を表示。除外後への更新はPRD RULE-1（:84-86）による帰結で、現行の表示前集計境界を維持する | 要件由来・既存接続可能 |
| AD-1：追加依存・権限変更・外部送信不要 | PRD RULE-2（:88）、`pyproject.toml:9`のruntime依存空配列、`wordfreq/`全実装のローカルファイル・標準ライブラリ処理。新たな外部技術を必要とする判断はない | 実装方針として整合。将来コードの達成は未検証 |
| AD-2：本文分割とcasefoldを維持 | `tokenizer.py:6,9-18`はUnicodeの`\w+`抽出後casefold。`tests/test_tokenizer.py:6-12,15-38,48-60`と`README.md:30`が補強 | 完全一致 |
| AD-2：回数降順・同数時は正規化後初出順 | `count_words`はCounterを構築（`aggregator.py:6-8`）、`top_words`はcountのみをkeyにソート（:11-17）。`tests/test_aggregator.py:17-24,37-46`に初出順と正規化後の反復の契約がある。`README.md:31,38`も一致 | 裏づけあり |
| AD-2：未指定では除外処理を起動せず既存出力・エラーを保存 | 未指定経路の非干渉はPRD FR-6（:78-80）の要求。現行書式は`formatters.py:6-14,22-127`、引数エラーと本文取得エラーは`__main__.py:23-33`、出力・終了は`:49-54`。将来の分岐実装に対する規則であり現時点の動作実証とは区別 | 互換性基準として整合 |
| AD-2：本文不存在exit1を保持、除外FILE不存在exit2と混同しない | 現行の`InputError`→exit1は`__main__.py:29-33`、原因のラップは`sources.py:18-22`。除外FILE不存在exit2はPRD FR-4（:70-72）。複合失敗はOQ-6に残しており現在の処理順から勝手に確定していない | 完全一致 |
| AD-2：残存語の回数・相対初出順を保持、除外重複で結果を変えない | PRD FR-1／RULE-1（:58,84-86）が根拠。既存トークン列の順序とCounter／top_wordsの境界に合う。具体的な集合型・関数署名を強制していない | 要件由来・既存接続可能 |
| Structural Seed：6モジュールの実在と責務、除外オプションなし | `__main__.py`、`sources.py`、`tokenizer.py`、`aggregator.py`、`formatters.py`、`__init__.py`を全読。spine:61の列挙・責務と一致 | 完全一致 |
| ローカルCLI継続、新サービス・provider・認証・永続モデル・通信なし | 現行コード全体、`README.md:7,25`、PRD Non-goals（:90-92）と整合。今回の変更がこれらを導入しないというスコープ制約であり、配備済み環境の網羅的監査ではない | 整合 |

## Technology / version / starter currency check

- **新規技術・ライブラリ・framework選定：なし。** spineは既存のCLI、Pythonソース上のcasefold／Counter、text/json/htmlを参照するだけで、用途に不要な新stackを拘束しない。Counter自体もspine:78で具体型の拘束対象から外れている。
- **Python標準ライブラリ処理の実在・適合：既存プロジェクトで確認。** `argparse`、`collections.Counter`、`re`、`json`、`html.escape`等のimportと使用箇所を実ファイルで確認した。本レビューではランタイムimportの再実行まではしていない。
- **versionに関する確定判断：なし。** `pyproject.toml:2,7,12`には既存の`setuptools>=61`、パッケージ版`0.1.0`、devの`pytest`があるが、spineはこれらの最新版・推奨版・更新方針を主張せず、追加もしていない。最新のPython／pytest／setuptools版が何かという情報を本設計の正当化に使っていないため、最新版検索・新たなpin提案は対象外。
- **starter：不使用。** brownfieldで既存6モジュールを継続する設計であり、greenfield starterのlive defaultsに依存する判断はない。
- **Web調査：未実施。** floorの「web-researched **or reality-checked**」について、本件の全確定技術判断は現行コード・依存宣言へのreality checkで満たす。最新versionや外部サービスの現存性など、既存プロジェクトでは検証できない主張はspineに見当たらない。Web未確認の新技術を既存技術として通したものではない。
- `.memlog.md:10-13`にもADと現行実装の対応が記録されているが、その自己申告のみを根拠にせず、上表のソースを独立照合した。

## Disposition / handoff

- このlensから設計修正要求はない。
- PRD OQ-1〜OQ-6は既存の担当・期限へ戻す。未決を新たな設計判断で補完しない。
- 後続実装ではFR-6の実行互換性とRULE-2を別途検証する。本レビューはテストの現在合格数・ブラウザ品質・実際の通信計測・配備環境・採用versionのサポート状況を保証しない。
- 作成／変更対象は本レビュー文書のみ。設計原本、memlog、実装、README、試験、git、Kanbanには変更を加えていない。
