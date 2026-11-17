# Real CLI evidence — quality t_6545be27

Target HEAD `30d9c175fd87a0d492ef6c1532271f55482c45b8`, Python 3.14.9 (local). Inputs are temporary files (path shown as IN). Raw transcript:

```text
$ python -m wordfreq IN/tie.txt
5	apple
5	zoo
1	b
[stderr] 
[exit] 0
$ python -m wordfreq --top 1 IN/tie.txt
5	apple
[stderr] 
[exit] 0
$ python -m wordfreq --format json IN/case.txt
[{"word": "hello", "count": 3}, {"word": "world", "count": 2}]
[stderr] 
[exit] 0
$ python -m wordfreq --format json IN/empty.txt
[]
[stderr] 
[exit] 0
$ python -m wordfreq IN/empty.txt
[stderr] 
[exit] 0
$ python -m wordfreq IN/ja.txt
2	東京
1	大阪
[stderr] 
[exit] 0
$ python -m wordfreq IN/bad.txt
[stderr] IN/bad.txt: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
[exit] 1
$ python -m wordfreq IN/nope.txt
[stderr] IN/nope.txt: [Errno 2] No such file or directory: 'IN/nope.txt'
[exit] 1
$ python -m wordfreq IN
[stderr] IN: [Errno 21] Is a directory: 'IN'
[exit] 1
$ python -m wordfreq --top 0 IN/tie.txt
[stderr] usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: --top must be >= 1
[exit] 2
$ python -m wordfreq --top x IN/tie.txt
[stderr] usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: argument --top: invalid int value: 'x'
[exit] 2
$ python -m wordfreq --format xml IN/tie.txt
[stderr] usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: argument --format: invalid choice: 'xml' (choose from 'text', 'json')
[exit] 2
$ python -m wordfreq 
[stderr] usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: the following arguments are required: filename
[exit] 2
$ python -m wordfreq IN/tie.txt IN/case.txt
[stderr] usage: wordfreq [-h] [--top TOP] [--format {text,json}] filename
wordfreq: error: unrecognized arguments: IN/case.txt
[exit] 2
determinism README.md seed1=6b8c60b85a85c71f782b654db4d363b4fb88895458677696ad213d1cf6506b72 seed777=6b8c60b85a85c71f782b654db4d363b4fb88895458677696ad213d1cf6506b72
```

All scenarios match spec FR-1..FR-4: ordering (count desc, word asc), --top, text/json, empty file exit 0, input errors exit 1 with one stderr line and empty stdout, usage errors exit 2, deterministic output across PYTHONHASHSEED. `git status` on wordfreq/ and tests/ was empty after the runs.
