# Design

## Context

動機はproposalのWhyを参照。現実装はFileSource→iter_tokens→Counter→top_words→text/json formatter→stdoutである。top_wordsは現在 `(-count, word)` で並べる。Counterの挿入順は正規化語が最初に現れた順で、順序の情報は現時点ですでに存在する。モジュール横断変更とHTML注入対策があるため本designを作るが、独立したBMAD Architectureは小変更に過大なので作らない。

Q-1〜4はt_0c7d0df4のblock後の人defaultコメント1794903097と正常完了run60で解決済み。明るい背景、順位・単語・回数の3列、1始まり表示行連番（同数同順位なし）、top前総数、basenameのみを本書へ反映した。解決履歴はBrief/PRDのDecisionsに保存する。未解決の問いはなく、更新仕様の再承認後に計画へ進む。

## Goals / Non-Goals

**Goals:**
- 既存の入力・トークン化・集計・整形の境界を保ち、1回の集計から全形式共通の順位を得る。
- HTMLに限って必要なメタデータを渡し、表示境界でescapeする。
- レイアウトと安全性を純粋な整形試験および実ブラウザの証跡の両方で確かめられる構成にする。

**Non-Goals:**
- 共通の巨大なレポートモデル、新しい入力種別、Web frameworkやJS、依存・CI変更を導入しない。
- text/JSONのAPIや出力構造へHTMLのメタデータを混ぜない。

## Decisions

### D-1: 共通の順位決定を集計部品に置く

count_wordsとtop_wordsの境界を保つ。CLIで集計を一度行い、挿入順を保つCounterのitemsを回数降順だけで安定sortし、その後topで切る。これにより同数時は正規化済み語の初出順となる。明示的な位置mapも可能だが同じ順序の重複保持になるので採らない。formattersごとのsortは形式間の不整合を生むので採らない。外部から順序を失ったmappingを渡して入力元の初出を復元することは保証しない。CLI経路はCounterを再構築・set化しない。

### D-2: HTMLの総数と名前は別引数で渡す（Q-3/Q-4回答反映）

CLIはcountsを保持し、topを切る前のcounts.valuesの和を総数とする。format_html(pairs, *, filename, total_count)相当の純粋整形部品へ、選択済みpairsと表示用basenameと総数を渡す。top後のpairsから総数を再集計しない。FileSourceの読取りは従来どおりで、formatterにファイルを読ませない。basenameはPath(args.filename).name相当（実行OSのパス規則）で得て、resolveによる絶対パスの露出は避ける。text/jsonのformatter署名と構造は維持する。

### D-3: 最小の静的HTMLと単一escape境界

HTML formatterはdoctype、html lang、headのUTF-8 charsetとviewport、title、内包style、body内のメタデータとtableを構築する。名前・語はテキストノードへhtml.escape(..., quote=True)相当で1回だけescapeする。動的な値をstyle・script・属性・URLへ入れない。tableはthead/tbodyとscope=colの見出しを持つ。JS・外部asset・通信は一切足さない。charsetはUTF-8保存を前提とし、出力ストリームの扱いは既存Python規則を維持する。利用例では必要に応じ `PYTHONIOENCODING=utf-8 python -m wordfreq input.txt --format html > report.html` とし、input/reportは別ファイルにする。

テンプレートエンジンは標準ライブラリのみの小出力に不要。単語・名前のescape責務はtokenizerでなくHTML整形境界に置くので、差替えtokenizerや直接formatter入力にも安全性を持つ。HTML解析の改行正規化に対しては、escape後にCRを `&#13;` へ置換する等で元のCR/CRLFをtextContentに保持し、直接部品試験と実ブラウザで照合する。

### D-4: 幅固定でなく折返し可能な表

明るい背景、順位・単語・回数の3列とする。選択済みpairsを1始まりで列挙し、表示行連番をHTMLだけに付ける。同数でも連番で、top1は順位1の1行、空入力は見出し3列・データ0行・順位セルなし。3列それぞれにscope=colの見出しを関連付ける。幅100%・box-sizing・table-layout等を使い、語/名前はoverflow-wrapとwhite-space: pre-wrap等で全内容を折り返す。順位・回数は読める幅を確保し、切捨て/ellipsisとページ・表の横スクロールに頼らない。viewportはdevice-widthを使用。200文字連続語、長い日本語名、空白文字、空表で3列の可読性を検証する。承認後GSDのUI-SPECへ決定を引継ぐ。テーマ切替は追加しない。

### D-5: 検証は純粋部品・CLI・ブラウザの三層

- 部品: Counterの初出保持、casefold統合、top境界、特殊文字を直接渡すHTML formatter、二重escape防止、charset/table/JSなしを検証する。
- CLI: 全形式の初出順、top/既定/空/記号のみ/入力エラー/未知format、text/JSON構造、入力不変と入力名・総数を検証する。旧語昇順試験は明示変更として初出順の期待に更新し、他の回帰は残す。
- ブラウザ: 実装後品質が実HTMLをローカルで開き、320/375px mobile viewportと1280px、DOM textContent/layout測定、画像、外部request 0、注入不実行を記録する。計画工程が既存のbrowser手段と証跡採取方法を確認し、品質に引継ぐ。手段不足は未検証として人へ回し、依存/CIを追加しない。検証記録はGSDの対象phase資料かカード添付として保持する。仕様工程では実装/ブラウザ検証済みと主張しない。

## Risks / Trade-offs

- [同数順の互換性変更] → text/JSONもtop境界の選択が変わる。仕様・テスト・CONCEPTSを同時更新し、旧語昇順の継続を約束しない。
- [入力名・語の露出] → basenameのみでも匿名化ではない。共有前確認を案内し、本文自体は出さず外部送信しない。
- [注入/二重escape] → テキスト境界で1回escape、直接部品試験と悪意あるfilenameのCLI/browser試験で元文字列一致と不実行を確認する。
- [長い語と任意の大きな回数] → 長語折返し、順位・単語・回数列の対応とoverflowを実browser測定で確認する。明るい背景の3列でも同条件を満たす。
- [非UTF-8 stdout] → 自動的にtext/JSONの出力規則を変えない。UTF-8環境と保存例でcharsetを一致させる。
- [同一ファイルへのリダイレクト] → シェルが起動前に入力を消すためCLIでは防げない。利用例は別出力、同一パス禁止の注意を明記する。

## Migration Plan

回答済みQ-1〜4を反映した文書の再承認後に計画・UI-SPEC・実装へ進む。製品の変更はCLI内に閉じ、データ移行やサービス配備は不要。既存pytestを維持したまま試験を追加・更新する。CI workflow・依存は変更せず、生成日時表示は追加しない。問題が出たら変更commitをrevertする通常の修正手順に戻すが、旧同数順へ戻すことは再び互換性変更なので人の判断を経る。OpenSpecのsync/archiveは実装後の最終化工程だけで行う。
