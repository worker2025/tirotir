# گزارش baseline مهندسی Tirotir 2.0

**تاریخ بررسی:** ۱۷ اکتبر ۲۰۲۶
**مخزن:** `https://github.com/worker2025/tirotir`
**checkout مرجع:** `/home/ubuntu/tirotir-upstream-inspection`
**worktree توسعه:** `/home/ubuntu/tirotir-2-worktree-20261017T110755Z`
**شاخهٔ توسعه:** `development/tirotir-2.0-20261017T110755Z`

این گزارش پیش از هر تغییر کدی تهیه شده است. هدف آن ثبت وضعیت واقعی checkout فعلی، تفکیک ادعاهای مستنداتی از شواهد قابل اجرا و ایجاد مبنای قابل بازیابی برای توسعهٔ نسخهٔ ۲٫۰ است.

## ۱. خلاصهٔ اجرایی

checkout واقعی شاخهٔ `main` روی commit زیر قرار دارد:

```text
18a1d2d767b55361b8e3a3fa9792f9be82eb4395
```

این commit از baseline ثبت‌شدهٔ Tirotir 1.1.0 با SHA زیر جلوتر است:

```text
481f15fcd18b21d38fc9161b69489d4560ce091b
```

در checkout واقعی، شاخهٔ `main` پاک است و تغییر ثبت‌نشده ندارد. توسعه در worktree و شاخهٔ جداگانه انجام شده است. یک Git bundle مستقل از تاریخچهٔ کامل و یک آرشیو جداگانه از پوشهٔ کاری جلسهٔ قبلی ساخته و restore آن‌ها آزمایش شده است.

در نخستین اجرای با محیط خام، pytest نصب نبود و دستور آزمون با خطای `No module named pytest` متوقف شد. پس از ایجاد backup و worktree ایزوله، pytest 9.1.1 فقط در محیط توسعه نصب شد و آزمون کامل checkout واقعی با موفقیت اجرا شد: `244 passed in 1.46s`. این نتیجه فقط Linux، Python 3.12.3، همین commit و همین dependency set را پوشش می‌دهد.

Smoke testهای مستقل نیز با Python 3.12.3 اجرا شدند. هستهٔ زبان، CLI، parser، interpreter، semantic analyzer، قرارداد capability و برخی نمونه‌های module در سطح import قابل اجرا هستند. دو مسئلهٔ ثبت‌شده مستقیماً بازتولید شدند: ابهام متن با تفریق و تغییر نیم‌فاصله در literal متن. نمونهٔ تابع موجود در README نیز خروجی `None` تولید کرد.

## ۲. وضعیت Git و نسخه

| مورد | وضعیت واقعی |
|---|---|
| remote | `https://github.com/worker2025/tirotir.git` |
| branch checkout مرجع | `main` |
| HEAD فعلی | `18a1d2d767b55361b8e3a3fa9792f9be82eb4395` |
| آخرین commit | `Update README.md` |
| tagهای موجود | `v1.1.0` و `v1.1.0.1` |
| وضعیت working tree مرجع | پاک، همگام با `origin/main` |
| نسخهٔ package در `pyproject.toml` | `1.1.0` |
| نسخهٔ CLI | `1.1.0` |
| نسخهٔ افزونهٔ VS Code | `1.1.0` |
| حداقل Python اعلام‌شده | `>=3.9` |

commit فعلی بعد از tagها چند commit مستنداتی دارد. بنابراین tag نسخهٔ 1.1.0 و HEAD فعلی را نباید بدون بررسی برابر فرض کرد.

## ۳. حفاظت، backup و بازیابی

backup مستقل در مسیر زیر ایجاد شد:

```text
/home/ubuntu/tirotir-backup-20261017T110755Z/
```

محتویات backup:

```text
tirotir-history.bundle       Git history and all refs
session-folder.tar.gz        پوشهٔ غیرگیتی جلسهٔ قبلی با مستندات تولیدشده
SHA256SUMS                   checksum هر دو فایل
```

SHA-256 ثبت‌شده:

```text
51dea35cd94bc092588cc6c75ab96fb5ed61507679cc83982144ab3b4075313f  tirotir-history.bundle
edd2d5b8768d32e6ac15b1a17e1de24016fd30769daa5e3ea0a4e1f0e9179b7f  session-folder.tar.gz
```

`git bundle verify` موفق شد و bundle در یک مسیر موقت clone شد. SHA کلون بازیابی‌شده با HEAD checkout مرجع یکسان بود. پوشهٔ کاری قبلی که Git checkout نبود نیز جداگانه archive شد تا فایل‌های تولیدشده و مستندات آن از توسعهٔ رسمی جدا بماند.

هیچ reset، clean، force checkout، amend یا force-push انجام نشد.

## ۴. محیط اجرا و آزمون baseline

```text
OS: Linux x86_64
Kernel: 6.18.38+
Python: 3.12.3
pytest: نصب نیست
```

دستور آزمون مورد انتظار پروژه:

```bash
PYTHONPATH=src python3 -m pytest -q
```

نتیجهٔ اجرای خام پیش از نصب dependency:

```text
/usr/bin/python3: No module named pytest
```

پس از ایجاد backup و worktree ایزوله، pytest 9.1.1 نصب و همان دستور دوباره اجرا شد:

```text
244 tests collected in 0.17s
244 passed in 1.46s
```

به‌صورت ایستا، ۶۱ تابع با نام `test_*` در هشت فایل آزمون و دو decorator از نوع `pytest.mark.parametrize` دیده می‌شود. عدد معتبر برای baseline همان نتیجهٔ اجرای واقعی pytest، یعنی ۲۴۴ مورد جمع‌آوری‌شده و موفق، است.

آمار ایستای فایل‌ها:

```text
source Python files: 16
examples/*.t and nested examples/*.t: 10
examples2/**/*.t: 41
```

مستندات چند عدد متفاوت مانند ۲۰۲، ۲۳۴، ۲۴۰ و ۲۴۴ تست و ۷۱ مثال را گزارش می‌کنند. این اختلاف‌ها پیش از هر release باید با یک منبع تولیدشونده از CI یکسان‌سازی شوند.

## ۵. smoke testهای قابل اجرا بدون pytest

دستور smoke test با `PYTHONPATH=src` و Python 3.12.3 اجرا شد. نتایج اصلی:

| سناریو | نتیجهٔ مشاهده‌شده | وضعیت |
|---|---:|---|
| `چاپ -سلام دنیا-` | `سلام دنیا` | Verified implemented در این محیط |
| `چاپ ۱۲۳٫۵` | `123.5` | Verified implemented در این محیط |
| `چاپ ۵ - ۳ + ۲ - ۱` | `3` | بازتولید شد |
| `چاپ ۵-۳+۲-۱` | `5` | بازتولید شد؛ ambiguity باقی است |
| `چاپ -قلم بالا-` | `قلم_بالا` | بازتولید شد؛ نیم‌فاصله حفظ نمی‌شود |
| مقایسهٔ `۳ بزرگتر از ۲` | `بله` | Verified برای این شکل |
| تابع جمع با پارامترهای `الف` و `ب` | `5` | Verified برای این شکل |
| نمونهٔ README برای تابع مربع با `عدد` | `None` | Known defective / مستندات ناسازگار |
| semantic check نام تعریف‌نشده | diagnostic `TIR2001` | Verified implemented در این مسیر |
| capability پیش‌فرض | فقط `core` | Verified برای registry |
| CLI version | `Tirotir 1.1.0` | Verified implemented |

نمونهٔ تابع ناسازگار:

```text
تابع مربع با عدد
    بازگردان عدد * عدد
چاپ مربع با ۵
```

خروجی مشاهده‌شده `None` بود، درحالی‌که نمونهٔ جمع با دو پارامتر خروجی درست تولید کرد. این مورد باید به acceptance test تبدیل شود و سپس یا syntax تابع اصلاح شود یا مثال رسمی تغییر کند.

## ۶. نقشهٔ معماری و قابلیت‌های موجود

### ۶.۱ موارد قابل مشاهده در source

| قابلیت | وضعیت baseline |
|---|---|
| lexer و parser | **Verified implemented**؛ `src/tirotir/core.py` |
| AST | **Verified implemented**؛ در core و AST JSON |
| interpreter | **Verified implemented**؛ core و runtimeهای مربوط |
| semantic analyzer | **Implemented but incomplete**؛ `src/tirotir/semantic.py` |
| قرارداد Diagnostic و SourceSpan | **Implemented but incomplete**؛ `src/tirotir/contracts.py` |
| CLI و REPL | **Verified implemented** در مسیرهای اصلی |
| formatter | **Implemented but incomplete**؛ formatter فعلی عمدتاً line-based است |
| سیستم پروژه و `tirotir.toml` | **Implemented but incomplete** |
| module sandbox و canonical path | **Verified implemented** در آزمون‌های source-level موجود، اجرای کامل import نیازمند آزمون runtime است |
| module graph و cycle diagnostic | **Verified implemented** در مسیر ساخت graph |
| namespace و انتقال نام importشده به scope اجرا | **Known defective / incomplete** طبق known issues و ساختار CLI |
| Event Runtime پایه | **Implemented but incomplete**؛ `src/tirotir/events.py` |
| Graphics و SVG | **Implemented but incomplete**؛ نیازمند آزمون کامل و capability اتصال‌یافته |
| Audio/WAV | **Implemented but incomplete**؛ playback به محیط وابسته است |
| GUI/Tkinter | **Implemented but incomplete**؛ desktop لازم است |
| capability registry | **Implemented but incomplete**؛ registry وجود دارد اما اتصال آن به همهٔ backendها ثابت نشده است |
| VS Code syntax extension | **Verified implemented** |
| Language Server کامل | **Not implemented** |
| debugger با breakpoint و call stack | **Not implemented** |
| object model | **Not implemented** در نسخهٔ فعلی |
| compiler/bytecode VM | **Deferred / not implemented** |
| Windows Setup artifact | **Unverified** در این محیط؛ اجرای واقعی Windows انجام نشده است |

### ۶.۲ نکتهٔ مهم دربارهٔ capability

`CapabilityRegistry` در `contracts.py` وجود دارد و حالت پیش‌فرض آن فقط `core` است. بااین‌حال، جستجوی source نشان داد که فراخوانی‌های `.require(...)` در backendهای اصلی به‌صورت گسترده دیده نمی‌شود. بنابراین وجود registry را نباید معادل enforcement واقعی در تمام مسیرهای graphics، audio، GUI، filesystem یا network دانست.

این بخش در نسخهٔ ۲٫۰ باید با regression test برای حالت فعال و غیرفعال هر capability، مسیر CLI، module و backend بررسی شود. capability language-level به‌تنهایی sandbox سطح سیستم‌عامل نیست.

## ۷. مسائل شناخته‌شده و ردیابی اولیه

| شناسه | وضعیت مشاهده‌شده در HEAD فعلی | evidence اولیه |
|---|---|---|
| KI-1 | **REPRODUCED** | تفاوت خروجی spaced و compact subtraction |
| KI-2 | **REPRODUCED** | نیم‌فاصله در متن به `_` تبدیل شد |
| KI-3 | **UNVERIFIED** | نیازمند اجرای شکل‌های گزارش‌شده با `بزرگ‌تر` و `نا برابر` |
| KI-4 | **REPRODUCED / incomplete** | diagnostics ساختاری وجود دارد، اما CLI JSON و پوشش کامل یکسان نیست |
| KI-5 | **OPEN / UNVERIFIED** | registry وجود دارد؛ enforcement همهٔ backendها اثبات نشده |
| KI-6 | **OPEN / incomplete** | graph و loader وجود دارند؛ namespace runtime باید end-to-end آزموده شود |
| KI-7 | **REPRODUCED / incomplete** | خروجی عدد و مقدارها قرارداد formatter واحد ندارد |
| KI-8 | **UNVERIFIED** | نیازمند سناریوهای outer/local و closure |
| KI-9 | **REPRODUCED** | تابع مربع README خروجی `None` داد |
| KI-10 | **UNVERIFIED** | Windows واقعی در دسترس نیست؛ build script به PyInstaller و Windows نیاز دارد |
| KI-11 | **REPRODUCED as metadata discrepancy** | `pyproject.toml` می‌گوید `>=3.9`، اما `project.py` از `tomllib` استفاده می‌کند |
| KI-12 | **OPEN** | نویسنده و repository افزونه با metadata اصلی همسان نیستند؛ گزارش کامل لازم است |
| KI-13 | **BLOCKED** | pytest نصب نیست و cross-platform در این محیط قابل اجرا نیست |
| KI-14 | **NOT IMPLEMENTED / DEFERRED** | LSP و debugger کامل در source وجود ندارد |
| KI-15 | **IMPLEMENTED BUT INCOMPLETE** | EventLoop پایه در `events.py` هست؛ syntax event زبان نهایی نیست |

وضعیت‌های بالا preliminary هستند. در مرحلهٔ بعد سند traceability جداگانه برای KI-1 تا KI-15 با reproduction program، root cause، تست و commit اصلاحی تکمیل خواهد شد. هیچ موردی در این گزارش `VERIFIED` اصلاح‌شده اعلام نشده است.

## ۸. ریسک‌های سازگاری

ریسک‌های مهم پیش از تغییر کد:

1. تغییر lexer برای حل KI-1 ممکن است برنامه‌های قدیمی با `-متن-` یا عبارت‌های بدون فاصله را تغییر دهد.
2. جداسازی normalization شناسه از literal متن ممکن است خروجی برنامه‌هایی را که به underscore فعلی وابسته‌اند تغییر دهد.
3. اصلاح scope توابع می‌تواند معنای برنامه‌های موجود را عوض کند.
4. فعال‌کردن واقعی capabilityها ممکن است backendهایی را که اکنون بدون permission اجرا می‌شوند متوقف کند؛ این تغییر از نظر امنیتی مطلوب است اما باید migration note داشته باشد.
5. تکمیل import و namespace می‌تواند ترتیب side effect اجرای پروژه‌های چندفایلی را تغییر دهد.
6. هماهنگ‌سازی نسخهٔ Python ممکن است نصب روی Python 3.9 و 3.10 را محدود یا نیازمند dependency جدید کند.
7. تغییر مستندات بدون اجرای نمونه‌ها می‌تواند ناسازگاری جدید ایجاد کند.

اصل حاکم: هیچ اصلاح semantics بدون regression test، acceptance test برای برنامه‌های legacy و توضیح migration پذیرفته نمی‌شود.

## ۹. زیرساخت انتشار و metadata

موارد زیر نیازمند بررسی و یکسان‌سازی هستند:

- `pyproject.toml` نسخهٔ 1.1.0 و Python `>=3.9` را اعلام می‌کند؛
- CLI از `tomllib` استفاده می‌کند که در Python استاندارد از 3.11 موجود است؛
- `CITATION.cff` نام نویسنده را Daryoush Alipour و نسخهٔ 1.1.0 اعلام می‌کند؛
- `vscode-tirotirLang/package.json` repository را `https://github.com/tirotir/tirotir` اعلام می‌کند که با repository اصلی worker2025 متفاوت است؛
- دو فایل `LICENSE` و `LICENSE.md` وجود دارد؛
- artifactهای wheel، VSIX و Setup داخل repository هستند، اما reproducibility کامل build و smoke test Windows در این محیط اثبات نمی‌شود؛
- CI workflow در checkout فعلی پیدا نشد؛
- مستندات تست و release اعداد متناقضی برای تست و مثال دارند.

## ۱۰. برنامهٔ مرحله‌ای پیشنهادی

### مرحلهٔ صفر — انجام‌شده

- clone مستقل repository؛
- ثبت HEAD، tags و status؛
- smoke test بدون نصب dependency؛
- ساخت Git bundle و آرشیو فایل‌های غیرگیتی؛
- restore test backup؛
- ایجاد worktree و branch توسعه؛
- ثبت این baseline report.

### مرحلهٔ یک — baseline regression، انجام‌شدهٔ جزئی

- نصب pytest فقط در محیط توسعهٔ ایزوله؛ انجام شد؛
- اجرای collection و test کامل با ثبت دقیق output؛ انجام شد: `244 collected`, `244 passed in 1.46s`؛
- ساخت legacy compatibility suite از نمونه‌های README و examples؛ هنوز انجام نشده؛
- ایجاد `docs/tirotir-2-known-issues-traceability.md` برای KI-1 تا KI-15؛ گام بعدی؛
- افزودن checkpoint commit پس از تکمیل traceability و پاک‌سازی artifactها؛ هنوز انجام نشده.

### مرحلهٔ دو — P0 correctness/security

ترتیب پیشنهادی:

1. KI-1: تفکیک متن و تفریق بدون شکستن legacy؛
2. KI-2: حفظ دقیق Unicode در literal متن؛
3. KI-5: enforcement واقعی capability؛
4. KI-9: اصلاح رفتار تابع یا نمونهٔ رسمی؛
5. diagnostics دقیق برای خطاهای مرتبط.

هیچ object model، debugger یا قابلیت بزرگ جدیدی پیش از تعیین تکلیف این مرحله وارد هسته نمی‌شود.

### مرحلهٔ سه — قراردادهای پایدار

- SourceSpan کامل با offset؛
- Diagnostic انسانی و JSON؛
- symbol table و scope resolution؛
- acceptance tests برای نمونه‌های رسمی؛
- قرارداد رسمی import، namespace و module cache.

### مرحلهٔ چهار — module و runtime

- اتصال graph به اجرای واقعی و namespace؛
- تست cycle، path escape، cache و side effect؛
- event loop deterministic با API زبانی فقط پس از تثبیت runtime؛
- حفظ adapter برای برنامه‌های نسخهٔ ۱.

### مرحلهٔ پنج — ابزار توسعه و انتشار

- LSP diagnostics و completion؛
- interpreter instrumentation و debugger؛
- CI چندسکویی؛
- Windows build و smoke test واقعی؛
- هماهنگ‌سازی metadata، version، citation، package و extension.

## ۱۱. blockerهای فعلی

1. Windows واقعی برای اجرای Setup، EXE، GUI و audio playback در دسترس نیست.
2. macOS در محیط فعلی آزمایش نشده است.
4. مسیر roadmap در repository موجود است، اما فایل `docs/known-issues-fa.md` وجود ندارد و known issues در ریشهٔ repository قرار دارد؛ prompt ورودی باید با این واقعیت reconciled شود.
5. اعداد آزمون و مثال در چند سند با هم یکسان نیستند.

## ۱۲. تصمیم release فعلی

این checkout در وضعیت **Release Candidate برای Tirotir 2.0 نیست**. وضعیت درست آن:

```text
Tirotir 1.1.0 current main snapshot
2.0 development branch prepared
baseline verified on Linux/Python 3.12.3: 244 passed
cross-platform/package verification unverified
```

هیچ tag، release، push به `main`، merge، انتشار PyPI یا انتشار VS Code انجام نشده است.

## ۱۳. checkpoint پس از اصلاح KI-2

پس از baseline اولیه، اصلاح محدود KI-2 انجام شد: نرمال‌سازی سراسری نیم‌فاصله از `parse()` حذف شد تا literal متن Unicode خود را حفظ کند؛ normalization شناسه در `norm()` باقی ماند و aliasهای دارای نیم‌فاصله regression شدند. نتیجهٔ آزمون پس از این اصلاح:

```text
245 passed in 0.80s
```

این نتیجه یک checkpoint پس از baseline است و نباید با baseline تاریخی ۲۴۴ تست خلط شود. اصلاح هنوز به‌عنوان release یا تغییر سازگارشدهٔ عمومی منتشر نشده است.

در مرحلهٔ ممیزی بعدی، هفت آزمون مستقل characterization در `tests/test_known_issues.py` اضافه شد. نتیجهٔ کامل پس از این آزمون‌ها `252 passed in 0.86s` است. این هفت آزمون علت KI-1، bypass فعلی KI-5 و collision نام `مربع` در KI-9 را ثبت می‌کنند و هیچ‌کدام اصلاح semantics این سه مورد نیستند.

## ۱۴. checkpoint پس از اصلاح KI-9

در commit مستقل بعدی، collision نام تابع `مربع` با primitive گرافیکی اصلاح شد. تغییر فقط dispatch graphics را محدود می‌کند تا اگر تابع کاربر با همان نام وجود داشت، تابع کاربر اولویت بگیرد؛ primitive بدون collision unchanged است. focused tests با `3 passed`، آزمون‌های acceptance/graphics با `32 passed` و full suite با `253 passed in 0.64s` موفق شدند. این اصلاح هنوز release-verified یا روی cross-platform تأییدشده نیست.

## ۱۵. نتیجه

دارایی اصلی پروژه حفظ شده و توسعهٔ نسخهٔ ۲٫۰ در مسیر مستقل آماده است. مهم‌ترین نتیجهٔ baseline این است که repository واقعی با نسخهٔ checkout قبلی جلسه یکسان نیست: HEAD فعلی روی commit جدیدتر قرار دارد، چند لایهٔ معماری ۲٫۰ از قبل در source وجود دارند، اما بعضی از آن‌ها فقط contract یا scaffold هستند و هنوز رفتار end-to-end و امنیتی آن‌ها اثبات نشده است.

گام بعدی مجاز، پس از تأیید این گزارش، نصب pytest در همین worktree ایزوله و اجرای کامل regression است. پس از آن می‌توان سند traceability مسائل را تکمیل کرد و فقط P0های قابل اثبات را به‌صورت کوچک و قابل بازگشت اصلاح کرد.
