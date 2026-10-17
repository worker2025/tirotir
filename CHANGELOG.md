# Changelog

## Unreleased — Tirotir 2.0 candidate

این بخش وضعیت توسعهٔ نسخهٔ ۲٫۰ را ثبت می‌کند. نسخهٔ ۲٫۰ هنوز release نهایی نیست و این تغییرات منتشر نشده‌اند.

### تغییر KI-1: arithmetic فشرده

رفتار lexer برای عبارت‌های حسابی فشرده اصلاح شده است:

```text
Historical baseline 1.1.0:
چاپ ۵-۳+۲-۱ → 5

Tirotir 2.0 candidate:
چاپ ۵-۳+۲-۱ → 3
```

این یک تغییر رفتاری عمدی در تفسیر عبارت‌های حسابی بدون فاصله است و ممکن است روی برنامه‌هایی که به رفتار تاریخی وابسته‌اند اثر بگذارد. تست تاریخی در مسیر baseline جدا نگه‌داری می‌شود و candidate acceptance آن را با expected جدید پنهان یا بازنویسی نمی‌کند.

رفتارهای زیر نیز با تست‌های candidate بررسی شده‌اند:

- literalهای فارسی قدیمی؛
- حفظ نیم‌فاصلهٔ U+200C داخل literal متن؛
- escapeهای مستندشده؛
- module import؛
- بازگشت مقدار از function؛
- اولویت تابع کاربر بر primitive گرافیکی هم‌نام.

### وضعیت validation

- candidate acceptance: `7 passed`؛
- KI-5 dedicated enforcement: `14 passed`؛
- full review suite: `273 passed` روی commit `d32f97abdfdee69e40b839e35b81f99531b3c0b3`؛
- historical baseline: assertion مستقل روی commit `a6dd5dec1b4b9e2a304fec0a6cf06aecac7b417` موفق شد؛
- module/release integration: `28 passed`؛
- شش failure مربوط به U+200C در identifierهای نمونه‌ها همچنان حل‌نشده و خارج از scope KI-1 هستند.

### خارج از این تغییر

این changelog به معنی sandbox کامل سیستم‌عامل، enforcement مستقل `network` و `project-files`، اجرای واقعی Windows EXE، GUI روی desktop واقعی، پخش صوت واقعی، تکمیل GUI-1، LSP، debugger، namespace کامل یا آماده‌بودن release عمومی Tirotir 2.0 نیست. برای جزئیات به [README](README.md)، [برنامهٔ پذیرش KI-1](docs/tirotir-2-ki1-acceptance-plan-fa.md)، [ماتریس verification KI-5](docs/tirotir-2-ki5-verification-fa.md) و [سند مسائل شناخته‌شده](known-issues-fa.md) مراجعه کنید.

## Tirotir 1.1.0

سوابق release نسخهٔ ۱٫۱٫۰ در اسناد تاریخی `docs/public-release-readiness-fa.md` و `docs/release-readiness-fa.md` نگه‌داری شده‌اند و در این commit بازنویسی نشده‌اند.
