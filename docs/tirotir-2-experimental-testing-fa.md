# راهنمای آزمایش Tirotir 2.0 — فارسی

این بسته **experimental candidate** است و release پایدار یا عمومی نیست.

## محیط تأییدشده

- Linux؛
- Python 3.11 یا 3.12؛
- package نام `tirotir`، نسخهٔ `2.0.0.dev0`؛
- فرمان CLI: `tirotir`.

Windows، macOS، اجرای واقعی VS Code، desktop GUI فیزیکی و پخش صوت سخت‌افزاری در این candidate تأیید نشده‌اند.

## نصب از source archive یا checkout

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install .
tirotir version
```

برای Python 3.12، `python3.11` را با `python3.12` جایگزین کنید. این package به Python `>=3.11` نیاز دارد.

## اولین اجرا

```bash
tirotir run examples2/basics/hello_world.t
tirotir check examples2/basics/hello_world.t
```

برای تولید SVG، capability را صریح بدهید:

```bash
tirotir graphics examples2/graphics/hello_shape.t --scene scene.svg --capability graphics
```

تولید WAV از مسیر مثال‌های audio با capability `audio` انجام می‌شود. `graphics`، `audio` و `gui` بدون مجوز صریح رد می‌شوند.

## تغییر شکستن‌ساز KI-1

```text
نسخهٔ 1.1.0: چاپ ۵-۳+۲-۱ → 5
نسخهٔ 2.0:   چاپ ۵-۳+۲-۱ → 3
```

عبارت‌های حسابی قدیمی را بازبینی کنید. متن سالم مانند `چاپ -سلام دنیا-` حفظ می‌شود.

## امنیت و محدودیت‌ها

`network` و `project-files` در این candidate primitive عمومی زبان ندارند؛ فعال‌کردن enum آن‌ها دسترسی واقعی ایجاد نمی‌کند. capabilityها sandbox کامل سیستم‌عامل نیستند و نباید برای اجرای کد نامطمئن به‌عنوان ایزوله‌سازی کامل استفاده شوند.

## گزارش خطا

برای گزارش خطا این موارد را ارسال کنید:

1. SHA commit؛
2. سیستم‌عامل و `python --version`؛
3. فرمان کامل؛
4. کمینهٔ فایل `.t` بازتولیدکننده؛
5. خروجی stdout/stderr؛
6. capabilityهای فعال؛
7. نتیجهٔ `python -m pytest -q` در صورت امکان.

از ارسال token، کلید، رمز، فایل خصوصی یا اطلاعات شخصی خودداری کنید.
