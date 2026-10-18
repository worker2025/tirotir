# Changelog

## Tirotir VS Code Extension 2.0.6 — Status Bar file creation

- added a Status Bar-only button for creating a new `.t` file when a saved Tirotir file is active;
- creates `program-001.t`, `program-002.t`, `program-003.t`, and the next available number in the active file's directory;
- writes the file to disk before opening it in VS Code;
- uses exclusive file creation and never overwrites or deletes an existing file;
- keeps the command out of the editor context menu, WebView, and title bar;
- added regression coverage for the manifest and implementation contract.

## Tirotir 2.0.1 — Final release

این آخرین رلیز رسمی Tirotir 2 است: بستهٔ Python نسخهٔ `2.0.1` در PyPI و افزونهٔ VS Code نسخهٔ `2.0.6` به‌صورت VSIX.

### تغییرات اصلی

- package metadata requires Python `>=3.11` and exposes the project URLs;
- `tirotir==2.0.1` is available from the public [PyPI project page](https://pypi.org/project/tirotir/);
- installation is documented with `python -m pip install tirotir==2.0.1`;
- maintained the `examples2` bundle with Persian instructions and capability-aware execution commands;
- added interactive UTF-8 input coverage, including stdin, EOF and invalid numeric input;
- documented direct wheel/source installation as alternatives for offline or development use;
- verified the current checkout with a full suite of `304 passed` tests;

### افزونهٔ VS Code و اسنیپت‌ها

- fixed VS Code snippet discoverability for `.t` files;
- kept the standard `contributes.snippets` declaration for language id `tirotirLang`;
- enabled snippet suggestions and `Tab` completion through language-specific defaults;
- added an extension-side completion provider using `SnippetString` as a fallback when native snippet suggestions are hidden by user settings;
- bundled and verified 14 Persian snippets in the final VSIX;
- rebuilt and integrity-checked `tirotirlang-2.0.6.vsix`.

### اعتبارسنجی نهایی

- full suite: `304 passed`;
- syntax و JSON manifest افزونه: موفق؛
- integrity بستهٔ VSIX: موفق؛
- اجرای مثال‌های هسته، ورودی تعاملی، Graphics و Audio: موفق؛
- GUI، اجرای native Windows، پخش سخت‌افزاری صدا و sandbox کامل OS همچنان وابسته به محیط واقعی و خارج از شواهد این sandbox هستند.


## Tirotir 2.0.0 — 2026-10-18
این release رسمی نسخهٔ ۲٫۰ است. محدودیت‌های پلتفرم، GUI، صوت، VS Code و sandbox در README و Known Issues صریحاً ثبت شده‌اند.

### تغییر KI-1: arithmetic فشرده

رفتار lexer برای عبارت‌های حسابی فشرده اصلاح شده است:

```text
Historical baseline 1.1.0:
چاپ ۵-۳+۲-۱ → 5

Tirotir 2.0.0:
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

### ممیزی U+200C در identifierها

در audit branch مستقل `audit/u200c-identifier-fix`، lexer اکنون U+200C را داخل identifier می‌پذیرد و normalization قراردادی آن را به underscore تبدیل می‌کند؛ بنابراین identifierهایی مانند `نام‌گذاری` به `نام_گذاری` نگاشت می‌شوند. مسیر literal متن و escapeها تغییر نکرده‌اند. شش مثال رسمی دارای این نویسه اکنون parse و اجرا می‌شوند.

این اصلاح ابتدا در audit branch ثبت و سپس همراه review به `development/tirotir-2.0-20261017T110755Z` منتقل شد؛ release عمومی محسوب نمی‌شود. commit ممیزی: `dc110f3`.

### تکمیل release در development

- metadata پکیج، runtime و افزونه به نسخهٔ رسمی `2.0.0` هماهنگ شد؛
- حداقل Python به `>=3.11` تغییر کرد، چون module loader از `tomllib` استفاده می‌کند؛
- EOF ورودی استاندارد اکنون پیام خطای فارسی کنترل‌شده می‌دهد؛
- مسیر GUI widgetها را نگه می‌دارد و callback سادهٔ دکمه را dispatch می‌کند؛ این مسیر با fake Tkinter و Tkinter واقعی تحت Xvfb آزمایش شد؛
- full suite پس از این تغییرات: `286 passed`؛
- security boundary tests برای `network`، `project-files`، traversal و symlink escape: `5 passed`؛ full suite فعلی: `291 passed`؛
- CI لینوکس برای Python 3.11 و 3.12 به `.github/workflows/ci.yml` اضافه شد؛ اجرای GitHub runner در این session انجام نشده است.

این release رسمی است، اما به‌معنای تأیید Windows/macOS، installer، VS Code واقعی یا پخش صوت دستگاهی نیست.

### وضعیت validation

- candidate acceptance: `7 passed`؛
- KI-5 dedicated enforcement: `14 passed`؛
- full review suite: `273 passed` روی commit `d32f97abdfdee69e40b839e35b81f99531b3c0b3`؛
- historical baseline: assertion مستقل روی commit `a6dd5dec1b4b9e2a304fec0a6cf06aecac7b417` موفق شد؛
- module/release integration: `28 passed`؛
- audit regression برای U+200C در identifierها: `9 passed`؛
- full suite در audit branch: `282 passed`؛
- دو مثال نیازمند ورودی تعاملی و ۱۳ مثال GUI در اجرای end-to-end محیط sandbox جداگانه گزارش شده‌اند؛ parse-only corpus برابر `51/51` موفق است.

### خارج از این تغییر

این changelog به معنی sandbox کامل سیستم‌عامل، enforcement مستقل `network` و `project-files`، اجرای واقعی Windows EXE، GUI روی desktop واقعی، پخش صوت واقعی، تکمیل GUI-1، LSP، debugger، namespace کامل یا آماده‌بودن release عمومی Tirotir 2.0 نیست. برای جزئیات به [README](README.md)، [برنامهٔ پذیرش KI-1](docs/tirotir-2-ki1-acceptance-plan-fa.md)، [ماتریس verification KI-5](docs/tirotir-2-ki5-verification-fa.md) و [سند مسائل شناخته‌شده](known-issues-fa.md) مراجعه کنید.

## Tirotir 1.1.0

سوابق release نسخهٔ ۱٫۱٫۰ در اسناد تاریخی `docs/public-release-readiness-fa.md` و `docs/release-readiness-fa.md` نگه‌داری شده‌اند و در این commit بازنویسی نشده‌اند.

### اعتبارسنجی پیش از انتشار آزمایشی

- remote branch `development/tirotir-2.0-20261017T110755Z` روی SHA `cf6a30dd536f11c1e42076ebc4778dae8418ee4b` تأیید شد؛
- GitHub Actions واقعی برای Linux و Python 3.11/3.12 موفق شد: [run 39102503306](https://github.com/worker2025/tirotir/actions/runs/39102503306)؛
- full suite محلی: `291 passed`؛ focused security/runtime/KI suite: `38 passed`؛
- parse مثال‌های رسمی: `51/51`؛ اجرای non-GUI با capability لازم: `38 passed`؛
- نصب پاک، CLI، تولید SVG و تولید WAV موفق شد؛ پخش سخت‌افزاری صدا و VS Code واقعی در محیط موجود نبود؛
- VSIX از commit نهایی ساخته و با `unzip -t` بررسی شد؛ checksum در گزارش ممیزی ثبت شده است.

این validation برای release رسمی در محدودهٔ Linux/Python 3.11-3.12 انجام شده است؛ محدودیت‌های خارج از این محدوده پابرجاست.

### راهنمای آزمایش candidate

راهنمای [فارسی آزمایش](docs/tirotir-2-experimental-testing-fa.md) و [انگلیسی آزمایش](docs/tirotir-2-experimental-testing-en.md) شامل نصب، اولین اجرا، KI-1، capabilityها، محدودیت‌های محیط و قالب گزارش خطا هستند.
