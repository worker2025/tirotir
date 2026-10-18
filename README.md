# تیروتیر — Tirotir 2

<p align="center">
<img src="assets/logo/tirotir-logo.png" alt="Tirotir Logo" width="180">
</p> <p align="center">
  <strong>تیروتیر (Tirotir)</strong>

  یک زبان برنامه‌نویسی متنی فارسی و مفسری
</p> <p align="center">
  <a href="https://tirotir.ir/">Website</a> •
  <a href="https://tirotir.com/">Tirotir.com</a> •
  <a href="https://github.com/worker2025/tirotir">GitHub</a> •
  <a href="https://doi.org/10.5281/zenodo.22874866">DOI</a>
</p>

---

## دربارهٔ تیروتیر

**تیروتیر** یک زبان برنامه‌نویسی متنی فارسی و مفسری است که برای **یادگیری برنامه‌نویسی، آموزش مفاهیم محاسباتی و ساخت برنامه‌های واقعی** طراحی شده است.

می‌توان با یک دستور ساده شروع کرد:

```
چاپ -سلام دنیا-
```

و سپس به مفاهیمی مانند:

- متغیر

- شرط

- حلقه

- تابع

- فهرست

- فرهنگ

- ورودی و خروجی

- پروژه‌های چندفایلی

- Module System

رسید.

تیروتیر همچنین ابزارها و قابلیت‌های پیرامونی برای **Graphics، Audio و GUI** ارائه می‌کند.

🌐 [tirotir.ir](https://tirotir.ir/)
🌐 [tirotir.com](https://tirotir.com/)
💻 [GitHub](https://github.com/worker2025/tirotir)

---

## DOI و استناد

**DOI:**
[https://doi.org/10.5281/zenodo.22874866](https://doi.org/10.5281/zenodo.22874866)

اگر از تیروتیر در یک مقاله، پژوهش، پروژهٔ دانشگاهی یا آموزشی استفاده می‌کنید، لطفاً به پروژه استناد کنید:

> Alipour, Daryoush. *Tirotir — Persian Programming Language*.
[https://doi.org/10.5281/zenodo.22874866](https://doi.org/10.5281/zenodo.22874866)

---

## 🤖 مشاور هوشمند زبان برنامه‌نویسی — Tirotir AI

**به Tirotir AI خوش آمدید**

مشاور فارسی‌زبان شما برای یادگیری و ساخت با زبان برنامه‌نویسی Tirotir؛ از کدهای `.t` تا GUI، Graphics، Audio، VS Code و EXE Builder.

🌐 **دسترسی:** [https://ai.tirotir.com/](https://ai.tirotir.com/)

---

# وضعیت فعلی

## Tirotir 2.0.1 — آخرین رلیز رسمی

برای نسخهٔ مرتب و نهایی رلیز، [سند نهایی Tirotir 2](docs/tirotir-2-final-release-fa.md) را ببینید.

نسخهٔ **2.0.1** آخرین رلیز رسمی بستهٔ Python تیروتیر ۲ است و از PyPI قابل نصب است. افزونهٔ VS Code این رلیز در نسخهٔ **2.0.5** ارائه می‌شود. full suite فعلی checkout برابر **۳۰۳ تست موفق** است.

ویژگی‌های اصلی نسخهٔ ۲:

- زبان برنامه‌نویسی مفسری فارسی

- پسوند رسمی فایل: `.t`

- پشتیبانی از شناسه‌های فارسی و Unicode

- Lexer

- Parser

- AST

- Semantic Analyzer

- Diagnostics ساختاریافته

- پیام‌های خطای فارسی

- CLI

- REPL

- Project System

- Module System چندفایلی

- Graphics با خروجی SVG

- Audio با تولید WAV

- GUI مبتنی بر Tkinter

- افزونهٔ VS Code

- Builder برای ساخت EXE در Windows

- Runtime با قابلیت‌های کنترل‌شده

- **۳۰۳ تست موفق در full suite فعلی نسخهٔ ۲**؛ آمار تاریخی baseline نسخهٔ ۱٫۱٫۰ برابر **۲۴۴ تست موفق** بوده است.

پسوند قدیمی نسخهٔ ۱:

```
.tirotir
```

نیز برای سازگاری با پروژه‌های قدیمی حفظ شده است.

> **یادداشت تاریخی:** نسخهٔ ۱٫۱٫۰ یک baseline قدیمی پروژه است و نباید به‌عنوان وضعیت فعلی یا آخرین رلیز تفسیر شود. آمار ۲۴۴ تست فقط به همان baseline تاریخی مربوط است.

---

## نصب رسمی Tirotir 2.0

نسخهٔ patch فعلی `2.0.1` است و بستهٔ رسمی در [PyPI](https://pypi.org/project/tirotir/) منتشر شده است. روش نصب پیشنهادی:

```bash
python -m pip install tirotir==2.0.1
```

برای نصب آفلاین یا توسعه، wheel یا source archive رسمی GitHub Release نیز قابل استفاده است:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
py -3.11 -m pip install tirotir==2.0.1
tirotir version
```

در دستور بالا برای اطمینان از interpreter درست در Windows از `py -3.11 -m pip show tirotir` و `Get-Command tirotir -All` استفاده کنید. راهنمای مثال‌های قابل‌اجرا در [examples2/README-fa.md](examples2/README-fa.md) و راهنمای جامع نسخهٔ ۲ قرار دارد.

## وضعیت توسعهٔ Tirotir 2.0

نسخهٔ رسمی **Tirotir 2.0.0** بر پایهٔ شاخهٔ توسعهٔ اعتبارسنجی‌شده منتشر شده است و patch release `2.0.1` اصلاحات بسته‌بندی و examples را اضافه می‌کند. full suite فعلی checkout برابر **۳۰۳ تست موفق** است؛ این عدد شامل regressionهای version/EOF، GUI، security boundary، ورودی تعاملی، VSIX و اسنیپت‌هاست. baseline تاریخی نسخهٔ ۱٫۱٫۰ جداگانه **۲۴۴ تست موفق** داشته است؛ این آمارها با هم جمع یا جایگزین نمی‌شوند.

### قابلیت‌های پیاده‌سازی‌شده و آزموده‌شده در checkpoint فعلی

- رفتار حسابی فشردهٔ جدید: `چاپ ۵-۳+۲-۱` خروجی `3` می‌دهد؛
- حفظ literalهای فارسی و نیم‌فاصلهٔ U+200C در متن؛
- حفظ escapeهای مستندشده، import ماژول و بازگشت مقدار از تابع؛
- اولویت تابع کاربر بر primitive گرافیکی هم‌نام؛
- enforcement قابلیت‌های `graphics`، `audio` و `gui` در مسیرهای مستقیم، CLI، project و builder launcher که آزموده شده‌اند؛
- پذیرش U+200C در شناسه‌ها با حفظ قرارداد normalization به underscore؛ شش مثال رسمی مرتبط اکنون parse و اجرا می‌شوند؛
- هستهٔ lexer، parser، interpreter، CLI و module system موجود در baseline؛
- تولید SVG، تولید WAV و GUI مبتنی بر Tkinter، با محدودیت‌های محیطی و release که در اسناد آمده‌اند.

### قابلیت‌های ناتمام یا برنامه‌ریزی‌شده

- enforcement مستقل `project-files` و `network` و بررسی همهٔ launcherهای خارجی هنوز انجام نشده است؛ کنترل graphics/audio/gui به‌تنهایی sandbox سیستم‌عامل نیست؛
- اصلاح شناسه‌های دارای نیم‌فاصله در release 2.0.0 ثبت و آزموده شده است؛
- metadata candidate، حداقل Python `>=3.11` و مدیریت EOF CLI هماهنگ و آزموده شده‌اند؛
- GUI با Tkinter و Xvfb به‌صورت واقعی smoke شده است، اما اجرای desktop فیزیکی و Windows هنوز تأیید نشده‌اند؛
- traversal و symlink escape در ModuleSandbox آزموده شده و برای `network` و `project-files` نبود backend زبانی عمداً صریح ثبت شده است؛
- CI لینوکس برای Python 3.11 و 3.12 در `.github/workflows/ci.yml` اضافه شده است؛
- namespace کامل ماژول، event syntax، LSP، debugger، object model، تست native ویندوز، GUI روی desktop واقعی و پخش صوت روی دستگاه واقعی هنوز نهایی یا آزموده نشده‌اند؛
- بستهٔ Python نسخهٔ `2.0.1` در PyPI و افزونهٔ VS Code نسخهٔ `2.0.5` در VSIX آماده شده‌اند؛ این release به‌عنوان framework کامل GUI/بازی یا release cross-platform معرفی نمی‌شود.

رفتار arithmetic فشرده یک تغییر سازگاری‌پذیر مهم است. رفتار تاریخی baseline چنین بود:

```text
baseline: چاپ ۵-۳+۲-۱ → 5
Tirotir 2.0.0/2.0.1: چاپ ۵-۳+۲-۱ → 3
```

برای قرارداد KI-1 به [برنامهٔ پذیرش KI-1](docs/tirotir-2-ki1-acceptance-plan-fa.md)، برای مهاجرت به [راهنمای مهاجرت ۲٫۰](docs/tirotir-2-migration-guide-fa.md)، برای شروع آزمایش به [راهنمای فارسی آزمایش](docs/tirotir-2-experimental-testing-fa.md) و [راهنمای انگلیسی آزمایش](docs/tirotir-2-experimental-testing-en.md)، برای معماری به [نقشهٔ معماری ۲٫۰](docs/tirotir-2-architecture-roadmap-fa.md)، برای ردیابی مسائل به [سند traceability](docs/tirotir-2-known-issues-traceability.md)، و برای تغییرات ثبت‌شده به [CHANGELOG](CHANGELOG.md) مراجعه کنید.

---

## 📚 مستندات HTML

در ریشهٔ مخزن دو سند مستقل HTML قرار دارد که برای مطالعه در مرورگر مناسب‌اند:

| سند | توضیح |
| --- | --- |
| [`report.html`](report.html) | گزارش جامع پروژهٔ Tirotir 1.1.0 |
| [`faq.html`](faq.html) | پرسش‌های پرتکرار تیروتیر (FAQ) |

---

### 📊 گزارش جامع پروژه — [`report.html`](report.html)

گزارش فنی و اجرایی کامل **Tirotir 1.1.0** شامل:

- خلاصهٔ اجرایی و هویت محصول
- معماری، هستهٔ زبان، تحلیل معنایی و قراردادها
- CLI، REPL، AST، پروژه و ماژول
- Runtime، امنیت و Capabilityها
- Graphics، Audio و GUI
- VS Code، Builder و EXE
- نصب، انتشار، مثال‌ها، تست‌ها و محدودیت‌ها
- جدول فرمان‌های CLI و نقشهٔ فایل‌های مهم

برای مشاهده، فایل [`report.html`](report.html) را دانلود یا در مرورگر باز کنید.

---

### ❓ پرسش‌های پرتکرار — [`faq.html`](faq.html)

FAQ فارسی **Tirotir 1.1.0** شامل ۶۱ پرسش در ۹ بخش:

- شروع سریع
- آشنایی با تیروتیر
- ساختار و نحو زبان
- معماری و اصطلاحات فنی
- قابلیت‌ها، نصب و امنیت
- محدودیت‌ها و مسیر آینده
- پرسش‌های مصاحبهٔ فنی
- واژه‌نامهٔ کوتاه
- منابع و مشارکت

این صفحه دارای جستجوی زنده، کپی کد و طراحی واکنش‌گرا است.

برای مشاهده، فایل [`faq.html`](faq.html) را دانلود یا در مرورگر باز کنید.

# نصب

## Windows — نصب نسخهٔ ۲ برای کاربران عادی

برای نسخهٔ ۲، نصب رسمی CLI در Windows از PyPI انجام می‌شود:

```powershell
py -3.11 -m pip install tirotir==2.0.1
```

پس از نصب، یک **PowerShell** یا **Command Prompt** جدید باز کنید:

```
tirotir version
```

خروجی:

```
Tirotir 2.0.1
```

برای بررسی interpreter و محل نصب:

```
py -3.11 -m pip show tirotir
```

---

## نصب برای توسعه‌دهندگان

Python 3.11 یا جدیدتر مورد نیاز است.

```bash
python -m pip install .
```

بررسی نصب:

```bash
tirotir version
```

برای نصب در حالت توسعه:

```bash
python -m pip install -e .
```

اجرای تست‌ها:

```bash
python -m pytest -q
```

---

# اولین برنامه

یک فایل با نام `hello.t` ایجاد کنید:

```
چاپ -سلام دنیا-
```

اجرا:

```bash
tirotir run hello.t
```

خروجی:

```
سلام دنیا
```

برای بررسی برنامه بدون اجرای عملیات اصلی:

```bash
tirotir check hello.t
```

---

# مبانی زبان

## متغیر

```
بگذار سن برابر ۲۰
بگذار نام برابر -سارا-

چاپ نام
چاپ سن
```

## شرط

```
بگذار سن برابر ۲۰

اگر سن بزرگتر یا مساوی ۱۸
    چاپ -بزرگسال-
وگرنه
    چاپ -نابالغ-
```

## حلقه

```
تکرار ۴ بار
    چاپ -سلام-
```

## تابع

```
تابع مربع با عدد
    بازگردان عدد * عدد

چاپ مربع با ۵
```

فهرست، فرهنگ، ورودی و خروجی نیز در هستهٔ زبان پشتیبانی می‌شوند.

---

# پروژهٔ چندفایلی

ساختار یک پروژهٔ نمونه:

```
my-project/
├── tirotir.toml
├── main.t
└── lib/
    └── tools.t
```

نمونهٔ `tirotir.toml`:

```
[project]
name = "my-project"
entry = "main.t"
language = "2.0"

[capabilities]
graphics = false
audio = false
gui = false
project-files = false
network = false
```

وارد کردن یک ماژول:

```
وارد کن -lib/tools-
```

اجرای پروژه از ریشهٔ پروژه:

```bash
tirotir run
```

---

# قابلیت‌های پیرامونی

قابلیت‌هایی مانند **Graphics، Audio و GUI** بخشی از زبان پایه نیستند؛ بلکه ابزارها و سرویس‌های پیرامونی اکوسیستم Tirotir هستند.

---

## Graphics

نمونه:

```
پنجره بازکن با ۸۰۰ و ۶۰۰
رنگ قلم برابر -آبی-
ضخامت قلم برابر ۳
مربع با ۱۲۰
```

اجرا:

```bash
tirotir graphics examples2/graphics/hello_shape.t --scene scene.svg
```

Graphics در نسخهٔ ۲ از renderer مبتنی بر **SVG** استفاده می‌کند.

> Animation کامل در این نسخه هنوز وجود ندارد.

---

## Audio

نمونه:

```
نت بنواز با ۲۶۲ و ۰٫۰۲
نت بنواز با ۲۹۴ و ۰٫۰۲
نت بنواز با ۳۳۰ و ۰٫۰۲
```

اجرا:

```bash
tirotir audio examples2/audio/scale.t
```

برای پخش Audio:

```bash
tirotir audio examples2/audio/scale.t --play-audio
```

تولید WAV مستقل از backend پخش سیستم‌عامل انجام می‌شود.

---

## GUI

نمونه:

```
پنجره بساز با -برنامهٔ من- و ۶۰۰ و ۴۰۰
برچسب بساز با -به تیروتیر خوش آمدید-
دکمه بساز با -اجرا-
ورودی بساز
نمایش پنجره
```

اجرا:

```bash
tirotir gui examples2/gui/hello_window.t
```

GUI فعلی بر پایهٔ **Tkinter** است.

> GUI در نسخهٔ ۲ هنوز یک framework کامل GUI محسوب نمی‌شود و به Tkinter و desktop/display نیاز دارد.

---

# VS Code

افزونهٔ VS Code:

```
tirotirlang-2.0.5.vsix
```

برای نصب از داخل VS Code:

```
Ctrl + Shift + P
```

سپس:

```
Extensions: Install from VSIX
```

یا از خط فرمان:

```bash
code --install-extension tirotirlang-2.0.5.vsix
```

امکانات فعلی شامل:

- شناسایی فایل‌های `.t`

- Syntax Highlighting

- اجرای برنامه

- Check

- AST

- خروجی RTL فارسی

- Live Scene

است.

موارد زیر هنوز در نسخهٔ ۲ کامل نیستند:

- LSP کامل

- Completion پیشرفته

- Hover کامل

- DAP

- Debugger حرفه‌ای

## محدودیت‌ها و مسائل شناخته‌شده

نسخهٔ **Tirotir 2** یک release واقعی و قابل استفاده است، اما همهٔ قراردادهای زبان، ابزارهای توسعه و بسته‌بندی آن هنوز نهایی نشده‌اند. برخی موارد، مانند ابهام متن با خط تیره و عملگر تفریق، تکمیل import و namespace، اجرای native Windows، LSP، debugger و اعتبارسنجی کامل بستهٔ Windows، همچنان محدودیت یا کار آینده هستند.

در حال حاضر نباید قابلیت‌های ناتمام یا ادعاهای آموزشی بدون مطالعهٔ کاربر به‌عنوان نتیجهٔ قطعی معرفی شوند. برای فهرست کامل موارد، شواهد، اثر هر مشکل و برنامهٔ اصلاح، به سند زیر مراجعه کنید:

- [فهرست کامل محدودیت‌ها و مسائل شناخته‌شده](known-issues-fa.md)

> این بخش وضعیت نسخهٔ ۲ را شفاف گزارش می‌کند؛ موارد ذکرشده هنوز قابلیت کامل یا cross-platform تضمین‌شده محسوب نمی‌شوند و اصلاح آن‌ها باید همراه با تست regression و مستندات به‌روز انجام شود.

## قابلیت‌های افزوده‌شدهٔ افزونهٔ TirotirLang در نسخهٔ ۲

افزونهٔ TirotirLang برای VS Code علاوه بر قابلیت‌های پایهٔ اجرای فایل، Check، AST، خروجی راست‌به‌چپ و Live Scene، امکانات تعاملی زیر را نیز فراهم می‌کند. این قابلیت‌ها در افزونه ارائه می‌شوند و هستهٔ زبان را از قراردادهای ثبت‌شدهٔ نسخهٔ ۲ خارج نمی‌کنند.

### اجرای زندهٔ تعاملی و دریافت ورودی

برنامه‌هایی که از `بخوان` استفاده می‌کنند، می‌توانند ورودی را مستقیماً از پنل اجرای زندهٔ فارسی دریافت کنند. پنل با `dir="rtl"` نمایش داده می‌شود و ورودی با دکمهٔ «ارسال ورودی» یا کلید Enter به برنامه فرستاده می‌شود.

نمونه:

```
بگذار ورودی_فارنهایت برابر بخوان

اگر (طول با ورودی_فارنهایت ) == ۰
    چاپ -خطا: ورودی خالی است؛ لطفاً یک عدد برای فارنهایت وارد کنید.-
وگرنه
    بگذار فارنهایت برابر به_عدد با ورودی_فارنهایت
    بگذار سانتیگراد برابر (فارنهایت - ۳۲) * ۵ / ۹
    چاپ -دمای واردشده بر حسب فارنهایت:-
    چاپ فارنهایت
    چاپ -دمای معادل بر حسب سانتیگراد:-
    چاپ سانتیگراد
```

در پنل اجرای زنده، مقدار فارنهایت را در کادر ورودی بنویسید و روی «ارسال ورودی» یا کلید Enter بزنید. افزونه برای اجرای زندهٔ Windows از UTF-8 استفاده می‌کند تا ورودی فارسی به شکل خراب‌شده‌ای مانند `Û¸...` به interpreter نرسد.

### ساخت فایل جدید `.t` از Status Bar

وقتی یک فایل `.t` فعال باشد، دکمهٔ ساخت فایل جدید فقط در **Status Bar پایین VS Code** نمایش داده می‌شود. با کلیک روی آن، افزونه ابتدا فایل را واقعاً روی دیسک می‌سازد و سپس آن را در VS Code باز می‌کند.

شماره‌گذاری به‌صورت خودکار ادامه پیدا می‌کند:

```
program-001.t
program-002.t
program-003.t
```

فایل‌های قبلی حذف یا بازنویسی نمی‌شوند. این دکمه در WebView، منوی راست‌کلیک یا نوار عنوان قرار ندارد.

### Snippetهای آموزشی

افزونه ۱۴ snippet آموزشی دارد. در فایل `.t`، prefix را بنویسید و `Ctrl+Space` بزنید؛ سپس با `Tab` درج کنید. نسخهٔ ۲.۰.۵ علاوه بر contribution استاندارد، completion provider پشتیبان دارد:

| نام | Prefix | کاربرد کوتاه |
| --- | --- | --- |
| سلام دنیا | `سلام` | چاپ پیام ساده |
| متغیر | `متغیر` | ساخت متغیر |
| چاپ | `چاپ` | چاپ متن |
| اگر وگرنه | `اگر` | ساخت شرط دوشاخه |
| تکرار | `تکرار` | تکرار تعداد مشخص |
| تاوقتی | `تاوقتی` | ساخت حلقهٔ شرطی |
| برای | `برای` | پیمایش فهرست |
| تابع | `تابع` | ساخت تابع و بازگردان مقدار |
| فهرست | `فهرست` | ساخت فهرست نمونه |
| فرهنگ | `فرهنگ` | ساخت فرهنگ نمونه |
| ورودی | `ورودی` | گرفتن و چاپ ورودی |
| پنجره | `پنجره` | ساخت پنجرهٔ GUI |
| نت صوتی | `نت` | ساخت دستور نت صوتی |
| گرافیک مربع | `مربع` | رسم مربع SVG |

فرمان‌های قبلی افزونه در منوی راست‌کلیک فایل‌های `.t` حفظ شده‌اند. این قابلیت‌های افزونه، زبان پایه و قراردادهای Audio و GUI را تغییر نمی‌دهند؛ ساخت EXE همچنان به Windows واقعی نیاز دارد.

---

# ساخت EXE

Builder را اجرا کنید:

```bash
tirotir builder
```

ساخت Native Windows EXE باید روی **Windows** انجام شود.

سه فایل مهم را از هم متمایز کنید:

### `tirotir.exe`

اجرایی اصلی زبان و CLI.

### `program.exe`

خروجی برنامه‌ای که کاربر با Tirotir ساخته است.

### `Tirotir-1.1.0-Setup.exe` — installer تاریخی

نصب‌کنندهٔ خود Tirotir.

---

# نمونه‌های آموزشی

بستهٔ آموزشی و مجموعهٔ `examples2` شامل نمونه‌های `.t` برای موضوعات زیر است:

- شروع کار

- Hello World

- متغیر

- ورودی و خروجی

- ریاضی

- شرط

- حلقه

- فهرست

- فرهنگ

- تابع

- GUI

- Graphics

- Audio

بستهٔ آموزشی:

راهنمای جاری: [`examples2/README-fa.md`](examples2/README-fa.md)

پس از استخراج، نمونه‌ها را اجرا کنید:

```bash
tirotir run examples2/basics/hello_world.t
```

---

# امنیت و Capabilityها

تیروتیر به‌صورت پیش‌فرض دسترسی آزاد به موارد زیر ندارد:

- Python

- `eval`

- `exec`

- shell

- network

- filesystem

قابلیت‌های پیرامونی به‌صورت جداگانه تعریف می‌شوند:

```
graphics
audio
gui
project-files
network
```

حالت پیش‌فرض فقط قابلیت‌های هسته را فعال می‌کند.

> **توجه:** این طراحی به معنی sandbox امنیتی کامل در سطح سیستم‌عامل نیست.

---

# محدودیت‌های نسخهٔ ۲

موارد زیر هنوز قابلیت کامل محسوب نمی‌شوند:

- Class و Object Model

- Inheritance

- Exception Model عمومی

- Type System کامل

- Generator

- Async/Await

- Animation Runtime کامل

- GUI Event System کامل

- LSP کامل

- DAP

- Debugger کامل

این موارد می‌توانند در نسخه‌های آینده توسعه پیدا کنند.

---

# ساختار اصلی پروژه

```
src/tirotir/
├── core.py          # Lexer، Parser، AST و Interpreter
├── semantic.py      # تحلیل معنایی و Diagnostics
├── contracts.py     # قراردادهای معماری
├── cli.py           # CLI
├── audio.py         # Audio و WAV
├── builder.py       # Builder و EXE
└── modules/         # Project و Module System

vscode-tirotirLang/  # افزونهٔ VS Code
examples/             # نمونه‌ها
tests/                # تست‌ها
docs/                 # مستندات فنی
```

---

# توسعه

اجرای تست‌ها:

```bash
python -m pytest -q
```

اجرای برنامه:

```bash
tirotir run hello.t
```

بررسی برنامه:

```bash
tirotir check hello.t
```

نمایش AST:

```bash
tirotir ast hello.t
```

قالب‌بندی:

```bash
tirotir format hello.t
```

مستندات فنی در پوشهٔ زیر قرار دارند:

```
docs/
```

---

## 📘 جزوه‌های آموزشی تیروتیر

جزوهٔ معرفی و آموزش سریع تیروتیر، با طراحی رنگی، کد، نکته و راهنما، در چند قالب آماده در پوشهٔ [`tirOtir-Booklets`](tirOtir-Booklets) قرار دارد:

| فایل | قالب | کاربرد |
| --- | --- | --- |
| [`Tirotir-Booklet.pdf`](tirOtir-Booklets/Tirotir-Booklet.pdf) | PDF رنگی (۸ صفحه) | مطالعهٔ آنلاین و اشتراک‌گذاری |
| [`Tirotir-Booklet-Print.pdf`](tirOtir-Booklets/Tirotir-Booklet-Print.pdf) | PDF چاپی (۸ صفحه) | چاپ؛ پس‌زمینهٔ سفید و حاشیهٔ صحافی |
| [`Tirotir-Booklet.docx`](tirOtir-Booklets/Tirotir-Booklet.docx) | Word | ویرایش و شخصی‌سازی |
| [`Tirotir-Slides.pptx`](tirOtir-Booklets/Tirotir-Slides.pptx) | PowerPoint (۸ اسلاید) | تدریس و ارائه در کلاس |

### 📖 محتوا

- معرفی تیروتیر، نصب، اولین برنامه و دستورهای CLI
- مبانی زبان: متغیر، شرط، حلقه و تابع
- مثال‌های کاربردی: فهرست، فرهنگ، تابع ترکیبی، ورودی و خروجی
- پروژهٔ چندفایلی، Graphics، Audio، GUI و Capabilityها
- معرفی [Tirotir AI](https://ai.tirotir.com/) و قابلیت‌های آن
- تمرین‌ها با پاسخ‌نامه
- مخزن [tirotir-new-examples](https://github.com/worker2025/tirotir-new-examples) و افزونهٔ VS Code
- QR لینک‌های مهم

> 💡 نمونه‌کدهای قدیمی جزوه با baseline نسخهٔ ۱ آزمایش شده‌اند؛ برای نمونه‌های نسخهٔ ۲ به `examples2/README-fa.md` مراجعه کنید. برای ظاهر دقیق‌تر، فایل Word را در Microsoft Word باز کنید.

---

# Tirotir Learning Lab

## 🎓 آزمایشگاه یادگیری تعاملی تیروتیر

**Tirotir Learning Lab** یک پلتفرم آموزشی تعاملی برای یادگیری مفاهیم تیروتیر و تجربهٔ عملی برنامه‌نویسی است.

### ویژگی‌ها

- 📚 محتوای آموزشی ساختارمند

- 🎨 رابط کاربری ساده

- ⚡ بارگذاری سریع

- 📱 طراحی واکنش‌گرا

- 🌐 دسترسی آزاد و رایگان

- 🧪 تجربهٔ عملی و تعاملی

### دسترسی

🌍 **نسخهٔ آنلاین:**
[https://worker2025.github.io/tirotir-learning-lab/](https://worker2025.github.io/tirotir-learning-lab/)

💻 **GitHub:**
[https://github.com/worker2025](https://github.com/worker2025)

---

# شروع سریع

برای شروع فقط کافی است:

```
چاپ -سلام دنیا-
```

این اولین قدم شما در دنیای **برنامه‌نویسی فارسی با تیروتیر** است.

---

## 🎨 نمونه‌های بیشتر زبان برنامه‌نویسی تیروتیر

مجموعه‌ای از آموزش‌ها، ملودی‌ها، نقاشی‌ها و برنامه‌های کاربردی زبان تیروتیر — به‌صورت آنلاین و قابل اجرا در مرورگر.

🌐 **مشاهدهٔ آنلاین:** [worker2025.github.io/tirotir-new-examples](https://worker2025.github.io/tirotir-new-examples/)

| نمونه | توضیح | لینک |
| --- | --- | --- |
| 🎨 نقاشی با تیروتیر | ۲۳ برنامهٔ گرافیکی — رسم شکل و خروجی SVG | [مشاهده](https://worker2025.github.io/tirotir-new-examples/graphics.html) |
| 🎵 موسیقی با تیروتیر | ملودی‌ها و آموزش — تولید فایل WAV | [مشاهده](https://worker2025.github.io/tirotir-new-examples/sound.html) |
| 📄 فرم و تبدیل‌ها | ۱۵ برنامهٔ کاربردی — فرم، تبدیل واحد و متن | [مشاهده](https://worker2025.github.io/tirotir-new-examples/form.html) |

> 💡 همهٔ نمونه‌ها به‌صورت زنده در مرورگر قابل اجرا هستند و نیازی به نصب ندارند. کدهای نمونه‌ها برای دانلود در پوشه ریپو قرار دارند.

---

# Tirotir 1.1.0 — بخش تاریخی

<p align="center">
<img src="assets/logo/tirotir-logo.png" alt="Tirotir" width="120">
</p> <p align="center">
  <strong>یک زبان برنامه‌نویسی فارسی برای یادگیری، ساخت و خلاقیت.</strong>
</p> <p align="center">
  <a href="https://tirotir.ir/">🌐 Website</a> ·
  <a href="https://tirotir.com/">🌐 Tirotir.com</a> ·
  <a href="https://github.com/worker2025/tirotir">💻 GitHub</a> ·
  <a href="https://doi.org/10.5281/zenodo.22874866">📚 DOI</a>
</p>

---

## License

The Tirotir source code is distributed under the **MIT License**.

See [`LICENSE`](LICENSE).

Copyright © 2026 **Daryoush Alipour**

Tirotir / تیروتیر
