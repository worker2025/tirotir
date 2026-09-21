# گزارش نهایی `.t` و Live Graphics Viewport — Tirotir 1.1.0

## وضعیت تست

```text
Tests: 237 passed
Examples: 71 passed
.t extension: PASS
Live Graphics: PASS
RTL: PASS
Audio Windows: PASS (manual verification reported by user; Linux playback not claimed)
```

## پسوند رسمی

پسوند رسمی فایل زبان از `.tirotir` به `.t` منتقل شد. همهٔ ۷۱ نمونهٔ رسمی به `.t` تغییر نام یافتند، مستندات اصلی اصلاح شدند و VS Code فقط `.t` را به زبان TirotirLang associate می‌کند.

CLI این موارد را برای `.t` پشتیبانی می‌کند:

```text
tirotir run hello.t
tirotir check hello.t
tirotir format hello.t
tirotir ast hello.t
```

فایل‌های قدیمی `.tirotir` برای جلوگیری از شکستن پروژه‌های قبلی در اجرای مستقیم CLI و ModuleLoader همچنان پذیرفته می‌شوند، اما پسوند رسمی و پیش‌فرض جدید `.t` است.

## اصلاح viewport

مختصات منطقی Graphics تغییر نکرده‌اند. اصلاح فقط در `Scene.save` انجام شد:

1. نقاط واقعی lineهای تولیدشده استخراج می‌شوند.
2. bounding box شکل با padding محاسبه می‌شود.
3. مختصات logical با توجه به translation و محور Y معکوس به viewBox تبدیل می‌شوند.
4. `preserveAspectRatio="xMidYMid meet"` از کشیدگی و خروج شکل از viewport جلوگیری می‌کند.
5. برای صحنهٔ خالی، viewBox استاندارد پنجره حفظ می‌شود.

نمونهٔ `hello_shape.t` اکنون چهار line دارد، رنگ `آبی` را بدون mojibake حفظ می‌کند و viewBox آن به‌جای کل صفحه، محدودهٔ واقعی شکل را با padding پوشش می‌دهد.

این تغییر semantics زبان یا دستگاه مختصات برنامه‌نویس را تغییر نمی‌دهد و فقط لایهٔ rendering را اصلاح می‌کند.

## Live Graphics

اکستنشن VS Code همچنان از `--live-scene` استفاده می‌کند:

```text
Tirotir source
→ tirotir --live-scene
→ JSON
→ SVG داخل WebView
```

در اجرای معمول VS Code، فایل SVG کنار source ذخیره نمی‌شود. ذخیرهٔ فایل فقط با گزینهٔ صریح `--scene` انجام می‌شود.

## Audio و RTL

Audio تغییر معماری نداشته است. تولید WAV و mapping نت‌ها regression شده‌اند و پخش واقعی Windows طبق تست دستی کاربر تأیید شده است. RTL پنل VS Code نیز طبق تست دستی کاربر صحیح است؛ تست sandbox نیز UTF-8، `dir="rtl"` و مسیر خطای فارسی را بررسی می‌کند.

## فایل خروجی

- `dist/tirotir-1.1.0-py3-none-any.whl`
- `dist/tirotir-1.1.0.tar.gz`
- `/home/ubuntu/tirotirLang-1.1.0.vsix`
- `/home/ubuntu/tirotir-1.1.0-release.tar.gz`

## محدودیت باقی‌مانده

تست Windows desktop و VS Code Windows در این sandbox قابل اجرای مستقیم نیست. نتیجهٔ Audio Windows و RTL Windows بر اساس تست دستی ارائه‌شده ثبت شده است؛ Windows CI workflow همچنان برای بازتولید build EXE و smoke test خودکار موجود است.
