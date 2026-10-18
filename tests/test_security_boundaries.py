from pathlib import Path

import pytest

from tirotir.contracts import Capability, CapabilityError, RuntimeContext
from tirotir.core import RuntimeErrorFa, execute
from tirotir.modules import ModuleLoader, ModuleSecurityError


def test_network_and_project_files_are_denied_by_default():
    context = RuntimeContext()
    with pytest.raises(CapabilityError, match="network"):
        context.require(Capability.NETWORK)
    with pytest.raises(CapabilityError, match="project-files"):
        context.require(Capability.PROJECT_FILES)


def test_explicit_unimplemented_capabilities_do_not_create_language_backends():
    context = RuntimeContext.from_capabilities(["network", "project-files"])
    context.require("network")
    context.require("project-files")
    with pytest.raises(RuntimeErrorFa, match="تعریف نشده"):
        execute("شبکه با -https://example.invalid-", runtime_context=context)
    with pytest.raises(RuntimeErrorFa, match="تعریف نشده"):
        execute("خواندن_فایل با -secret.txt-", runtime_context=context)


def test_module_sandbox_rejects_absolute_and_parent_escape(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    loader = ModuleLoader(root)
    for candidate in (tmp_path / "outside.t", root / "nested" / ".." / ".." / "outside.t"):
        with pytest.raises(ModuleSecurityError):
            loader.sandbox.module_id(candidate)


def test_module_sandbox_rejects_symlink_escape(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.t").write_text("چاپ -secret-\n", encoding="utf8")
    link = root / "linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable in this environment")
    with pytest.raises(ModuleSecurityError):
        ModuleLoader(root).sandbox.module_id(link / "secret.t")


def test_project_root_remains_the_only_module_file_boundary(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    entry = root / "main.t"
    entry.write_text("چاپ -ok-\n", encoding="utf8")
    loader = ModuleLoader(root)
    module_id = loader.sandbox.module_id(entry)
    assert loader.load(module_id) == "چاپ -ok-\n"
    assert Path(module_id.canonical_path).is_relative_to(root.resolve())
