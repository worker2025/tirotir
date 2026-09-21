# Tirotir 1.1.0 — Release Fix Gate نهایی

## ۱. مشکل واقعی چه بود؟

در اجرای Windows، فایل SVG از نظر اندازه و ساختار تولید می‌شد، اما گزارش شده بود مقدار رنگ فارسی `آبی` به شکل mojibake مانند `Ø¢Ø¨ÛŒ` دیده می‌شود. همچنین افزونهٔ VS Code ممکن بود scene قبلی را نشان دهد یا SVG را فقط به‌عنوان متن خروجی نمایش دهد. بررسی مستقیم runtime نشان داد فایل با UTF-8 صحیح نوشته می‌شود؛ این نتیجه با regression test و Chromium headless تأیید شد. برای حذف ریشه‌ای stale output، افزونه اکنون از پروتکل `--live-scene` استفاده می‌کند و SVG اجرای فعلی را مستقیماً در JSON دریافت می‌کند؛ در اجرای معمول WebView هیچ فایل دائمی کنار source ساخته نمی‌شود.

## ۲. فایل‌های تغییرکرده

فایل‌های اصلی این gate عبارت‌اند از:

- `src/tirotir/core.py`: mapping نت‌های فارسی، duration پیش‌فرض و diagnostic `TIR4001` برای GUI headless.
- `src/tirotir/audio.py`: سرویس پخش اختیاری با fallback WAV.
- `vscode-tirotirLang/extension.js`: UTF-8، CSP، پروتکل live scene و نمایش SVG اجرای فعلی.
- `src/tirotir/cli.py`: تنظیم UTF-8 برای stdout/stderr، fallback stream سفارشی و خروجی JSON live scene.
- `tests/test_release_integration.py`: تست UTF-8، رنگ فارسی، Chromium contract، نت فارسی و GUI headless.
- `.github/workflows/windows-exe-release.yml`: ساخت و smoke test واقعی EXE روی Windows runner.
- `README.md`، `CHANGELOG.md` و `docs/release-readiness-fa.md`: همگام‌سازی وضعیت واقعی.

## ۳. وضعیت Graphics CLI

نمونهٔ `examples/graphics/hello_shape.t` با `--scene` فایل SVG غیرخالی تولید می‌کند. فایل دارای عنصر `<svg>`، چهار `<line>` برای مربع و رنگ UTF-8 واقعی `آبی` است. UTF-8 با خواندن مستقیم bytes و نبود رشته‌های `Ø` و `Â` بررسی شد.

## ۴. وضعیت SVG در مرورگر

در محیط فعلی Chromium موجود بود. SVG تولیدشده با `chromium --headless --no-sandbox --disable-gpu --dump-dom` باز شد و DOM شامل SVG، چهار خط و متن رنگ فارسی بود. بنابراین مسیر CLI تا parser مرورگر در این محیط تأیید شده است. تست تعاملی Edge/Chrome روی Windows desktop انجام نشده است.

## ۵. وضعیت VS Code WebView

WebView اکنون charset UTF-8 و CSP محدود دارد، SVG را در container راست‌به‌چپ/چپ‌به‌راست مناسب render می‌کند و scene را از JSON اجرای فعلی دریافت می‌کند. خروجی اجرای قبلی در WebView باقی نمی‌ماند، زیرا محتوای پنل هنگام شروع با پیام اجرای جدید جایگزین می‌شود. در صورت نبود SVG تازه پیام مشخص نمایش داده می‌شود. smoke test قرارداد JavaScript و تست CLI JSON این مسیر را بررسی می‌کنند. اجرای کامل خود VS Code در این sandbox انجام نشده و manual acceptance روی desktop باقی است.

## ۶. وضعیت Audio

تولید WAV بدون dependency خارجی باقی مانده است. نام نت‌های فارسی `دو`، `ر`، `می`، `فا`، `سل`، `لا` و `سی` به‌صورت deterministic به فرکانس نگاشت می‌شوند و duration اختیاری است. اگر backend صوتی سیستم موجود باشد، `--play-audio` یا فرمان `audio` تلاش به پخش می‌کند؛ در غیر این صورت پیام فارسی داده می‌شود و WAV حفظ می‌شود. پخش از بلندگوی واقعی در این محیط ادعا نشده است.

## ۷. وضعیت GUI

Tkinter backend پنجره، label، button و input را حفظ می‌کند. در نبود Tkinter یا desktop، خطای ساختاریافتهٔ `TIR4001` ارائه می‌شود و traceback خام کاربرمحور نیست. اجرای پنجره روی desktop Windows/Linux/macOS باید به‌صورت manual یا CI desktop runner تأیید شود. checkbox، listbox، event syntax سطح زبان و callbackهای برنامه‌نویسی هنوز تکمیل نشده‌اند.

## ۸. وضعیت EXE

`tools/build_windows_exe.ps1` و workflow مستقل Windows با PyInstaller آماده‌اند. workflow این موارد را انجام می‌دهد: نصب، ساخت one-file EXE، اجرای `version`، اجرای hello world، تولید SVG و بسته‌بندی artifact. چون workflow در این محیط اجرا نشده است، `dist/tirotir.exe` را Windows-verified اعلام نمی‌کنیم.

## ۹. تعداد نهایی تست‌ها

```text
234 passed
```

## ۱۰. تعداد نمونه‌های موفق

```text
71 examples
71 non-GUI examples passed
```

## ۱۱. Known Limitations

LSP کامل، DAP debugger، object model، inheritance، package manager، export/import نام‌دار، event syntax سطح زبان، callback کامل GUI، checkbox/listbox، پخش قطعی روی دستگاه صوتی و build اجراشدهٔ Windows هنوز محدودیت یا کار آینده هستند.

## ۱۲. فایل‌های release

- `dist/tirotir-1.1.0-py3-none-any.whl`
- `dist/tirotir-1.1.0.tar.gz`
- `/home/ubuntu/tirotirLang-1.1.0.vsix`
- `/home/ubuntu/tirotir-1.1.0-release.tar.gz`

## جمع‌بندی

Release Fix Gate برای مشکلات UTF-8، SVG stale، نمایش WebView، نام نت‌های فارسی و GUI headless تکمیل و در Linux sandbox تأیید شد. نسخهٔ ۱٫۱٫۰ برای انتشار عمومی به‌عنوان زبان فارسی آموزشی/کاربردی آماده است، مشروط به این‌که Windows EXE و تجربهٔ GUI/audio واقعی پس از اجرای workflow و manual acceptance روی سیستم‌های مقصد تأیید شوند.
