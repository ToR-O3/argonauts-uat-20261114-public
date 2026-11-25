# Phase 08: wordfreq HTML displayed types - Pattern Map

**Mapped:** 2026-11-26
**Files analyzed:** 下表の製品・試験・検証補助・証拠出力候補（未確定名は明記）
**Analogs found:** 全候補に既存の部分/同役割analogあり。ただし今回用の完成済browser受入driverとHTML限定期待値adapterは存在を確認できていない。
**Scope:** pattern mapperのみ。製品変更・試験実行・browser起動・Kanban・commit/pushは実施していない。

## File Classification

CONTEXT D-01〜06、RESEARCHのRegression Contact Map / Validation Architectureから抽出。新規名はplannerの決定対象であり、実在する実行ファイル・コマンドとして扱わない。

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `wordfreq/formatters.py` | utility / static component | transform: final pairs → HTML | 同ファイル `format_html` | exact |
| `tests/test_formatters.py` | test | transform → strict DOM/CSS assertions | 同ファイル `HTMLDocument`, hostile/empty/CSS試験 | exact |
| `tests/test_cli.py` | test | file-I/O / request-response subprocess | 同ファイル metadata/max matrix/saved bytes | exact |
| `README.md` | documentation | CLI契約 → 利用者向け説明 | 同ファイル HTML説明 | exact |
| `tests/test_max_count_verifier.py` | test | file-I/O / subprocess / sealed evidence validation | 同ファイル `collected_capture` とsaved integrity試験 | exact |
| `tools/verify_wordfreq_max_count.py`（current互換接点が必要な場合だけ） | utility / verifier | file-I/O / batch / subprocess | 同ファイル collect/validateのoracle接点 | exact、変更範囲限定 |
| 今回専用HTML期待値adapter/fixture（新規path未定。既存tests内helperも可） | test utility | transform: sealed bytes → current expected bytes | `tests/test_cli.py` saved-byte tests、max verifierのliteral oracle | partial：承認差分変換自体は未実装 |
| 今回専用browser/CLI検証ファイル（新規path未定） | utility / verifier | file-I/O / batch / event-driven browser | `tools/verify_wordfreq_html.py` の `collect_view` | role-match：下層のみ再利用 |
| 今回専用verifier回帰試験（新規path未定） | test | file-I/O / batch / rejection assertions | `tests/test_max_count_verifier.py` | role-match：画像免除は継承不可 |
| `tools/wordfreq_html_geometry.js`（共通collectorを拡張する場合だけ） | utility | browser DOM → raw geometry transform | 同ファイル targets / Range / dom | exact、legacy読み出し契約維持 |
| 今回専用検証手順（新規path未定） | documentation / config | operator → independent verification workflow | `docs/wordfreq-html-verification.md` | role-match：旧head/scope/件数は非互換 |
| 今回用変更前/変更後CLI・browser証拠、RED/GREEN/full suiteログ、品質 `VERIFICATION.md` / CLI・CI文字証拠（`.planning/argonauts/r-6ae2cbf2/` 下等、詳細path未定） | evidence / test output | file-I/O / batch / event-driven | max verifierのfresh-root/provenance/seal、HTML検証手順 | role-match：新依頼・新head・実画像を記録 |

### Read-only dependencies / 非変更対象

- `wordfreq/__main__.py` はfinal pairs/元totalの供給元。変更不要。
- `tools/verify_wordfreq_html.py` は下層analog。旧高層driver全体を今回の受入として実行しない。共有変更を選ぶならplannerがfiles_modifiedへ理由付き追加する。
- RESEARCHに挙がる `tools/verify_wordfreq_min_count.py` / `tests/test_min_count_verifier.py` はlegacy接点・integrityの保持対象。今回mapperでは原文を追加読取りしていないため、そこから新たな抜粋を作っていない。
- 過去Phase4/7のCONTEXT、封印baseline、保存済capture/RED、旧scope hash/allow-listを更新対象にしない。`.planning/INGEST-CONFLICTS.md` はPMへの添付対象であり、書換えによる製品判断の解消はしない。

## Pattern Assignments

### `wordfreq/formatters.py` (utility, transform)

**Analog:** 同ファイル。公開署名とpure formattingをそのまま使う。

**Imports / encoding pattern — lines 2–3,17–19:**
```python
import json
from html import escape

def _html_text(value: str) -> str:
    """Escape once, protecting CR from HTML's input newline normalization."""
    return escape(value, quote=True).replace("\r", "&#13;")
```

**Core pattern — lines 22–32:**
```python
def format_html(pairs: list[tuple[str, int]], basename: str, total: int) -> str:
    """Render ordered pairs and caller-supplied metadata as escaped text only.

    No I/O, counting or sorting occurs here. The caller supplies a basename
    (never a full path) and the total before limiting the displayed pairs.
    """
    rows = "".join(
        f'<tr><td class="rank">{_html_text(str(rank))}</td>'
        f'<td class="word">{_html_text(word)}</td>'
        f'<td class="count">{_html_text(str(count))}</td></tr>\n'
        for rank, (word, count) in enumerate(pairs, 1)
    )
```

**DOM/CSS seam:** lines 71–85のmetadata stylesと113–117の総数区画に局所追加。現在の独立leafは次のとおり（lines 113–116）。
```python
<div class="metadata-item">
<div class="label">総出現回数</div>
<div class="total-value">''' + _html_text(str(total)) + '''</div>
</div>
```

**Apply:** `len(pairs)` を表示する独立leafと局所wrapperを追加する。`.total-value` のtextは元totalだけのまま。新class名は未定。divを使えば既存tag allow-listを広げずに済む。既存wrap・palette・表を保持し、UI-SPECに従う最小局所layoutだけを許可する。tokenize/filter/top/ソートは追加しない。formatterにI/O、例外握り潰し、認証機構を持ち込まない。

### `tests/test_formatters.py` (test, transform assertions)

**Analog:** 同ファイル。標準 `HTMLParser` とnode ancestryで静的安全性・構造を厳密に確認する。importsはlines 2–6（importlib/json/HTMLParser/re）、製品関数のimportは各test内。

**Tree/leaf pattern — lines 66–72,90–91:**
```python
    def handle_starttag(self, tag, attrs):
        assert len(attrs) == len(dict(attrs)), "duplicate attributes"
        node = {"tag": tag, "attrs": dict(attrs), "text": "",
                "ancestors": list(self.stack)}
        self.nodes.append(node)
        if tag != "meta":
            self.stack.append(node)

    def classified(self, name):
        return [node for node in self.nodes if node["attrs"].get("class") == name]
```

**Safety pattern — lines 103–109:**
```python
    classes = {"metadata", "metadata-item", "label", "filename-value",
               "total-value", "rank", "word", "count", "empty-message"}
    for node in document.nodes:
        assert node["tag"] in allowed
        assert set(node["attrs"]) <= allowed[node["tag"]]
        if "class" in node["attrs"]:
            assert node["attrs"]["class"] in classes
```

**Apply:** 新文言・N・単独total・同一局所区画・table前・final行数を先にassertしてREDを採る。既存class集合には実装したclassだけ追加。hostile test（136–161）の未ソートpairs/引数不変/一度escape、empty test（164–178）のheaderのみ、CR test（181–195）を残す。CSSは218–262の完全辞書一致を局所rule分だけ更新し、262のclip/ellipsis/nowrap/縮小等の禁止を維持する。parser構造試験を横配置の描画合格と呼ばない。

### `tests/test_cli.py` (test, real file/subprocess)

**Analog:** 同ファイル。`tmp_path`入力、literal期待pairs/total、実subprocessのraw bytesを用いる。

**Execution pattern — lines 418–422:**
```python
def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
```

**Matrix pattern — lines 860–866,877–886:**
```python
@pytest.mark.parametrize("content,minimum,maximum,top,expected,total", [
    (MAX_NORMAL, 1, 2, None, [("alpha", 2), ("gamma", 1), ("delta", 1)], 7),
    (MAX_NORMAL, 1, 1, 3, [("gamma", 1), ("delta", 1)], 7),
    (MAX_NORMAL, 2, 2, None, [("alpha", 2)], 7),
    (MAX_NORMAL, 2, 3, None, [("beta", 3), ("alpha", 2)], 7),
    (MAX_NORMAL, 1, 2, 1, [("alpha", 2)], 7),
    (MAX_THREE, 2, 3, 1, [("zoo", 3)], 12),
```
```python
def test_max_count_selection(tmp_path, output_format, reverse, content, minimum, maximum, top, expected, total):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    low, high = ["--min-count", str(minimum)], ["--max-count", str(maximum)]
    options = high + low if reverse else low + high
    if top is not None:
        options += ["--top", str(top)]
    result = run_cli_bytes(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format, expected, path.name, total)
```

**Apply:** `assert_output_bytes`（425–441）と `CLIHTML`（201–239）へ新件数の独立抽出・assertionを設計する。既存valuesのfilename/total契約を不必要に拡張しない。上の抜粋はparameter listの一部であり、全matrixはUnicode、候補12の既定10/top99等も持つ（867–875）。空/全除外は889–908、共有pairs同一性と元Counter/total保持は968–1000を継承。text/jsonの全bytes不変は下記saved bytesと今回用literal bytesで保証する（JSON parse一致だけでは不足）。

### Current期待値adapterと旧saved-byte試験 (test utility, transform)

**Analog:** `tests/test_cli.py:796–817,1017–1029`。元ファイルは読取りのみ、現CLIのstdoutを固定bytesと比較する。

**Existing exact-byte seam — lines 1023–1029:**
```python
    assert path.read_bytes() == case["body"].encode("utf-8")
    expected = (root / case["stdout"]).read_bytes()
    for extra in [[], ["--max-count", str(10**100)], ["--min-count", "1"]
                  if "--min-count" not in case["options"] else []]:
        result = run_cli_bytes(path, *case["options"], *extra, env=index["environment"])
        assert (result.returncode, result.stderr) == (case["exit"], (root / case["stderr"]).read_bytes())
        assert result.stdout == expected
```

**Missing pattern:** 承認されたHTML差分だけを変換する実装は未確認。旧HTMLの正確なtotal断片/局所CSSの出現1回を要求し、独立literal pairsからNを決めるfail-closed adapter、または別current固定fixtureをplannerが割り当てる。製品formatterをoracleに呼ばない。HTML以外は元bytesを無変換。変換に失敗したらassertionで拒否し、空白全正規化・HTML全無視・広いregex除去は使わない。adapterを別moduleへ出す場合、CLIのcold-copy試験（1059–1168）が依存moduleを含めて実行できる設計も必要。

### `tools/verify_wordfreq_max_count.py` / `tests/test_max_count_verifier.py` (legacy-current compatibility boundary)

**Analog:** trackedな同ファイル。新依頼の受入driverではなく、全pytestに含まれるcurrent fixture接点だけの参考。

**Current capture seam — tools lines 399–401:**
```python
        check_output(run.stdout, case)
        if 'oracle' in case and run.stdout != (baseline/fixed_cases[case['oracle']]['stdout']).read_bytes():
            raise ValueError('pre-feature bytes differ: '+case['id'])
```

validation側にも同等比較がある（445–449）。fixtureは `tests/test_max_count_verifier.py:98–110` で現CLIを呼び、scopeだけをmockする。
```python
        with patch.object(d, 'validate_scope', return_value={'fixture_only': True}):
            d.collect_capture(target, 'builder', ROOT / d.BASELINE)
```

**Apply:** 必要ならcurrent fixture専用の明示adapter seamをcollect/validateの両方に接続する。ただしlegacy既定validator・保存済captureは従来のまま検査できなければならない。scope mockを追加しただけではbytes差分は解消しない。`test_saved_builder_capture`（167–178）、`test_saved_baseline`（272–277）、`test_saved_preimplementation_red`（280–282）、履歴git非依存試験（285–296）を保持する。旧scope（tools463–494）のhashやallow-listを今回に合わせて書換えない。`review_session`（549–553）はbrowser無しであり今回品質受入に転用不可。

### 今回用browser検証ファイル / geometry (utility, event-driven / transform)

**Closest analog:** `tools/verify_wordfreq_html.py:586–671` の下層 `collect_view`。旧request/scope/AC/finalizeをそのままコピーしない。browser依存は明示browser操作だけでimportする既存方針（同ファイル1–4）を維持。

**Context/observer ordering — lines 586–592:**
```python
def collect_view(browser, case, width, output, live=None):
    folder = output / case["id"] / str(width)
    folder.mkdir(parents=True)
    context = browser.new_context(viewport=dict(width=width, height=900), device_scale_factor=1)
    observer = Observer(browser, context)
    page = context.new_page()
    cdp = observer.attach(page)
```

**Read-only measurement seam — lines 609–612:**
```python
        cdp.send("Emulation.setScrollbarsHidden", dict(hidden=True))
        page.goto(url, wait_until="load", timeout=15000)
        page.evaluate("document.fonts.ready")
        raw = page.evaluate((ROOT / "tools/wordfreq_html_geometry.js").read_text(encoding="utf-8"))
```

**Final event flush / error persistence — lines 658–663,668–671:**
```python
        page.wait_for_timeout(100)
        net = observer.finish()
        save_json(folder / "network.json", net)
        if live is None:
            observer.browser_cdp.detach()
            context.close()
```
```python
    errors += network_errors(net, url)
    view["errors"] = errors
    save_json(folder / "derived.json", view)
    return view
```

**Raw Range analog — `tools/wordfreq_html_geometry.js:48–56`:**
```javascript
      for (const char of node.data) {
        const utf16End = utf16Start + char.length;
        const range = document.createRange();
        range.setStart(node, utf16Start); range.setEnd(node, utf16End);
        characters.push({index,utf16Start,utf16End,char,codepoint:char.codePointAt(0),rects:boxes(range.getClientRects())});
        utf16Start=utf16End; index++;
      }
      texts.push({id:selector(el)+'::text('+nodeIndex+')',owner:selector(el),nodeIndex,
        text:node.data,fullRects:boxes(full.getClientRects()),characters});
```

**Apply:** 新leafをtargets（JS28）へ含め、今回専用DOM期待値にNを追加する。既存dom_errors（Python556–583）はbasename/total/rows/headersだけでN・横配置を判定しない。currentだけ新leaf必須とし、過去rawの保存検査へ必須fieldを逆輸入しない。共通wrapper・total左/N右・同じ行・表の上をrawと実画像で確認する。全祖先clip、全text間非重複、元Range/actual fontsを保持。full/tileは同じ描画条件（collector609,626–651）。open前からflushまで試行を監視し、成功response0を無通信にしない。canaryの観測判別力も必要。

今回driverのCLI/pathは未定。plannerは実在しないcommandを試さず、Builderが検証ファイルを作成し読取り確認した後に実行する。変更前同条件画像は製品編集前に別rootへ保存する。Phase7画像なし履歴を比較画像に見立てない。

### 今回用verifier試験・証拠出力 (test / evidence, file-I/O)

**Analog:** `tests/test_max_count_verifier.py:65–95,113–150` の欠損・改ざん拒否、tools max158–203のfresh-root/provenance/raw保存。例：

**Fresh-root guard — `tools/verify_wordfreq_max_count.py:158–161`:**
```python
def capture_baseline(output):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('no overwrite/resume/recapture of an existing baseline root')
```

**Tamper rejection — `tests/test_max_count_verifier.py:141–144`:**
```python
    d.save_json(root / 'manifest.json', m)
    (root / 'manifest.sha256').write_text(d.digest(root / 'manifest.json') + '\n')
    with pytest.raises((ValueError, FileNotFoundError)):
        d.validate_collection(root, ROOT / d.BASELINE)
```

**Apply:** 新検証seamにN不一致・横配置不成立・原本欠落・head不一致・未閲覧・通信試行の拒否試験を設ける。synthetic試験の成功は実browserや実画像閲覧の証明ではない。元total/rows/escapeも厳密に残す。旧request ID、START、画像0免除、旧scopeを新driverへコピーしない。REDは未変更製品に対する新表示assertion失敗として保存し、環境error/0 collectedと区別する。

### `README.md` / 今回検証手順 / 品質文字報告 (documentation, handoff)

**Analog:** README19,27–28,55–58。既存契約はbasename・総数・pure formatter・静的HTML・独立品質pendingを明記している。

**Current HTML explanation — README27:**
> - HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / max-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。

**Apply:** この近傍に承認文を1行だけ追加する：
> HTMLでは総出現回数の横に「表示 N 種類」を示し、Nは絞込み・top適用後の表示語種類数で、空結果は0です。

既存JSON例・末尾の検証B文は保持（CLI README試験1171–1208も参照）。

**Verification runbook analog:** `docs/wordfreq-html-verification.md:28–40,52–60,105–125`。再利用するのはfresh quality root、自身のCLI入力原本、actual head/profile/argv/env/exit、生HTML/raw/network/full/tile、全画像実閲覧、最終判定と観測終了の分離。旧request用コマンド・固定件数・exact-ref scopeは今回用に転記しない。

品質 `VERIFICATION.md` とCLI/CI文字証拠にはREQ-29/30/31との対応、RED/GREEN/full実数、CIの実状態、画像path/実閲覧枚数/内容/判定を残す。PMへplain原本を標準添付しread_fileで読める形にする。mapperは添付を実施しない。未実施はpending/blockであり合格ではない。

## Shared Patterns

### Final pairsとoriginal totalの分離

**Source:** `wordfreq/__main__.py:35–46`（変更不要）。
```python
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count
                               and (args.max_count is None or count <= args.max_count)})
    pairs = top_words(selected_counts, args.top)
```
`format_html(pairs, basename, total)` へ既に選択済pairsが渡る。Nはlenだけ。min/maxの包含AND、top既定10、初出順、元totalを壊さない。

### Validation / Error handling / Authentication

- 製品は静的CLIでauth/session/DB/routeは適用外。新機構を加えない。
- `_html_text`で一度escape、CR保護。入力値をclass/CSS/URLへ流さない。
- unittest側はassertion、verifier側は明示ValueError/FileExistsError等で拒否し、元stdout/stderr/partial証拠を残す。例外を成功verdictへ変換しない。
- class/tag/attribute/CSSを狭いallow-listとexact期待値で守る。N追加を理由にHTML全体をignoreしない。

### Execution / verification boundary

- OpenSpec1.1（先行RED）→1.2（最小GREEN/README/full）→2.1（品質独立CLI/full/browser/文字証拠）を同依頼branchで直列配置する。
- 後続の実在試験は `tests/test_formatters.py` / `tests/test_cli.py` / `tests/test_max_count_verifier.py` 等。RESEARCH掲載のinterpreter prefixでBuilder/品質が実行し、環境は実測する。mapperはテストや未作成commandを実行しない。
- 実browserは1280×900と320×900 DPR1。長basename/語、空/全除外、default10、escape等を覆い、全full/tileを品質本人が実閲覧する。構造/geometry/画像の存在だけで合格にしない。

## No Analog Found

| Capability / proposed file | Role | Data Flow | Gap / Planner action |
|---|---|---|---|
| HTML限定current期待値adapter（path未定） | test utility | byte transform | saved-byte比較は存在するが、出現1回を要求する承認差分変換は未確認。literal期待値とfail-closed試験を新設 |
| Phase08用browser受入driver（path未定） | verifier | event-driven / batch | 下層collectorはあるが、N/同一行/今回head・request/変更前比較を統合した完成driverは未確認 |
| Phase08用plain品質報告・画像台帳（path未定） | evidence | file-I/O / handoff | 旧runbookは型の参考のみ。今回の実行結果・閲覧枚数・CI状態を後続で採取し、未実施結果を埋めない |

## Metadata

- **Analog search scope:** `wordfreq/`, `tests/`, `tools/`, `docs/`, `README.md`。既存ファイル自体を優先し、browserは下層だけ読むことで検索を打ち切った。
- **Primary pattern families:** pure formatter、strict DOM/CSS unit test、real CLI/literal bytes、fresh-root evidence/integrity、browser Range/network/image collector。
- **Tracked-source gate:** `git ls-files -- wordfreq tests tools docs README.md .planning/phases/08-wordfreq-html-displayed-types` の出力により、ここでanalogとして命名した製品/tests/tools/docs/READMEの全pathがtrackedであることを確認。runtime/install mirrorは使用していない。
- **Project context:** working directoryの `HERMES.md` は検索結果なし。`.hermes/skills/` と `.agents/skills/` は存在しなかった。指定pattern-mapper roleと `gsd-plan-phase` skillを読んだ。
- **Source validity:** 抜粋は当セッションread_fileの行番号。formatter/tests/toolsが変更されたら関連割当を再確認する。公式GSDの状態判定が必要な操作は今回実施していない。
- **Output boundary:** この `08-PATTERNS.md` だけを書いた。新規検証driver名・class名・証拠leaf pathは提案/未定として保持し、架空の実在識別子や試験成功を主張していない。
