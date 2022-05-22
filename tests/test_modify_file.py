from utf8csv import modify_file
from pathlib import Path
from tempfile import TemporaryDirectory

sample_without_prefix = b"a,b,c\r\n\xf0\x9f\x91\x8c,\xe2\x82\xac,\xe2\x84\x96"
sample_with_prefix = b"\xef\xbb\xbf" + sample_without_prefix
sample_with_gb18030_prefix = b"\x84\x31\x95\x33" + sample_without_prefix


def test_strip_with_utf8():
    # Antecedent: a CSV file with a BOM prefix present
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_with_prefix)
        # Behavior: pass the file path to `strip_bom`
        modify_file.strip_bom(file=source)
        # Consequence: the file is the same, except without the BOM
        result = source.read_bytes()
        assert result == sample_without_prefix


def test_strip_with_gb18030():
    # Antecedent: a CSV file with a non-UTF8 BOM prefix present
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_with_gb18030_prefix)
        # Behavior: pass the file path to `strip_bom`
        modify_file.strip_bom(file=source)
        # Consequence: the file is unchanged
        result = source.read_bytes()
        assert result == sample_with_gb18030_prefix


def test_strip_without():
    # Antecedent: a CSV file without a BOM prefix present
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_without_prefix)
        # Behavior: pass the file path to `strip_bom`
        modify_file.strip_bom(file=source)
        # Consequence: the file is unchanged
        result = source.read_bytes()
        assert result == sample_without_prefix


def test_prepend_without():
    # Antecedent: a CSV file without a BOM prefix present
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_without_prefix)
        # Behavior: pass the file path to `prepend`
        modify_file.prepend(file=source)
        # Consequence: the file is the same, except with a BOM added
        result = source.read_bytes()
        assert result == sample_with_prefix


def test_prepend_with():
    # Antecedent: a CSV file with a not-UTF8 BOM prefix present
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_with_gb18030_prefix)
        # Behavior: pass the file path to `prepend`
        modify_file.prepend(file=source)
        # Consequence: the file is unchanged
        result = source.read_bytes()
        assert result == sample_with_gb18030_prefix
