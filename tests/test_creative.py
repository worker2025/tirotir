from pathlib import Path
from tirotir.core import execute

def test_repeat_and_svg(tmp_path):
 out=tmp_path/'scene.svg'
 execute('پنجره بازکن با ۳۰۰ و ۳۰۰\nتکرار ۴ بار\n    حرکت با ۱۰\n    چرخش با ۹۰\n',scene_path=str(out))
 text=out.read_text(encoding='utf8')
 assert text.startswith('<svg') and text.count('<line')==4

def test_shapes(tmp_path):
 out=tmp_path/'shape.svg'
 execute('رنگ قلم برابر -قرمز-\nمربع با ۲۰\n',scene_path=str(out))
 text=out.read_text(encoding='utf8')
 assert 'stroke="#dc2626"' in text and 'data-tirotir-color="قرمز"' in text

def test_note(tmp_path,monkeypatch):
 monkeypatch.chdir(tmp_path)
 execute('نت بنواز با ۴۴۰ و ۰٫۰۱')
 assert (tmp_path/'tirotir-note.wav').exists()

def test_emoji():
 out=[];execute('چاپ -سلام 😀-',out.append);assert out==['سلام 😀']
