from pathlib import Path

import pytest

from tirotir import CapabilityError, CapabilityRegistry, RuntimeContext, execute
from tirotir.builder import make_entry_launcher
from tirotir.cli import main


def test_direct_graphics_denied_without_side_effect(tmp_path):
    output = tmp_path / "scene.svg"
    with pytest.raises(CapabilityError, match="graphics"):
        execute("مربع با ۱۰", output=lambda _: None, scene_path=str(output))
    assert not output.exists()


def test_direct_graphics_allowed_with_explicit_capability(tmp_path):
    output = tmp_path / "scene.svg"
    execute("مربع با ۱۰", output=lambda _: None, scene_path=str(output), capabilities=["graphics"])
    assert output.read_text(encoding="utf8").count("<line") == 4


def test_direct_audio_denied_without_wav_side_effect(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(CapabilityError, match="audio"):
        execute("نت بنواز با ۴۴۰ و ۰٫۰۱")
    assert not (tmp_path / "tirotir-note.wav").exists()


def test_direct_audio_allowed_with_explicit_context(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    context = RuntimeContext.from_capabilities(["audio"], project_root=str(tmp_path))
    execute("نت بنواز با ۴۴۰ و ۰٫۰۱", runtime_context=context)
    assert (tmp_path / "tirotir-note.wav").is_file()


def test_direct_gui_denied_before_backend_creation():
    with pytest.raises(CapabilityError, match="gui"):
        execute("پنجره بساز با -برنامه- و ۳۲۰ و ۲۰۰")


def test_cli_graphics_command_is_explicit_consent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "shape.t"
    source.write_text("مربع با ۱۰\n", encoding="utf8")
    output = tmp_path / "shape.svg"
    assert main(["graphics", str(source), "--scene", str(output)]) == 0
    assert output.is_file()


def test_cli_run_denies_graphics_without_capability(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "shape.t"
    source.write_text("مربع با ۱۰\n", encoding="utf8")
    assert main(["run", str(source)]) == 1
    assert not (tmp_path / "tirotir-scene.svg").exists()


def test_project_config_controls_graphics(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.t").write_text("مربع با ۱۰\n", encoding="utf8")
    (tmp_path / "tirotir.toml").write_text(
        '[project]\nname="demo"\nentry="main.t"\n'
        '[capabilities]\ngraphics=true\naudio=false\ngui=false\n',
        encoding="utf8",
    )
    assert main(["run"]) == 0
    assert (tmp_path / "tirotir-scene.svg").is_file()


def test_project_config_denies_graphics_when_false(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.t").write_text("مربع با ۱۰\n", encoding="utf8")
    (tmp_path / "tirotir.toml").write_text(
        '[project]\nname="demo"\nentry="main.t"\n'
        '[capabilities]\ngraphics=false\n',
        encoding="utf8",
    )
    assert main(["run"]) == 1
    assert not (tmp_path / "tirotir-scene.svg").exists()


def test_project_config_rejects_unknown_capability(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.t").write_text("چاپ -سلام-\n", encoding="utf8")
    (tmp_path / "tirotir.toml").write_text(
        '[project]\nname="demo"\nentry="main.t"\n'
        '[capabilities]\ntelepathy=true\n',
        encoding="utf8",
    )
    assert main(["run"]) == 1


def test_builder_launcher_is_core_only_by_default(tmp_path):
    entry = tmp_path / "main.t"
    entry.write_text("مربع با ۱۰\n", encoding="utf8")
    generated = make_entry_launcher(entry, tmp_path)
    assert "RuntimeContext.from_capabilities([])" in generated.read_text(encoding="utf8")


def test_builder_launcher_can_receive_explicit_audio_capability(tmp_path, monkeypatch):
    entry = tmp_path / "main.t"
    entry.write_text("نت بنواز با ۴۴۰ و ۰٫۰۱\n", encoding="utf8")
    generated = make_entry_launcher(entry, tmp_path, capabilities=["audio"])
    monkeypatch.chdir(tmp_path)
    namespace = {"__name__": "__main__", "__file__": str(generated)}
    exec(compile(generated.read_text(encoding="utf8"), str(generated), "exec"), namespace)
    assert (tmp_path / "tirotir-note.wav").is_file()


def test_runtime_context_rejects_conflicting_policies():
    with pytest.raises(CapabilityError, match="هم‌زمان"):
        execute("چاپ -x-", capabilities=["graphics"], runtime_context=RuntimeContext())


def test_registry_from_mapping_keeps_core_and_validates_values():
    registry = CapabilityRegistry.from_mapping({"graphics": True, "audio": "false"})
    assert registry.allows("core")
    assert registry.allows("graphics")
    assert not registry.allows("audio")
