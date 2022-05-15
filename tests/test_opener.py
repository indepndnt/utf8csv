from utf8csv import main, modify_file, registry
from pathlib import Path
import pytest
import sys
from tempfile import TemporaryDirectory

sample_without_prefix = b"a,b,c\r\n\xf0\x9f\x91\x8c,\xe2\x82\xac,\xe2\x84\x96"
sample_with_prefix = b"\xef\xbb\xbfa,b,c\r\n\xf0\x9f\x91\x8c,\xe2\x82\xac,\xe2\x84\x96"


def test_init():
    obj = main.Opener()
    assert obj._command.endswith(' "%1"')


def test_excel_association():
    obj = main.Opener()
    excel = obj.excel_association
    assert isinstance(excel, str)
    assert obj._xls_assoc == excel


def test_options_key():
    key = registry.excel_options_key()
    assert isinstance(key, str)


def test_install(capsys):
    obj = main.Opener()
    obj(file=None, uninstall=False, dry_run=True)
    capture = capsys.readouterr()
    assert not capture.err
    assert "DefaultIcon: '" in capture.out


def test_uninstall(capsys):
    obj = main.Opener()
    obj(file=None, uninstall=True, dry_run=True)
    capture = capsys.readouterr()
    assert not capture.err
    assert "Current: '" in capture.out


def test_strip():
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_with_prefix)
        modify_file.strip_bom(file=source)
        result = source.read_bytes()
        assert result == sample_without_prefix


def test_prepend():
    with TemporaryDirectory() as temp:
        source = Path(temp) / "sample.csv"
        source.write_bytes(sample_without_prefix)
        modify_file.prepend(file=source)
        result = source.read_bytes()
        assert result == sample_with_prefix


def test_cli_help(capsys):
    sys.argv = [sys.argv[0], "-h"]
    with pytest.raises(SystemExit) as exit_obj:
        main.main()
    capture = capsys.readouterr()
    assert exit_obj.type == SystemExit and exit_obj.value.code == 0
    assert not capture.err
    assert capture.out.endswith("Thank you for using utf8csv!\n")
