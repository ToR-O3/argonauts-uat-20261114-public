# Phase 5: README validation B - Pattern Map

**Mapped:** 2026-11-22
**Files analyzed:** 5（製品1、工程記録4。CLI証拠の保存先は未確定）
**Analogs found:** 5 / 5（exact 1、role-match 4）

## Scope and Extraction

- CONTEXT:15-22とRESEARCH:28,46-48,71-73,140-146から抽出。製品の変更先は `README.md` だけで、指定の独立した最終行を1回追加する。
- 工程側は単一PLANのSUMMARY、phaseのVERIFICATION、CLI証拠文書、および既存 `05-VALIDATION.md` の実行後判定更新を区別する。SUMMARY名はRESEARCHの単一PLAN推奨からの推定であり、CLI証拠の保存先はBuilder/品質の工程で確定する。以下の `<担当工程>` は説明用で実在パスではない。
- CONTEXTのCanonical Referencesは参照入力であり、一括変更リストではない。CONTEXT/RESEARCH/PATTERNS/将来のPLANは計画成果物で、製品編集や実行証拠と混同しない。OpenSpec sync/archiveは後続の最終化工程であり、このマッピングから実装taskを増やさない。
- コード・試験・新規スクリプト・validator・fixture・依存の変更はなし。文書の役割をcontroller/serviceなどへ無理に分類せず、documentation / process-recordとする。imports/auth/runtime error handlingは対象外。

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `README.md`（変更） | documentation（製品説明） | file-I/O: 既存文書 → 局所追記 → 読取 | `README.md`:28-34 | exact（同一文書・同一書式） |
| `.planning/phases/05-readme-validation-b/05-01-SUMMARY.md`（単一PLANなら新規） | process-record（Builder報告） | batch / file-I/O: 実変更・実CLI → 実装報告 | `.planning/phases/04-wordfreq-min-count/04-04-SUMMARY.md`:62-73,99-117 | role-match |
| `.planning/phases/05-readme-validation-b/05-VERIFICATION.md`（新規） | process-record（独立phase検証） | batch / transform: 対象head・証拠 → 条件別判定 | `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md`:40-45,60-68,142-152 | role-match |
| CLI証拠文書（例 `.planning/argonauts/<担当工程>/cli-evidence.md`、保存先未確定） | process-record（CLI一次結果） | batch / file-I/O: argv・stdout/stderr・exit → 文字証拠 | `.planning/argonauts/t_c9dd351a/cli-evidence.md`:1-8 | role-match |
| `.planning/phases/05-readme-validation-b/05-VALIDATION.md`（既存draftの実行後更新） | process-record（検証戦略・判定索引） | transform: 実行証拠 → sampling/sign-off状態 | `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md`:129-152 | role-match（判定表の形のみ） |

## Pattern Assignments

### `README.md` — 既存末尾を保持する局所編集

**Analog:** `README.md`:28-34。同一ファイルの既存書式が最も近い。独立した検証B行の前例はなく、追加文言は類似機能の説明から生成せず、承認原文に従う。

既存の末尾側の短い段落例（30行）:

```markdown
`count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。
```

最後の段落（34行）は「自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。」で始まる既存説明。その行を変更せず、直後の最終行に承認原文だけを置く。

```text
検証B: v1.12 の通しの確かめ（2026-11-22）
```

- 見出し、箇条書き、引用符、コードフェンス、追加説明、余分な空行は付けない。
- 本文・書式・改行形式を保持する。read_file表示だけからCRLF/LFや末尾LFのバイト状態を断定しない。
- 34行に書かれた過去の試験・ブラウザgateを今回のREQ-22へ移植しない。指定行そのものも検証合格の証拠ではない。

### `05-01-SUMMARY.md` — Builder実施と独立受入を分離

**Analog:** `.planning/phases/04-wordfreq-min-count/04-04-SUMMARY.md`:62-73,99-117。

実行記録への導入（71-73行）:

```markdown
## Actual execution, environment and results

All commands repo-root, `/usr/bin/python3` 3.12.15, pytest9.0.3, PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages, WSL2 Linux6.18.58.1, Chromium156.0.8078.73. Actual per-command logs under `.planning/argonauts/t_e22f75a9/run154/`.
```

合格状態の誤解を防ぐ記載（105行）:

```text
Requirements-completed frontmatter copies the PLAN IDs per official template; it is an implementation coverage index, NOT independent AC acceptance. Do not use it to close OpenSpec2.2 or PM acceptance.
```

継承するのは「実変更範囲」「実コマンドと結果への参照」「未実施gate」「問題の明記」の構造だけ。過去の環境値、SHA、試験件数、commit工程、画像、archive方式はコピーしない。今回はREADME指定1行の編集と直接CLI確認の報告で十分。Builder完了を独立品質・PM受入へ昇格させない。

### `05-VERIFICATION.md` — 対象headとREQ-22の条件別判定

**Analog:** `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md`:40-45,60-68,142-152。

対象状態と未実施の区別（43-45行）:

```markdown
**Verified:** 2026-11-18T03:30:00Z (target head `afaa56fc022c895ee2243b8f67a239c7c0096086`)
**Status:** human_needed
**Re-verification:** No. This is the initial verification (no earlier 04-VERIFICATION.md).
```

要件索引の見出し（142-145行）:

```markdown
### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
```

今回は実測した固定基底SHA・対象head、実コマンドの証拠文書を明示し、REQ-22の最終行完全一致／出現1回／既存保持と追加1削除0／製品変更READMEのみを個別判定する。未実行・失敗・未確認は合格にしない。画像閲覧0枚・UI変更なしと明記し、文字証拠を標準添付する。過去ファイルはfrontmatterのpassedと本文のhuman_neededが異なるため、判定値をそのまま複製しない。今回の公式工程の形式と実結果に整合させる。

### CLI証拠文書 — 文字で追跡できるコマンド・結果表

**Analog:** `.planning/argonauts/t_c9dd351a/cli-evidence.md`:1-8。

表の構造（5-6行）:

```markdown
| # | command (suffix after the interpreter prefix) | exit | result |
|---|---|---|---|
```

同ファイル3行はchecked head、actor、cwd、環境を明示する。継承するのは対象を特定してコマンドと終了値と結果を一緒に残す方法。今回は省略されたsuffixではなく、置換済みの実argv、固定基底、対象head、stdout、stderr、exit、手動の期待値照合結果を残す。実行エラーと不一致を分ける。保存先は実行担当の工程領域に定め、過去カードの証拠を上書きしない。

RESEARCH:95-115のtail/grep/Git例は未実行の提案であり、このマッピングでは試行していない。既存 `README.md` を直接読むCLIを使い、新しい検証ファイルは参照・作成しない。grepのexit0やdiffのexit0だけで期待条件成立とはしない。README全体の一致文字列1件は完全行数と文字列一致出力を両方読み、numstatと実patchも両方読む。

### `05-VALIDATION.md` — draftと実行済みを区別する索引

**Analog:** `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md`:129-152。検証コマンド・結果・判定と要件索引を併置する形だけを再利用する。

```markdown
### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
```

現行 `05-VALIDATION.md`:1-8,28-56はstatus=draft、nyquist_compliant=false、実task pending、Approval pending。実行前にチェック済みへ変えない。実行後に実証拠への参照と確認結果で更新し、Wave 0のtest/script作成を追加しない。今回読んだdraftは工程入力であり、git追跡済みanalogとしては採用していない。

## Shared Patterns

1. **製品と工程の分離:** 製品はREADMEの指定1行のみ。工程記録の例外はパス単位で分類し、Markdown全体やdocs全体を除外しない。全変更一覧と未追跡も確認する。
2. **基底と対象の固定:** Builderの編集前基底と品質の検証headを分け、報告文書追加後のheadを過去の検証headと取り違えない。未来のSHAは書かない。
3. **実行証拠と判定の分離:** コマンド、出力、stderr、exit、期待値、条件別判定を文字で記録する。新規assertプログラムや試験は不要かつ範囲外。
4. **gateの分離:** Builder確認、独立品質、phase検証、PM受入、最終化を別状態で記す。以前のphaseのpass件数や未決gateはREQ-22へ流用しない。
5. **既存資料の限定利用:** 上記analogは構造の手本だけ。新規スクリプト、pytest全件、ブラウザ、画像や圧縮ファイルの閲覧要件は追加しない。GSDの状態判定が必要な後工程は公式CLIを使い、独自parserを作らない。

## No Analog Found

分類した5対象には書式または工程記録の類似例がある。ただし「指定の検証B行」の既存例はない。文言と最終行・1回・差分1行の条件はCONTEXT:15-18の承認原文に従う。CLI証拠の将来の正確な保存先は未確定であり、存在すると主張しない。

## Metadata

- Analog search scope: `README.md`、`.planning/phases/04-wordfreq-min-count/`、`.planning/argonauts/`。強い類似元4ファイルで探索を終了。
- 全analogは `git ls-files -- <path>` で追跡済みと確認。インストールmirrorは使っていない。
- 読取り入力: 公式gsd-pattern-mapper役割全文、05-CONTEXT、05-RESEARCH、README、過去SUMMARY/VERIFICATION/CLI証拠、既存05-VALIDATION。
- ルートHERMES.md、`.hermes/skills/`、`.agents/skills/` は見つからず。追加のローカル規則を推定していない。
- この作業ではGSDの新しい状態判定は行っていない。RESEARCHにある公式CLI結果を実行し直したとは主張しない。
- 作業前から `.planning/state.json` に変更、Phase 05の `.gitkeep`、RESEARCH、VALIDATIONに未追跡があった。触れていない。
- 本作業の書込みは `05-PATTERNS.md` のみ。README編集・試験実行・製品受入検証・新規スクリプト・commit/push/kanban操作はなし。
