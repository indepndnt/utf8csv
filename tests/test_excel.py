from utf8csv import excel
from pathlib import Path


def test_execute_dir():
    # Antecedent: a non-file input
    file = Path()
    # Behavior: Opener.execute called
    exit_code = excel.open_csv(file, dry_run=True)
    # Consequence: program returns error code
    assert exit_code > 0


def test_execute_non_csv():
    # Antecedent: a non-CSV file input
    file = Path(__file__)
    # Behavior: Opener.execute called
    exit_code = excel.open_csv(file, dry_run=True)
    # Consequence: program returns error code
    assert exit_code > 0
