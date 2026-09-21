from pathlib import Path
from .model import ModuleId

class ModuleSecurityError(PermissionError): pass

class ModuleSandbox:
    def __init__(self, project_root: str|Path):
        self.project_root = Path(project_root).resolve()
        if not self.project_root.exists(): raise ModuleSecurityError('ریشهٔ پروژه وجود ندارد.')

    def canonical(self, path: str|Path) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute(): candidate = self.project_root / candidate
        return candidate.resolve()

    def ensure_inside(self, path: str|Path) -> Path:
        canonical = self.canonical(path)
        try: canonical.relative_to(self.project_root)
        except ValueError: raise ModuleSecurityError(f'مسیر ماژول خارج از پروژه مجاز نیست: {path}')
        return canonical

    def module_id(self, path: str|Path) -> ModuleId:
        canonical = self.ensure_inside(path)
        return ModuleId(self.project_root, canonical)
