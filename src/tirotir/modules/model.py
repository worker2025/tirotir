from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True, order=True)
class ModuleId:
    project_root: Path
    canonical_path: Path

    def __post_init__(self):
        object.__setattr__(self, 'project_root', Path(self.project_root).resolve())
        object.__setattr__(self, 'canonical_path', Path(self.canonical_path).resolve())

    @property
    def namespace(self) -> str:
        try: return self.canonical_path.relative_to(self.project_root).with_suffix('').as_posix().replace('/', '.')
        except ValueError: return self.canonical_path.stem

@dataclass(frozen=True)
class ModuleSpec:
    module_id: ModuleId
    imports: tuple[str, ...] = ()
    source: str = ''

@dataclass
class ModuleGraph:
    nodes: dict[ModuleId, ModuleSpec] = field(default_factory=dict)
    edges: dict[ModuleId, tuple[ModuleId, ...]] = field(default_factory=dict)

    def add(self, spec: ModuleSpec, dependencies: Iterable[ModuleId] = ()):
        self.nodes[spec.module_id] = spec
        self.edges[spec.module_id] = tuple(dependencies)

    def dependencies(self, module_id: ModuleId) -> tuple[ModuleId, ...]:
        return self.edges.get(module_id, ())

    def topological_order(self) -> list[ModuleId]:
        temporary, permanent, result = set(), set(), []
        def visit(node):
            if node in temporary: raise ValueError('cycle')
            if node in permanent: return
            temporary.add(node)
            for dep in self.dependencies(node): visit(dep)
            temporary.remove(node); permanent.add(node); result.append(node)
        for node in self.nodes: visit(node)
        return result
