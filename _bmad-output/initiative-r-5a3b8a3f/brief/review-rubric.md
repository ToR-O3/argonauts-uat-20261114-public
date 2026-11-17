# Rubric review — brief-wordfreq-cli.md (r-5a3b8a3f)

Stakes: 社内ツール（UAT リポジトリ）。Rubric: rubric-planning。併読: .memlog.md。

## Verdict

未決 2 点を D-1・D-2 として決定に落とし、推定（A-1〜A-3）と範囲外を明示でタグ付けしており、内部ツールの Brief として決定準備は十分に済んでいる。残る実質的な弱点は Executive summary の「誰のためか・なぜ今か」の伝達と、部品分離・入力元抽象（WF-04/WF-06）の受け入れチェック方法の未定義で、どちらも下流の PRD 転記前に直せる局所的な穴である。

## Done when チェック

「Executive summary だけ読んで、これが何か・誰のためか・なぜ今かが言える」— **部分達成**。
- 何か: 達成（実行方法・オプション・部品構成・UI なしまで一文で特定できる）。
- 誰のためか: 弱い。「依頼者はこのツールを必要としており」とあるだけで、主利用者（この repository を使う、頻度をたまに数えるエンジニア）が Executive summary からは分からない。
- なぜ今か: 弱い。「未決 2 点は本 Brief で決定した」は進捗の報告であって、why-now（即席パイプラインの再組立コストが継続的に発生している、という Problem の論点）が Executive summary に届いていない。

## 3 fixes that matter most

1. **Executive summary に利用者と why-now を各 1 文足す**（Done when の穴）。「主利用者はこのリポジトリでテキスト頻度をたまに数えるエンジニア」「即席パイプラインの再組立と再現性問題が継続的に発生しているため、挙動を固定した最小ツールを置く価値が今ある」程度で十分。
2. **WF-04 / WF-06 の受け入れチェックを 1 行ずつ定義する**。「部品が分離している」「追加できる構成」は主観語で、そのままでは受け入れカードに落とせない。例: 「標準入力ソースを追加する変更で集計・出力整形の部品を編集しなくて済むことを示す試験」「設計文書のファイルパス（ADR-0001 等）を指定する」。
3. **Success criteria と WF/D ID をクロスリンクする**。Scope の WF-01〜WF-07 と Success criteria 1〜5 は実質同一内容なのに ID 対応がなく、「ID 対応づけて転記する」と書いておいて自分で対応表を書いていない。下流の PRD/OpenSpec への転記ミスを防ぐため 1〜5 に WF/D ID を付す。

## Findings by dimension

### 1. Decision-ready — **strong**

- 明確な主張（「性能や多言語対応ではなく、標準化と拡張性のための最小ツール」）が 1 つ通っている。
- D-1・D-2 で未決 2 点を挙動レベル（降順＋正規化後単語の昇順）まで決定済み。memlog の decision エントリと文書の内容が完全一致。
- the-ask / vision 節を「settled out」と理由つきで省略しており、ピッチ文書ではなく実装範囲文書という位置づけが首尾一貫。

### 2. Earned — **strong**

- ペルソナ演出・ビジョン劇場なし。単発 CLI に数年先の展望を置かない判断はstakesに合う。
- 既存 PyPI パッケージとの比較を A-3 として「早断」と明示して棚上げしており、未調査の優位性を事実のように語っていない。
- （軽微・info）Executive summary 2 文目の「データ消失・権限・外部送信・課金のリスクは小さい」はチェックリスト的な定型文。内部ツール向けに短く済んでいるので減点対象まではしない。

### 3. Testable — **adequate**

- WF-02/WF-03 の既定値・不正値時の使い方エラー、D-2 の決定論的並び順はそのまま試験に落とせる。
- **medium** — WF-04・WF-06（Scope）および Success criteria 2: 「独立した部品」「追加できる構成」が検証方法を伴わない抽象語。fix: 上記 fix 2 の受け入れチェックを追加。
- **low** — Who it serves「成功は『調べるのに 1 コマンドで足りた』状態」は比喩。Success criteria 1 で実質検証化されているので注記レベル。

### 4. Honest scope — **strong**

- 範囲外（GUI、URL 入力そのもの、日本語形態素解析、標準ライブラリ以外へのランタイム依存）が節として明示。memlog の scope 決定と一致。
- 推定 A-1〜A-3 が本文該当箇所に番号つきで引用され、Assumptions 節で根拠（依頼本文の裏付け / PM 指摘）まで区別されている。
- Open questions「なし」が決定の理由つきで、内部ツールのstakesに合った整理。
- **low** — 「pyproject.toml 等が避けられない場合」の例外節（Scope 範囲外末尾）は smart マージ方針への参照のみで、誰が承認するか（PM 等）が書かれていない。memlog の PM 指摘から復元は可能なので軽微。fix: 承認者を 1 語明記。

### 5. Usable downstream — **adequate**

- WF/D/A の ID は文書内で一意で、相互参照（WF-06、D-1、D-2、A-1、A-3）はすべて解決している。用語（正規化、集計・出力整形、入力元、使い方エラー）は全節で一致。
- 長さ・深さは内部ツールの Brief として適切。
- **medium** — Success criteria に WF ID の対応表がない（fix 3 参照）。「ID 対応づけて転記する」との宣言と自己矛盾。
- **low** — Table of Contents に Open questions 節が欠落（Assumptions までしか列挙されていない）。fix: 1 行追加。
