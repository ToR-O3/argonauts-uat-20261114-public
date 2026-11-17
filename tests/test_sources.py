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
