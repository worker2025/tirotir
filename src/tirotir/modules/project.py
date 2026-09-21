from dataclasses import dataclass
from pathlib import Path
import tomllib

@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    name: str
    entry: str
    language: str
    capabilities: dict[str, bool|str]

def load_project(path: str|Path) -> ProjectConfig:
    config_path=Path(path)
    if config_path.is_dir(): config_path=config_path/'tirotir.toml'
    config_path=config_path.resolve()
    data=tomllib.loads(config_path.read_text(encoding='utf-8'))
    project=data.get('project',{})
    return ProjectConfig(config_path.parent, str(project.get('name',config_path.parent.name)), str(project.get('entry','main.t')), str(project.get('language','2.0')), dict(data.get('capabilities',{})))
