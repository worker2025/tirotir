import pytest
from tirotir.core import execute

@pytest.mark.parametrize('a,b', [(i, i+1) for i in range(85)])
def test_arithmetic_regression(a,b):
    out=[]
    execute(f'بگذار نتیجه برابر {a} + {b}\nچاپ نتیجه', out.append)
    assert out == [a+b]
