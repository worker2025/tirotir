from .model import ModuleGraph, ModuleId
from .loader import ModuleLoader, ModuleLoadError
from ..contracts import Diagnostic, SourceSpan

class ModuleCycleError(Exception):
    def __init__(self, cycle): self.cycle=tuple(cycle); super().__init__('چرخهٔ وابستگی ماژول‌ها')

class ModuleGraphBuilder:
    def __init__(self, loader: ModuleLoader): self.loader=loader

    def build(self, entry: ModuleId) -> tuple[ModuleGraph, list[Diagnostic]]:
        graph=ModuleGraph(); diagnostics=[]; visiting=[]; visited=set()
        def visit(module_id):
            if module_id in visiting:
                cycle=visiting[visiting.index(module_id):]+[module_id]
                names=' → '.join(item.namespace for item in cycle)
                diagnostics.append(Diagnostic('TIR3001','error','module_cycle',f'چرخهٔ وابستگی ماژول‌ها: {names}',SourceSpan(str(module_id.canonical_path))))
                return
            if module_id in visited:return
            visiting.append(module_id)
            try: spec=self.loader.spec(module_id)
            except ModuleLoadError as exc:
                diagnostics.append(Diagnostic('TIR3002','error','module_not_found',str(exc),SourceSpan(str(module_id.canonical_path))))
                visiting.pop();visited.add(module_id);return
            deps=[]
            for name in spec.imports:
                try: dep=self.loader.resolve(module_id,name); deps.append(dep); visit(dep)
                except Exception as exc: diagnostics.append(Diagnostic('TIR3003','error','module_path',str(exc),SourceSpan(str(module_id.canonical_path))))
            graph.add(spec,deps); visiting.pop();visited.add(module_id)
        visit(entry)
        return graph, diagnostics
