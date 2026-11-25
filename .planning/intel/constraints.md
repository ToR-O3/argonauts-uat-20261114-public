# Constraints (intel)

今回のSPEC分類はspec.mdとtasks.md。実装・検証は未実施。抽出内容は次工程への契約であり、この取込みの実行指示ではない。

DATA_fcb99877_START

## 最大出現回数の整数契約
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:5-26; openspec/changes/r-d4bcda40-max-count/tasks.md:5-6
- type: api-contract
- content: --max-countはtype=int・省略Noneで上限なし。0/負整数/+2/02/大きな整数/--max-count=-1受理、正値制約やmin/max関係エラーなし。helpはファイルなしでもexit0・stderr空で--max-count MAX_COUNTを表示。abc/1.5/欠落は入力前exit2・stderr通知・stdout空、Traceback/エラーHTMLなし。既存min/top正値制約は維持。

## 共通頻度帯選択からtopへの順序
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:6-18,64-101,126-139; openspec/changes/r-d4bcda40-max-count/tasks.md:5-6,11
- type: api-contract
- content: casefold後countsへ下限AND任意上限を包含適用→回数降順・同数正規化後初出順→独立top。全形式同一pairs、CLI指定順不変。旧単語昇順へ戻さず、抽出/casefold不変。max2/top1でalpha2、min2/max2/top1でzoo2。Straße STRASSE 日本語 日本語はmax1で空、min2/max2でstrasse2/日本語2。選択後11種類以上で既定top10、大きいtopで全残存種類。spyでtop入力・選択順序・元Counter不変・formatter共有pairsを確認。

## 空集合とエラー出口
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:28-49,141-162; openspec/changes/r-d4bcda40-max-count/tasks.md:5-6,11
- type: api-contract
- content: 正常読込み後のmax0/負数/min>max/全除外/空/抽出0語はexit0・stderr空。text空、json[]と改行1つ、html既存メタ情報・3列見出し・データ0行・空状態を保持。空集合でも入力取得を短絡せず、有効max0/負数でも不存在/ディレクトリ/権限失敗/不正UTF-8はexit1・stderr通知・stdout空。不正min0/top0との併用は入力前exit2。

## HTML元総数と既存表示安全性
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:29-37,103-124,149-162; openspec/changes/r-d4bcda40-max-count/tasks.md:6,11
- type: api-contract
- content: 元Counterを変更せず、HTML総数はmin/max/top前の回数和、種類数・表示行和ではない。通常入力のmax0/負数/逆転でも総数7。beta4/zoo3/apple2/pear2/single1でmin2/max3/top1は順位1のzoo3と総数12。抽出0語は0。basenameのみ、title/属性を含めディレクトリなし。既存formatter API・見た目・CSS・空文言・UTF-8・escape・静的安全性を保つ。

## 省略互換と製品変更境界
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:47-52,149-154; openspec/changes/r-d4bcda40-max-count/tasks.md:5-6,11
- type: nfr
- content: 上限省略と十分大きい上限は既存保存済み出力または変更前固定期待バイト列・exit・stderrと一致。変更後同士だけの比較不可。既存min省略/明示1・既定text/top10・初出順・構造を保つ。製品差分は引数/共通選択/関連試験/README、依存・CI・見た目・無関係機能を追加変更しない。

## READMEの再現可能な1例
- source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:51-56; openspec/changes/r-d4bcda40-max-count/tasks.md:7
- type: protocol
- content: READMEへpython -m wordfreq input.txt --min-count 2 --max-count 3 --format jsonの1例を追加し、入力beta beta beta alpha gamma alpha deltaと期待JSON（beta3、alpha2）を併記。整数全域・省略上限なし・包含・min併用・0/負数/逆転は正常空結果・全除外時の上限調整・HTML元総数を説明。同じ掲載コマンドを走らせるpytestでexit0/stdout/stderrとREADME内容を検証。

## 先行試験と全体回帰
- source: openspec/changes/r-d4bcda40-max-count/tasks.md:3-11; openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:51-60
- type: protocol
- content: task1.1で不足する変更前期待値を固定し追加pytestを先に書いて未実装RED、task1.2で最小実装GREEN、task1.3でREADME例検証。境界/異常/全形式/Unicode/top/空/入力失敗を含め既存全試験と成功させ、件数・環境・コマンド・exitを残す。既存期待値を新コードで作り直さず既存試験を削除/回避しない。git差分で範囲外変更なしを確認する。

## 独立品質と後続工程の境界
- source: openspec/changes/r-d4bcda40-max-count/tasks.md:12-17; openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:58-60
- type: protocol
- content: 品質が対象headから実CLIを独立実行し省略互換・境界・min併用・全除外・元総数を確認。HTMLは通常幅/狭幅の既存独立ブラウザ検証を維持、入力/argv/exit/stdout/stderr/HTML原本/実測/画像/通信検査を追跡可能に残す。VERIFICATION.mdとCLI/CI文字証拠をPMへ添付し、受入別結果と閲覧画像枚数・確認内容・結果を記載。PMに画像/圧縮ファイル閲覧を求めず未実施/未報告CIを成功扱いしない。PLAN作成・実装・受入・sync/archiveは後続工程、この取込みでは実施しない。Bot自身はPRをマージしない。

DATA_fcb99877_END
