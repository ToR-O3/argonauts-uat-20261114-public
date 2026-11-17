"""Composition across the text-source boundary, without CLI coupling."""
from unittest.mock import Mock

import pytest

from wordfreq import __main__ as cli
from wordfreq import sources
from wordfreq.aggregator import count_words
from wordfreq.sources import FileSource, TextSource
from wordfreq.tokenizer import iter_tokens


def test_aggregation_does_not_acquire_files(monkeypatch):
    calls = []
    original = FileSource.read_text

    def spy(source):
        calls.append(source)
        return original(source)

    monkeypatch.setattr(FileSource, "read_text", spy)
    assert count_words(iter_tokens("Hello hello WORLD")) == {"hello": 2, "world": 1}
    assert calls == []


def test_fake_source_supplies_equivalent_text():
    class FakeSource:
        def read_text(self) -> str:
            return "Hello hello WORLD"

    source: TextSource = FakeSource()
    assert count_words(iter_tokens(source.read_text())) == {"hello": 2, "world": 1}


def test_file_boundary_is_crossed_exactly_once(tmp_path, monkeypatch):
    path = tmp_path / "input.txt"
    path.write_text("Hello hello WORLD", encoding="utf-8")
    calls = []
    original = FileSource.read_text

    def spy(source):
        calls.append(source)
        return original(source)

    monkeypatch.setattr(FileSource, "read_text", spy)
    source: TextSource = FileSource(str(path))
    assert count_words(iter_tokens(source.read_text())) == {"hello": 2, "world": 1}
    assert calls == [source]


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_cli_composition_once_per_format(tmp_path, monkeypatch, capsys, output_format):
    path = tmp_path / "nested" / "資料.txt"
    path.parent.mkdir()
    content = "Zoo apple zoo APPLE beta"
    path.write_text(content, encoding="utf-8")
    reads = []
    original_read = FileSource.read_text

    def read(source):
        reads.append(source._path)
        return original_read(source)

    monkeypatch.setattr(FileSource, "read_text", read)
    spies = {}
    for name in ("iter_tokens", "count_words", "top_words", "format_text", "format_json", "format_html"):
        spies[name] = Mock(wraps=getattr(cli, name))
        monkeypatch.setattr(cli, name, spies[name])
    with pytest.raises(SystemExit) as exit_info:
        cli.main([str(path), "--format", output_format, "--top", "1"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().err == ""
    assert reads == [str(path)]
    spies["iter_tokens"].assert_called_once_with(content)
    spies["count_words"].assert_called_once()
    spies["top_words"].assert_called_once()
    counts, top = spies["top_words"].call_args.args
    assert list(counts.items()) == [("zoo", 2), ("apple", 2), ("beta", 1)]
    assert top == 1
    for name in ("format_text", "format_json", "format_html"):
        if name == f"format_{output_format}":
            if output_format == "html":
                spies[name].assert_called_once_with([("zoo", 2)], filename=path.name, total_count=5)
            else:
                spies[name].assert_called_once_with([("zoo", 2)])
        else:
            spies[name].assert_not_called()


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_cli_read_permission_fault(tmp_path, monkeypatch, capsys, output_format):
    path = tmp_path / "denied.txt"
    original = b"hello"
    path.write_bytes(original)
    calls = []
    path.chmod(0)
    try:
        try:
            with path.open("rb") as probe:
                probe.read()
        except PermissionError:
            injected = False  # Real permissions are effective on this host.
        else:
            injected = True  # Privileged host: exercise the FileSource open boundary.
            calls = []

            def denied(filename, *args, **kwargs):
                calls.append((filename, args, kwargs))
                raise PermissionError(13, "Permission denied", str(filename))

            monkeypatch.setattr(sources, "open", denied, raising=False)
        with pytest.raises(SystemExit) as exit_info:
            cli.main([str(path), "--format", output_format])
        assert exit_info.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""
        assert str(path) in captured.err
        assert "Permission denied" in captured.err
        assert len(captured.err.splitlines()) == 1
        assert "Traceback" not in captured.err
        if injected:
            assert calls == [(str(path), ("r",), {"encoding": "utf-8"})]
    finally:
        path.chmod(0o600)
    assert path.read_bytes() == original
