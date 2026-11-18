# Phase 04: wordfreq min-count - Pattern Map

**Mapped:** 2026-11-18 JST
**Files analyzed:** 最小編集案5ファイル（新規driverとその試験のpathは提案、plannerが確定）
**Analogs found:** 内容・役割の対応5 / 5。tracked-source gateは未確認（下記制限）。実装・試験・受入の完了を意味しない。

## Scope and Evidence Status

- 公式 `gsd-pattern-mapper.md` 全文→`04-CONTEXT.md`→`04-RESEARCH.md`を読了し、以下の現物を照合した。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/gsd-core/bin/gsd-tools.cjs query init.phase-op 4` はexit0、`phase_found=true`、`phase_number="04"`、`has_context=true`、`has_research=true`、`has_plans=false`、`plan_count=0`。global defaultsのmodel/runtime無視警告あり。設定は変更しない。
- `HERMES.md`、`.hermes/skills/`、`.agents/skills/` は不存在。追加agent-skillsの取得・追加は行っていない。
- **Tracked-source gateの制限:** 今回はGit操作禁止のため、公式役割が要求する `git ls-files -- <analog>` を実行していない。以下はrepo内の現物に基づく**候補対応**であり、tracked確認済みとは主張しない。install/runtime mirrorをanalogに使用していない。plannerはGit読取りが許可される工程で各analogのtracked所属を確認し、未確認のままgate完了扱いしない。
- この調査で書くのは本PATTERNS.mdだけ。baseline採取、pytest収集/実行、browser起動/閲覧、scope合格、CI、配送は未実施。未作成検証コマンドの試走なし。下記の引用は実行結果ではない。

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `wordfreq/__main__.py`（変更） | controller / composition | argv→file-I/O→transform→stdout | 同ファイルの`--top`検証と共通pairs合成 | exact（自己類似） |
| `tests/test_cli.py`（変更） | test | subprocess request-response / file-I/O | 同ファイルの全形式bytes matrix・usage/input失敗・monkeypatch | exact（自己類似） |
| `README.md`（最小変更） | documentation | CLI使用契約→利用者説明 | 同ファイル18–30行のtop/形式/順序/総数/エラー説明 | exact（自己類似） |
| `tools/verify_wordfreq_min_count.py`（新規提案・未実在） | utility / verification driver | batch / file-I/O / browser event-driven | `tools/verify_wordfreq_html.py`の汎用採取・監査部品 | role-match、Phase4 orchestrationは新規 |
| `tests/test_min_count_verifier.py`（新規提案・未実在） | test | deterministic transform / subprocess / file-I/O | `tests/test_html_verifier.py`の実ファイルimport・欠落拒否試験 | role-match、今回baseline/AC/scopeは新規 |

新規pathはこの調査時点の `tools` / `tests` の `*min*count*` 検索に該当なし。実在コマンドとして引用しない。driverを採用するなら製品変更前baselineを採れる段階で作成・試験する。別サービス、依存追加、CI編集、旧verifier全面改修は提案しない。

### 調査に現れるが変更不要を基本とするファイル

| File | Role / Data Flow | 今回の位置付け・最寄り現物 |
|---|---|---|
| `wordfreq/aggregator.py` | utility / transform | 既存`top_words(counts, n)`をそのまま使用。11–17行の安定sortを保持。 |
| `wordfreq/formatters.py` | utility / transform | 全形式の公開引数・HTML/CSS/空文言を維持。6–38行が共通pairs/空結果の既存受け皿。 |
| `wordfreq/sources.py`、`wordfreq/tokenizer.py` | provider / file-I/O、utility / transform | RESEARCHの保護対象。今回新たな変更先にしない。本文の直接引用には使っていない。 |
| `tests/test_aggregator.py` | test / transform | 17–46行の非破壊・初出順試験を維持。CLIのfilter非破壊はCLI試験側でspy等により追加でき、集計API拡張不要。 |
| `tests/test_sources_boundary.py` | test / file-I/O boundary | 7–17行のspyをCLI新試験へ移す候補。元ファイル変更は必須でない。 |
| `tests/test_formatters.py` | test / transform | 94–175行の静的安全性・空HTML、218–262行の固定CSS回帰を維持。min-count専用formatter試験のために製品APIを変えない。 |
| `tools/verify_wordfreq_html.py`、`tools/wordfreq_html_geometry.js` | utility / event-driven、transform | 読取り・import再利用元。旧固定scope/ケース/ACの置換先ではない。 |
| `tests/test_html_verifier.py`、`tests/test_html_finalization.py` | test / evidence lifecycle | 旧契約の既存回帰を保持。旧期待値の機械置換で今回を合格にしない。後者はRESEARCH参照のみ。 |
| `docs/wordfreq-html-verification.md` | documentation / verification workflow | 既存の原本・実閲覧・通信契約の参照元。旧scope/AC/起動例をPhase4受入コマンドとしてコピーしない。新driverの使用法はplannerが今回成果物の中で確定し、既存guide全面変更は避ける。 |

この表は保護対象・参照部品であり、5ファイルの変更件数には含めない。plannerが試験の分割先を変更する場合は役割と所有pathを明示する。

## Pattern Assignments

### `wordfreq/__main__.py` — 引数から共通pairsまで

**Analog:** 同ファイル。標準ライブラリimports→相対部品imports（2–9行）。認証/DB/middlewareは対象外。

**引数・失敗の最寄り原文**（15行、20–29行、別箇所を連記）:

```python
parser.add_argument("--top", type=int, default=10)

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    try:
        text = FileSource(args.filename).read_text()
    except InputError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
```

**適用:** `--min-count`もargparse/int・既定1、正数検証を入力取得前へ置く。0/負数はparser.error、非整数/非数値/欠落は既存argparseへ任せる。独自の字句規則やtopとの大小制約を加えない。有効N>1の読込み失敗は既存exit1。HTML専用の失敗処理を追加しない。

**共通合成の原文**（30–32行）:

```python
counts = count_words(iter_tokens(text))
total = sum(counts.values())
pairs = top_words(counts, args.top)
```

**順位部品の原文**（`wordfreq/aggregator.py:11–17`）:

```python
def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    """Rank by descending count, preserving insertion order for ties.

    Callers must supply counts in normalized first-occurrence order.
    Stable sorting happens before limiting; counts are not mutated.
    """
    return sorted(counts.items(), key=lambda wc: -wc[1])[:n]
```

**適用:** 元Counterとtotalを保持→元itemsの順で`count >= min_count`の別mapping/Counter→既存top_words→同じpairsを3形式へ渡す。Counterへタプル列をトークン列として渡さない。set化・語の昇順キーは禁止。二引数top_words、basename化、HTML UTF-8出力（main35–47行）は維持。品質は変更後のフィルタ位置→top呼出しのソース行を記録し、出力一致だけで内部順序の証明にしない。

### `tests/test_cli.py` — 実CLIと境界spy

**Analog:** 同ファイル。importsは2–11行の標準ライブラリ+pytest、ROOTは13行。新framework不要。

**実bytes subprocess**（418–422行）:

```python
def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
```

**全形式の既存matrix内での照合**（467–472行）:

```python
args = [path, "--format", output_format]
if top is not None:
    args += ["--top", top]
result = run_cli_bytes(*args)
assert (result.returncode, result.stderr) == (0, b"")
assert_output_bytes(result.stdout, output_format, expected, path.name, total)
```

**適用:** `assert_output_bytes`（425–441行）とCLIHTML（201–239行）を再利用。期待pairs/totalはliteral、製品のtop_wordsから算出しない。閾値未満/ちょうど/超、Unicode casefold、初出順、独立topと指定順、未指定/明示1、空/空白/句読点/全除外を3形式へ展開。例はbeta3/alpha2/元total7、全除外[]/元total7、Zoo→zoo2,apple2/元total5、Straße→strasse2。既定互換は変更前保存原本との比較も別途必要。

**入力未取得spyの部品**（`tests/test_sources_boundary.py:7–17`）:

```python
def test_aggregation_does_not_acquire_files(monkeypatch):
    calls = []
    original = FileSource.read_text

    def spy(source):
        calls.append(source)
        return original(source)

    monkeypatch.setattr(FileSource, "read_text", spy)
    assert count_words(iter_tokens("Hello hello WORLD")) == {"hello": 2, "world": 1}
    assert calls == []
```

**適用:** このspy形式をCLI main呼出しに使い、不正min-countでread_text未呼出しを直接検証。SystemExit/capsysの形式はtest_cli549–561行。実subprocess usage matrix（530–545行）も拡張しexit2/stdout空/stderr/Tracebackなしを確認。読込み失敗matrix（503–527行）へ有効N2を追加し、permissionは同実効userで実PermissionErrorを証明する。skipを成功にしない。

**非破壊oracle**（`tests/test_aggregator.py:20–24`）:

```python
counts = Counter({"zoo": 5, "rare": 1, "middle": 3, "apple": 5})
original = counts.copy()
assert aggregator.top_words(counts, 3) == [("zoo", 5), ("apple", 5), ("middle", 3)]
assert counts == original
assert list(counts.items()) == list(original.items())
```

値だけでなくitems順も検査する。CLI側の集計/選択境界をspyし元Counter非破壊を検査する場合にもこの二重比較を使う。空結果試験は共通フィルタ実装前に追加し、後付けREDを捏造しない。

### `README.md` — CLI契約の短い追記

**Analog原文**（18行、22行の別箇所）:

```text
- `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
- HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
```

**適用:** 既存実行例9–14行と箇条書きへmin-count指定/既定1/exit2/先min後top/元総数/全除外は閾値を下げる案内だけを加える。22行と30行の「top前」はmin-count前でもあることを明記。順序21行の初出順を維持。旧ブラウザguideへのリンクを壊さず、旧guideを今回合格の根拠にしない。背景・期限・新要件は創作しない。

### `tools/verify_wordfreq_min_count.py` — 新規提案driver

**Analog:** `tools/verify_wordfreq_html.py`。imports5–22行は標準ライブラリ、browser importは操作内（687行等）の遅延方式。旧moduleはmain guardがある（1407–1408行）。汎用部品だけを通常のmodule importまたは実ファイルloaderで使い、旧定数をmonkeypatchして旧受入を通す設計は採らない。

**独立oracle・原本記録の最寄り原文**（32–34行、127–132行、別箇所）:

```python
def add(name, basename, body, pairs, total, top=10, fmt="html"):
    cases.append(dict(id=name, basename=basename, body=body, pairs=pairs,
                      total=total, top=top, format=fmt))

record = dict(case, input=str(source), basename_repr=repr(case["basename"]),
              argv=argv, cwd=str(ROOT), executable=sys.executable,
              environment={key: env[key] for key in ("PYTHONIOENCODING", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
              exit=result.returncode, stdout=str(stdout), stderr=str(stderr), views=[])
records.append(record)
save_json(folder / "cli.json", record)
```

このschemaと保存方式を参考に、今回driverがmin-count argv・全形式baseline/比較・今回ケースを所有する。**旧generate_casesをそのまま呼んでも今回ケースは生成されない。** baselineでは製品にmin-countを渡さず、最初の製品変更前に同数かつ10種類超の同一入力・basenameで全形式bytes/HTML/両幅画像を保存。post-changeでは未指定/明示1をその原本と比較する。driver準備変更自体のhead/provenanceも隠さず記録する。

**ブラウザ採取の原文**（586–592行）:

```python
def collect_view(browser, case, width, output, live=None):
    folder = output / case["id"] / str(width)
    folder.mkdir(parents=True)
    context = browser.new_context(viewport=dict(width=width, height=900), device_scale_factor=1)
    observer = Observer(browser, context)
    page = context.new_page()
    cdp = observer.attach(page)
```

**再利用部品と呼出し条件:**

| Component / 現物行 | 再利用できる責務 | 今回driver側の責務・注意 |
|---|---|---|
| `Document` 67–107 | タグ/属性/CSS資源監査 | 今回stdoutのstrict UTF-8、basename/総数/3列/親path不在を今回oracleで確認。 |
| `geometry_errors` 157–221 | raw文字/clip/viewport/重複の派生検査 | rawをclamp/丸め/削除しない。 |
| `png_size` 224–234、`digest` 903–904 | PNG実寸・bytes同一性 | 実在原本のpath/SHAを今回索引へ。 |
| `Observer` 418–480、`network_errors` 506–553 | open前observer・失敗/未知帰属も拒否 | 期待file URLのみ。許可URL拡大や遮断を無通信証明にしない。 |
| `collect_view` 586–671、geometry JS 28–67 | 任意caseのraw/fonts/full/tile/network採取 | caseにはid/stdout/basename/pairs/totalが必要。`long` idには固有wrap検査（dom_errors573–582）がある。今回case IDを安易に使い回さない。 |
| `review_errors` 875–896 | actor/path/hash/実閲覧時刻/尺度/全域/notes検査 | 実際に品質が開いた後だけ台帳記入。未閲覧を自動readableにしない。 |
| `image_coverage_errors` 937–952、`view_identity_errors` 955–962 | 全域tile/raw・画像同一性 | 今回manifestで各viewへ適用。画像存在だけでは閲覧の証明にならない。 |

collect_viewはnavigation前のscrollbar条件（609行）から測定・撮影・閲覧まで同layoutを保つ。`live`を渡さない場合contextは採取後に閉じる（661–667行）。したがって通常captureだけではlive独立閲覧を満たさない。今回の品質orchestrationがlive保持・flush・終了時再照合を所有する必要があり、旧review-sessionの実行で代用しない。通信canaryの観測/拒否方式（716–801行）は保持し、実行時のhead/roleを今回証拠へ結ぶ。

**そのまま流用禁止:**

| Old component | 理由 / 今回必要なもの |
|---|---|
| fixed_cases28–53 / generate_cases110–154 / capture_errors237–262 | 閾値ケースなし、completenessも旧固定ケース依存。今回matrixと欠落拒否を別所有。 |
| SCOPE_BASE806 / APPROVED_PRODUCT807 / scope_report827–862 | 旧基点`5a7659b949dc118b59cea5ef3eb40bcd94337d8d`と旧snapshot`ed7e6cc9d608bc40a82da76e85ca6e57a0808b54`。今回実装前head/対象headを今回scopeで扱い、旧定数の黙示置換・旧合格流用禁止。 |
| scope_path_errors818–824 | Phase3のallow-list。今回所有pathと禁止差分を別に列挙。 |
| ledger_errors907–934 / ac_index1032–1035 / final判定1124–1127 | 旧AC1〜6。今回AC1〜7=REQ-15〜21の対応を別所有。 |
| evidence_errors965–1029 / review_session1216–1326 / finalize1329–1347 | 旧scope/cases/ACへ推移的に依存。汎用関数を組み合わせても旧gateを今回合格装置にしない。 |

今回品質は既定・部分表示・top併用・全除外・空を1280×900/320×900 DPR1で自ら再生成・実閲覧。同環境baseline比較とソース順序確認をAC1/2/4/5/6/7へ結ぶ。AC3の自動境界証拠も含め全AC索引が必要。保存・標準添付・PM原本読取りは別gateで、head/run/root/path/SHAを保持。能力不足・拒否は迂回せずgaps。

### `tests/test_min_count_verifier.py` — 新規提案driverの拒否回帰

**Analog:** `tests/test_html_verifier.py:14–20`。

```python
def verifier():
    path = ROOT / "tools/verify_wordfreq_html.py"
    assert path.is_file(), "real-file collector is required"
    spec = importlib.util.spec_from_file_location("html_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

**適用:** 実在ファイルをimportしbrowser不要のpredicate試験を先に実行可能にする。新path/CLIが存在するまで起動しない。旧fixture数15（26行）、旧scope IDs（629–630行）、旧AC range（779–781行）はコピーしない。

**欠落・原本改変拒否の最寄り原文**（1009–1016行）:

```python
view = dict(raw=str(raw), raw_sha256=v.digest(raw),
            images=[dict(path=str(image), sha256=v.digest(image))])
assert v.view_identity_errors(view) == []
view["raw_sha256"] = "false"
assert v.view_identity_errors(view)
view["raw_sha256"] = v.digest(raw)
image.write_bytes(b"stale image")
assert v.view_identity_errors(view)
```

今回追加する拒否観点: baseline欠落/変更後baselineによる代用、全形式または幅欠落、min-count case欠落、AC7欠落、head/root/path/SHA不一致、元total誤り、0件suite、未閲覧台帳、scope取得失敗をclean扱い。browser-free synthetic試験の成功と実ブラウザ/品質受入は分ける。旧suiteは改変せず全件回帰へ残す。

## Shared Patterns

### Pure formatter / 元totalを呼出し側が所有

`wordfreq/formatters.py:6–14` はtext空文字とJSON末尾改行を既に所有する。HTML22–38行は渡されたpairsだけを描画し、空pairsの既存文言を使う。HTML totalは呼出し側から渡す。CLI・試験・driver共通で元Counterと表示pairsを区別し、空入力total0と語あり全除外total正を混同しない。CSS/文言/HTML公開契約は変更しない。

### TDD・検証実ファイル・原本

1. baseline用driver/試験が必要なら先に準備し、製品未変更時点の原本を保存。保存不能なら製品変更へ進めない。
2. tasks1.2/1.3/1.4は試験先行RED→最小実装→GREEN。空・総数の新試験は選択実装前に置き、既存GREEN項目はGREENと正直に記録。
3. PLANの検証はそのtask終了時点で実在するfile/nodeをBuilderが確認してから実行。後続PLANの新driverに依存して現PLANを検証不能にしない。
4. 現存する全suiteの参照コマンドはguide19行の `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`。本調査では未実行。環境・実件数・exit・stdout/stderrをBuilder/品質が保存し0件を成功にしない。
5. 品質の独立CLI再実行・全画像実閲覧・ソース確認・配送はBuilderの自己承認へ移さない。CIは有限回の後工程確認、pending/未報告を成功と呼ばない。

## No Analog Found

完全に同じ機能のanalogはない項目:

| Capability | Role / Data Flow | Gap / plannerへの引継ぎ |
|---|---|---|
| min-count CLI filter | controller / transform | 現行mainには閾値なし。既存top検証とCounter/安定sortを組み合わせ、承認design15–18行へ従う。 |
| 製品変更前の全形式baseline→未指定/明示1の同環境bytes/画像比較 | verification / file-I/O | 旧verifierに今回比較modeなし。今回driver内に最小の新規orchestrationが必要。 |
| Phase4 scope・AC1〜7・REQ-15〜21・原本配送の今回索引 | verification / workflow | 旧scope/ACは非互換。今回実headと担当証拠で作成し、過去合格を流用しない。 |

ファイル単位では全5件に内容上のanalogがあるが、上記新規責務まで既存実装済みとは数えない。

## Metadata

- Analog search scope: repo `wordfreq/`、`tests/`、`tools/`、`README.md`、`docs/`、承認OpenSpec design。主analogは分類表の5対応で打切り、周辺ファイルは境界確認のみ。
- Pattern extraction date: terminal `date --iso-8601=seconds` → `2026-11-18T06:42:03+09:00`。
- 根拠: required reading全文、本書で直接引用した製品・試験・verifier・geometry・guide・designのread_file結果。RESEARCHだけの参照はその旨を明記した。
- Outstanding: tracked-source gate未確認（Git操作禁止）、今回driverの最終path/CLI、baseline・TDD・全件回帰・browser/画像比較・独立品質・配送は後工程。GSD状態確認は計画可能なPhase4の存在を示すだけで、これらの完了を示さない。
- 本調査はPATTERNS.mdのみ作成。製品/検証コード/PLAN/設定/skills、Git/Kanbanは変更・操作していない。
