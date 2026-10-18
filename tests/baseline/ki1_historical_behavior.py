"""Historical KI-1 characterization; run only against the original baseline checkout.

This file intentionally does not match pytest's default test-file pattern in the
candidate tree. The assertion is preserved verbatim in meaning: the old lexer
reported 5 for compact subtraction.
"""

from tirotir.core import execute, tokenize


def run(source):
    output = []
    execute(source, output.append)
    return output


def test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized():
    assert [(token.kind, token.value) for token in tokenize("چاپ -سلام دنیا-")] == [
        ("WORD", "چاپ"),
        ("STRING", "سلام دنیا"),
        ("NEWLINE", ""),
        ("EOF", ""),
    ]
    assert run("چاپ ۵ - ۳ + ۲ - ۱") == [3]
    # This is the historical behavior recorded before the KI-1 fix.
    assert run("چاپ ۵-۳+۲-۱") == [5]


if __name__ == "__main__":
    test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized()
    print("historical KI-1 assertion passed")
