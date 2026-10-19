# ردیابی مسائل شناخته‌شدهٔ Tirotir 2.0

> **یادداشت نسخهٔ فعلی:** این سند شامل checkpointها و اعداد تاریخی ممیزی است. وضعیت جاری و عدد رسمی release در [گزارش پایدار Tirotir 2](tirotir-2-stable-release-fa.md) ثبت می‌شود: Python `2.0.2`، افزونه `2.0.6` و full suite برابر `291 passed`.

**مبنای بررسی:** `cf6a30dd536f11c1e42076ebc4778dae8418ee4b`
**baseline تاریخی مسائل:** `481f15fcd18b21d38fc9161b69489d4560ce091b`
**محیط:** Linux x86_64، Python 3.12.3، pytest 9.1.1
**وضعیت انتشار:** شواهد این سند ابتدا در candidate توسعه جمع‌آوری شد و سپس برای release رسمی `v2.0.0` بازبینی شد. `VERIFIED` در این سند به محدودهٔ آزموده‌شده اشاره دارد و به‌معنای پشتیبانی همهٔ سیستم‌عامل‌ها یا sandbox کامل OS نیست.
**نتیجهٔ regression baseline:** `244 passed in 1.46s`
**نتیجهٔ validation نهایی:** full suite برابر `291 passed`، focused security/runtime/KI suite برابر `38 passed`، همهٔ `51/51` مثال parse شدند، `38` مثال non-GUI با capability لازم اجرا شدند و GitHub Actions برای همین SHA با موفقیت کامل شد؛ historical baseline جداگانه روی `a6dd5de` موفق شد.
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
| KI-1 | متن و تفریق | `VERIFIED` | P0 | e333c67 |
| KI-2 | Unicode و نیم‌فاصله | `VERIFIED` | P0 | 3749e69 / dc110f3 |
| KI-3 | شکل‌های مقایسهٔ فارسی | `OPEN` | P1 | ندارد |
| KI-4 | diagnostics ساختاریافته | `REPRODUCED` | P1 | ندارد |
| KI-5 | enforcement قابلیت‌ها | `VERIFIED` | P0 | 20f01ab |
| KI-6 | import و namespace | `OPEN` | P1 | ندارد |
| KI-7 | formatter خروجی | `OPEN` | P1 | ندارد |
| KI-8 | scope تابع | `OPEN` | P1 | ندارد |
| KI-9 | مثال‌ها و بازگشت تابع | `VERIFIED` | P0 | e3c1cd8 |
| KI-10 | Windows artifact | `BLOCKED` | P1 | ندارد |
| KI-11 | حداقل Python | `VERIFIED` | P1 | 276e55f |
| KI-12 | metadata و انتشار | `VERIFIED` در candidate | P2 | a44ca6b |
| KI-13 | پوشش cross-platform | `BLOCKED` خارج از Linux CI | P1 | d51941a |
| KI-14 | LSP و debugger | `DEFERRED` | P2 | ندارد |
| KI-15 | Event Runtime | `OPEN` | P2 | ندارد |

---

## KI-1 — ابهام متن با خط تیره و عملگر تفریق

**شرح اصلی:** قرارداد سالم متن `-متن-` باید حفظ شود، اما delimiter فعلی با عملگر `-` در عبارت حسابیِ بدون فاصله هم‌پوشانی دارد.

**Reproduction فعلی:**

```text
چاپ ۵ - ۳ + ۲ - ۱
چاپ ۵-۳+۲-۱
```

**Actual در candidate:** نمونهٔ سالم `چاپ -سلام دنیا-` خروجی `سلام دنیا` می‌دهد. `چاپ ۵-۳` خروجی `2`، عبارت فاصله‌دار `چاپ ۵ - ۳ + ۲ - ۱` خروجی `3` و عبارت فشرده `چاپ ۵-۳+۲-۱` نیز خروجی `3` می‌دهد.

**Expected:** دو عبارت حسابی معادل باید یا نتیجهٔ یکسان بدهند، یا حالت مبهم با diagnostic دقیق رد شود. متن معتبر legacy باید تا حد امکان حفظ شود.

**Evidence:** `src/tirotir/core.py` در tokenizer/parser؛ `tests/test_ki1_candidate_acceptance.py` و اجرای مستقل ماتریس arithmetic روی commit `d32f97a`.

**Root cause تاریخی:** در سطح lexer اثبات شد: نسخهٔ baseline هر `-` را در این موقعیت به‌صورت متن مصرف می‌کرد. اصلاح KI-1 در commitهای `60d5197` و `e333c67` lexer را grammar-aware کرد و رفتار compact arithmetic را به قرارداد candidate رساند.

**اثر امنیتی:** خروجی اشتباه بدون خطا؛ مسئلهٔ correctness با اولویت P0.

**آزمون ثبت‌شده:** `tests/test_ki1_candidate_acceptance.py` شامل ۷ آزمون candidate؛ baseline تاریخی در `tests/baseline/ki1_historical_behavior.py` جدا نگه‌داری شده است. تست تابع، return، module import، literal فارسی، U+200C و escape نیز موفق شدند.

**وضعیت:** `VERIFIED` در candidate scope؛ رفتار تاریخی `5` فقط روی baseline commit `a6dd5de` حفظ شده و در candidate معرفی نمی‌شود.

**Migration risk:** زیاد؛ compact arithmetic از خروجی تاریخی `5` به `3` تغییر کرده و برنامه‌های وابسته به misclassification تاریخی نیازمند بررسی مهاجرت هستند.

**Commit و verification:** انتقال KI-1 در `e333c67`؛ candidate `7 passed` روی `d32f97a`؛ historical assertion روی `a6dd5de` موفق.

## KI-2 — تغییر ناخواستهٔ نیم‌فاصله و Unicode در literal متن

**شرح اصلی:** در متن فارسی، U+200C یا نیم‌فاصله ممکن است به underscore تبدیل شود.

**Reproduction فعلی:**

```text
چاپ -قلم بالا-
```

**Actual تاریخی:** در baseline خروجی `قلم_بالا` مشاهده شد؛ در candidate فعلی این reproduction دیگر برقرار نیست و literal به‌صورت `قلم‌بالا` حفظ می‌شود.

**Expected:** literal متن باید محتوای Unicode منبع را حفظ کند، مگر آنکه specification صریحاً transformation تعریف کند.

**Evidence:** `src/tirotir/core.py` و smoke test baseline.

**Root cause:** اثبات‌شده در `parse()`: پیش از tokenization کل source با `src.replace('\u200c', '_')` تغییر می‌کرد. `norm()` همچنان فقط روی tokenهای عدد/شناسه اعمال می‌شود؛ literal رشته مستقیماً از buffer token ساخته می‌شود.

**اثر امنیتی:** امنیت مستقیم ندارد، اما محتوای کاربر تغییر می‌کند و می‌تواند در متن آموزشی یا دادهٔ فارسی زیان‌بار باشد.

**اصلاح پیشنهادی:** جداسازی normalization شناسه از literal؛ افزودن تست حروف فارسی/عربی، نیم‌فاصله، کشیده، combining marks، ارقام فارسی و mixed script.

**وضعیت:** `VERIFIED` در candidate/review scope. `parse()` دیگر کل منبع را با `replace(\u200c, _)` تغییر نمی‌دهد؛ normalization شناسه در `norm()` باقی مانده است و lexer اکنون U+200C داخلی را نیز می‌پذیرد. این وضعیت به‌معنای release نهایی یا تأیید native Windows/دستگاه صوتی نیست. Regressionهای literal و identifier در `tests/test_core.py::test_zero_width_non_joiner_is_preserved_in_string` و `tests/test_u200c_identifiers.py` ثبت شده‌اند.

**Migration risk:** متوسط؛ برنامه‌هایی که به underscore فعلی در literal تکیه دارند باید شناسایی شوند، اما aliasهای دارای نیم‌فاصله با تست integration حفظ شدند.

**Verification:** پس از checkpoint اولیه `245 passed`؛ پس از افزودن تست‌های مستقل characterization، `252 passed`؛ در review نهایی `282 passed` و در candidate نهایی `291 passed`. آزمون‌ها حفظ متن و نیم‌فاصله، نرمال‌سازی `ك/ي` برای شناسه، alias نیم‌فاصله‌دار و پذیرش U+200C داخلی در identifier را پوشش می‌دهند. اصلاح literal در commit `3749e69` و اصلاح identifier در `dc110f3` ثبت شده‌اند؛ candidate نهایی با full suite و CI Linux تأیید شده، اما release عمومی نیست.

**افزونهٔ ممیزی U+200C در شناسه‌ها:** سند محصول نیم‌فاصله را در شناسه‌ها مجاز و معادل underscore تعریف می‌کند، اما lexer پیش از این آن را در الگوی شناسه نمی‌پذیرفت. در شاخهٔ مستقل `audit/u200c-identifier-fix`، الگوی lexer با کمترین تغییر در `src/tirotir/core.py` اصلاح شد؛ `norm()` همچنان `نام‌گذاری` را به `نام_گذاری` تبدیل می‌کند و مسیر literal دست‌نخورده است. آزمون مستقل `tests/test_u200c_identifiers.py` شامل ۹ مورد regression است: انتساب/استفاده، تابع و return، شش مثال رسمی، و حفظ literal/escape. نتیجه: `9 passed`، full suite نهایی `291 passed` و وضعیت candidate `VERIFIED` است؛ این مورد هنوز release عمومی محسوب نمی‌شود.

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

**Actual پیش از اصلاح:** registry در حالت پیش‌فرض فقط `core` را فعال می‌کرد، اما مسیر واقعی `execute()` به registry/context دسترسی نداشت و `execute("مربع با ۱۰", scene_path=...)` بدون capability SVG می‌ساخت. هیچ فراخوانی `.require()` در مسیر graphics/audio/gui وجود نداشت.

**Actual پس از اصلاح:** `RuntimeContext` با پیش‌فرض core-only به `execute()` و `Interpreter` منتقل می‌شود. graphics، audio و GUI درست پیش از اثر جانبی capability متناظر را require می‌کنند. CLI commandهای explicit، project config و launcher builder policy را به runtime می‌رسانند.

**Expected:** هر عملیات بیرونی قبل از اجرا capability مناسب را require کند؛ bypass از CLI، module، GUI و builder ممکن نباشد.

**Evidence:** `src/tirotir/contracts.py`، `src/tirotir/core.py`، `src/tirotir/audio.py`، `src/tirotir/builder.py`.

**Root cause پیش از اصلاح:** اثبات‌شده؛ `CapabilityRegistry` فقط در `contracts.py` تعریف شده بود و `Interpreter.__init__`، `execute()`، `graphics()`، `audio_note()` و `gui_command()` registry نمی‌گرفتند.

**اصلاح پیشنهادی:** RuntimeContext واحد با registry، service adapterها، تست active/disabled برای هر capability و تست path traversal. این سازوکار sandbox کامل OS نیست.

**وضعیت:** `VERIFIED` در branch KI-5؛ enforcement runtime برای scope graphics/audio/gui و مسیرهای مستقیم، CLI، project و builder launcher تأیید شده است.

**آزمون‌ها:** `tests/test_ki5_capability_enforcement.py` شامل ۱۴ تست مثبت/منفی؛ `tests/test_known_issues.py::test_ki5_graphics_execution_requires_registry`؛ تست‌های module و release integration.

**Migration risk:** متوسط؛ رفتارهایی که اکنون بدون permission اجرا می‌شوند ممکن است بعد از اصلاح رد شوند.

**Verification:** تست اختصاصی `14 passed`، full regression `273 passed`، و module/release integration `28 passed`. تست‌های منفی نبود SVG/WAV و رد GUI پیش از ساخت backend را بررسی می‌کنند. تست parse-only و اجرای native Windows/دستگاه صوتی همچنان خارج از این verification هستند.

**Commit و verification:** `20f01ab5cb8eb998fd12fa215977baa994f87e51`؛ طراحی مسیر اجرا در `4cbee2400f8a44828918764b4829bde66a528f90` ثبت شده است.

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

**Root cause:** اثبات‌شده و مربوط به پارامتر/Return نیست. `parse()` برای نمونهٔ مربع AST درست با `Func(args=["عدد"])`، `Return` و `Call(args=[5])` می‌سازد. در `Interpreter.val()`، نام `مربع` پیش از lookup تابع کاربر در فهرست primitiveهای graphics بررسی می‌شود؛ `Scene.command("مربع", ...)` مقدار `None` می‌دهد و تابع کاربر اصلاً اجرا نمی‌شود. تابع جمع با همان مسیر Return مقدار `5` می‌دهد.

**آزمون تاریخی:** `tests/test_known_issues.py::test_ki9_square_example_is_a_builtin_name_collision` AST معتبر و خروجی baseline `None` را characterization می‌کرد. regression جدید اولویت تابع کاربر را مستقل تأیید می‌کند.

**وضعیت:** `VERIFIED` در candidate scope. قرارداد این candidate آن است که تابع کاربرِ هم‌نام بر primitive گرافیکی اولویت دارد؛ primitive گرافیکی وقتی تابع هم‌نام تعریف نشده باشد بدون تغییر اجرا می‌شود. کوچک‌ترین تغییر فقط شرط dispatch graphics را به `n.name not in self.funcs` محدود کرد.

**آزمون‌ها:** `tests/test_known_issues.py::test_ki9_user_function_takes_precedence_over_graphics_name_collision`، `test_ki9_graphics_primitive_still_runs_without_name_collision` و آزمون موجود تابع جمع.

**Verification:** focused regression و acceptance/graphics موفق؛ focused نهایی شامل این مسیر در مجموعهٔ `38 passed` و full suite نهایی `291 passed` است. این وضعیت `VERIFIED` candidate است، نه ادعای release عمومی یا cross-platform.

**Migration risk:** متوسط؛ برنامه‌ای که عمداً تابعی با نام primitive گرافیکی تعریف کرده باشد اکنون اولویت تابع کاربر را دریافت می‌کند. برنامه‌های بدون collision unchanged هستند.

**Commit و verification:** `e3c1cd8`; regression collision و primitive بدون collision موفق شدند.

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

**وضعیت:** `VERIFIED` در candidate scope. `pyproject.toml` اکنون حداقل Python را `>=3.11` اعلام می‌کند؛ این مقدار با import مستقیم `tomllib` و نصب پاک candidate سازگار است. این تغییر به‌معنای پشتیبانی آزموده‌نشده از Python 3.9/3.10 نیست و آن نسخه‌ها دیگر target اعلام‌شده نیستند.

**Migration risk:** متوسط؛ تغییر حداقل نسخه روی کاربران قدیمی اثر دارد.

**Commit و verification:** `276e55f`؛ تست consistency در `tests/test_2_runtime_contracts.py` و نصب پاک wheel با Python 3.12 موفق شد.

## KI-12 — ناسازگاری metadata و انتشار

**شرح اصلی:** version، author، repository، citation، license و artifactها باید منبع واحد داشته باشند.

**Actual تاریخی:** `CITATION.cff` repository اصلی را ثبت می‌کرد و `vscode-tirotirLang/package.json` repository متفاوت `github.com/tirotir/tirotir` را اعلام می‌کرد. در candidate فعلی URL افزونه با repository واقعی هماهنگ شده است؛ وجود فایل‌های license و اسناد تاریخی همچنان باید در release review جداگانه بررسی شود.

**Expected:** یک source of truth برای name/version/author/date/repository و validation خودکار.

**Evidence:** `CITATION.cff`، `pyproject.toml`، `vscode-tirotirLang/package.json`، docs release.

**Root cause:** metadata در چند فایل دستی نگه‌داری می‌شود.

**اصلاح پیشنهادی:** version check script، validation `CITATION.cff`، CI consistency test، تصمیم دربارهٔ LICENSE تکراری و repository افزونه.

**وضعیت:** `VERIFIED` در candidate scope برای version/repository metadata؛ بررسی نهایی license و release artifact هنوز خارج از این verification است.

**Migration risk:** کم برای runtime؛ زیاد برای اعتماد release و citation.

**Commit و verification:** `a44ca6b`؛ consistency regression، package metadata و VSIX integrity check موفق شدند.

## KI-13 — پوشش سیستم‌عامل و artifact کامل نیست

**شرح اصلی:** regression فعلی فقط در Linux/Python 3.12.3 اجرا شده است.

**Actual:** Linux با Python 3.12 و GitHub Actions matrix برای Python 3.11/3.12 تأیید شده است. Windows، macOS، Setup، GUI روی desktop فیزیکی و playback واقعی تأیید نشده‌اند.

**Expected:** CI برای Linux/Windows/macOS و نسخه‌های Python پشتیبانی‌شده، artifact test و نمونه‌های رسمی.

**Evidence:** `.github/workflows/ci.yml`، run موفق GitHub Actions برای SHA `cf6a30d` در [run 39102503306](https://github.com/worker2025/tirotir/actions/runs/39102503306)، full suite `291 passed` و docs release.

**Root cause:** CI cross-platform در checkout موجود نیست یا قابل مشاهده نیست.

**اصلاح پیشنهادی:** matrix CI، coverage، artifact install test، smoke test Windows و ثبت environment.

**وضعیت:** `BLOCKED` برای آزمون کامل cross-platform؛ Linux/Python 3.11-3.12 CI در candidate verified.

**Migration risk:** کم تا متوسط؛ ممکن است failureهای platform-specific آشکار شوند.

**Commit و verification:** `d51941a`؛ CI واقعی run `39102503306` موفق، اما Windows/macOS هنوز blocked.

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

## وضعیت مستندات مرجع

فایل `known-issues-fa.md` در ریشهٔ repository عمداً به‌عنوان گزارش تاریخی نسخهٔ منتشرشدهٔ 1.1.0 باقی مانده است؛ خود فایل commit مبنای `481f15fcd18b21d38fc9161b69489d4560ce091b` را اعلام می‌کند. این سند traceability وضعیت worktree توسعه و شواهد جدید را ثبت می‌کند و بدون انتشار نسخهٔ جدید، ادعاهای سند تاریخی را بازنویسی نمی‌کند.

## checkpoint آزمون مستقل این مرحله

فایل `tests/test_known_issues.py` هفت آزمون مستقل دارد:

1. حفظ literal فارسی و U+200C؛
2. استمرار نرمال‌سازی `ك/ي` در شناسه‌ها؛
3. characterization توکن‌های متن سالم و تفریق فاصله‌دار/فشرده؛
4. حفظ برنامهٔ تابع جمع موجود؛
5. تصمیم مثبت/منفی registry؛
6. اثبات bypass مسیر graphics در نبود context؛
7. اثبات collision نام `مربع` با primitive graphics در KI-9.

این آزمون‌ها ابتدا characterization بودند؛ در candidate نهایی KI-1، KI-2، KI-5 و KI-9 با regression و integration verification شده‌اند. این وضعیت به‌معنای release عمومی یا sandbox کامل سیستم‌عامل نیست.
