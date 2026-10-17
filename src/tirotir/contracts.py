"""قراردادهای پایدار معماری تیروتیر ۲٫۰.

این ماژول باید مستقل از parser، interpreter و backendها بماند تا ابزارها
بتوانند قراردادهای زبان را بدون اجرای برنامه مصرف کنند.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence

CONTRACT_VERSION = "2.0-contract-1"
LANGUAGE_V1 = "1.1"

@dataclass(frozen=True)
class SourceSpan:
    """محدودهٔ دقیق یک token، node یا diagnostic در متن منبع."""
    source: str = "<متن>"
    start_line: int = 1
    start_column: int = 1
    end_line: int = 1
    end_column: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "start": {"line": self.start_line, "column": self.start_column},
            "end": {"line": self.end_line, "column": self.end_column},
        }

@dataclass(frozen=True)
class NodeId:
    """شناسهٔ پایدار در طول یک parse برای ابزار formatter و debugger."""
    value: str

    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class Diagnostic:
    """خطای قابل مصرف برای CLI، LSP و محیط آموزشی."""
    code: str
    severity: str
    type: str
    message: str
    span: SourceSpan = field(default_factory=SourceSpan)
    suggestion: str | None = None
    source_text: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "code": self.code,
            "severity": self.severity,
            "type": self.type,
            "message": self.message,
            "span": self.span.to_dict(),
        }
        if self.suggestion is not None:
            result["suggestion"] = self.suggestion
        if self.source_text is not None:
            result["source_text"] = self.source_text
        return result

class Capability(str, Enum):
    CORE = "core"
    GRAPHICS = "graphics"
    AUDIO = "audio"
    GUI = "gui"
    PROJECT_FILES = "project-files"
    NETWORK = "network"

class CapabilityError(PermissionError):
    """وقتی سرویس خارج از capabilityهای فعال درخواست شود."""

class RuntimeService(Protocol):
    """قرارداد مشترک سرویس‌های runtime مانند graphics، audio و GUI."""
    name: str
    capability: Capability

    def call(self, operation: str, args: Sequence[Any]) -> Any:
        ...

class CapabilityRegistry:
    """whitelist سرویس‌های فعال؛ حالت پیش‌فرض فقط core است."""
    def __init__(self, enabled: Sequence[Capability | str] | None = None):
        values = (Capability.CORE,) if enabled is None else enabled
        self._enabled = {Capability(v) for v in values}

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any] | None = None):
        """ساخت policy از بخش capabilities در تنظیمات پروژه."""
        enabled = [Capability.CORE]
        for raw_name, raw_value in (mapping or {}).items():
            try:
                capability = Capability(raw_name)
            except ValueError as exc:
                raise CapabilityError(f'قابلیت ناشناخته «{raw_name}» است.') from exc
            if isinstance(raw_value, bool):
                active = raw_value
            elif isinstance(raw_value, str):
                active = raw_value.strip().lower() not in {'', '0', 'false', 'no', 'off', 'none'}
            else:
                raise CapabilityError(f'مقدار قابلیت «{raw_name}» باید boolean یا متن باشد.')
            if active and capability not in enabled:
                enabled.append(capability)
        return cls(enabled)

    def allows(self, capability: Capability | str) -> bool:
        return Capability(capability) in self._enabled

    def require(self, capability: Capability | str) -> None:
        capability = Capability(capability)
        if not self.allows(capability):
            raise CapabilityError(f"قابلیت «{capability.value}» فعال نیست.")

    def enabled(self) -> frozenset[Capability]:
        return frozenset(self._enabled)

@dataclass(frozen=True)
class RuntimeContext:
    """سیاست قابلیت‌های یک اجرای مشخص؛ پیش‌فرض فقط core است."""
    registry: CapabilityRegistry = field(default_factory=CapabilityRegistry)
    project_root: str | None = None

    @classmethod
    def from_capabilities(cls, enabled: Sequence[Capability | str] | None = None, project_root: str | None = None):
        return cls(CapabilityRegistry(enabled), project_root)

    def require(self, capability: Capability | str) -> None:
        self.registry.require(capability)

def node_id(source: str, ordinal: int, kind: str) -> NodeId:
    """تولید شناسهٔ قابل تکرار برای node در یک parse مشخص."""
    return NodeId(f"{source}:{ordinal}:{kind}")

def v1_contract() -> Mapping[str, Any]:
    """قرارداد سازگاری قابل بررسی برای برنامه‌های نسخهٔ ۱."""
    return {
        "language": LANGUAGE_V1,
        "text_delimiter": "-...-",
        "assignment": ["بگذار ... برابر ...", "name = expression"],
        "indentation": True,
        "unicode_identifiers": True,
        "capabilities_default": [Capability.CORE.value],
        "unsafe_python_import": False,
    }
