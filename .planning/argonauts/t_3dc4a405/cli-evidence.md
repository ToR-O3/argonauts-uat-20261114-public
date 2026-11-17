# 実CLI確認の証拠（t_3dc4a405, head 0cd4673）

Python 3.14.9、repo直下で `python -m wordfreq`。入力は品質のscratchに作成（<tmp>）。case="Hello hello HELLO world"、punct="one, two. one"、tie=apple×5 zoo×5 b、many=a..l と a 2回、ja=日本語、bad=0xff 0xfe 0xfa、empty=0バイト。

```text
$ python -m wordfreq <tmp>/case.txt
3	hello
1	world
[exit=0]
$ python -m wordfreq <tmp>/punct.txt
2	one
1	two
[exit=0]
$ python -m wordfreq <tmp>/tie.txt
5	apple
5	zoo
1	b
[exit=0]
$ python -m wordfreq <tmp>/many.txt
2	a
1	b
1	c
1	d
1	e
1	f
1	g
1	h
1	i
1	j
[exit=0]
$ python -m wordfreq --top 3 <tmp>/many.txt
2	a
1	b
1	c
[exit=0]
$ python -m wordfreq --top 3 <tmp>/case.txt
3	hello
1	world
[exit=0]
$ python -m wordfreq --format json <tmp>/tie.txt
[{"word": "apple", "count": 5}, {"word": "zoo", "count": 5}, {"word": "b", "count": 1}]
[exit=0]
$ python -m wordfreq --format json <tmp>/empty.txt
[]
[exit=0]
$ python -m wordfreq <tmp>/empty.txt
[exit=0]
$ python -m wordfreq <tmp>/ja.txt
2	日本語のテキスト
1	です
[exit=0]
$ python -m wordfreq <tmp>/missing.txt
<tmp>/missing.txt: [Errno 2] No such file or directory: '<tmp>/missing.txt'
[exit=1]
$ python -m wordfreq <tmp>/bad.txt
<tmp>/bad.txt: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
[exit=1]
$ python -m wordfreq 
usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: the following arguments are required: filename
[exit=2]
$ python -m wordfreq <tmp>/case.txt <tmp>/tie.txt
usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: unrecognized arguments: <tmp>/tie.txt
[exit=2]
$ python -m wordfreq --top 0 <tmp>/case.txt
usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: --top must be >= 1
[exit=2]
$ python -m wordfreq --top abc <tmp>/case.txt
usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: argument --top: invalid int value: 'abc'
[exit=2]
$ python -m wordfreq --format xml <tmp>/case.txt
usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: argument --format: invalid choice: 'xml' (choose from 'text', 'json')
[exit=2]
DETERMINISTIC_OK（同じjson出力を2回比較）
PYTHONHASHSEED=1 / 99 の text 出力 md5 が一致: e95a0e9bc3a8bca69f3c0d5e1f93a76f
python -m pytest: 43 passed（exit 0）、PYTHONHASHSEED=42 python -m pytest -q: 43 passed
```
