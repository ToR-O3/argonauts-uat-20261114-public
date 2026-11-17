"""Composition across the text-source boundary, without CLI coupling."""
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
