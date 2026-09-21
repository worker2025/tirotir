from pathlib import Path
import pytest
from tirotir.modules import ModuleCache, ModuleGraphBuilder, ModuleLoader, ModuleSecurityError, load_project

def project(tmp_path):
    (tmp_path/'lib').mkdir()
    (tmp_path/'main.tirotir').write_text('وارد کن -lib/tools-\nچاپ -main-\n',encoding='utf8')
    (tmp_path/'lib/tools.tirotir').write_text('چاپ -tools-\n',encoding='utf8')
    return tmp_path

def test_module_id_is_canonical(tmp_path):
    root=project(tmp_path); loader=ModuleLoader(root)
    entry=loader.sandbox.module_id(root/'main.tirotir')
    resolved=loader.resolve(entry,'lib/../lib/tools')
    assert resolved.canonical_path==(root/'lib/tools.tirotir').resolve()
    assert resolved.namespace=='lib.tools'

def test_sandbox_rejects_escape(tmp_path):
    root=project(tmp_path); loader=ModuleLoader(root)
    with pytest.raises(ModuleSecurityError): loader.sandbox.module_id(root/'../../secret.tirotir')

def test_loader_only_loads_and_parses(tmp_path):
    root=project(tmp_path); loader=ModuleLoader(root); mid=loader.sandbox.module_id(root/'main.tirotir')
    assert loader.spec(mid).imports==('lib/tools',)
    assert loader.parse(mid).body

def test_graph_and_topological_order(tmp_path, capsys):
    root=project(tmp_path); loader=ModuleLoader(root); entry=loader.sandbox.module_id(root/'main.tirotir')
    graph, diagnostics=ModuleGraphBuilder(loader).build(entry)
    assert not diagnostics and [x.namespace for x in graph.topological_order()]==['lib.tools','main']
    assert capsys.readouterr().out == ''

def test_cycle_diagnostic(tmp_path):
    (tmp_path/'a.tirotir').write_text('وارد کن -b-\n',encoding='utf8')
    (tmp_path/'b.tirotir').write_text('وارد کن -a-\n',encoding='utf8')
    loader=ModuleLoader(tmp_path); graph, diagnostics=ModuleGraphBuilder(loader).build(loader.sandbox.module_id(tmp_path/'a.tirotir'))
    assert any(d.code=='TIR3001' for d in diagnostics)

def test_module_cache_loads_once(tmp_path):
    cache=ModuleCache(); calls=[]; mid=ModuleLoader(tmp_path).sandbox.module_id(tmp_path/'main.tirotir') if tmp_path.exists() else None
    value=lambda _: calls.append(1) or 'ok'
    assert cache.get_or_load(mid,value)=='ok' and cache.get_or_load(mid,value)=='ok'
    assert calls==[1]

def test_project_config(tmp_path):
    (tmp_path/'tirotir.toml').write_text('[project]\nname="demo"\nentry="main.t"\n[capabilities]\ngraphics=false\n',encoding='utf8')
    config=load_project(tmp_path)
    assert config.name=='demo' and config.entry=='main.t' and config.capabilities['graphics'] is False
