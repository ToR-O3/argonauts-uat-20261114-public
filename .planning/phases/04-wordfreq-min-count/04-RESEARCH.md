# Phase 4: wordfreq min-count - Research

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は `04-CONTEXT.md:14–41,65–66` の原文。ここでの引用は承認済み制約であり、過去phaseの実行済み証明ではない。

### Implementation Decisions (locked)

### 引数・入力境界
- D-01: min-countは既定1、1以上の整数のみ。既存argparse/int規則を維持し、0/負数/非整数/非数値/欠落は入力取得より先にexit2、stderr通知、stdout空、Traceback/エラーHTMLなし。topとの大小相互制約を追加しない（MC-1、AC3、task1.2）。
- D-02: 有効N>1でも不存在/ディレクトリ/開けない/不正UTF-8は既存exit1、stderr通知、stdout空を維持する。既存のファイル入力境界・抽出/casefold・formatter公開契約を変えない。

### 選択順序と全形式
- D-03: casefold後のcountsからN未満だけを除外し、回数降順・同数時正規化後初出順で選び、その後topを適用する。text/json/htmlは同じpairsを使う。旧単語昇順への復帰は禁止。top/min-count値は独立で指定順によらない（MC-1/FR-2/FR-4、AC1/AC4、task1.3）。
- D-04: 閾値ちょうど/超を保持。Straße STRASSE→strasse2、Zoo apple APPLE zoo banana→N2/top10でzoo2,apple2、N2/top1でzoo2。出力比較だけで除外→topの内部順序を証明したことにせず、品質が該当ソース箇所を記録する。

### 元集計・空結果・見た目
- D-05: 元countsを破壊しない。HTML総数はmin-count/top前の回数和、表示行の和や種類数ではない。語あり全除外でも元正数を保持し、抽出0語は0（HTML-2、AC5、task1.4）。
- D-06: 空ファイル/空白のみ/句読点のみ/全除外は正常exit0。text空文字、json[]+末尾改行1つ、HTML既存メタ情報・3列見出し・0データ行・空文言を保持。basename限定/UTF-8/escape/静的安全性/formatter/CSS/文言/見た目は変えない（MC-2、AC1/AC5/AC7）。

### 既定互換と試験順序
- D-07: 最初の製品変更前にtask1.1を実施する。着手前head/環境/入力/argvと全3形式のstdout、HTML原本、1280×900・320×900 DPR1画像を保存。同数語と10種類超の入力を含める。後の未指定/明示1を同条件で比較し、既定text/top10と既存構造・初出順を維持する。変更後同士の比較で代用しない（MC-2、AC2、tasks1.1/2.1）。
- D-08: tasks1.2/1.3/1.4は対応するpytestを先に追加しRED確認→最小実装→GREEN。全3形式、境界/正常/異常/Unicode/独立top/空/抽出0語/全除外/既定互換と既存全pytestを実行する。環境/収集件数/実コマンド/exit/結果を保存し、0件収集・未実施を成功にしない（MC-3、AC6、task2.1）。

### 独立品質と配送
- D-09: task2.2の実行主体は品質。対象headで自らCLIを再実行し、既定/閾値部分表示/top併用/全除外/空のHTMLを1280×900と320×900 CSS px・DPR1で開き実閲覧。同環境のbaseline画像と比較し、対象head/argv/入力/stdout/stderr/exit/HTML/画像/閲覧結果/ソース順序をAC1/2/4/5/6/7へ対応付ける。既存文字範囲・安全性の証拠契約を維持。Builder証拠や自動captureを独立閲覧へ代用しない。未検証はgaps。
- D-10: 証拠原本の保存・標準添付・受取PMの読取りは別gate。索引とAC対応、head/run/root/path/SHAを残し、PMが読める原本を渡す。拒否や能力不足を迂回せず停止して理由を報告する。過去の証拠のscope/head/合格を流用しない。

### 説明・範囲・工程
- D-11: READMEの指定法/既定1/不正値exit2/先min後top/元HTML総数/全除外時の閾値調整のみ最小更新。新サービス・依存・CI追加変更・新入力元・抽出変更・全体リファクタ・テーマ/対話/サーバー・外部送信/権限/課金/削除は対象外（MC-3、AC7）。
- D-12: 有限回の既存CI確認・draft PR・レビュー・phase検証・OpenSpec verify・受入・sync/archiveはチームの該当カードで扱い、CI待機ループを導入しない。既存CI未報告/pending/不調を成功と呼ばない。Q-01背景/Q-02期限とA-01〜04は未提示/未承認のまま非要件。旧phase1/3のstaleは表示しても今回計画へ混ぜない。

### Claude's Discretion
既存コードを調べた最小の関数境界、試験ファイルの分け方、PLAN分割。各PLANは3task以内、同じ依頼branchへ順に積み上げる。baseline保存を製品変更より先に置く。検証コマンドと入力は当該task終了時点で存在し、他PLANの成果の有無にかかわらない独立PLAN検証を確保する。品質専用の確認はBuilderの自己承認タスクにしない。

### Deferred Ideas
新たな利用背景や期限・効果を創作しない。依存/CI/見た目/入力元/形態素解析/全体リファクタは対象外。マージは人または品質が許可された予約のみ。今回のカードは計画まで。
</user_constraints>

**Researched:** 2026-11-18 JST（terminal `date --iso-8601=seconds`）
**Domain:** Python CLIの引数・共通表示選択、既存静的HTMLの回帰証拠
**Confidence:** LOW（公式confidence seamの機械分類。下記「Metadata」参照。一次コードの読取り事実と、未実行の受入結果を区別する。）

## Summary

**推奨:** 製品変更前baselineを最初のgateに置き、CLIの既存argparseにmin-countを追加する。正規化済みの元Counterとtotalを保持し、挿入順を保つ別Counterへ閾値を適用してから既存 `top_words(counts, n)` を呼ぶ。3形式のformatterは触らない。これは承認済みdesignの具体化であり、新設計への変更ではない。[VERIFIED: openspec/changes/r-e476c11d-wordfreq-min-count/design.md:9–18（原文 `top_words(counts, n)`、`count>=min_count`）; wordfreq/__main__.py:20–47]

現行の処理は既に入力取得→casefold→Counter→元total→共通pairs→形式分岐に分かれている。最小の製品変更箇所はCLI合成部分で足り、集計関数の公開引数も維持できる。初出順はCounterの挿入順と回数だけの安定ソートに依存するため、フィルタをset化・語順ソートしてはいけない。[VERIFIED: wordfreq/tokenizer.py:14–18; wordfreq/aggregator.py:6–17; wordfreq/__main__.py:30–42]

計画上の主な作業量は製品コードよりもbaselineと独立証拠である。既存HTML verifierには再利用できる幾何・通信・画像同一性部品がある一方、固定ケース・旧scope・AC番号はPhase 3専用であり、そのままPhase 4の合格装置にできない。研究時点ではpytest本体の版を確認しただけでsuite・browser受入・baseline保存は未実施。[VERIFIED: tools/verify_wordfreq_html.py:28–53,806–862,925–927,1032–1035; 本セッションterminal版確認]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 引数解析・exit優先度 | ローカルCLI | 入力境界 | 読込み前検証と終了をCLIが所有する。[VERIFIED: wordfreq/__main__.py:20–29] |
| 正規化・元集計 | 純粋なPython部品 | CLI合成 | 正規化済みトークンからCounterを作る。[VERIFIED: wordfreq/tokenizer.py:14–18; wordfreq/aggregator.py:6–8] |
| 閾値→順位→top | CLIの共通選択 | 集計部品 | 全formatterへ同じpairsを渡す承認設計。[VERIFIED: openspec/changes/r-e476c11d-wordfreq-min-count/design.md:16–17] |
| HTMLメタ情報・静的表示 | 純粋formatter / 静的文書 | ブラウザ描画 | totalは呼出し側、formatterは表示だけ。[VERIFIED: wordfreq/formatters.py:22–32] |
| 既定互換・独立閲覧・配送 | 検証工程 | Builder / 品質 / PM | 実行者と証拠の種類を分離する。[VERIFIED: .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:28–34] |

<phase_requirements>
## Phase Requirements

下表のDescriptionは `.planning/REQUIREMENTS.md:56–62` の原文。[VERIFIED: .planning/REQUIREMENTS.md:56–62]

| ID | Description | Research Support |
|---|---|---|
| REQ-15 | AC1: 正規化後の出現回数がmin-count未満の語をtext/json/html共通で除外し、ちょうどと超過を残す。空入力・抽出0語・全除外も既存の空形式でexit0。 | 共通pairs選択、独立literal oracle、空結果matrix |
| REQ-16 | AC2: 未指定と明示min-count1は変更前の全形式stdout・構造・既定top10・同数初出順と一致。最初の製品変更前headで同数/10種類超を含む入力、argv、環境、stdout/HTML/画像を保存して比較する。 | baseline最初のgate、全形式bytes比較、同環境画像 |
| REQ-17 | AC3: min-count既定1、1以上の整数のみ。0/負数/非整数/非数値/値欠落は入力取得前exit2、stderr通知、stdout空。有效N>1の入力取得失敗exit1は維持。 | 既存argparse方式、read_text未呼出しspy、実CLI異常matrix |
| REQ-18 | AC4: casefold後のcountsから閾値除外→回数降順/同数初出順→topの順。両値は独立、指定順でも不変。品質は出力に加えて該当ソース順序を確認。 | 元Counterの順序保持、ソース行/diffの独立記録 |
| REQ-19 | AC5: HTML総数はmin-count/top前の元countsの回数和。全件除外でも正の元総数、抽出0語は0。既存formatter/CSS/文言・basename限定・静的安全性を維持。 | 先にsum、formatter無変更、全除外正総数試験 |
| REQ-20 | AC6: 全3形式の正常/境界/異常/Unicode/併用/既定互換/空結果をpytestで追加し既存全件も成功。品質自身が対象headでCLI再実行と1280×900/320×900 DPR1ブラウザ閲覧・変更前同条件画像比較を行い、入力/argv/stdout/stderr/exit/HTML/画像/閲覧結果/ソース箇所をAC別に保存・標準添付しPMが原本を読めるようにする。未検証は合格としない。 | Validation Architecture、今回専用証拠索引・3段配送gate |
| REQ-21 | AC7: CI追加変更・依存追加・見た目変更・新サービス・新入力元・抽出変更・全体リファクタなし。READMEの指定法/既定1/先min後top/元総数/不正値exit2/全除外の閾値調整のみ最小更新。既存出力/安全性/入力境界/formatter公開契約を維持。既存CIの未報告を成功と呼ばず待機処理を追加しない。 | 差分scopeを今回基点から確認、READMEのみ最小追記 |
</phase_requirements>

## Project Constraints (from HERMES.md)

root `HERMES.md` と設定参照先 `.hermes/HERMES.md` は今回のread_fileでともにnot_found。プロジェクト `.hermes/skills` と `.agents/skills` も検索先不存在。追加ルールを推定しない。公式 `query agent-skills gsd-phase-researcher --skills-only` はexit0・空出力だった。[VERIFIED: 本セッションread_file/search_files/公式CLI結果]

この調査の操作制約は呼出し元指示による。製品・新検証コードは作らない、研究原本のみ保存、commit/push/Kanban/自動継続なし。インライン実行・ヒアドキュメント・未作成試験の試走はしない。将来PLANの検証コマンドは、そのtaskで実在化・確認したファイルを実行させる。

## Standard Stack

| 項目 | 現物・版 | 用途 / 計画上の扱い |
|---|---|---|
| Python標準ライブラリ | CI宣言 `python-version: "3.12"` | 既存 `argparse`、`Counter`、安定sort、`sum`、HTML escapeを使う。CIを編集しない。[VERIFIED: .github/workflows/pytest.yml:13–18] |
| 製品metadata | `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` | 同名の外部パッケージをinstallしない。[VERIFIED: pyproject.toml:5–8] |
| pytest | 既存dev宣言 `dev = ["pytest"]`、実環境9.0.3 | パラメータ化、tmp_path、monkeypatch、capsys、実subprocessを継続。[VERIFIED: pyproject.toml:10–11; tests/test_cli.py:16–20,503–561; terminal版確認] |
| HTML証拠補助 | 既存Playwright CLI 1.60.0、Chromium 156.0.8078.73 | 検証環境の既存部品。製品依存に追加しない。版の存在とbrowser起動成功は別。[VERIFIED: 本セッションterminal版確認] |

**Installation:** 不要・追加禁止。最新版への更新調査やpackage-legitimacy gateは、新規外部packageを導入しないため対象外。上記は既存環境の確認であり版固定・対応版全列挙の提案ではない。[VERIFIED: 04-CONTEXT.md:37; pyproject.toml:8–11]

## Architecture Patterns

### Data Flow

```text
argv → argparse / 正数検証 ──不正──→ stderr / exit2（入力取得なし）
                 │有効
                 ↓
UTF-8 FileSource ──読込み失敗──→ stderr / exit1
                 ↓
Unicode抽出 → casefold → 元Counter → 元total
                                  │
                                  ↓
                        挿入順を保つ閾値フィルタ
                                  ↓
                      回数安定sort → top → 共通pairs
                                  ↓
                   text / json / html（basename, 元total）
                                  ↓
                              stdout / exit0
```

新規フィルタ以外は現行構成であり、フィルタ位置は承認済み設計。[VERIFIED: wordfreq/__main__.py:20–48; wordfreq/aggregator.py:6–17; openspec/changes/r-e476c11d-wordfreq-min-count/design.md:15–18]

### Component Responsibilities / 最小編集方針

| 現行ファイル（実際に読了） | 現行根拠 | 今回の推奨 |
|---|---|---|
| `wordfreq/__main__.py` | `parser.add_argument("--top", type=int, default=10)`、`if args.top < 1:`、`total = sum(counts.values())`、`pairs = top_words(counts, args.top)` [VERIFIED: wordfreq/__main__.py:15,23–24,30–32] | min-countのparser追加、正数検証、順序保持の別Counter生成をここに限定。total算出の元データを変えない。 |
| `wordfreq/aggregator.py` | `return sorted(counts.items(), key=lambda wc: -wc[1])[:n]` [VERIFIED: wordfreq/aggregator.py:11–17] | `top_words(counts, n)`を維持。閾値専用関数へ大きく再編しない。 |
| `wordfreq/formatters.py` | `def format_html(pairs: list[tuple[str, int]], basename: str, total: int) -> str:` [VERIFIED: wordfreq/formatters.py:22–27] | 編集不要を基本とする。空メッセージも変更しない。 |
| `wordfreq/sources.py` / `wordfreq/tokenizer.py` | `encoding="utf-8"`、`except (OSError, UnicodeDecodeError)`、`re.compile(r"\w+", re.UNICODE)`、`token.casefold()` [VERIFIED: wordfreq/sources.py:17–22; wordfreq/tokenizer.py:6,14–18] | 編集不要。新入力源・字句制限を導入しない。 |
| `README.md` | 現行top/形式/順序/元総数/エラー説明 [VERIFIED: README.md:18–30] | min-countの指定、既定1、先min後top、元総数、exit2、全除外時は閾値を下げる案内だけを追記。 |

**フィルタの注意:** Counterを既存itemsの順で作る。Counterへ `(word, count)` の列をそのまま「トークンiterable」として渡すと、語→回数のmappingではなくタプル自体を数える危険があるため、mappingとして構築する。元countsのitems順・値が変わらないことを試験する。これは設計提言であり新関数・コードは本研究では書かない。[CITED: https://docs.python.org/3.12/library/collections.html#collections.Counter; VERIFIED: tests/test_aggregator.py:20–24,41–46]

## Code Examples（現物からの引用のみ）

次は現行コードであり、min-count実装済みの例ではない。

```python
# wordfreq/__main__.py:30–32
counts = count_words(iter_tokens(text))
total = sum(counts.values())
pairs = top_words(counts, args.top)

# wordfreq/aggregator.py:17
return sorted(counts.items(), key=lambda wc: -wc[1])[:n]

# wordfreq/formatters.py:13–14
items = [{"word": word, "count": count} for word, count in pairs]
return json.dumps(items, ensure_ascii=True) + "\n"
```

上記文字列・式は各読了箇所の原文。[VERIFIED: wordfreq/__main__.py:30–32; wordfreq/aggregator.py:17; wordfreq/formatters.py:13–14]

## Don't Hand-Roll

| 問題 | 自作しないもの | 使用するもの / 根拠 |
|---|---|---|
| 整数解析・usage error | 独自regex、桁数上限、int環境制限解除 | 既存argparse/intとparse後正数検証。`ArgumentParser.error`はstderr・status2。[CITED: https://docs.python.org/3.12/library/argparse.html#argparse.ArgumentParser.error; VERIFIED: design.md:15] |
| 順位決定 | lexical tieキー、set経由、新topアルゴリズム | 既存回数のみstable sort。Python公式は同キーの元順保持を保証。[VERIFIED: wordfreq/aggregator.py:11–17; CITED: https://docs.python.org/3.12/howto/sorting.html#sort-stability-and-complex-sorts] |
| 空結果・escape | min-count専用HTML、別CSS、閾値ラベル | 既存formatterの空pairs・標準escape。[VERIFIED: wordfreq/formatters.py:17–38] |
| ブラウザ測定 | 新幾何エンジン、raw補正 | 既存geometry collector / errors関数。原本を丸めない。[VERIFIED: tools/wordfreq_html_geometry.js:1–68; tools/verify_wordfreq_html.py:157–221] |
| 受入判定 | 自動でreadableを埋める台帳 | 品質本人の画像実閲覧と明示記録。[VERIFIED: docs/wordfreq-html-verification.md:64–79] |

## Existing Verifier Reuse Boundary

### そのまま再利用できる部品

- `Document`（静的タグ・属性・CSS資源参照監査）、`geometry_errors`、`network_errors`、`dom_errors`、`png_size`、`digest`、画像coverage/identity検査は、今回の実入力・期待pairs・元total・raw/画像に適用できる部品である。各関数の現物を読了。ただし再利用可能性の読取りであり、今回環境で成功したという意味ではない。[VERIFIED: tools/verify_wordfreq_html.py:67–107,157–262,506–583,899–904,937–962]
- `collect_view` は任意case recordのHTMLをfile URLで開き、幅・DPRを指定し、raw・font・network・full/tileを採取する。原文は `viewport=dict(width=width, height=900), device_scale_factor=1`。`Emulation.setScrollbarsHidden` をnavigation前に設定し、測定と画像で同layoutを維持する。幾何JSもそのまま使い、DOM/CSSを直さない。[VERIFIED: tools/verify_wordfreq_html.py:586–671; tools/wordfreq_html_geometry.js:28–67]
- 通信observer/canaryの判別力は既存方式を維持する。許可URLを広げて今回ケースを通す、成功responseがないだけで無通信とする、といった変更をしない。[VERIFIED: tools/verify_wordfreq_html.py:418–553,716–801]

### そのままPhase 4受入に使えない部分

| 部分 | 現物上の制約 | 今回の最小対応（将来Builder/品質） |
|---|---|---|
| `fixed_cases()` / `generate_cases()` | argvは `"--format"` と任意 `"--top"` だけ。min-countなし。既定top・10種類超のfixtureはHTML、tieのtext/jsonはtop1/2。[VERIFIED: tools/verify_wordfreq_html.py:28–53,118–120] | min-count部分表示・top併用・全除外・空、全形式baselineと未指定/明示1比較を今回専用ケースとして追加する。過去15ケースだけでAC2/AC6を満たしたことにしない。 |
| `scope_report()` | 固定 `SCOPE_BASE = "5a7659b949dc118b59cea5ef3eb40bcd94337d8d"`、`APPROVED_PRODUCT = "ed7e6cc9d608bc40a82da76e85ca6e57a0808b54"`。`"product differs from approved03-02 snapshot"` を拒否条件にする。[VERIFIED: tools/verify_wordfreq_html.py:806–807,848–853] | 旧定数を今回headへ黙って置換しない。今回実装前headと対象headの差分を今回scopeとして別記録し、製品のmin-count差分だけを許容、formatter/tokenizer/source/依存/CIの変更なしを確認する。 |
| `scope_path_errors()` | 許可範囲は旧 `".planning/phases/03-wordfreq-html-output/"` 等。[VERIFIED: tools/verify_wordfreq_html.py:809–824] | 旧allow-listは今回の範囲証明に流用しない。Phase 4の実際の所有pathを計画に列挙する。 |
| `ac_index` / ledger / finalization | `range(1, 7)`、旧AC1〜6。[VERIFIED: tools/verify_wordfreq_html.py:925–927,1032–1035,1124–1127] | 今回はAC1〜7とREQ-15〜21へ対応する独立索引を作る。旧AC5等と意味を混同しない。 |
| `capture` / `review-session` | captureは `"pending-review"`、independent_acceptance false。review-sessionは旧scopeを呼ぶ。[VERIFIED: tools/verify_wordfreq_html.py:683–707,1227–1239] | capture成功は保存補助のみ。旧review-sessionをそのまま今回合格装置としてPLANへ転記しない。 |
| 既存verifier試験 | 固定ケース数、旧scope IDs、旧AC数を意図的にassert。[VERIFIED: tests/test_html_verifier.py:23–44,625–647,770–806] | 既存fixtureの期待値を機械置換して今回へ転用しない。既存全pytestも維持する。 |

**推奨する最小の今回適用:** 製品の共通選択変更と分け、今回専用の実ファイル検証driverを準備する（保存場所とCLIはplannerが確定する提案で、現時点の実在ファイルではない）。既存の汎用採取/監査部品をimportして使い、今回のケース・baseline比較・scope・AC索引だけを所有する。旧verifier全体の書換えや受入条件弱体化はしない。baseline modeは製品にmin-countを渡さず採取し、post-change modeだけが閾値argvを使う。ツール自身の変更はbaseline時のprovenanceへ正直に記録する。既存captureのdirty拒否を使う場合はツール変更を無視して通すのでなく、後工程の正式な変更確定後・製品未変更のheadで保存する。今回研究では新driverも作らない。[設計提言; 根拠: 上表および04-CONTEXT.md:29–41]

## Recommended Implementation Order

各PLANは3task以内・同じbranchへ直列。以下は分割案でありPLAN原本や実行開始ではない。[VERIFIED: 04-CONTEXT.md:40–41]

1. **最初にtask1.1 / baseline保存。** 必要な検証driver/入力原本の準備→製品変更前headで全3形式のstdout・stderr・exit・argv・環境とHTML/両幅DPR1画像を保存→原本の読取りと索引を確認。全形式に同数かつ10種類超の同一入力を使い、basenameも固定する。デフォルトtext実行と既定top10も採る。保存失敗なら製品編集へ進まない。後から旧headをcheckoutして取り直すことを「先に保存」の代わりにしない。
2. **task1.2 / 引数を縦sliceでTDD。** 既存CLI試験へ正数/既定/不正/欠落/入力取得前検証を追加し、意図したRED→parserと正数検証だけを追加→GREEN。READMEの引数・exit2説明と実help/実例結果を同taskで用意する。
3. **task1.3 / 全形式共通選択をTDD。** ちょうど/超・Unicode・初出順・独立top・指定順・元Counter非破壊を追加してRED→共通フィルタの最小実装→GREEN。READMEの先min後top例。品質用ソース確認対象を特定する。
4. **task1.4 / 空と元総数をTDD。** 先に試験追加し、全除外と元正数の総数、抽出0語とtotal0を別々に確認する。既存formatterを変えず通る項目は「既存green」と正直に記録する。必要な新REDは意味のある差分が欠けている段階で確保し、REDを作るためだけの製品破壊はしない。空結果試験の先行追加を1.3の実装前に置く、または1.3/1.4を同PLANの小さいRED→GREEN連続sliceに統合し、1.3で全て実装してから1.4のREDを捏造する構成を避ける。
5. **task2.1 / Builder統合確認。** 既存全件と追加試験を実行・件数/exitを保存。変更前原本/未指定/明示1を全形式bytes比較。CI/依存/formatter/CSS等の差分なしを確認。
6. **task2.2 / 品質専用gate。** 品質本人が対象headで独立CLI再生成し、既定・部分表示・top併用・全除外・空を両幅で開く。長語・特殊basename・注入候補の既存安全性観点も保持する。全画像/全tile/raw/通信・baseline画像比較・除外→topソース行を確認し、AC1/2/4/5/6/7へ紐付ける。保存→標準添付→PM原本読取りは別gate。

順序の根拠はPRD tasks1.1〜2.2とD-07〜D-10。[VERIFIED: .planning/argonauts/r-e476c11d-prd.md:134–144; 04-CONTEXT.md:28–34]

## Common Pitfalls

1. **変更後同士だけを比較する。** 明示1と未指定が等しくても変更前互換は未証明。変更前のbytes/画像を最初に保存する。[VERIFIED: PRD:60–62,136]
2. **フィルタで元Counterを削る。** totalも減る、同数順が変わる。元itemsとtotalを保持する。[VERIFIED: design.md:16,22–25; tests/test_aggregator.py:20–24]
3. **出力で内部順序を証明したと言う。** 今回の頻度降順と下限閾値では複数の処理順が同じ出力になり得る。品質が実際のフィルタ→top呼出しソースを読む。[VERIFIED: design.md:18; PRD:79–81]
4. **エラーを空結果へ変換する。** 有効閾値の読込み失敗はexit1。入力失敗matrixへN>1を追加する。[VERIFIED: PRD:53–55; tests/test_cli.py:503–527]
5. **permission試験をchmodだけで済ます。** 現行試験は同じ実効ユーザーで実際のPermissionErrorも検証している。root等で失敗を再現できない場合、skipで合格にしない。[VERIFIED: tests/test_cli.py:511–527]
6. **HTML空文言を改善する。** 今回は文言/CSS変更禁止。全除外時の閾値調整はREADMEだけ。[VERIFIED: design.md:17,26; wordfreq/formatters.py:34–38]
7. **旧scope/旧ACを流用する。** verifierにはPhase 3専用snapshotとAC数が埋込まれている。今回の基点・対象・索引を別にする。[VERIFIED: tools/verify_wordfreq_html.py:806–862,1032–1035]
8. **TDDを後付けする。** 1.3の共通選択を実装すれば1.4の全除外も自然にgreenになり得る。PLAN分割時点で新空結果試験を先に追加する順序を設ける。[設計提言; VERIFIED: PRD:138–139; wordfreq/formatters.py:6–14,34–38]
9. **版確認を実行合格と取り違える。** pytest 9.0.3の存在はsuite greenではなく、Chromium版表示は画像生成・閲覧成功ではない。[VERIFIED: 本セッションterminal版確認のみ]

## Validation Architecture

設定の `"nyquist_validation": true`、`"security_enforcement": true` をread_fileで確認したため両節を含む。[VERIFIED: .planning/config.json:25,49–51]

### Test Framework

| Property | Value |
|---|---|
| Framework | pytest 9.0.3（確認済み既存環境） |
| Config file | pyprojectはpackage設定のみ。読了範囲にpytest設定節なし。追加config不要。[VERIFIED: pyproject.toml:1–14] |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py -q` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` |
| Collected-count command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --collect-only -q` |
| Environment record | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --version` と `/usr/bin/python3 --version` |

コマンドは既存実ファイルへ向く。full commandは既存guide原文 `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` と一致する。[VERIFIED: docs/wordfreq-html-verification.md:18–22; tests/test_cli.py:1–20; tests/test_aggregator.py:1–14; tests/test_formatters.py:1–16]

**研究中は上のsuite/collectコマンドを実行していない。** quickの30秒未満や既存件数を推測で確定しない。Builderは個別taskの実在node IDまたは追加済み試験を収集で確認してから絞り込んでRED/GREENを採る。まだ存在しないtest node・新driverの起動コマンドを本研究で試さない。

### Existing Test Assets

- 実CLIを `sys.executable` とrepo rootから実行しstdout/stderrを分離する `run_cli`、bytes版 `run_cli_bytes`、3形式の明示期待値を照合する `assert_output_bytes` がある。これらを既存CLI試験ファイル内で再利用すれば別framework不要。[VERIFIED: tests/test_cli.py:16–20,418–441]
- `CLIHTML` は3列・basename・totalをparseする。全形式matrixは独立literal pairsを持つ。HTML静的安全性の `HTMLDocument` と `assert_static_document` もある。[VERIFIED: tests/test_cli.py:201–260,448–478; tests/test_formatters.py:51–133]
- 既存入力失敗・permission・使用エラー・hashseed・encoding試験を維持し、今回のN>1も追加する。[VERIFIED: tests/test_cli.py:266–415,503–578]
- formatterの空・escape・固定CSS・長文試験と、source境界のspy試験がある。read-before-validationを避ける新spyもこの既存monkeypatch方式に合わせる。[VERIFIED: tests/test_formatters.py:136–262; tests/test_sources_boundary.py:7–42; tests/test_cli.py:548–561]
- verifier/finalizationの多くはsynthetic predicate・fixture試験であり、本物の画像閲覧や今回scope合格へ転用しない。[VERIFIED: tests/test_html_finalization.py:1,15–36; tools/verify_wordfreq_html.py:1350–1371]

### Phase Requirements → Test Map

「File Exists」は受け皿の存在と今回試験実装の有無を区別する。下記自動コマンドは全て既存ファイルを実行するが、min-count試験はWave 0で追加するまで網羅しない。

| Req ID | Behavior | Test Type | Automated Command（repo root、同じenv指定を前置） | File Exists? |
|---|---|---|---|---|
| REQ-15 | 未満/ちょうど/超、空/空白/句読点/全除外、全3形式 | integration | `/usr/bin/python3 -m pytest tests/test_cli.py -q` | ✅受け皿 / ❌今回matrix追加 |
| REQ-16 | 変更前/未指定/明示1、同数+10種類超、既定text/top10 | integration + browser比較 | `/usr/bin/python3 -m pytest tests/test_cli.py -q`、baseline照合driverは作成後に確定 | ✅既存既定試験 / ❌保存比較driver・今回試験 |
| REQ-17 | 正数、0/負数/1.5/abc/欠落、read_text未呼出し、有効2の読込み失敗 | integration + boundary | `/usr/bin/python3 -m pytest tests/test_cli.py tests/test_sources_boundary.py -q` | ✅受け皿 / ❌今回N試験 |
| REQ-18 | casefold合算、同数初出順、独立top・指定順、元counts不変 | unit + integration + source review | `/usr/bin/python3 -m pytest tests/test_cli.py tests/test_aggregator.py -q`、品質が対象headソースを別確認 | ✅既存順位 / ❌閾値・併用 |
| REQ-19 | 元total0/正数、部分表示と全除外、空HTML契約 | integration + formatter | `/usr/bin/python3 -m pytest tests/test_cli.py tests/test_formatters.py -q` | ✅既存総数/空部品 / ❌閾値総数 |
| REQ-20 | 全件回帰、再実行の件数/環境、品質本人の全画像/原本配送 | full regression + independent browser/workflow | `/usr/bin/python3 -m pytest`、今回driverは実在化後。実閲覧/配送は人・担当ツールの原本で確認 | ✅suite / ❌今回独立証拠 |
| REQ-21 | 既存境界/escape/CSS不変、README、禁止差分なし | regression + diff/document review | `/usr/bin/python3 -m pytest` と今回基点からの `git diff` 読取り | ✅既存試験 / ❌今回diff・README証拠 |

実閲覧はmanual-only相当（品質本人が画像を開く必要があり自動captureに置換不可）。head/scope、原本配送もpytestだけでは充足しない。[VERIFIED: 04-CONTEXT.md:32–34; docs/wordfreq-html-verification.md:38–40,60,64–79]

### Required Matrix / 独立期待値

以下はPRD掲載scenarioの期待値であり研究時の実行結果ではない。[VERIFIED: .planning/argonauts/r-e476c11d-prd.md:37–70,127–129]

| Input | 条件 | 全形式期待pairs / HTML total |
|---|---|---|
| `beta beta beta alpha gamma alpha delta` | min2/top10 | beta3, alpha2 / total7 |
| 同上 | min2/top1 | beta3 / total7 |
| 同上 | min4 | 空 / total7 |
| `Zoo apple APPLE zoo banana` | min2/top10 | zoo2, apple2 / total5 |
| 同上 | min2/top1、オプション指定順を逆転 | zoo2 / total5 |
| 同上 | min3 | 空 / total5 |
| `Straße STRASSE` | min2 | strasse2 |
| 空・空白・句読点 | 有効N | 空 / total0 |

追加する試験では、未指定/明示1、topよりminが大きい/小さい/等しい、thresholdちょうど、top上限より少ない残件、hashseed違いも区別する。oracleを製品の `top_words` から生成しない。入力失敗は不存在・directory・permission・decodeを全形式N2で確認。不正値/欠落は不存在パスだけでなくread_textが未呼出しであることも直接確認する。[設計提言; VERIFIED: 04-CONTEXT.md:17–30; tests/test_cli.py:503–578]

### Sampling Rate

- task毎: 該当新試験のRED→GREEN（task終了時に存在するnode/fileから実行）、上記quick run。
- wave毎: 上記full suite。任意の別PYTHONHASHSEED再実行は実argv/envを残す。
- phase gate: 全pytestが0件でなく成功し、品質本人の対象head独立ブラウザ・全画像比較・ソース順序・PM可読原本がそろってから正式検証へ渡す。自動継続はしない。

### Wave 0 Gaps

- [ ] 製品変更前baseline用の実入力・全形式bytes/HTML/画像・head/env/argv索引（既存固定casesだけでは不足）。
- [ ] 既存CLI試験へのmin-count matrixと入力取得未呼出しspy。空結果REDが後回しにならない順序。
- [ ] 今回専用の実ファイルdriver（提案）。最小のbaseline保存/比較、ケースargv、AC1〜7索引・scopeを持つ。既存汎用部品を再利用し、新サービス/依存は作らない。
- [ ] 品質の実際のprofile・fresh root・画像閲覧手段とPM原本読取り手段を後工程の開始前に確認する。不能ならgaps。
- [ ] 各PLANに「ファイル作成→存在と収集確認→検証実行」を含め、後続PLANが未着手でもそのPLANの検証が成立するようにする。

## Environment Availability

| Dependency | Required By | 確認結果 | Fallback / 扱い |
|---|---|---|---|
| `python3`（既定PATH） | 汎用実行 | Python3.14.9、`-m pytest --version` は `No module named pytest` | これをpytestコマンドに使わない。 |
| `/usr/bin/python3` + 既存PYTHONPATH | CIと同minorのローカル検証 | Python3.12.15、pytest9.0.3 | 既存guide方式を使用。新install不要。 |
| Playwright CLI | ブラウザ補助 | 同envで `-m playwright --version` → `Version 1.60.0` | CLI存在のみ。起動・実画像・通信は未検証。 |
| Chromium | 描画 | `/usr/bin/chromium-browser --version` → Chromium156.0.8078.73 | 同環境をbaseline/変更後で維持。 |
| locale | 既存encoding試験 | `locale -a` に `en_US.utf8`、`C.utf8`、`en_GB.iso885915` | charmapの実一致は既存試験で改めて確認。 |
| 実効user | permission試験 | `id -u` → 1000 | 実EACCESは後工程の試験で証明する。 |
| jq | JSON抽出 | `/usr/bin/jq` をcommand -vで確認 | JSON原本はread_file、必要項目抽出にjq。 |
| websockets同期API / browser実起動 / 画像閲覧 | verifier部品 | 本研究では起動/import試験しない | 既存環境の実ファイル操作として後工程で確認。不足時installせず未検証で停止。 |

上表の版・実効user・localeは本セッションterminal出力。全件成功や対応版保証ではない。短いTMPDIRが必要なChromium socket制約は既存guideに記載されているので、管理scratchへの短い相対symlinkを使う場合も既存物を上書きせずsystem /tmpへ逃がさない。[VERIFIED: docs/wordfreq-html-verification.md:7–14; tools/verify_wordfreq_html.py:359–387]

## Security Domain

security設定はASVS level1、highでblock。今回はローカルCLIと自己完結静的HTMLであり、新しい認証/サービス層は作らない。[VERIFIED: .planning/config.json:49–51; 04-CONTEXT.md:37]

| ASVS領域（既存テンプレートの区分） | Applies | 今回の制御 |
|---|---|---|
| V2 Authentication | 対象外 | 認証機能追加なし。実profile帰属は検証者識別補助であって認証強度の主張ではない。 |
| V3 Session Management | 製品は対象外 | 検証live sessionの生存と観測区間は証拠契約として維持。 |
| V4 Access Control | 新機能は対象外 | FileSourceのOS読込み失敗をexit1で保持。 |
| V5 Input Validation | 対象 | argparse/int正数、読込み前exit2、basename限定、HTML escape。 |
| V6 Cryptography | 製品は対象外 | 証拠の既存SHA-256は同一性確認だけ、暗号方式を自作しない。 |

適用判断は実構成に基づく研究判断であり、ASVS認証取得や網羅監査を主張しない。[VERIFIED: wordfreq/__main__.py:20–47; wordfreq/sources.py:17–22; wordfreq/formatters.py:17–38; docs/wordfreq-html-verification.md:28]

| Threat Pattern | STRIDE | Standard Mitigation |
|---|---|---|
| 語/basenameのHTML注入 | Tampering | 既存 `escape(value, quote=True)` と独立textノード。formatter直呼びのhostile試験を維持。[VERIFIED: wordfreq/formatters.py:17–19; tests/test_formatters.py:136–161] |
| 親directory情報漏洩 | Information disclosure | CLIのbasename化、全HTMLのpath非埋込み試験。[VERIFIED: wordfreq/__main__.py:35–38; tests/test_cli.py:473–500] |
| 外部通信試行・隠れた遷移 | Information disclosure | 内包CSS/static監査、open前observer、失敗・popupも含む通信原本。遮断を無通信証明にしない。[VERIFIED: tools/verify_wordfreq_html.py:418–553; docs/wordfreq-html-verification.md:105–111] |
| 出力・証拠の帰属偽装 | Repudiation | 対象head/run/root/path/SHA・実profile・原本読取り、未閲覧台帳を作らない。[VERIFIED: CONCEPTS.md:5–15,29–39; 04-CONTEXT.md:32–34] |

## State of the Art / 現行契約と履歴

- 同数時の現行契約は正規化後初出順。旧REQ-04の単語昇順は履歴であり今回へ復帰しない。[VERIFIED: .planning/REQUIREMENTS.md:20,34–38; CONCEPTS.md:49–51]
- 公式 `query init.phase-op 4` は `phase_found=true`、`phase_number="04"`、`has_context=true`、`has_plans=false`、`plan_count=0` を返した。研究開始時点の状態であり、過去STATEの「全phase完了」を今回完了根拠にしない。[VERIFIED: 本セッション公式CLI]
- 公式 `graphify status` は `disabled=true`。今回graphを有効化せず、実ファイルを根拠とした。[VERIFIED: 本セッション公式CLI]
- 研究開始時 `git rev-parse HEAD` は `1106acb0766fb7de446a1bce6382677f923879c7`。statusは既存 `.planning/state.json` 変更とPhase4 `.gitkeep` 未追跡。これを製品変更や受入baseline保存済みと取り違えず、触っていない。[VERIFIED: 本セッションgit出力]

## Assumptions Log

機能・設計について新しい `[ASSUMED]` 要件は追加していない。上記「推奨」「提案」はplanner向け作業設計であり、実装・試験合格の事実ではない。未実行条件は次節へ明示する。

## Open Questions / 後工程の未検証事項

1. **RESOLVED — 今回検証driverの最終path/CLI（計画確定、実装未実施）。** 処置先は04-01-01で `tools/verify_wordfreq_min_count.py` と `tests/test_min_count_verifier.py` を作成、browser-free実ファイルself-test→公式task commit、04-01-02で製品変更前baselineを一度採取/封印。固定公開APIは `--mode baseline|capture|review-session|finalize --role builder|quality --output-dir`、capture/review-sessionは `--baseline-dir` も必須、finalizeはさらに `--review-ledger` 必須、baselineは両者不要。新mode/flagなし。04-03-01にcapture/保存原本validator、04-03-02にreview-session/finalize/実owner publication、両公式task commit後04-03-03にclean head実captureを配置。採取はactionのみ、反復automatedは同test moduleのsaved_baseline/saved_captureへpytest専用root環境変数を束縛してread-only照合（PLANのexact command参照）。旧verifierの汎用部品だけ再利用し、固定scope/head/合格は使わない。未作成コードの試走・製品実行はしていない。
2. **RESOLVED — baseline環境の固定と品質閲覧能力（後工程hard gate、未実証）。** 04-01-02でBuilderが実browser/websockets/font/OS/版/両幅DPR1/通信原本を確認し封印、04-03-03/04-04-01は同環境比較が必須。04-04-02 runbook/independent_quality_gateで品質本人のfresh root/全画像実閲覧とPMの原本読取り能力を開始前確認、保存→標準添付→PM読取りを別gateにする。環境差/能力不足は停止/gaps、版確認を起動/閲覧成功へ昇格しない。
3. **RESOLVED — pytest全件の実件数・所要時間・結果（実測担当とgate確定、未収集/未実行）。** 04-01-01/04-03-01/02/04-04-02のbrowser-free pytestを先行高速feedbackとし、04-01-02 baseline・04-03-03 capture・04-04-01統合・最終品質review-session/finalizeを必須の高遅延full E2E統合gateとして分離する。各実行担当Builder/品質が全suite/browser/閲覧/最終化の実argv/env/正件数/exit/開始終了/所要時間を区別して保存。0件・必須skip・未実施・synthetic-onlyは実原本成功にしない。30秒超を実測したとの主張もしていない。
4. **RESOLVED — 既存CIの対象head結果（後工程担当へ引継ぎ、実run未取得）。** D-12と04-04-01/02の引継ぎに従いPR/CI担当カードが対象最終headの既存CIを有限回確認する。pending/未報告/不調は未達であって成功でない。待機loop・CI追加変更・依存追加を行わず、この計画修正ではCIを確認済みにしない。
5. **RESOLVED — 背景Q-01/Q-02（承認済み非blocker処置）。** D-12と04-04 F5/04-04-02へ対応。Q-01利用背景/Q-02期限とA-01〜04は未提示/未承認のまま非要件として保持し、問いへの架空回答・新仕様・実装追加をしない。この処置は承認済みCONTEXT/OpenSpecの非blocker境界であり、背景が回答済みという意味ではない。[VERIFIED: 04-CONTEXT.md D-12; openspec/changes/r-e476c11d-wordfreq-min-count/design.md:33–35]

## Sources

### Primary / このセッションで読了

- 公式役割 `agents/gsd-phase-researcher.md` と関連reference、GSD公式CLIのinit/agent-skills/graphify/confidence。
- `.planning/phases/04-wordfreq-min-count/04-CONTEXT.md` 全文、`.planning/REQUIREMENTS.md` 全文、`.planning/STATE.md` 全文、`.planning/ROADMAP.md` 全文、`.planning/config.json` 全文。
- `.planning/argonauts/r-e476c11d-prd.md` 全文、同learnings全文、承認OpenSpecの `design.md` 全文。今回の学習は技術/工程への注意点であり、過去head合格の流用ではない。
- 本文で行範囲を示したwordfreq/製品各ファイル、README、CONCEPTS、pyproject、CI、tests、tools、既存HTML検証guide。旧verifierの固定IDsを確認するため実装と試験の両方を照合した。

### Official Documentation / 今回取得・参照

- https://docs.python.org/3.12/library/argparse.html#argparse.ArgumentParser.error — usage errorのstderr/status2。
- https://docs.python.org/3.12/library/collections.html#collections.Counter — mapping/iterable構築と挿入順。
- https://docs.python.org/3.12/howto/sorting.html#sort-stability-and-complex-sorts — 安定sort。

公式文書は取得時Python3.12.16 documentation表示だが、実機は3.12.15と記録する。マイクロ版の一致や全版互換を主張しない。[VERIFIED: 今回web_extract/terminal結果]

## Metadata

- confidence seam: `query classify-confidence --provider local --verified` と `--provider webfetch --verified` はともに `confidence="LOW"`。公式実装は未登録providerをauthority noneへ分類するため、この分類を勝手にHIGHへ書換えない。一次コードの `[VERIFIED: path:lines]` はread_file読了の出典表示であり、seamが実行合格やHIGHを返したという意味ではない。[VERIFIED: 本セッション公式CLI; gsd-core/bin/lib/research-provider.cjs:20–36,46–68]
- research-plan/cache seam: この呼出しは研究原本だけの保存を指定しているため、補助JSON入力や研究storeを書き足すフローは実行していない。新ライブラリ探索は不要で、repo一次情報とPython公式既知URLの直接読取りに限定した。provider利用・cache保存を実施したとは報告しない。
- 公式CLIはglobal defaultsのmodel/runtimeがproject configにより無視される警告を出したが、initはPhase4を返した。設定を書換えて解消しようとはしていない。
- Runtime State Inventoryはrename/refactor/migrationではないため対象外。既存stateの修正や過去phaseの再計画は行わない。
- 有効期限は依存の暦日よりrepo head・承認spec・環境の変更で判断する。headが動けば計画前に該当ソースと検証環境を再確認する。
- 本研究の作成物はこのRESEARCH原本のみ。製品、新検証コード、baseline、受入証拠の生成、commit/push、Kanban、自動継続は実施していない。
