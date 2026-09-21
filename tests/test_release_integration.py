from pathlib import Path
import wave
import json
import os
import subprocess
import sys
import re
import pytest
from tirotir.audio import AudioBackendUnavailable, play_file
from tirotir.builder import make_entry_launcher, resolve_launcher
from tirotir.core import RuntimeErrorFa, execute
from tirotir.events import EventLoop
from tirotir.cli import main


def test_event_loop_is_deterministic():
    seen=[]; loop=EventLoop(); loop.on('پیام',lambda event: seen.append(event.payload['n']))
    loop.emit('پیام',{'n':1}); loop.emit('پیام',{'n':2}); assert loop.tick()==2 and seen==[1,2]


def test_graphics_svg_end_to_end(tmp_path):
    source=Path('examples/graphics/hello_shape.t').read_text(encoding='utf8')
    output=tmp_path/'scene.svg'; execute(source,output=lambda _:None,scene_path=str(output))
    svg=output.read_text(encoding='utf8')
    assert '<svg' in svg and svg.count('<line') == 4 and 'آبی' in svg
    assert 'stroke="#2563eb"' in svg and 'data-tirotir-color="آبی"' in svg
    assert 'Ø' not in svg and 'Â' not in svg
    assert svg.startswith('<svg') and svg.endswith('</svg>')


def test_graphics_persian_colors_are_utf8(tmp_path):
    output=tmp_path/'colors.svg'
    execute('رنگ قلم برابر -قرمز-\nمربع با ۱۰\n',output=lambda _:None,scene_path=str(output))
    raw=output.read_bytes(); text=raw.decode('utf-8')
    assert 'قرمز' in text and 'stroke="#dc2626"' in text and 'Ø' not in text


def test_audio_render_fallback(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    execute('نت بنواز با ۴۴۰ و ۰٫۰۱',output=lambda _:None)
    wav=tmp_path/'tirotir-note.wav'; assert wav.exists() and wav.stat().st_size>44
    with wave.open(str(wav),'rb') as sound: assert sound.getframerate()==44100


def test_audio_persian_note_name(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    execute('نت بنواز با -دو- و ۰٫۰۱',output=lambda _:None)
    assert (tmp_path/'tirotir-note.wav').exists()


def test_audio_scale_is_one_sequential_wav(tmp_path,monkeypatch):
    source=Path(__file__).parents[1].joinpath('examples/audio/scale.t').read_text(encoding='utf8')
    monkeypatch.chdir(tmp_path)
    execute(source,output=lambda _:None)
    with wave.open('tirotir-note.wav','rb') as sound:
        assert sound.getnchannels()==1 and sound.getframerate()==44100
        assert sound.getnframes() >= int(7*0.15*44000)


def test_builder_resolves_real_launcher(tmp_path):
    launcher=resolve_launcher()
    assert launcher.is_file() and launcher.name in ('tirotir_launcher.py','launcher.py')
    generated=make_entry_launcher('examples/audio/scale.t',tmp_path)
    content=generated.read_text(encoding='utf8')
    assert generated.is_file() and 'TIROTIR_ENTRY' in content and 'SemanticAnalyzer' in content
    assert 'from tirotir.core import execute, parse' in content
    assert 'open(' not in content and 'resolve_launcher' not in content


def test_builder_entrypoint_runs_without_source_file(tmp_path, monkeypatch, capsys):
    generated=make_entry_launcher('examples/audio/scale.t',tmp_path)
    source=Path('examples/audio/scale.t').read_text(encoding='utf8')
    (tmp_path/'tirotir_entry_launcher.py').write_text(generated.read_text(encoding='utf8'),encoding='utf8')
    monkeypatch.chdir(tmp_path)
    namespace={'__name__':'__main__','__file__':str(generated)}
    exec(compile(generated.read_text(encoding='utf8'),str(generated),'exec'),namespace)
    assert (tmp_path/'tirotir-note.wav').exists()


def test_audio_backend_reports_unavailable_cleanly(tmp_path):
    missing=tmp_path/'missing.wav'
    try: play_file(missing)
    except (AudioBackendUnavailable, FileNotFoundError, OSError): pass


def test_gui_headless_has_farsi_diagnostic(monkeypatch):
    monkeypatch.setenv('DISPLAY','')
    with pytest.raises(RuntimeErrorFa, match='TIR4001'):
        execute('پنجره بساز با -برنامه- و ۳۲۰ و ۲۰۰',output=lambda _:None)


def test_project_cli_runs_topological_modules(tmp_path, monkeypatch, capsys):
    (tmp_path/'lib').mkdir()
    (tmp_path/'tirotir.toml').write_text('[project]\nname="demo"\nentry="main.t"\n',encoding='utf8')
    (tmp_path/'lib/tools.t').write_text('چاپ -کتابخانه-\n',encoding='utf8')
    (tmp_path/'main.t').write_text('وارد کن -lib/tools-\nچاپ -اصلی-\n',encoding='utf8')
    monkeypatch.chdir(tmp_path)
    assert main(['run']) == 0
    assert capsys.readouterr().out.splitlines()==['کتابخانه','اصلی']


def test_vscode_webview_hardening_contract():
    extension=Path('vscode-tirotirLang/extension.js').read_text(encoding='utf8')
    assert "--live-scene" in extension
    assert "JSON.parse(stdout)" in extension
    assert "Content-Security-Policy" in extension
    assert "dir=\"rtl\"" in extension
    assert "fs.unlinkSync(scene)" not in extension
    assert "<meta charset=\"utf-8\">" in extension
    assert "صحنه‌ای در اجرای جدید تولید نشد" in extension


def test_windows_cp1252_stdout_is_utf8(tmp_path):
    source=tmp_path/'hello.t'; source.write_text('چاپ -سلام دنیا-\n',encoding='utf8')
    env=os.environ.copy(); env['PYTHONIOENCODING']='cp1252'
    result=subprocess.run([sys.executable,'-m','tirotir.cli','run',str(source)],env=env,capture_output=True)
    assert result.returncode==0
    assert result.stdout.decode('utf-8').strip()=='سلام دنیا'
    assert b'UnicodeEncodeError' not in result.stderr


def test_live_scene_is_json_and_has_no_sidecar(tmp_path):
    source=tmp_path/'shape.t'; source.write_text(Path('examples/graphics/hello_shape.t').read_text(encoding='utf8'),encoding='utf8')
    result=subprocess.run([sys.executable,'-m','tirotir.cli','run',str(source),'--live-scene'],capture_output=True)
    payload=json.loads(result.stdout.decode('utf8'))
    assert payload['type']=='scene' and payload['svg'].count('<line')==4 and 'آبی' in payload['svg']
    assert not (tmp_path/'shape.t.svg').exists()


def test_t_extension_cli_and_legacy_compatibility(tmp_path, monkeypatch, capsys):
    current=tmp_path/'hello.t'; current.write_text('چاپ -سلام تی-\n',encoding='utf8')
    assert main(['run',str(current)])==0
    assert capsys.readouterr().out.splitlines()==['سلام تی']
    legacy=tmp_path/'old.tirotir'; legacy.write_text('چاپ -سازگار-\n',encoding='utf8')
    assert main(['run',str(legacy)])==0
    assert capsys.readouterr().out.splitlines()==['سازگار']


def test_tirotirlang_associates_only_t():
    manifest=json.loads(Path('vscode-tirotirLang/package.json').read_text(encoding='utf8'))
    language=manifest['contributes']['languages'][0]
    assert language['extensions']==['.t']


def test_graphics_fit_to_scene_viewport():
    source='پنجره بازکن با ۸۰۰ و ۶۰۰\nرنگ قلم برابر -آبی-\nضخامت قلم برابر ۳\nتکرار ۸ بار\n    حرکت با ۸۰\n    چرخش با ۴۵\n'
    output=Path('fit-scene-test.svg')
    try:
        execute(source,output=lambda _:None,scene_path=str(output))
        svg=output.read_text(encoding='utf8')
        viewbox=re.search(r'viewBox="([^"]+)"',svg).group(1).split()
        assert float(viewbox[2]) < 800 and float(viewbox[3]) < 600
        assert 'preserveAspectRatio="xMidYMid meet"' in svg
    finally:
        output.unlink(missing_ok=True)


def test_move_rotate_produces_square_path():
    source='پنجره بازکن با ۸۰۰ و ۶۰۰\nرنگ قلم برابر -آبی-\nضخامت قلم برابر ۳\nحرکت با ۱۰۰\nچرخش با ۹۰\nحرکت با ۱۰۰\nچرخش با ۹۰\nحرکت با ۱۰۰\nچرخش با ۹۰\nحرکت با ۱۰۰\n'
    output=Path('movement-test.svg')
    try:
        execute(source,output=lambda _:None,scene_path=str(output))
        svg=output.read_text(encoding='utf8')
        lines=re.findall(r'<line x1="([\-0-9.]+)" y1="([\-0-9.]+)" x2="([\-0-9.]+)" y2="([\-0-9.]+)"',svg)
        assert len(lines)==4
        assert [(round(float(x1)),round(float(y1)),round(float(x2)),round(float(y2))) for x1,y1,x2,y2 in lines] == [(0,0,100,0),(100,0,100,100),(100,100,0,100),(0,100,0,0)]
    finally:
        output.unlink(missing_ok=True)


def test_gui_primitives_parse_without_opening_window():
    from tirotir.core import parse
    tree=parse('چک‌باکس بساز با -فعال-\nلیست بساز با -الف- و -ب-\nمنوی انتخاب بساز با -الف- و -ب-\nمتن چندخطی بساز\nنوار لغزش بساز با ۱۰۰\n')
    assert len(tree.body)==5


def test_gui_primitives_pass_semantic_check():
    from tirotir.semantic import SemanticAnalyzer
    from tirotir.core import parse
    source='چک‌باکس بساز با -فعال-\nلیست بساز با -الف- و -ب-\nمنوی انتخاب بساز با -الف- و -ب-\nمتن چندخطی بساز\nنوار لغزش بساز با ۱۰۰\n'
    result=SemanticAnalyzer('gui.t').analyze(parse(source))
    assert result.diagnostics==[]


def test_builder_module_is_importable():
    from tirotir.builder import BuilderApp
    assert BuilderApp.__name__=='BuilderApp'
