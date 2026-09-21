from tirotir.core import parse
from tirotir.semantic import SemanticAnalyzer

def analyze(source):
    return SemanticAnalyzer('test.tirotir').analyze(parse(source))

def codes(source):
    return [item.code for item in analyze(source).diagnostics]

def test_undefined_name():
    assert 'TIR2001' in codes('چاپ تعداد')

def test_duplicate_constant():
    assert 'TIR2002' in codes('ثابت x برابر ۱\nثابت x برابر ۲')

def test_constant_assignment():
    assert 'TIR2003' in codes('ثابت x برابر ۱\nx = ۲')

def test_context_errors():
    result=codes('بازگردان ۱\nبیرون\nادامه')
    assert {'TIR2004','TIR2005','TIR2006'} <= set(result)

def test_argument_count_mismatch():
    assert 'TIR2007' in codes('تابع جمع با الف و ب\n    بازگردان الف + ب\nچاپ جمع با ۱')

def test_nested_scope_and_parameter():
    result=analyze('تابع دوبرابر با عدد\n    بازگردان عدد + عدد\nچاپ دوبرابر با ۲')
    assert not result.diagnostics
    assert any(scope.name == 'function:دوبرابر' for scope in result.symbols.scopes)

def test_recursive_function_is_resolved_before_body():
    result=analyze('تابع شمارش با عدد\n    اگر عدد > ۰\n        بازگردان شمارش با عدد - ۱\n    بازگردان ۰\nچاپ شمارش با ۳')
    assert not result.diagnostics

def test_analysis_has_no_runtime_side_effect(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result=analyze('نت بنواز با ۴۴۰ و ۰٫۰۱\nچاپ ناشناخته')
    assert result.diagnostics and not (tmp_path/'tirotir-note.wav').exists()
