# Tirotir 2.0.0 Testing Guide

This guide describes testing the official `2.0.0` release; platform and backend limitations remain explicit below.

## Validated environment

- Linux;
- Python 3.11 or 3.12;
- package name: `tirotir`, version: `2.0.0`;
- CLI command: `tirotir`.

Windows, macOS, real VS Code activation, physical desktop GUI, and hardware audio playback are not validated for this candidate.

## Install from a checkout or source archive

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install .
tirotir version
```

Use `python3.12` instead when testing with Python 3.12. The package requires Python `>=3.11`.

## First run

```bash
tirotir run examples2/basics/hello_world.t
tirotir check examples2/basics/hello_world.t
```

For SVG generation, pass the capability explicitly:

```bash
tirotir graphics examples2/graphics/hello_shape.t --scene scene.svg --capability graphics
```

Audio examples require the `audio` capability. `graphics`, `audio`, and `gui` operations are denied unless explicitly permitted.

## KI-1 breaking change

```text
Tirotir 1.1.0: چاپ ۵-۳+۲-۱ → 5
Tirotir 2.0:   چاپ ۵-۳+۲-۱ → 3
```

Review legacy compact arithmetic. A valid text literal such as `چاپ -سلام دنیا-` remains text.

## Security and limitations

`network` and `project-files` do not expose public language primitives in this candidate; enabling their enum does not create real access. Capability enforcement is not a full operating-system sandbox and must not be treated as complete isolation for untrusted code.

## Bug reports

Include:

1. the commit SHA;
2. operating system and `python --version`;
3. the exact command;
4. a minimal `.t` reproducer;
5. stdout/stderr;
6. enabled capabilities;
7. `python -m pytest -q` output when available.

Do not include tokens, keys, passwords, private files, or personal information.
