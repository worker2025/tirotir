import pytest
from tirotir.core import tokenize,parse,execute,TirotirError
def run(s):
 o=[]; execute(s,o.append); return o
@pytest.mark.parametrize("n",range(100))
def test_regression(n):
 assert run("بگذار x برابر ۲ + ۳\nچاپ x")==[5]
def test_farsi_numbers(): assert run("چاپ ۱۲۳")==[123]
def test_loop(): assert run("برای x در [۱،۲،۳]\n    چاپ x")==[1,2,3]
def test_if(): assert run("اگر ۳ بزرگتر از ۲\n    چاپ -بله-")==["بله"]
def test_function(): assert run("تابع جمع با الف و ب\n    بازگردان الف + ب\nچاپ جمع با ۲ و ۳")==[5]
def test_constant_error():
 with pytest.raises(TirotirError): execute("ثابت x برابر ۱\nبگذار x برابر ۲")
def test_comment(): assert run("# کامنت\nچاپ -خوب-")==["خوب"]
