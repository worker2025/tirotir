# بستهٔ مثال‌های Tirotir 2.0

این bundle فقط نمونه‌هایی را شامل می‌شود که syntax و مسیر اجرای آن‌ها در Tirotir 2.0.1 بررسی شده است.

## نصب و اجرای harness

wheel نسخهٔ `tirotir-2.0.1-py3-none-any.whl` را از [GitHub Release نسخهٔ v2.0.1](https://github.com/worker2025/tirotir/releases/tag/v2.0.1) دریافت و اجرا کنید:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install /مسیر/tirotir-2.0.1-py3-none-any.whl
python tests/run_examples.py
```

harness از همان interpreter نصب‌شده استفاده می‌کند و موارد passed، failed و skipped را جدا گزارش می‌دهد. GUI به‌صورت پیش‌فرض skip است و با `--include-gui` فعال می‌شود. Graphics و audio به capability صریح نیاز دارند.

## اجرای مستقیم

```bash
tirotir run basics/hello_world.t
tirotir check basics/hello_world.t
tirotir graphics graphics/hello_shape.t --scene scene.svg --capability graphics
tirotir audio audio/render_only.t --capability audio
```

مثال GUI به desktop display و capability `gui` نیاز دارد. آزمون‌های منفی capability عمداً بدون مجوز باید رد شوند.
