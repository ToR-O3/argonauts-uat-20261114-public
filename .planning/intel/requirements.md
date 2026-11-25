# Requirements (intel)

MODE: merge。今回のPRD分類2文書のみを要求の入力とする。proposalの同義な条件は下記FR-1〜FR-6へ出典付きで対応付け、競合variantを創作しない。以下は後続実装の受入条件であり達成宣言ではない。

DATA_512f285d_START

## REQ-max-count-option
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:57,86-93; openspec/changes/r-d4bcda40-max-count/proposal.md:9-11
- description: FR-1。任意の整数オプション--max-count Nを追加する。
- acceptance: 既存type=intと同じ整数解釈、省略時上限なし。0・負整数・+2・02・大きな整数・--max-count=-1を受理し、正値限定しない。非整数abc/1.5と値欠落は入力取得前exit2、stderr通知、stdout空、Tracebackなし。ファイル名なしの--helpはexit0・stderr空、stdoutに--max-count MAX_COUNTを表示する。
- scope: CLI引数、整数受理、help、入力前検証。

## REQ-max-count-selection
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:58,73-80,86-90,97-98; openspec/changes/r-d4bcda40-max-count/proposal.md:9-10
- description: FR-2。全形式に共通の包含的な頻度帯を選択してからtopを適用する。
- acceptance: 正規化後count >= min_count AND count <= max_count、上限省略時は下限のみ。両端包含、引数指定順によらない。選択→回数降順/同数初出順→topの順。全formatterへ同じ選択結果を渡し、HTMLで別集計しない。内部spyでtop入力・元Counter不変・共有選択を確認。max2の通常入力はalpha2/gamma1/delta1、max1はgamma1/delta1、min2/max2はalpha2、min2/max3はbeta3/alpha2、max2/top1はalpha2。Unicode合算後に判定、同数初出順維持。選択後11種類以上なら既定top10、大きいtopなら残った全件。
- scope: 共通選択、正規化後集計、text/json/html、top。

## REQ-max-count-empty-errors
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:59,78,81,83-84,91; openspec/changes/r-d4bcda40-max-count/proposal.md:11
- description: FR-3。正常な空集合と入力失敗・既存不正引数を区別する。
- acceptance: 読込み成功後のmax0・負数・min>max・全除外・空入力・抽出0語はexit0、stderr空。text空、jsonは[]と改行1つ、htmlは既存3列見出し・0データ行・空状態・basename・元総数。空集合でも入力を省略せず、不存在・ディレクトリ・権限による読込み失敗・不正UTF-8は有効max0/負数でもexit1、stderr通知、stdout空。max0/負数と不正min0/top0の併用は入力取得前exit2でstdout空。min/max大小関係エラーを追加しない。
- scope: 入力境界、全形式の空結果、exit0/1/2。

## REQ-max-count-compatibility
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:60,86,90,93,102,118,123-127; openspec/changes/r-d4bcda40-max-count/proposal.md:10,23-27
- description: FR-4。上限省略の互換性と全フィルタ前HTML総数を維持する。
- acceptance: 上限省略と十分大きい上限のstdoutバイト列・exit・stderrは既存保存済み出力または変更前固定期待値と一致。変更後2呼出し同士の比較だけは不可。元Counter不変、HTML総数はmin/max/top前の回数和。beta4/zoo3/apple2/pear2/single1でmin2/max3/top1はzoo3のみ・元総数12。全除外でも元正数、抽出0語は0。抽出/casefold・同数初出順・UTF-8・escape・basename限定・静的安全性・text/json構造・formatter API・既定text/top10・既存min/top正値検証を変更しない。依存/CI/見た目/CSS/空文言/新入力元/無関係変更なし。
- scope: 既存互換、元集計、HTML総数、最小変更境界。

## REQ-max-count-verification
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:64,69-93,110-119,135; openspec/changes/r-d4bcda40-max-count/proposal.md:12
- description: FR-5。追加pytestと全既存試験を成功させ、未実施を成功と報告しない。
- acceptance: 全3形式の境界/併用/top/Unicode/空/異常/省略互換を試験し全既存試験も成功、既存試験の削除・回避なし。環境・コマンド・件数・exitを記録し、既存検証義務を省略せず、未実施・未報告CIを成功扱いしない。製品受入は実装後に判断する。
- scope: pytest、既存回帰保護、証拠記録。

## REQ-max-count-readme
- source: _bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md:65,129-131; openspec/changes/r-d4bcda40-max-count/proposal.md:13
- description: FR-6。READMEへ使用例1つと直接関連する説明を追加する。
- acceptance: python -m wordfreq input.txt --min-count 2 --max-count 3 --format json の同じ例に入力beta beta beta alpha gamma alpha deltaと期待JSON [{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]を併記、末尾改行・exit0を実CLIで検証。整数全域・省略上限なし・包含・min併用・逆転は正常空結果を説明。上限全除外時はmaxを上げるか省略する案内とし、minを下げるだけの旧案内を修正。HTML総数説明にmax前を反映する。
- scope: READMEの関連説明と再現可能な1例。

DATA_512f285d_END
