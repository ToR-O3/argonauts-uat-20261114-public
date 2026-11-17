"""Real filesystem input contracts."""
import importlib.util

import pytest


def test_file_source_reads_utf8_without_modification(tmp_path):
    assert importlib.util.find_spec("wordfreq.sources") is not None, "input boundary module is required"
    from wordfreq.sources import FileSource, TextSource

    path = tmp_path / "input.txt"
    data = "Hello 日本語\nStraße\n".encode("utf-8")
    path.write_bytes(data)
    source: TextSource = FileSource(str(path))
    assert callable(source.read_text)
    assert source.read_text() == data.decode("utf-8")
    assert path.read_bytes() == data
    assert sorted(p.name for p in tmp_path.iterdir()) == ["input.txt"]


def test_file_source_normalizes_missing_file(tmp_path):
    from wordfreq.sources import FileSource

    path = tmp_path / "missing.txt"
    with pytest.raises(Exception) as caught:
        FileSource(str(path)).read_text()
    assert type(caught.value).__name__ == "InputError"
    assert str(path) in str(caught.value)
    assert isinstance(caught.value.__cause__, FileNotFoundError)
    assert list(tmp_path.iterdir()) == []


def test_file_source_normalizes_invalid_utf8(tmp_path):
    from wordfreq.sources import FileSource, InputError

    path = tmp_path / "invalid.txt"
    data = b"\xff\xfe"
    path.write_bytes(data)
    with pytest.raises(InputError) as caught:
        FileSource(str(path)).read_text()
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)
    assert str(path) in str(caught.value)
    assert path.read_bytes() == data


def test_file_source_normalizes_unopenable_path(tmp_path):
    from wordfreq.sources import FileSource, InputError

    with pytest.raises(InputError) as caught:
        FileSource(str(tmp_path)).read_text()
    assert isinstance(caught.value.__cause__, OSError)
    assert str(tmp_path) in str(caught.value)


def test_file_source_reads_empty_file(tmp_path):
    from wordfreq.sources import FileSource

    path = tmp_path / "empty.txt"
    path.write_bytes(b"")
    assert FileSource(str(path)).read_text() == ""
    assert path.read_bytes() == b""


def test_file_source_chains_permission_error(monkeypatch):
    from wordfreq.sources import FileSource, InputError

    original = PermissionError(13, "Permission denied", "private.txt")
    calls = []

    def denied(*args, **kwargs):
        calls.append((args, kwargs))
        raise original

    monkeypatch.setattr("builtins.open", denied)
    with pytest.raises(InputError) as caught:
        FileSource("private.txt").read_text()
    assert caught.value.__cause__ is original
    assert "private.txt" in str(caught.value)
    assert "Permission denied" in str(caught.value)
    assert calls == [(("private.txt", "r"), {"encoding": "utf-8"})]
