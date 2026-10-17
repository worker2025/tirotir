# قرارداد پذیرش KI-1

## وضعیت

Prototype C هنوز در branch مستقل است و این سند فقط contract و برنامهٔ تست را ثبت می‌کند. هیچ کدی به development منتقل نمی‌شود.

## ۱. Historical baseline

رفتار تاریخی زیر در commit development baseline ثبت شده است:

```text
Commit: a6dd5dec1b4b9e2a304fec0a6cf06aecac7b417a
Input:  چاپ ۵-۳+۲-۱
Old output: 5
```

این رفتار از misclassification در lexer ناشی می‌شود و evidence سازگاری تاریخی است؛ قرارداد arithmetic مورد نظر Tirotir 2.0 نیست.

بازآزمایی baseline باید با checkout همان commit، Python همان محیط، و اجرای زیر انجام شود:

```bash
PYTHONPATH=src python3 -m pytest -q \
  tests/test_known_issues.py::test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized
```

در candidate suite نباید این assertion با expected `3` جایگزین شود؛ baseline باید در گزارش/فایل جدا باقی بماند.

## ۲. Candidate acceptance contract

Candidate باید این رفتارها را اثبات کند:

| ورودی | خروجی مورد انتظار |
|---|---|
| `چاپ ۵-۳` | `2` |
| `چاپ ۵ - ۳ + ۲ - ۱` | `3` |
| `چاپ ۵-۳+۲-۱` | `3` |
| `چاپ -سلام دنیا-` | `سلام دنیا` |
| `چاپ -فارسی‌زبان-` | حفظ U+200C |
| `چاپ -۱۲۳-` | literal رشته‌ای |
| `چاپ -الف\-ب-` | `الف-ب` |
| `وارد کن -lib/tools-` | import موفق |
| `تابع جمع با الف و ب ...` | نتیجهٔ function بدون تغییر |
| `format_result.t` | parse و execute بدون regression |

## ۳. تغییرات دقیق موردنیاز در تست‌ها

در یک integration operation جداگانه، تغییرات زیر پیشنهاد می‌شود:

1. assertion فعلی در `tests/test_known_issues.py` حذف یا rewrite نشود؛ به‌عنوان historical characterization باقی بماند.
2. فایل جدید `tests/test_ki1_acceptance.py` ایجاد شود و فقط candidate contract جدول بالا را بررسی کند.
3. تست compact arithmetic با فاصله و بدون فاصله جدا باشند تا failure مکان‌پذیر باشد.
4. تست literalهای legacy، escape و U+200C مستقل باشند.
5. تست module import و `examples2/functions/format_result.t` مستقل باشند.
6. parse-only corpus test از execution corpus جدا گزارش شود.
7. در گزارش CI، baseline failure با عنوان `historical baseline evidence` و candidate suite با عنوان `candidate acceptance` چاپ شود.

## ۴. ابهام‌های حل‌نشده

- آیا compact subtraction بدون فاصله از نظر compatibility یک breaking change رسمی است؟
- آیا `-۱۲۳-` برای همیشه string می‌ماند یا فقط تا زمان تصویب literal delimiter جدید؟
- آیا syntax صریح string در 2.0 افزوده می‌شود؟
- آیا برنامه‌های قدیمی که عمداً به خروجی `5` تکیه دارند migration warning دریافت می‌کنند؟

## ۵. اثر سازگاری

- برنامه‌هایی که عبارت compact arithmetic را به‌صورت حسابی نوشته‌اند، نتیجهٔ درست‌تر `3` می‌گیرند.
- برنامه‌هایی که به misclassification تاریخی و خروجی `5` وابسته‌اند، ریسک رفتاری دارند.
- literalهای legacy، import path، function return و U+200C باید بدون تغییر بمانند.
- تغییر فقط باید در lexer و تست‌های لازم محدود بماند؛ parser، AST، interpreter، module system و security runtime نباید در integration KI-1 بازطراحی شوند.

## ۶. فرمان‌های اعتبارسنجی candidate

پس از آماده‌سازی test file در branch integration، فرمان‌های زیر لازم‌اند:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_ki1_acceptance.py
PYTHONPATH=src python3 -m pytest -q tests/test_known_issues.py::test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized
PYTHONPATH=src python3 -m pytest -q tests/test_known_issues.py tests/test_core.py
PYTHONPATH=src python3 -m pytest -q tests/test_modules.py tests/test_release_integration.py
PYTHONPATH=src python3 -m pytest -q
```

full suite فقط زمانی «سبز» گزارش شود که assertion تاریخی به‌درستی از candidate suite جدا شده باشد؛ نباید failure با `xfail` یا حذف تست پنهان شود.

## ۷. توصیهٔ فعلی

Prototype C برای **human integration review** آماده است، اما برای انتقال به development هنوز به این تصمیم‌ها نیاز دارد:

1. تصویب arithmetic contract جدید؛
2. تصویب نحوهٔ نگهداری و اجرای baseline؛
3. تصویب migration policy برای compact arithmetic؛
4. اجرای integration operation جداگانه با checkpoint و review diff.
