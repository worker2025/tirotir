import argparse, json, os, sys, tempfile
from .core import parse, execute, ast_json, TirotirError
from .semantic import SemanticAnalyzer
from .modules import ModuleGraphBuilder, ModuleLoader, load_project

VERSION='1.1.0'

def configure_utf8_stdio():
    """روی Windows/PowerShell و pipeها UTF-8 را ترجیح می‌دهد، بدون شکستن stream سفارشی."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='backslashreplace')
        except (AttributeError, ValueError):
            pass

def write_utf8(stream, text, end='\n'):
    value=str(text)+end
    try:
        stream.write(value); stream.flush(); return
    except UnicodeEncodeError:
        buffer=getattr(stream, 'buffer', None)
        if buffer is not None:
            buffer.write(value.encode('utf-8', errors='backslashreplace')); buffer.flush(); return
        # Streamهای سفارشی بدون buffer نباید اجرای interpreter را متوقف کنند.
        stream.write(value.encode('utf-8', errors='backslashreplace').decode('latin1')); stream.flush()

def output_writer():
    return lambda value: write_utf8(sys.stdout, value)

def error_writer(value):
    write_utf8(sys.stderr, value)

def run_live(source, play_audio=False):
    fd, path=tempfile.mkstemp(prefix='tirotir-live-', suffix='.svg')
    os.close(fd)
    output=[]
    try:
        execute(source, output=output.append, scene_path=path, play_audio=play_audio)
        svg=open(path, encoding='utf-8').read() if os.path.exists(path) else ''
        return {'type':'scene','width':800,'height':600,'stdout':'\n'.join(map(str,output)), 'svg':svg}
    finally:
        try: os.unlink(path)
        except FileNotFoundError: pass

def main(argv=None):
    configure_utf8_stdio()
    p=argparse.ArgumentParser(prog='tirotir',add_help=False)
    p.add_argument('command',nargs='?'); p.add_argument('file',nargs='?')
    p.add_argument('--write',action='store_true'); p.add_argument('--scene',default=None)
    p.add_argument('--play-audio',action='store_true'); p.add_argument('--live-scene',action='store_true')
    a=p.parse_args(argv)
    try:
        if a.command and a.command.endswith(('.t','.tirotir')) and a.file is None:
            a.file=a.command; a.command='run'
        if a.command in ('version','--version'):
            write_utf8(sys.stdout,f'Tirotir {VERSION}'); return 0
        if a.command in ('help','--help',None):
            write_utf8(sys.stdout,'تیروتیر ۱٫۱\nاستفاده: tirotir run FILE | project | graphics FILE | audio FILE | gui FILE | builder | check FILE | ast FILE | format FILE | repl'); return 0
        if a.command in ('builder','build-gui'):
            from .builder import main as builder_main
            builder_main(); return 0
        if a.command=='repl':
            write_utf8(sys.stdout,'REPL تیروتیر ۱٫۱ — برای خروج «خروج» بنویسید.')
            while True:
                try:s=input('تیروتیر> ')
                except EOFError:break
                if s.strip()=='خروج':break
                try: execute(s,output_writer())
                except TirotirError as e: error_writer(e)
            return 0
        if a.command=='project':
            config=load_project(a.file or '.')
            write_utf8(sys.stdout,f'پروژه: {config.name}\nورودی: {config.entry}\nزبان: {config.language}'); return 0
        if not a.file and a.command=='run':
            config=load_project('.')
            loader=ModuleLoader(config.root); entry=loader.sandbox.module_id(config.root/config.entry)
            graph, diagnostics=ModuleGraphBuilder(loader).build(entry)
            if diagnostics:
                for diagnostic in diagnostics:error_writer(f'{diagnostic.code}: {diagnostic.message}')
                return 1
            for module_id in graph.topological_order():
                source=loader.load(module_id); result=SemanticAnalyzer(str(module_id.canonical_path)).analyze(parse(source))
                if result.diagnostics:
                    for diagnostic in result.diagnostics:error_writer(f'{diagnostic.code}: {diagnostic.message}')
                    return 1
            for module_id in graph.topological_order():execute(loader.load(module_id),output_writer(),scene_path=a.scene,play_audio=a.play_audio)
            return 0
        if not a.file: error_writer('نام فایل لازم است.'); return 2
        src=open(a.file,encoding='utf-8').read(); tree=parse(src)
        semantic=SemanticAnalyzer(a.file).analyze(tree)
        if semantic.diagnostics and a.command in ('check','run','graphics','audio','gui'):
            for diagnostic in semantic.diagnostics:error_writer(f'{diagnostic.code}: {diagnostic.message}\nپیشنهاد: {diagnostic.suggestion or ""}')
            return 1
        if a.live_scene:
            write_utf8(sys.stdout,json.dumps(run_live(src,play_audio=a.play_audio),ensure_ascii=False,separators=(',',':'))); return 0
        if a.command=='ast': write_utf8(sys.stdout,json.dumps(ast_json(tree),ensure_ascii=False,indent=2))
        elif a.command=='check': write_utf8(sys.stdout,'برنامه صحیح است.')
        elif a.command=='format':
            text='\n'.join(x.rstrip() for x in src.replace('\r\n','\n').split('\n'))+'\n'
            if a.write: open(a.file,'w',encoding='utf8').write(text)
            else: write_utf8(sys.stdout,text,end='')
        elif a.command in ('run','graphics','audio','gui',a.file):
            scene=a.scene or (a.file+'.svg' if a.command=='graphics' else None)
            execute(src,output_writer(),scene_path=scene,play_audio=(a.play_audio or a.command=='audio'))
        else: error_writer('فرمان ناشناخته است.'); return 2
        return 0
    except (OSError,TirotirError) as e:
        error_writer(f'خطا: {e}'); return 1

if __name__=='__main__':sys.exit(main())
