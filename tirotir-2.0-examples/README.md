# Tirotir 2.0 examples

This is the tested example bundle for Tirotir 2.0.1. It contains only syntax and runtime paths verified in the repository.

## Install and run

Download the `tirotir-2.0.1-py3-none-any.whl` from the [v2.0.1 GitHub Release](https://github.com/worker2025/tirotir/releases/tag/v2.0.1), then run:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install /path/to/tirotir-2.0.1-py3-none-any.whl
python tests/run_examples.py
```

The harness uses the installed interpreter and separates passed, failed, and skipped cases. GUI is skipped unless `--include-gui` is supplied. Graphics and audio use explicit capabilities.

## Direct examples

```bash
tirotir run basics/hello_world.t
tirotir check basics/hello_world.t
tirotir graphics graphics/hello_shape.t --scene scene.svg --capability graphics
tirotir audio audio/render_only.t --capability audio
```

The GUI example needs a desktop display and the `gui` capability. The capability-negative checks intentionally fail without permission.
