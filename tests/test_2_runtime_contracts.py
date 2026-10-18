import json
from pathlib import Path
import builtins
import tomllib

from tirotir import __version__
from tirotir.cli import VERSION, main


ROOT = Path(__file__).parents[1]


def test_candidate_version_is_consistent_across_runtime_and_manifests():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf8"))
    extension = json.loads((ROOT / "vscode-tirotirLang/package.json").read_text(encoding="utf8"))
    assert __version__ == VERSION == metadata["project"]["version"] == "2.0.0.dev0"
    assert extension["version"] == "2.0.0-dev"
    assert metadata["project"]["requires-python"] == ">=3.11"


def test_cli_reports_version_from_package(capsys):
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == "Tirotir 2.0.0.dev0"


def test_cli_reports_eof_as_user_error_without_traceback(tmp_path, monkeypatch, capsys):
    source = tmp_path / "input.t"
    source.write_text("بخوان\n", encoding="utf8")

    def eof():
        raise EOFError

    monkeypatch.setattr(builtins, "input", eof)
    assert main(["run", str(source)]) == 1
    captured = capsys.readouterr()
    assert "ورودی استاندارد" in captured.err
    assert "Traceback" not in captured.err
