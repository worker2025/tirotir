import re
from pathlib import Path
from .model import ModuleId, ModuleSpec
from .sandbox import ModuleSandbox, ModuleSecurityError
from ..core import parse

class ModuleLoadError(Exception): pass

_IMPORT_RE = re.compile(r'^\s*وارد\s+کن\s+-([^\n-]+)-\s*$', re.MULTILINE)

class ModuleLoader:
    """فقط resolve/load/parse؛ هرگز semantic analysis یا execution نمی‌کند."""
    def __init__(self, project_root: str|Path):
        self.sandbox = ModuleSandbox(project_root)

    def resolve(self, importer: ModuleId, import_name: str) -> ModuleId:
        name = import_name.strip().replace('\\','/')
        if not name.endswith(('.t','.tirotir')):
            primary=name+'.t'; legacy=name+'.tirotir'
            base = importer.canonical_path.parent if importer else self.sandbox.project_root
            candidate=self.sandbox.ensure_inside(base/primary)
            name=primary if candidate.exists() else legacy
        base = importer.canonical_path.parent if importer else self.sandbox.project_root
        return self.sandbox.module_id(base / name)

    def load(self, module_id: ModuleId) -> str:
        path = self.sandbox.ensure_inside(module_id.canonical_path)
        if not path.is_file(): raise ModuleLoadError(f'ماژول پیدا نشد: {path}')
        try: return path.read_text(encoding='utf-8')
        except OSError as exc: raise ModuleLoadError(f'خواندن ماژول ممکن نیست: {path}') from exc

    def parse(self, module_id: ModuleId):
        return parse(self.load(module_id))

    def spec(self, module_id: ModuleId) -> ModuleSpec:
        source = self.load(module_id)
        imports = tuple(match.group(1).strip() for match in _IMPORT_RE.finditer(source))
        return ModuleSpec(module_id, imports, source)
