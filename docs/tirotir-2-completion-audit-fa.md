# گزارش ممیزی عملی Tirotir 2.0

> **یادداشت نسخهٔ فعلی:** این سند شامل checkpointها و اعداد تاریخی ممیزی است. وضعیت جاری و عدد رسمی release در [گزارش پایدار Tirotir 2](tirotir-2-stable-release-fa.md) ثبت می‌شود: Python `2.0.2`، افزونه `2.0.6` و full suite برابر `291 passed`.

**تاریخ ممیزی:** ۱۸ اکتبر ۲۰۲۶
**شاخه:** `development/tirotir-2.0-20261017T110755Z`
**نقطهٔ شروع:** `385da8a11f8c6a3939046a3ee31790583094e0c0`
**commitهای این مرحله:** `276e55f` و `5fa8882`
**محیط:** Linux x86_64، Python 3.12.3، pytest 9.1.1

**وضعیت سند:** این گزارش ابتدا برای candidate توسعه نوشته شد؛ پس از validation نهایی و هماهنگ‌سازی نسخه، release رسمی `v2.0.0` بر همان شواهد و با محدودیت‌های ثبت‌شده ساخته می‌شود.

## نتیجهٔ اجرایی

نسخهٔ فعلی یک **candidate عملی برای Linux/Python 3.11+** است، نه release عمومی نهایی. هستهٔ زبان، CLI، نصب Python package، تولید SVG، تولید WAV، capabilityهای graphics/audio/gui، module execution و مسیر VS Code دارای کد و regression واقعی هستند. GUI با Tkinter در این sandbox پس از نصب `python3-tk` و با `Xvfb` به‌صورت واقعی smoke شد.

اعلام «آمادهٔ انتشار عمومی» مجاز نیست؛ اجرای native Windows، macOS، installer، VS Code واقعی و پخش صوت از بلندگوی واقعی در این محیط تأیید نشده‌اند.

## تغییرات این مرحله

### هماهنگ‌سازی version و Python requirement — `276e55f`

- `pyproject.toml` از نسخهٔ تاریخی `1.1.0` به `2.0.0.dev0` تغییر کرد.
- حداقل Python از `>=3.9` به `>=3.11` تغییر کرد؛ علت استفادهٔ مستقیم از `tomllib` در `src/tirotir/modules/project.py` است.
- `src/tirotir/__init__.py` و CLI از یک version واحد استفاده می‌کنند.
- نسخهٔ VS Code extension به `2.0.0-dev` تغییر کرد.
- CLI خطای EOF ورودی استاندارد را به پیام فارسی قابل‌فهم تبدیل می‌کند و traceback خام نشان نمی‌دهد.
- چهار regression جدید در `tests/test_2_runtime_contracts.py` اضافه شد.

### تکمیل مسیر پایهٔ GUI — `5fa8882`

- widgetهای Tkinter اکنون واقعاً در `Gui.widgets` نگه‌داری می‌شوند؛ پیش از این نتیجهٔ `pack()` ذخیره می‌شد و widget واقعی از دست می‌رفت.
- دکمه می‌تواند پیام callback ساده دریافت کند و هنگام click آن را از مسیر runtime به output تحویل دهد.
- تست headless با fake Tkinter و تست واقعی با Tkinter/Xvfb اضافه و اجرا شدند.

## نتایج آزمون

### تست واحد و regression

```text
python3 -m pytest -q
286 passed
```

نتایج قبلی پیش از این مرحله `282 passed` بود. چهار تست مربوط به قرارداد version و EOF اضافه شدند. تست GUI جدید نیز در همین مجموعه حضور دارد.

### تست‌های متمرکز

```text
tests/test_2_runtime_contracts.py                         4 passed
 tests/test_gui_runtime.py                                1 passed
tests/test_u200c_identifiers.py                           9 passed
tests/test_ki1_candidate_acceptance.py و KI-5             21 passed
```

### نصب پاک

در یک virtualenv موقت، checkout با `git archive` نصب شد:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --no-deps <checkout>
.venv/bin/tirotir version
.venv/bin/tirotir run examples2/basics/hello_world.t
.venv/bin/tirotir check examples2/basics/hello_world.t
.venv/bin/tirotir graphics examples2/graphics/hello_shape.t --scene scene.svg
```

نتیجهٔ واقعی:

- نصب wheel موفق؛
- `Tirotir 2.0.0.dev0`؛
- اجرای hello فارسی موفق؛
- semantic check موفق؛
- تولید SVG غیرخالی موفق.

### GUI واقعی

وابستگی سیستم `python3-tk` نصب شد و با `Xvfb` آزمایش شد. smoke test واقعی:

- ایجاد پنجرهٔ Tkinter؛
- تنظیم title و geometry؛
- ایجاد label و button؛
- اجرای event loop؛
- invoke واقعی button؛
- دریافت پیام callback در output؛
- خاتمهٔ صحیح پنجره.

نتیجه:

```text
real_gui_smoke=PASS
widgets=2
output=['کلیک واقعی']
```

این آزمایش GUI واقعی در display مجازی است، نه تأیید تجربهٔ کاربر روی desktop فیزیکی Windows/macOS.

## وضعیت قابلیت‌ها

| قابلیت | وضعیت واقعی | مدرک |
|---|---|---|
| lexer/parser/interpreter | عملیاتی و آزموده‌شده | full suite، 286 تست |
| KI-1 arithmetic | عملیاتی با breaking change مستند | candidate tests و baseline تاریخی |
| U+200C در literal و identifier | عملیاتی و آزموده‌شده | `test_u200c_identifiers.py`، 9 تست |
| function/return و KI-9 | عملیاتی در scope تست‌شده | known issues و release integration |
| capability graphics/audio/gui | enforcement عملی در مسیرهای پشتیبانی‌شده | positive/negative KI-5 tests |
| SVG | تولید واقعی و آزموده‌شده | release integration و نصب پاک |
| WAV | تولید واقعی و آزموده‌شده | audio integration tests |
| audio playback | فقط backend اختیاری؛ playback واقعی دستگاهی تأیید نشده | `audio.py` و تست unavailable |
| GUI | مسیر Tkinter و event callback با Xvfb smoke شد | `real_gui_smoke` و `test_gui_runtime.py` |
| modules/import | اجرای topological نمونه‌ها آزموده‌شده | module/release integration |
| CLI | نصب پاک، version، run، check و graphics موفق | clean-install smoke |
| VS Code | extension manifest و webview hardening تست شده؛ اجرای VS Code واقعی نشده | `test_vscode_webview_hardening_contract` |
| Windows/macOS artifacts | مسدود/تأییدنشده | محیط فعلی Linux است |

## امنیت و محدودیت‌ها

Capabilityهای `graphics`، `audio` و `gui` در مسیرهای مستقیم و CLI با positive/negative tests enforce می‌شوند. این سازوکار sandbox کامل سیستم‌عامل نیست و در این milestone ادعای ایزوله‌سازی کامل filesystem، network، subprocess یا secrets وجود ندارد.

Module sandbox مسیر canonical را داخل project root محدود می‌کند. اجرای import آزاد Python، `eval` و `exec` از زبان پشتیبانی نمی‌شود؛ بااین‌حال این موضوع جایگزین sandbox OS یا اجرای untrusted code در process جدا نیست.

## breaking changes

رفتار arithmetic فشرده همچنان عمداً تغییر کرده است:

```text
baseline 1.1.0: چاپ ۵-۳+۲-۱ → 5
candidate 2.0:  چاپ ۵-۳+۲-۱ → 3
```

همچنین حداقل Python از 3.9 اعلام‌شده به 3.11 تغییر کرده است. این تغییر برای سازگاری metadata با `tomllib` ضروری است و باید در راهنمای مهاجرت ثبت شود.

## موارد باقی‌مانده

- اجرای native Windows و ساخت/اجرای EXE؛
- اجرای macOS؛
- installer و package signing؛
- اجرای واقعی VS Code در خود VS Code؛
- پخش صوت از بلندگوی واقعی؛
- تست GUI روی desktop فیزیکی؛
- CI matrix برای Python و سیستم‌عامل‌های مختلف؛
- event syntax کامل زبان و LSP/debugger؛
- بررسی کامل project-files و network capability.

## rollback

نقطهٔ بازیابی قبل از تکمیل این مرحله:

```text
385da8a11f8c6a3939046a3ee31790583094e0c0
```

commitهای این مرحله مستقل و قابل بازگشت‌اند:

```text
276e55f  fix: align 2.0 candidate metadata and handle CLI EOF
5fa8882  fix: retain GUI widgets and dispatch button events
```

نسخهٔ پایدار `main` و tag تاریخی `v1.1.0` در این مرحله تغییر نکرده‌اند.

## ممیزی امنیت و CI پس از گزارش اولیه

در commit `d51941a`، `tests/test_security_boundaries.py` پنج آزمون واقعی برای موارد زیر اضافه کرد:

- deny-by-default برای `network` و `project-files`؛
- اثبات اینکه فعال‌کردن این enumها به‌تنهایی backend زبانی ایجاد نمی‌کند؛
- رد مسیر مطلق و parent traversal در ModuleSandbox؛
- رد symlink escape از project root؛
- بارگذاری موفق فایل داخل project root.

نتیجهٔ این تست‌ها `5 passed` و full suite جدید `291 passed` است.

فایل `.github/workflows/ci.yml` نیز matrix لینوکس برای Python 3.11 و 3.12، نصب package، نصب pytest، اجرای suite و CLI smoke را تعریف می‌کند. این workflow در این session روی GitHub runner اجرا نشده و صرفاً contract آن به‌صورت محلی بررسی شده است.

برای `network` و `project-files` در زبان فعلی primitive یا backend عمومی وجود ندارد؛ بنابراین آن‌ها عمداً «قابلیت عملیاتی» اعلام نشده‌اند. افزودن API فایل یا شبکه بدون قرارداد مسیر، policy و تست end-to-end امن، تغییر پرخطر و خارج از این patch کوچک است.

## افزونهٔ VS Code و بسته‌بندی

در این محیط `code`/VS Code CLI نصب نیست، بنابراین نصب و فعال‌سازی واقعی extension در VS Code انجام نشد. بااین‌حال VSIX با `npx @vscode/vsce package` واقعاً ساخته و با `unzip -t` بررسی شد:

```text
/tmp/tirotirlang-2.0.0-dev.vsix
SHA-256: 4ed65fe63cd7ae9de71947a9bb69f865b5d0e1b23ac42dabc8c89096cd85edd4
```

هشدار اولیهٔ vsce دربارهٔ نبودن `.vscodeignore` با افزودن این فایل رفع شد و repository metadata افزونه به `https://github.com/worker2025/tirotir` اصلاح شد. این نتیجه فقط package integrity و manifest را ثابت می‌کند، نه اجرای واقعی VS Code.

## event syntax

زیرساخت Python برای event وجود دارد و GUI callback واقعی smoke شده است، اما syntax عمومی event هنوز به زبان اضافه نشده است. افزودن syntax بدون قرارداد پایدار برای scope، lifetime، callback و ارتباط با event loop، در این مرحله تغییر پرخطر محسوب می‌شود؛ بنابراین قابلیت صوری یا نیمه‌کاره اضافه نشده است.

## اجرای مثال‌های رسمی

همهٔ ۵۱ مثال رسمی از مسیر CLI با `check` parse شدند. پس از اعمال capability صریح برای مثال‌های graphics و audio و ارسال stdin مشخص برای دو مثال ورودی، ۳۸ مثال non-GUI با موفقیت اجرا شدند. ۱۳ مثال GUI به‌دلیل نیاز به چرخهٔ تعاملی و محیط نمایش جداگانه از این ماتریس CLI کنار گذاشته شدند؛ GUI به‌صورت مستقل با Tkinter/Xvfb smoke شده است.
