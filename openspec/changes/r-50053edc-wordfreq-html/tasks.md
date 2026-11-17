# Tasks

## 1. 全形式の同数時初出順（AC3・既存回帰）
- [x] 1.1 集計時の正規化後初出順を保持し、回数降順の安定ソート後にtopで切る。集計単体とtext/jsonの実CLI試験で `Zoo apple APPLE zoo banana`、top 1/2、後の再出現、回数が異なる入力を確認し、旧仕様の語の昇順なら失敗することを示す。部品の順序契約と意図した互換性変更を同時に文書へ記録する。

## 2. 安全な静的HTMLとメタ情報（AC1・AC2・AC5）
- [x] 2.1 単語・basenameを安全な表示テキストとして埋め込むHTML整形を作り、順位・単語・回数の見出し、UTF-8宣言、内包CSSだけの1枚文書を返す。整形単体試験で空pairs、特殊文字 `& < > " '`、タグ・イベント候補が表示文字となり、余分なタグ・スクリプト・外部リソースが生成されないことを確認し、部品契約を文書化する。
- [x] 2.2 CLIへhtml形式を接続し、top前countsからの総数と実行環境のbasenameを整形へ渡す。入力パスはtitle/属性等にも出さない。実CLI試験で `zoo apple zoo banana apple cherry` のtop 1/2/10でも総数6、別の頻度入力 `beta beta beta alpha gamma alpha delta` のtop 2でも総数7、表の上の表示位置、既定10・種類数超過・空入力0行を確認する。利用説明へ実行と保存の使用例を追記する。
- [x] 2.3 同じ入力のtext/json/htmlの語・回数・順序を照合し、html指定でも不正top（0・負・非整数）、不正format、引数個数、読込み/デコード失敗のexit・stderr・空stdout、Unicode抽出・casefold・入力境界を回帰試験する。特殊文字を含む有効なbasenameをCLIで検査し、単語認識を緩めない。text/jsonの構造・空出力は同数時順序以外に変更せず、試験結果で確認する。

## 3. 明るいレスポンシブ表示（AC4）
UI設計・PLANで通常幅と対象ブラウザ、320 CSS pxで実際に折返す長い語・有効なbasenameの固定入力を確定する。名前の連続空白・改行・タブの保持、保存HTMLの実UTF-8と宣言の一致、複数桁の数値列も検証対象へ含める。
- [ ] 3.1 明るい背景のみ・切替なし・1始まり表示行連番を適用し、長い語とbasenameを折返して読める表にする。通常幅と320 CSS pxの実CLI生成HTMLで、空・通常・長文・同数topの表示を試験し、順位1/2、横はみ出しなし、省略なしを確認する。採用したUIと確認条件を説明文書に残す。
- [ ] 3.2 ブラウザ検証手順と必要なローカル補助を用意し、viewport・要素・文字Range行断片・切取り祖先・隣接内容の実測原本および画面画像を保存する。横方向の収まり、切取り祖先内の収まり、隣接内容との非重複、画像の可読性で判定し、要素自身への厳格な縦包含を必須にしないことを試験/手順で確認する。値を補正して合格に見せず、全文を確認できる画像と実測を対応付ける。

## 4. 独立した統合検証と証拠（AC1–AC6）
検証開始時の作業状態と製品コードの差分を保存し、headと実行コードの対応を確認する。通信観測は文書を開く前から表示確認終了までとし、失敗試行と文書由来の遷移を含め、ブラウザ背景通信を区別する根拠も残す。
- [ ] 4.1 品質担当が対象headで入力原本からCLIを独立再実行し、text/json/htmlの一致と、空・通常・top・長文・注入候補のHTMLを通常幅および320 CSS pxで確認する。外部参照の静的検査と外部通信の試行記録を残し、通信遮断だけで無通信と判定しない。全画像を実際に読み、幾何原本と合わせACごとに判定する。head・入力・コマンド・exit/stdout/stderr・期待値・生成HTML・ブラウザ/viewport・矩形・画像・通信記録を保存して添付する。Builderの画像だけで代用しない。
- [ ] 4.2 全自動試験と変更差分を確認し、AC1–AC6と既存回帰の結果を追跡可能にまとめる。未実施条件は未検証として残し、証拠不足のまま合格にしない。CI追加・変更、依存追加、生成日時、テーマ切替、対話操作、サーバー、単語認識変更がないことを差分で確認する。

## Workflow follow-up
- 03-01 task 1: 共通初出順・HTML CLI接続・最終UI構造/CSSを実装し、集計5件・CLI27件・全50件が成功。1.1の文書と2.1の部品安全性試験はtask 2へ続く。2.2の全メタ情報行列と3.1のブラウザ確認は後続PLANまで未完了。独立品質4.1は未実施。
- 03-01 task 2: HTMLParserで元値の一度escape/空tbody/意味構造/固定タグ属性/CSS外部経路不在/非破壊を確認。READMEとCONCEPTSに現行契約を記録。整形6件・全52件成功。1.1/2.1だけを完了とし、2.2/3.1は接続・CSS・使用例までの部分完了（後続の全行列/ブラウザ/品質は未実施）。
- 03-01 review rework CR-01/WR-01: 不正UTF-8 basenameの置換表示とHTML専用UTF-8バイト出力をCLI境界で修正。各2件の実CLI REDを確認後、回帰4件と全56件成功。READMEの環境前提を修正。2.2/2.3の全行列・3.1のブラウザ・4.1の独立品質は未完了のまま。
- 03-01 review rework round2 CR-01: basenameを実行環境のfilesystem encodingで復号し、復号不能バイトだけ置換するよう修正。ISO-8859-15の有効なcafé.txtを実CLIでRED確認後、既存UTF-8/出力encoding回帰を含む5件と全57件成功。新規試験はlocale実在/charmapを確認。READMEも訂正。後続taskのチェック・公式計画位置は進め直さない。
- 03-02 task 1: 実CLIの全形式・明示期待値で総数6/7/0/200、top1/2/10/12/既定/超過、保存UTF-8 bytes、有効な注入候補basenameと全HTMLの生/escape済み親path不在を確認。全形式の読込み/引数失敗・実PermissionError（chmod後に同一実効ユーザーの読込み拒否とCLI stderrを確認、finallyでmode復元）・例外cause・hash seed0/1/42・cold-copy非破壊を検証。CLI95件とsource/tokenizer/boundary15件が成功し、2.2/2.3を完了。
- 03-02 task 2: HTML前処理のCR→LFを再現する試験を先に失敗させ、公式RED_EVIDENCE_OK後、全動的値をhtml.escapeしてからCRだけ&#13;へ符号化。固定長basename/語・12連番・123/巨大整数・完全な固定CSS宣言・構造/安全性の静的契約を追加。実CLIでも長いbasenameとCRを保持、locale charmapを確認して黙ったfallback/locale不足skipを防ぐ。整形9件・全126件成功（skipなし）。3.1は静的実装・試験までの部分完了、ブラウザ実測・全画像/通信観測・独立品質4.1は未実施のため未チェック。
- 03-03 tooling（独立品質gateの完了ではない）:
  - [x] 3.1 tooling部分: 固定15 CLIケース・HTML11ケース×両幅の実再生成、DOM/順序/総数/長文折返しと数値の自動幾何判別を用意。全画像の可読性はpendingのため3.1全体は未チェックのまま。
  - [x] 3.2 tooling部分: raw element/全文/文字Range・空矩形・UTF-16/codepoint・全祖先・実フォント・full/tile画像の対応採取と、own-height越え許容/clip/隣接非重複の判別試験を実装。実閲覧は未実施で3.2全体は未チェック。
  - [x] 4.1 tooling部分のみ: pre-open context/main-CDP/browser-flatten-autoattach観測と、clean/failed-resource/document-navigation/early-popup/client-redirectの実canaryを用意。採取はcapture-only/pending-review、品質の独立再生成・全画像閲覧・live観測・AC別判定は未完了。4.1の独立品質gateは未チェック。
  - [x] 03-03 review round2 tooling修正: coverageをready順序と同文書context/main/flatten要求・paused target対応から導出し、検証側も再計算。各td/メタ値等は文字record・character Range・全文一致を必須とし、欠落/空/部分測定は失敗。回帰のRED後、58 verifier/全184試験成功。全画像閲覧・live・独立品質gateのチェックは進めない。
- GSD対応表は03-COVERAGE.md。チェックは実際に完了したtaskだけを更新する。
- 実装・品質検証・受入が済んでから、別工程でsync・archiveと最終確認を行う。本カードでは実装・製品ブラウザ合格・archiveを行わない。
