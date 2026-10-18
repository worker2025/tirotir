#!/usr/bin/env python3
"""Run the Tirotir 2.0 example bundle with the installed interpreter."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = Path(__import__("tirotir").__file__).resolve().parent.parent

CASES = [
    ("basics/hello_world.t", [], 0, "سلام دنیا", "run"),
    ("basics/print_messages.t", [], 0, "به تیروتیر خوش آمدید", "run"),
    ("variables/multiple_values.t", [], 0, "کتاب تیروتیر", "run"),
    ("conditions/grade.t", [], 0, "عالی", "run"),
    ("loops/repeat_count.t", [], 0, "5", "run"),
    ("functions/add_numbers.t", [], 0, "12", "run"),
    ("functions/function_condition_loop.t", [], 0, "11", "run"),
    ("lists/create_and_read.t", [], 0, "سیب", "run"),
    ("unicode/zwnj_identifier.t", [], 0, "1", "run"),
]

def call(command, cwd, timeout=15):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PACKAGE_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run([sys.executable, "-m", "tirotir.cli", *command], cwd=cwd,
                          env=env, capture_output=True, text=True, encoding="utf-8", timeout=timeout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-gui", action="store_true")
    args = parser.parse_args()
    passed, failed, skipped = [], [], []
    with tempfile.TemporaryDirectory(prefix="tirotir-examples-") as temp:
        work = Path(temp)
        for rel, extra, expected_code, expected_text, kind in CASES:
            result = call([kind, str(ROOT / rel), *extra], work)
            ok = result.returncode == expected_code and expected_text in result.stdout
            (passed if ok else failed).append({"case": rel, "returncode": result.returncode,
                                               "stdout": result.stdout, "stderr": result.stderr})
        scene = work / "scene.svg"
        result = call(["graphics", str(ROOT / "graphics/hello_shape.t"), "--scene", str(scene), "--capability", "graphics"], work)
        if result.returncode == 0 and scene.is_file() and scene.stat().st_size > 0:
            passed.append({"case": "graphics/hello_shape.t", "artifact": str(scene), "bytes": scene.stat().st_size})
        else:
            failed.append({"case": "graphics/hello_shape.t", "returncode": result.returncode, "stderr": result.stderr})
        result = call(["run", str(ROOT / "capabilities/graphics.t")], work)
        if result.returncode != 0 and not (work / "tirotir-scene.svg").exists():
            passed.append({"case": "capabilities/graphics.t (denied)", "returncode": result.returncode})
        else:
            failed.append({"case": "capabilities/graphics.t (denied)", "returncode": result.returncode})
        result = call(["audio", str(ROOT / "audio/render_only.t"), "--capability", "audio"], work)
        wav = work / "tirotir-note.wav"
        if result.returncode == 0 and wav.is_file() and wav.stat().st_size > 44:
            passed.append({"case": "audio/render_only.t", "artifact": str(wav), "bytes": wav.stat().st_size})
        else:
            failed.append({"case": "audio/render_only.t", "returncode": result.returncode, "stderr": result.stderr})
        if args.include_gui and os.environ.get("DISPLAY"):
            result = call(["gui", str(ROOT / "gui/hello_window.t"), "--capability", "gui"], work, timeout=10)
            if result.returncode == 0: passed.append({"case": "gui/hello_window.t"})
            else: failed.append({"case": "gui/hello_window.t", "returncode": result.returncode, "stderr": result.stderr})
        else:
            skipped.append({"case": "gui/hello_window.t", "reason": "desktop DISPLAY not supplied"})
    summary = {"passed": len(passed), "failed": len(failed), "skipped": len(skipped),
               "details": {"passed": passed, "failed": failed, "skipped": skipped}}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
