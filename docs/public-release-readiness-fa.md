# گزارش آمادگی انتشار عمومی Tirotir 1.1.0

## جمع‌بندی اجرایی

**وضعیت:** آمادهٔ انتشار به‌عنوان release candidate برای نصب و توسعه روی Windows، با یک مرحلهٔ smoke test native پیشنهادی قبل از انتشار عمومی گسترده.

هستهٔ زبان، semantic diagnostics، module system، graphics SVG، تولید sequence صوتی WAV، GUI اختیاری Tkinter، CLI، VS Code WebView و prototype EXE Builder در این branch یکپارچه و regression شده‌اند. یک regression واقعی در semantic layer رفع شد: پنج primitive GUI که runtime آن‌ها را داشت اما analyzer نمی‌شناخت، اکنون end-to-end ثبت شده‌اند. پسوند رسمی فایل `.t` است؛ `.tirotir` فقط برای سازگاری با پروژه‌های قدیمی پذیرفته می‌شود.

## Verified در sandbox

| حوزه | نتیجه |
|---|---|
| Unit/integration/semantic tests | **244 passed** |
| مثال‌های رسمی قابل اجرای headless | **9/9 passed** |
| نمونه‌های موجود repository | **71 فایل** با نام‌های انگلیسی استاندارد و پسوند رسمی `.t` |
| Audio sequence | تولید یک WAV پیوسته با 46,305 frame برای `scale.t` |
| Graphics regression | چهار خط واقعی برای مربع، movement/rotation و رنگ فارسی آبی |
| SVG viewport | fit-to-scene با padding و پشتیبانی مختصات منفی |
| Project/module config | entry رسمی `main.t` و sandbox/module graph tests |
| VS Code assets | JSON معتبر و VSIX قابل ساخت |
| Builder path resolver | پیدا کردن launcher و تولید entrypoint مستقل تایید شد |
| Builder standalone source | با حذف فایل source اصلی، entrypoint جاسازی‌شده با موفقیت اجرا و WAV تولید کرد |
| Python syntax | تمام فایل‌های `src/tirotir` و زیرماژول‌ها compile شدند |

## CI Verified

فرمان quality gate اجراشده:

```text
python3 -m pytest -q
python3 -m json.tool vscode-tirotirLang/package.json
python3 -m json.tool vscode-tirotirLang/syntaxes/tirotir.tmLanguage.json
python3 -m py_compile src/tirotir/*.py src/tirotir/modules/*.py
```

خروجی تست Python: `244 passed in 0.91s`. همهٔ **۱۰ نمونهٔ موجود با پسوند `.t`** از semantic check عبور کردند. هر سه نمونهٔ صوتی `melody.t`، `render_only.t` و `scale.t` WAV معتبر با نرخ 44100 هرتز ساختند. Wheel نسخهٔ `1.1.0` و VSIX نسخهٔ `1.1.0` ساخته شدند. Source archive نیز به‌صورت tar.gz آماده شد.

## Manual Acceptance پیشنهادی روی Windows

این موارد به native Windows یا desktop session نیاز دارند و در sandbox headless ادعا نشده‌اند:

1. نصب wheel با Python 3.11 یا 3.12 و اجرای `tirotir version`؛
2. اجرای `tirotir run examples\audio\scale.t --play-audio` و شنیدن sequence یک‌باره؛
3. اجرای `tirotir run examples\graphics\square.t` و مشاهدهٔ SVG در VS Code WebView؛
4. اجرای `tirotir gui examples\gui\hello_window.t`، `widgets.t` و `form.t`؛
5. بازکردن فایل `.t` در VS Code و مشاهدهٔ association، highlighting و خروجی RTL؛
6. اجرای `tirotir builder`، انتخاب یک `.t`، ساخت EXE و اجرای EXE خروجی؛
7. بررسی این‌که فایل‌های legacy `.tirotir` هنوز با CLI و ModuleLoader کار می‌کنند.

## محدودیت‌های شناخته‌شده

GUI به Tkinter و desktop نیاز دارد و در محیط headless قابل مشاهده نیست. Audio playback به backend سیستم‌عامل وابسته است؛ تولید WAV مستقل و بدون dependency اجباری است. Builder اکنون source را در entrypoint جاسازی می‌کند و packageٔ runtime را برای PyInstaller در اختیار می‌گذارد، اما native PyInstaller build و اجرای EXE باید روی Windows انجام شود. Graphics فعلی renderer استاتیک SVG است و timeline/event animation هنوز بخشی از نسخهٔ 1.1.0 نیست. VS Code extension live rendering به اجرای CLI و protocol فعلی متکی است و هنوز LSP/DAP کامل ندارد.

## وضعیت مستندات و migration

نمونه‌های رسمی و راهنماهای اصلی به `.t` مهاجرت کرده‌اند. referenceهای عمدی `.tirotir` فقط در تست‌های compatibility، قراردادهای تاریخی SourceSpan/semantic و توضیح migration نگه داشته شده‌اند. این موارد نباید به‌عنوان پسوند پیش‌فرض جدید تفسیر شوند.

## artifactهای release

- `tirotir-1.1.0-py3-none-any.whl`: بستهٔ نصب Python
- `tirotir-1.1.0.tar.gz`: source archive
- `tirotirLang-1.1.0.vsix`: افزونهٔ VS Code

## توصیهٔ انتشار

نسخه را ابتدا به‌صورت **Release Candidate** روی Windows با چک‌لیست Manual Acceptance بالا منتشر کنید. پس از تایید GUI، audio playback، VSIX association و EXE واقعی، tag `v1.1.0` را برای انتشار عمومی ثبت کنید. برای Tirotir 2.0، event runtime، LSP، object model و debugger باید بعد از تثبیت همین قراردادهای فعلی و بدون افزودن APIهای backend-specific طراحی شوند.
