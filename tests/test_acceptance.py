import pytest
from tirotir.core import execute, TirotirError

def run(src, inputs=None):
 out=[]; vals=iter(inputs or [])
 execute(src, out.append, lambda: next(vals))
 return out

def test_equals_assignment_and_typo_is_error():
 assert run('بگذار نتیجه برابر ۱۰ + ۵\nچاپ نتیجه\nنتیجه = نتیجه + ۱\nچاپ نتیجه') == [15,16]
 with pytest.raises(TirotirError): run('چاپ نتیچه')

def test_list_index_and_mutation():
 assert run('بگذار اعداد برابر [۱، ۲، ۳]\nچاپ اعداد[۰]\nاعداد[۱] = ۹\nچاپ اعداد[۱]') == [1,9]

def test_dictionary():
 src='بگذار شخص برابر فرهنگ\n    نام برابر -سارا-\n    سن برابر ۲۴\nچاپ شخص نام\nچاپ شخص[سن]'
 assert run(src)==['سارا',24]

def test_while_break_continue():
 src='بگذار شمارنده برابر ۰\nتاوقتی شمارنده کوچکتر از ۵\n    بگذار شمارنده برابر شمارنده + ۱\n    اگر شمارنده == ۳\n        بیرون\n    چاپ شمارنده'
 assert run(src)==[1,2]

def test_input_expression():
 assert run('بگذار نام برابر بخوان\nچاپ نام', ['سارا']) == ['سارا']

def test_comparison_phrases():
 assert run('اگر ۵ بزرگتر یا مساوی ۵\n    چاپ -درست-') == ['درست']

def test_infinite_loop_protection():
 with pytest.raises(TirotirError): run('تاوقتی درست\n    چاپ -x-')
