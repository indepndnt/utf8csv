from utf8csv import main
from pathlib import Path
import pytest
import sys


def test_init():
    # Antecedent: program exists
    # Behavior: initialize primary class
    obj = main.Opener()
    # Consequence: have an Opener instance with a reasonable _command string property
    assert obj._command.endswith(' "%1"')


def test_excel_association():
    # Antecedent: run on a Windows platform with Excel installed
    obj = main.Opener()
    # Behavior: request the Excel file association command
    excel = obj.excel_association
    # Consequence: receive a string that also populates the _xls_assoc attribute
    assert isinstance(excel, str)
    assert obj._xls_assoc == excel


def test_cli_help(capsys):
    # Antecedent: a help argument
    sys.argv = [sys.argv[0], "-h"]
    # Behavior: utf8csv.main() called
    with pytest.raises(SystemExit) as exit_obj:
        main.main()
    # Consequence: program returns help text
    capture = capsys.readouterr()
    assert exit_obj.type == SystemExit and exit_obj.value.code == 0
    assert not capture.err
    assert capture.out.endswith("Thank you for using utf8csv!\n")


def test_execute_dir():
    # Antecedent: a non-file input
    file = Path()
    # Behavior: Opener.execute called
    exit_code = main.Opener()(file, dry_run=True)
    # Consequence: program returns error code
    assert exit_code > 0


def test_execute_non_csv():
    # Antecedent: a non-CSV file input
    file = Path(__file__)
    # Behavior: Opener.execute called
    exit_code = main.Opener()(file, dry_run=True)
    # Consequence: program returns error code
    assert exit_code > 0
