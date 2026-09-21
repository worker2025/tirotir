# گزارش Windows / VS Code Release Fix — Tirotir 1.1.0

## خلاصه

این مرحله فقط روی کارکرد واقعی Windows، UTF-8 خروجی، live graphics در VS Code و مسیر audio تمرکز داشت. نسخهٔ فعلی با **۲۳۴ تست موفق** و **۷۱ نمونهٔ موفق** اعتبارسنجی شده است.

## ۱. UTF-8 خروجی Windows

مشکل ریشه‌ای وابستگی stdout/stderr به locale پیش‌فرض Windows و CP1252 بود. CLI اکنون در شروع اجرا `stdout` و `stderr` را تا حد امکان با UTF-8 و `backslashreplace` تنظیم می‌کند. برای streamهای سفارشی نیز writer دارای مسیر fallback است و در صورت وجود `.buffer` مستقیماً bytes UTF-8 می‌نویسد.

تست شبیه‌سازی CP1252 با این برنامه اجرا شد:

```text
چاپ -سلام دنیا-
```

نتیجهٔ stdout با UTF-8 decode شد و `UnicodeEncodeError` تولید نشد. این تست در Linux با `PYTHONIOENCODING=cp1252` شبیه‌سازی شده است؛ تأیید نهایی PowerShell واقعی در Windows همچنان در Windows CI/manual acceptance انجام می‌شود.

## ۲. Graphics و live scene

CLI گزینهٔ داخلی زیر را دارد:

```bash
tirotir run program.t --live-scene
```

خروجی JSON قرارداد زیر را دارد:

```json
{"type":"scene","width":800,"height":600,"stdout":"...","svg":"<svg ...>...</svg>"}
```

اکستنشن VS Code به‌جای ساخت sidecar دائمی، همین JSON اجرای جاری را دریافت می‌کند و SVG را مستقیماً داخل WebView render می‌کند. هنگام شروع اجرای جدید، WebView فوراً با پیام اجرای جدید جایگزین می‌شود. در صورت خطا، stderr و پیام همان اجرای جدید نمایش داده می‌شود. اگر SVG تولید نشود، scene قبلی باقی نمی‌ماند و پیام مشخص نمایش داده می‌شود.

`--scene` همچنان برای export و debugging موجود است:

```bash
tirotir graphics examples/graphics/hello_shape.t --scene test.svg
```

## ۳. RTL و WebView

WebView اکنون شامل موارد زیر است:

- `lang="fa"`؛
- `dir="rtl"`؛
- `charset="utf-8"`؛
- CSP با `default-src 'none'` و style inline محدود؛
- container جداگانه برای SVG با direction چپ‌به‌راست؛
- container متن با direction راست‌به‌چپ؛
- حذف script از SVG پیش از render؛
- تفکیک خطای اجرای Tirotir از خطای JSON پروتکل.

در این محیط Chromium headless فایل SVG واقعی را باز کرد و وجود SVG، چهار خط مربع و رنگ `آبی` را تأیید کرد. اجرای کامل خود VS Code روی Windows هنوز manual acceptance است.

## ۴. Audio

تولید WAV مستقل از backend سیستم‌عامل است. نام نت‌های فارسی زیر mapping deterministic دارند:

```text
دو، ر، می، فا، سل، لا، سی
```

مسیر اجرای صوت:

```bash
tirotir audio examples/audio/scale.t
tirotir run examples/audio/scale.t --play-audio
```

در Windows backend `Media.SoundPlayer` با `PlaySync` استفاده می‌شود؛ در Linux backendهای `aplay`، `paplay` و `ffplay` و در macOS `afplay` بررسی می‌شوند. پخش چند نت به‌صورت ترتیبی و blocking انجام می‌شود و از race اجرای هم‌زمان جلوگیری می‌کند. اگر backend وجود نداشته باشد، WAV حفظ می‌شود و پیام فارسی قابل‌فهم ارائه می‌شود.

تولید WAV و mapping نت‌ها در sandbox تست شده‌اند. صدای واقعی بلندگو در این محیط قابل تأیید نیست.

## ۵. GUI

پنجره، label، button و input حفظ شده‌اند. در محیط headless یا بدون Tkinter، diagnostic زیر ارائه می‌شود:

```text
TIR4001: رابط گرافیکی در این محیط در دسترس نیست؛ Tkinter و desktop لازم است.
```

اجرای واقعی پنجره در desktop Windows باید manual acceptance شود. checkbox، listbox، event syntax کامل و callbackهای سطح زبان هنوز جزو این release نیستند.

## ۶. EXE

این فرمان روی Windows رسمی است:

```powershell
pyinstaller --clean --onefile --name tirotir --paths src tools\tirotir_launcher.py
```

workflow مستقل در `.github/workflows/windows-exe-release.yml` ایجاد شده و پس از ساخت EXE موارد زیر را smoke test می‌کند:

- `version`؛
- اجرای hello world؛
- تولید SVG؛
- اجرای `--live-scene` و بررسی UTF-8 رنگ `آبی`؛
- تولید WAV.

در محیط فعلی Linux، Windows runner اجرا نشده است؛ بنابراین Windows EXE هنوز **CI verified** نیست.

## ۷. وضعیت بر اساس محیط

| مورد | وضعیت |
|---|---|
| Linux sandbox | Verified |
| UTF-8 با شبیه‌سازی CP1252 | Verified |
| SVG UTF-8 | Verified |
| Chromium headless | Verified |
| live scene JSON | Verified |
| WAV generation | Verified |
| Persian note mapping | Verified |
| GUI headless diagnostic | Verified |
| Windows CI workflow | آماده، اجرا نشده در این محیط |
| Windows desktop stdout | Manual Acceptance Required |
| Windows desktop GUI | Manual Acceptance Required |
| Windows desktop audio | Manual Acceptance Required |
| VS Code Windows live WebView | Manual Acceptance Required |
| macOS CI | workflow موجود، نتیجهٔ runner در این محیط موجود نیست |

## ۸. نتایج نهایی

```text
tests: 234 passed
examples: 71 passed
live-scene: passed
utf8-cp1252-regression: passed
svg-chromium-smoke: passed
wav-fallback: passed
```

## ۹. فایل‌های release

- `dist/tirotir-1.1.0-py3-none-any.whl`
- `dist/tirotir-1.1.0.tar.gz`
- `/home/ubuntu/tirotirLang-1.1.0.vsix`
- `/home/ubuntu/tirotir-1.1.0-release.tar.gz`

## نتیجهٔ انتشار

Tirotir 1.1.0 برای انتشار عمومی به‌عنوان زبان فارسی آموزشی/کاربردی آماده است، اما Windows desktop، VS Code Windows و پخش audio واقعی باید پس از اجرای Windows CI و manual acceptance روی سیستم مقصد تأیید شوند. هیچ‌کدام از این موارد بدون اجرای واقعی Windows در این گزارش verified اعلام نشده‌اند.
