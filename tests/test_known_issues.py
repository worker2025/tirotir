import pytest

from tirotir import Capability, CapabilityError, CapabilityRegistry
from tirotir.core import Call, Func, ast_json, execute, parse, tokenize


def run(source):
    output = []
    execute(source, output.append)
    return output


def test_ki2_preserves_plain_persian_and_zero_width_non_joiner_literals():
    assert run("چاپ -سلام دنیا-") == ["سلام دنیا"]
    value = run("چاپ -فارسی‌زبان-")[0]
    assert value == "فارسی‌زبان"
    assert "\u200c" in value
    assert "_" not in value


def test_ki2_keeps_identifier_normalization_for_arabic_variants():
    # Identifier normalization is distinct from literal preservation.
    assert run("بگذار كليد برابر ۷\nچاپ کلید") == [7]
    assert run("بگذار يک برابر ۸\nچاپ یک") == [8]


def test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized():
    assert [(token.kind, token.value) for token in tokenize("چاپ -سلام دنیا-")] == [
        ("WORD", "چاپ"),
        ("STRING", "سلام دنیا"),
        ("NEWLINE", ""),
        ("EOF", ""),
    ]
    assert run("چاپ ۵ - ۳ + ۲ - ۱") == [3]
    # This is the current legacy behavior and is recorded before any KI-1 fix.
    assert run("چاپ ۵-۳+۲-۱") == [5]


def test_ki1_existing_function_program_remains_unchanged():
    assert run("تابع جمع با الف و ب\n    بازگردان الف + ب\nچاپ جمع با ۲ و ۳") == [5]


def test_ki5_registry_has_positive_and_negative_decisions():
    registry = CapabilityRegistry([Capability.CORE, Capability.GRAPHICS])
    assert registry.allows(Capability.CORE)
    assert registry.allows(Capability.GRAPHICS)
    assert not registry.allows(Capability.GUI)
    with pytest.raises(CapabilityError):
        registry.require(Capability.GUI)


def test_ki5_graphics_execution_path_is_not_currently_bound_to_registry(tmp_path):
    # Characterizes the unresolved issue: execute() has no registry/context and
    # graphics currently runs despite the default registry denying graphics.
    output = tmp_path / "scene.svg"
    execute("مربع با ۱۰", output=lambda _: None, scene_path=str(output))
    assert output.is_file()
    assert "<line" in output.read_text(encoding="utf8")


def test_ki9_square_example_is_a_builtin_name_collision():
    source = "تابع مربع با عدد\n    بازگردان عدد * عدد\nچاپ مربع با ۵"
    tree = parse(source)
    assert isinstance(tree.body[0], Func)
    assert isinstance(tree.body[1].expr, Call)
    assert tree.body[1].expr.name == "مربع"

    # The function body and return expression are valid; the observed None is
    # caused by Interpreter.val dispatching the builtin graphics name first.
    output = []
    execute(source, output.append)
    assert output == [None]
    assert ast_json(tree.body[0].body[0].expr)["op"] == "*"
