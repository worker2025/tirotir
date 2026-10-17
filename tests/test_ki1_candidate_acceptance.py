from pathlib import Path

from tirotir.core import execute
from tirotir.cli import main


def run(source):
    output = []
    execute(source, output.append)
    return output


def test_legacy_text_literal_remains_text():
    assert run("چاپ -سلام دنیا-") == ["سلام دنیا"]


def test_zero_width_non_joiner_is_preserved():
    value = "فارسی\u200cزبان"
    assert run(f"چاپ -{value}-") == [value]


def test_escaped_hyphen_remains_inside_literal():
    assert run(r"چاپ -الف\-ب-") == ["الف-ب"]


def test_arithmetic_contract_with_and_without_spaces():
    assert run("چاپ ۵-۳") == [2]
    assert run("چاپ ۵ - ۳ + ۲ - ۱") == [3]
    assert run("چاپ ۵-۳+۲-۱") == [3]


def test_function_and_return_contract_remains_compatible():
    source = "تابع جمع با الف و ب\n    بازگردان الف + ب\nچاپ جمع با ۲ و ۳"
    assert run(source) == [5]


def test_module_import_contract_remains_compatible(tmp_path, monkeypatch, capsys):
    (tmp_path / "lib").mkdir()
    (tmp_path / "tirotir.toml").write_text(
        '[project]\nname="candidate"\nentry="main.t"\n', encoding="utf8"
    )
    (tmp_path / "lib/tools.t").write_text("چاپ -کتابخانه-\n", encoding="utf8")
    (tmp_path / "main.t").write_text(
        "وارد کن -lib/tools-\nچاپ -اصلی-\n", encoding="utf8"
    )
    monkeypatch.chdir(tmp_path)
    assert main(["run"]) == 0
    assert capsys.readouterr().out.splitlines() == ["کتابخانه", "اصلی"]


def test_format_result_example_executes_without_regression():
    path = Path("examples2/functions/format_result.t")
    output = []
    execute(path.read_text(encoding="utf8"), output.append)
    assert output
