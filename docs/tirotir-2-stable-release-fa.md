# گزارش رسمی وضعیت پایدار Tirotir 2

**نسخهٔ Python:** `2.0.2`  
**نسخهٔ افزونهٔ VS Code:** `2.0.6`  
**artifact افزونه:** `tirotirlang-2.0.6.vsix`  
**مخزن:** `worker2025/tirotir`  
**پسوند رسمی:** `.t`  
**حداقل Python:** `3.11`

## نتیجهٔ انتشار

Tirotir 2 برای استفادهٔ عمومی در محدودهٔ مستندشده پایدار اعلام می‌شود. هستهٔ زبان، CLI، interpreter، parser، diagnostics، module/project path، Graphics/SVG، تولید WAV و مسیرهای آزموده‌شدهٔ افزونه در quality gate فعلی بررسی شده‌اند.

این اعلام به معنی تکمیل LSP، DAP، object model، sandbox کامل سطح سیستم‌عامل، موتور بازی، event syntax عمومی، GUI framework کامل یا تضمین cross-platform برای همهٔ محیط‌ها نیست.

## شواهد اعتبارسنجی

- full suite روی tag منتشرشده و checkout فعلی: `291 passed`؛
- CI GitHub روی Ubuntu با Python 3.11 و 3.12: موفق؛
- نصب wheel رسمی و اجرای `tirotir version`: موفق؛
- نسخهٔ `tirotir==2.0.2` در PyPI در ۲۰ اکتبر ۲۰۲۶ منتشر شده است؛ نصب پاک در virtualenv جدید روی Linux/Python 3.12.3 با `pip install tirotir==2.0.2` انجام شد و `tirotir version` خروجی `Tirotir 2.0.2` داد؛
- هر ۴۱ فایل `.t` در `examples2/` با `tirotir check` با موفقیت parse شدند؛ ۳۲ مثال non-GUI با capability و ورودی لازم با `tirotir run`/فرمان تخصصی اجرا شدند؛ ۹ مثال GUI با خطای ساختاریافتهٔ `TIR4001` رد شدند، چون Tkinter و desktop در محیط موجود نبود؛
- تولید SVG و WAV: موفق؛
- VSIX `tirotirlang-2.0.6.vsix`: تست Windows توسط مالک پروژه با نتیجهٔ عالی گزارش شده و artifact حفظ شده است؛
- افزونهٔ VS Code و Python عمداً version مستقل دارند: Python `2.0.2` و VSIX `2.0.6`.

## قرارداد نسخه‌ها

برای جلوگیری از تناقض، این دو نسخه را یکی نکنید:

| جزء | نسخه | توضیح |
|---|---:|---|
| Python package/runtime | `2.0.2` | نسخهٔ زبان و CLI |
| VS Code extension | `2.0.6` | نسخهٔ مستقل افزونه و artifact آزمایش‌شده |
| VS Code publisher | `tirotir` | شناسهٔ publisher داخل manifest |

## محدودیت‌های اعلام‌شده

GUI به Tkinter و display واقعی نیاز دارد. پخش صدا به backend و دستگاه سیستم‌عامل وابسته است؛ تولید WAV مستقل است. capabilityها کنترل دسترسی runtime هستند و sandbox کامل OS محسوب نمی‌شوند. module system و namespace در محدودهٔ فعلی قراردادهای پشتیبانی‌شده کار می‌کنند، اما package system کامل و dotted namespace عمومی هنوز هدف آینده است.

## راهنمای گزارش خطا

برای هر خطا این اطلاعات ثبت شود: نسخهٔ Python و افزونه، سیستم‌عامل، نسخهٔ VS Code، دستور یا فایل `.t`، خروجی مورد انتظار، خروجی واقعی و traceback/diagnostic.
