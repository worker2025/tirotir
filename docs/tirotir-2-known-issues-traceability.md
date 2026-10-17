# ردیابی مسائل شناخته‌شدهٔ Tirotir 2.0

**مبنای بررسی:** `18a1d2d767b55361b8e3a3fa9792f9be82eb4395`  
**baseline تاریخی مسائل:** `481f15fcd18b21d38fc9161b69489d4560ce091b`  
**محیط:** Linux x86_64، Python 3.12.3، pytest 9.1.1  
**نتیجهٔ regression baseline:** `244 passed in 1.46s`  
**قاعده:** هیچ موردی بدون regression test و شواهد اجرای مرتبط `VERIFIED` اصلاح‌شده علامت نمی‌خورد.

## وضعیت‌های مجاز

- `OPEN`: مسئله در scope است اما هنوز root cause یا reproduction کامل نشده است.
- `REPRODUCED`: رفتار گزارش‌شده در checkout فعلی بازتولید شده است.
- `IN PROGRESS`: اصلاح در شاخهٔ توسعه شروع شده است.
- `FIXED LOCALLY`: کد تغییر کرده، اما همهٔ آزمون‌های لازم یا compatibility verification کامل نیست.
- `VERIFIED`: اصلاح، regression، integration و مستندات مرتبط تأیید شده‌اند.
- `DEFERRED`: عمداً به milestone بعد منتقل شده است.
- `BLOCKED`: زیرساخت یا محیط لازم موجود نیست.
- `NOT REPRODUCIBLE`: پس از بررسی، رفتار گزارش‌شده در checkout فعلی مشاهده نشده است.

## خلاصهٔ فعلی

| ID | حوزه | وضعیت فعلی | اولویت | commit اصلاحی |
|---|---|---|---|---|
| KI-1 | متن و تفریق | `REPRODUCED` | P0 | ندارد |
| KI-2 | Unicode و نیم‌فاصله | `FIXED LOCALLY` | P0 | pending checkpoint |
| KI-3 | شکل‌های مقایسهٔ فارسی | `OPEN` | P1 | ندارد |
| KI-4 | diagnostics ساختاریافته | `REPRODUCED` | P1 | ندارد |
| KI-5 | enforcement قابلیت‌ها | `OPEN` | P0 | ندارد |
| KI-6 | import و namespace | `OPEN` | P1 | ندارد |
| KI-7 | formatter خروجی | `OPEN` | P1 | ندارد |
| KI-8 | scope تابع | `OPEN` | P1 | ندارد |
| KI-9 | مثال‌ها و بازگشت تابع | `REPRODUCED` | P0 | ندارد |
| KI-10 | Windows artifact | `BLOCKED` | P1 | ندارد |
| KI-11 | حداقل Python | `REPRODUCED` | P1 | ندارد |
| KI-12 | metadata و انتشار | `OPEN` | P2 | ندارد |
| KI-13 | پوشش cross-platform | `BLOCKED` | P1 | ندارد |
| KI-14 | LSP و debugger | `DEFERRED` | P2 | ندارد |
| KI-15 | Event Runtime | `OPEN` | P2 | ندارد |

---

## KI-1 — ابهام متن با خط تیره و عملگر تفریق

**شرح اصلی:** قرارداد متن `-متن-` با عملگر `-` هم‌پوشانی دارد.

**Reproduction فعلی:**

```text
چاپ ۵ - ۳ + ۲ - ۱
چاپ ۵-۳+۲-۱
```

**Actual:** عبارت فاصله‌دار خروجی `3` و عبارت فشرده خروجی `5` تولید کرد. در حالت فشرده parser بخشی از عبارت را به literal متن تبدیل می‌کند.

**Expected:** دو عبارت حسابی معادل باید یا نتیجهٔ یکسان بدهند، یا حالت مبهم با diagnostic دقیق رد شود. متن معتبر legacy باید تا حد امکان حفظ شود.

**Evidence:** `src/tirotir/core.py` در tokenizer/parser؛ smoke test ثبت‌شده در baseline report.

**Root cause:** هنوز به‌صورت خط‌به‌خط isolate نشده، اما محل اولیهٔ مسئله تشخیص token متن در lexer و precedence/parser است.

**اثر امنیتی:** خروجی اشتباه بدون خطا؛ مسئلهٔ correctness با اولویت P0.

**اصلاح پیشنهادی:** افزودن regression برای حالت spaced، compact، متن دارای فاصله، متن دارای خط تیره و عملگر unary. بررسی delimiter صریح فقط با migration analysis. از replacement متنی ad hoc استفاده نشود.

**وضعیت:** `REPRODUCED`؛ هنوز اصلاح نشده.

**Migration risk:** زیاد؛ هر تغییر lexer ممکن است برنامه‌های 1.1.0 را تغییر دهد.

**Commit و verification:** ندارد.

## KI-2 — تغییر ناخواستهٔ نیم‌فاصله و Unicode در literal متن

**شرح اصلی:** در متن فارسی، U+200C یا نیم‌فاصله ممکن است به underscore تبدیل شود.

**Reproduction فعلی:**

```text
چاپ -قلم بالا-
```

**Actual:** خروجی `قلم_بالا` مشاهده شد.

**Expected:** literal متن باید محتوای Unicode منبع را حفظ کند، مگر آنکه specification صریحاً transformation تعریف کند.

**Evidence:** `src/tirotir/core.py` و smoke test baseline.

**Root cause:** احتمالاً یک normalization مشترک برای identifier و text literal؛ خط دقیق normalization باید در مرحلهٔ implementation با token dump و تست U+200C مشخص شود.

**اثر امنیتی:** امنیت مستقیم ندارد، اما محتوای کاربر تغییر می‌کند و می‌تواند در متن آموزشی یا دادهٔ فارسی زیان‌بار باشد.

**اصلاح پیشنهادی:** جداسازی normalization شناسه از literal؛ افزودن تست حروف فارسی/عربی، نیم‌فاصله، کشیده، combining marks، ارقام فارسی و mixed script.

**وضعیت:** `FIXED LOCALLY`. `parse()` دیگر کل منبع را با `replace(\u200c, _)` تغییر نمی‌دهد؛ normalization شناسه در `norm()` باقی مانده است. Regression جدید در `tests/test_core.py::test_zero_width_non_joiner_is_preserved_in_string` اضافه شد.

**Migration risk:** متوسط؛ برنامه‌هایی که به underscore فعلی در literal تکیه دارند باید شناسایی شوند، اما aliasهای دارای نیم‌فاصله با تست integration حفظ شدند.

**Verification:** full suite: `245 passed in 0.80s`; smoke مستقیم مقدار U+200C را حفظ کرد. Commit اصلاحی در checkpoint بعدی ثبت می‌شود.

## KI-3 — پشتیبانی ناقص از شکل‌های مقایسهٔ فارسی

**شرح اصلی:** برخی ترکیب‌های طبیعی مانند «بزرگ‌تر از» یا «نا برابر با» ممکن است رد شوند یا diagnostic تورفتگی نامرتبط تولید کنند.

**Reproduction لازم:**

```text
اگر ۳ بزرگ‌تر از ۲
    چاپ -بله-

اگر ۳ نا برابر با ۲
    چاپ -بله-
```

**Actual فعلی:** در این مرحلهٔ baseline هنوز اجرای مستقل همهٔ شکل‌های گزارش‌شده تکمیل نشده است.

**Expected:** شکل‌های رسمی مستند باید parse شوند؛ شکل نامعتبر باید خطای عبارت ناشناخته با SourceSpan مناسب بدهد، نه خطای بدنهٔ تورفته.

**Evidence:** `src/tirotir/core.py` و گزارش historical `known-issues-fa.md`.

**Root cause:** `OPEN`؛ نیازمند token trace و grammar comparison table.

**اصلاح پیشنهادی:** جدول canonical phraseها، تست parser/semantic، diagnostic مستقل برای comparison phrase.

**وضعیت:** `OPEN`.

**Migration risk:** کم تا متوسط؛ در صورت افزودن aliasها معمولاً backward-compatible است.

**Commit و verification:** ندارد.

## KI-4 — خطاهای زمان اجرا و نحو همیشه ساختاریافته نیستند

**شرح اصلی:** `Diagnostic` و `SourceSpan` در contracts وجود دارند، اما همهٔ مسیرهای CLI، parser، runtime و JSON از یک قرارداد واحد استفاده نمی‌کنند.

**Actual:** semantic analyzer برای نام تعریف‌نشده diagnostic ساختاریافته با code `TIR2001` تولید می‌کند؛ CLI آن را به متن فارسی تبدیل می‌کند و حالت عمومی `--format json` در command `check` در CLI فعلی پیاده‌سازی نشده است.

**Expected:** human و JSON output با code، severity، type، source، span و suggestion در همهٔ diagnostics.

**Evidence:** `src/tirotir/contracts.py`، `src/tirotir/semantic.py`، `src/tirotir/cli.py`.

**Root cause:** contract در سطح data model موجود است، اما plumbing کامل از parser/runtime تا CLI و extension وجود ندارد.

**اصلاح پیشنهادی:** تکمیل SourceSpan با offset، serializer واحد، `check --format human|json`، تست golden برای خطاهای syntax و runtime.

**وضعیت:** `REPRODUCED / incomplete`.

**Migration risk:** متوسط؛ format متنی legacy باید حفظ و JSON به‌صورت opt-in اضافه شود.

**Commit و verification:** ندارد.

## KI-5 — اعمال کامل capabilityها

**شرح اصلی:** registry و whitelist وجود دارد، اما enforcement همهٔ backendها به‌صورت end-to-end ثابت نشده است.

**Actual:** `CapabilityRegistry()` فقط `core` را فعال می‌کند و `require()` قابلیت غیرفعال را رد می‌کند. جستجوی source استفادهٔ گسترده از `require()` در graphics/audio/gui را نشان نداد.

**Expected:** هر عملیات بیرونی قبل از اجرا capability مناسب را require کند؛ bypass از CLI، module، GUI و builder ممکن نباشد.

**Evidence:** `src/tirotir/contracts.py`، `src/tirotir/core.py`، `src/tirotir/audio.py`، `src/tirotir/builder.py`.

**Root cause:** contract registry از service binding و interpreter execution جداست.

**اصلاح پیشنهادی:** RuntimeContext واحد با registry، service adapterها، تست active/disabled برای هر capability و تست path traversal. این سازوکار sandbox کامل OS نیست.

**وضعیت:** `OPEN`.

**Migration risk:** متوسط؛ رفتارهایی که اکنون بدون permission اجرا می‌شوند ممکن است بعد از اصلاح رد شوند.

**Commit و verification:** ندارد.

## KI-6 — اتصال module system به namespace و اجرای پروژه کامل

**شرح اصلی:** loader، canonical path، graph و cycle detection وجود دارد، اما import به namespace اجرایی کامل متصل نشده است.

**Actual:** `ModuleLoader` و `ModuleGraphBuilder` graph را می‌سازند و CLI در حالت project graph را تحلیل و سپس source ماژول‌ها را اجرا می‌کند. انتقال نام تعریف‌شدهٔ ماژول به scope واردکننده و قرارداد namespace مستقل هنوز کامل نیست.

**Expected:** import یک ModuleId و namespace مشخص بسازد، هر module یک‌بار initialize شود و dotted access/exports طبق قرارداد کار کند.

**Evidence:** `src/tirotir/modules/*.py`، `src/tirotir/cli.py`، `tests/test_modules.py`، `tests/test_release_integration.py`.

**Root cause:** graph/loader از semantic namespace و runtime environment جدا مانده‌اند.

**اصلاح پیشنهادی:** تعریف export/import، namespace object، topological execution، cache side effect و diagnostics `TIR3001` تا `TIR3003` در CLI.

**وضعیت:** `OPEN`.

**Migration risk:** زیاد؛ ترتیب side effect و visibility نام‌ها تغییر می‌کند.

**Commit و verification:** ندارد.

## KI-7 — خروجی مقدارها قرارداد رسمی و کاملاً فارسی ندارد

**شرح اصلی:** نمایش مقدارهای runtime ممکن است از representation داخلی Python استفاده کند.

**Actual:** در baseline smoke، عدد اعشاری با ارقام لاتین `123.5` نمایش داده شد؛ سیاست رسمی برای boolean، None، float، list و dict در formatter واحد ثبت نشده است.

**Expected:** formatter رسمی Tirotir برای human output، همراه با حالت machine-readable جداگانه.

**Evidence:** `src/tirotir/core.py` و `src/tirotir/cli.py`.

**Root cause:** output path مستقیماً `str(value)` یا representation runtime را مصرف می‌کند.

**اصلاح پیشنهادی:** `format_value(value, mode)` و تست قراردادی برای همهٔ typeهای پایه؛ JSON نباید با human output مخلوط شود.

**وضعیت:** `OPEN`.

**Migration risk:** متوسط؛ snapshot و برنامه‌هایی که output را parse می‌کنند ممکن است تغییر کنند.

**Commit و verification:** ندارد.

## KI-8 — قرارداد scope متغیرها در تابع

**شرح اصلی:** رفتار assignment داخل function در حضور variable بیرونی باید صریح شود.

**Actual فعلی:** تست nested scope و parameter وجود دارد، اما coverage آن معادل تصمیم specification دربارهٔ local، outer، closure و mutation نیست.

**Expected:** declaration و assignment محلی، parameter، closure و دسترسی outer قرارداد روشن و regression-tested داشته باشند.

**Evidence:** `src/tirotir/semantic.py` و `tests/test_semantic.py`.

**Root cause:** `OPEN`؛ باید با matrix رفتار و اجرای چند سناریوی function/closure isolate شود.

**اصلاح پیشنهادی:** scope resolver رسمی، default local برای declaration جدید، syntax مشخص برای outer در صورت نیاز، migration note.

**وضعیت:** `OPEN`.

**Migration risk:** زیاد؛ semantics برنامه‌های موجود ممکن است تغییر کند.

**Commit و verification:** ندارد.

## KI-9 — مثال‌ها با رفتار اجرایی هماهنگ نیستند

**شرح اصلی:** بعضی مثال‌های README یا اسناد با interpreter فعلی سازگار نیستند.

**Reproduction فعلی:**

```text
تابع مربع با عدد
    بازگردان عدد * عدد
چاپ مربع با ۵
```

**Actual:** خروجی `[None]` در smoke test.

**Expected:** خروجی `25` یا اصلاح رسمی مثال به syntaxی که واقعاً قرارداد زبان است.

**Evidence:** `README.md`، `src/tirotir/core.py`، smoke test baseline.

**Root cause:** هنوز بین parser function call و semantics پارامتر تک‌نامی isolate نشده است.

**اصلاح پیشنهادی:** acceptance test برای تمام code blockهای README، تصمیم دربارهٔ grammar تک‌پارامتری، جلوگیری از انتشار مثال اجرا نشده.

**وضعیت:** `REPRODUCED`.

**Migration risk:** متوسط تا زیاد؛ اصلاح parser می‌تواند syntax قدیمی را تغییر دهد.

**Commit و verification:** ندارد.

## KI-10 — بستهٔ Windows و ادعای اجرای مستقل

**شرح اصلی:** Setup و VSIX در repository هستند، اما build و اجرای واقعی Windows در محیط baseline ممکن نیست.

**Actual:** script ساخت `tools/build_windows_exe.ps1` به Windows، Python launcher و PyInstaller نیاز دارد. در Linux فعلی Setup اجرا نشده است.

**Expected:** build از commit مشخص در Windows CI، smoke test `version/run/check/graphics`، checksum و خطای قابل فهم.

**Evidence:** `tools/build_windows_exe.ps1`، `install/Tirotir-1.1.0-Setup.exe`، docs Windows.

**Root cause:** زیرساخت Windows CI و اجرای desktop در این محیط موجود نیست.

**اصلاح پیشنهادی:** workflow Windows، build config pin شده، artifact checksum، manual acceptance و ثبت معماری x64.

**وضعیت:** `BLOCKED`.

**Migration risk:** کم برای زبان؛ زیاد برای release claim.

**Commit و verification:** ندارد.

## KI-11 — حداقل Python با metadata و کد یکسان نیست

**شرح اصلی:** `pyproject.toml` مقدار `>=3.9` اعلام می‌کند، اما `src/tirotir/modules/project.py` مستقیماً `tomllib` را import می‌کند.

**Actual:** discrepancy در source قطعی است. Python 3.9 و 3.10 در این محیط اجرا نشدند.

**Expected:** یا حداقل Python 3.11 اعلام شود، یا dependency سازگار برای 3.9/3.10 اضافه و CI شود.

**Evidence:** `pyproject.toml:10` و `src/tirotir/modules/project.py:3`.

**Root cause:** metadata از پیاده‌سازی فعلی عقب مانده است.

**اصلاح پیشنهادی:** تصمیم رسمی، هماهنگ‌سازی pyproject، README، wheel metadata، CI و docs.

**وضعیت:** `REPRODUCED` به‌عنوان discrepancy metadata؛ اصلاح نشده.

**Migration risk:** متوسط؛ تغییر حداقل نسخه روی کاربران قدیمی اثر دارد.

**Commit و verification:** ندارد.

## KI-12 — ناسازگاری metadata و انتشار

**شرح اصلی:** version، author، repository، citation، license و artifactها باید منبع واحد داشته باشند.

**Actual:** `CITATION.cff` repository اصلی را ثبت می‌کند، اما `vscode-tirotirLang/package.json` repository متفاوت `github.com/tirotir/tirotir` را اعلام می‌کند. دو فایل license و اسناد متناقض release نیز وجود دارد.

**Expected:** یک source of truth برای name/version/author/date/repository و validation خودکار.

**Evidence:** `CITATION.cff`، `pyproject.toml`، `vscode-tirotirLang/package.json`، docs release.

**Root cause:** metadata در چند فایل دستی نگه‌داری می‌شود.

**اصلاح پیشنهادی:** version check script، validation `CITATION.cff`، CI consistency test، تصمیم دربارهٔ LICENSE تکراری و repository افزونه.

**وضعیت:** `OPEN`.

**Migration risk:** کم برای runtime؛ زیاد برای اعتماد release و citation.

**Commit و verification:** ندارد.

## KI-13 — پوشش سیستم‌عامل و artifact کامل نیست

**شرح اصلی:** regression فعلی فقط در Linux/Python 3.12.3 اجرا شده است.

**Actual:** `244 passed in 1.46s` در Linux. Windows، macOS، Setup، GUI واقعی و playback واقعی تأیید نشده‌اند.

**Expected:** CI برای Linux/Windows/macOS و نسخه‌های Python پشتیبانی‌شده، artifact test و نمونه‌های رسمی.

**Evidence:** اجرای pytest baseline، نبود workflow در `.github/workflows`، docs release.

**Root cause:** CI cross-platform در checkout موجود نیست یا قابل مشاهده نیست.

**اصلاح پیشنهادی:** matrix CI، coverage، artifact install test، smoke test Windows و ثبت environment.

**وضعیت:** `BLOCKED` برای آزمون کامل؛ baseline Linux verified.

**Migration risk:** کم تا متوسط؛ ممکن است failureهای platform-specific آشکار شوند.

**Commit و verification:** ندارد.

## KI-14 — Language Server و debugger کامل نیستند

**شرح اصلی:** افزونهٔ فعلی syntax highlighting و command integration دارد، اما LSP و debugger با breakpoint، step، locals و call stack کامل نیست.

**Actual:** فایل extension JavaScript و grammar وجود دارد؛ implementation مستقل LSP/DAP در source دیده نشد.

**Expected:** diagnostics، completion، hover، definition، references، rename و debugger instrumentation/DAP.

**Evidence:** `vscode-tirotirLang/extension.js`، `package.json`، نبود server/debug adapter مستقل.

**Root cause:** milestone architecture هنوز پیاده‌سازی نشده است.

**اصلاح پیشنهادی:** بعد از تثبیت Diagnostic و node/source span، LSP و سپس debugger؛ استفاده نکردن از Python eval/exec برای evaluation.

**وضعیت:** `DEFERRED` تا بعد از P0 و contract freeze.

**Migration risk:** کم برای هسته؛ API ابزار توسعه باید versioned باشد.

**Commit و verification:** ندارد.

## KI-15 — Event Runtime و syntax رویدادمحور نهایی نیست

**شرح اصلی:** `Event`, `EventQueue`, `HandlerRegistry` و `EventLoop` پایه وجود دارند، اما syntax زبان و اتصال کامل GUI/graphics/game به event runtime تثبیت نشده است.

**Actual:** تست determinism برای queue پایه وجود دارد؛ event syntax رسمی در parser و API کاربر نهایی کامل نیست.

**Expected:** event queue deterministic، handler، timer، run/pause/step/stop و backend-independent API.

**Evidence:** `src/tirotir/events.py`، `tests/test_release_integration.py`، roadmap.

**Root cause:** runtime پایه از language syntax و backend integration جدا مانده است.

**اصلاح پیشنهادی:** قرارداد Event/Handler/Clock، test deterministic، سپس syntax و اتصال GUI/graphics؛ callback مستقیم Python در اختیار برنامه قرار نگیرد.

**وضعیت:** `OPEN`؛ implementation پایه موجود است.

**Migration risk:** متوسط؛ event loop می‌تواند lifecycle GUI و ترتیب side effect را تغییر دهد.

**Commit و verification:** ندارد.

## معیار بستن هر مسئله

یک مسئله فقط زمانی `VERIFIED` می‌شود که همهٔ موارد زیر ثبت شده باشد:

1. reproduction قبل از اصلاح؛
2. root cause با file/function evidence؛
3. تغییر کوچک و محدود؛
4. regression test؛
5. integration/acceptance test مرتبط؛
6. اجرای کامل baseline بدون regression؛
7. بررسی compatibility و migration؛
8. به‌روزرسانی README/docs؛
9. commit SHA؛
10. محیط و output verification.

تا پیش از آن، عبارت‌هایی مانند «حل شد»، «امن شد»، «سازگار شد» یا «آمادهٔ انتشار» نباید در README یا release note استفاده شوند.
