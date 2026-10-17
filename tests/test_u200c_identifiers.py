from pathlib import Path

import pytest

from tirotir.core import execute, tokenize


ROOT = Path(__file__).parents[1]


def run(source):
    output = []
    execute(source, output.append)
    return output


def test_zero_width_non_joiner_identifier_normalizes_to_underscore():
    source = "بگذار نام‌گذاری برابر ۱\nچاپ نام‌گذاری\nچاپ نام_گذاری"
    assert run(source) == [1, 1]
    words = [token.value for token in tokenize(source) if token.kind == "WORD"]
    assert "نام‌گذاری" not in words
    assert words.count("نام_گذاری") == 3


def test_zero_width_non_joiner_works_in_function_and_return():
    source = "تابع جمع‌مثبت با عدد\n    بازگردان عدد\nچاپ جمع‌مثبت با ۳"
    assert run(source) == [3]


@pytest.mark.parametrize(
    "relative_path",
    [
        "examples/00_رسمی.t",
        "examples2/00_رسمی.t",
        "examples2/functions/function_condition_loop.t",
        "examples2/lists/create_and_read.t",
        "examples2/loops/for_list.t",
        "examples2/variables/multiple_values.t",
    ],
)
def test_official_zero_width_non_joiner_examples_parse_and_execute(relative_path):
    source = (ROOT / relative_path).read_text(encoding="utf8")
    output = []
    execute(source, output.append)
    assert output


def test_zero_width_non_joiner_literal_and_escape_remain_unchanged():
    value = "فارسی‌زبان"
    assert run(f"چاپ -{value}-") == [value]
    assert run(r"چاپ -الف\-ب-") == ["الف-ب"]
