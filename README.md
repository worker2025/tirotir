# Tirotir — تیروتیر

**تیروتیر** یک زبان برنامه‌نویسی متنی فارسی و مفسری است.

تیروتیر برای یادگیری و ساخت برنامه‌های واقعی طراحی شده است. می‌توان با یک دستور ساده مانند `چاپ -سلام دنیا-` شروع کرد و سپس به متغیر، شرط، حلقه، تابع، فهرست، فرهنگ، پروژه‌های چندفایلی و قابلیت‌های خلاقانه مانند Graphics، Audio و GUI رسید.

🌐 https://tirotir.ir  
🌐 https://tirotir.com

---
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22874866.svg)](https://doi.org/10.5281/zenodo.22874866)

> **Cite this project:** [https://doi.org/10.5281/zenodo.22874866](https://doi.org/10.5281/zenodo.22874866)

---
## وضعیت فعلی

**Tirotir 1.1.0 — Frozen Baseline**

- زبان برنامه‌نویسی مفسری فارسی
- پسوند رسمی فایل: `.t`
- پشتیبانی از شناسه‌های فارسی و Unicode
- Lexer، Parser، AST و Semantic Analyzer
- Diagnostics ساختاریافته و پیام‌های خطای فارسی
- CLI و REPL
- پروژه و Module System چندفایلی
- Graphics با خروجی SVG
- Audio با تولید WAV
- GUI مبتنی بر Tkinter
- افزونهٔ VS Code
- Builder برای ساخت EXE در Windows
- Runtime با قابلیت‌های کنترل‌شده
- **۲۴۴ تست موفق در baseline**

پسوند قدیمی `.tirotir` نیز برای سازگاری با پروژه‌های قدیمی حفظ شده است.

---

# نصب

## Windows — برای کاربران عادی

اگر فقط می‌خواهید تیروتیر را نصب و استفاده کنید، فایل زیر را در پوشه install یا بخش Releases اجرا کنید:

```text
Tirotir-1.1.0-Setup.exe
```

در این روش نیازی به Python، pip، Git، PyInstaller یا Inno Setup ندارید.

پس از نصب، یک PowerShell یا Command Prompt جدید باز کنید و اجرا کنید:

```text
tirotir version
```

باید نسخهٔ زیر نمایش داده شود:

```text
Tirotir 1.1.0
```

اگر `tirotir` در PATH نبود:

```powershell
& "C:\Program Files\Tirotir\tirotir.exe" version
```

## نصب برای توسعه‌دهندگان

با Python 3.11 یا جدیدتر:

```bash
python -m pip install .
tirotir version
```

برای نصب توسعه:

```bash
python -m pip install -e .
python -m pytest -q
```

---

# اولین برنامه

فایل `hello.t`:

```text
چاپ -سلام دنیا-
```

اجرا:

```bash
tirotir run hello.t
```

خروجی:

```text
سلام دنیا
```

بررسی بدون اجرای اثر اصلی:

```bash
tirotir check hello.t
```

---

# مبانی زبان

## متغیر

```text
بگذار سن برابر ۲۰
بگذار نام برابر -سارا-

چاپ نام
چاپ سن
```

## شرط

```text
بگذار سن برابر ۲۰

اگر سن بزرگتر یا مساوی ۱۸
    چاپ -بزرگسال-
وگرنه
    چاپ -نابالغ-
```

## حلقه

```text
تکرار ۴ بار
    چاپ -سلام-
```

## تابع

```text
تابع مربع با عدد
    بازگردان عدد * عدد

چاپ مربع با ۵
```

فهرست، فرهنگ، ورودی و خروجی نیز در هستهٔ زبان پشتیبانی می‌شوند.

---

# پروژهٔ چندفایلی

```text
my-project/
├── tirotir.toml
├── main.t
└── lib/
    └── tools.t
```

نمونهٔ `tirotir.toml`:

```toml
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

واردکردن ماژول:

```text
وارد کن -lib/tools-
```

اجرای پروژه از ریشه:

```bash
tirotir run
```

---

# قابلیت‌های پیرامونی

Graphics، Audio و GUI بخشی از **زبان پایه** نیستند؛ سرویس‌ها و ابزارهای پیرامونی Tirotir هستند.

## Graphics

```text
پنجره بازکن با ۸۰۰ و ۶۰۰
رنگ قلم برابر -آبی-
ضخامت قلم برابر ۳
مربع با ۱۲۰
```

```bash
tirotir graphics examples/graphics/hello_shape.t --scene scene.svg
```

Graphics نسخهٔ 1.1.0 یک renderer مبتنی بر SVG است. Animation کامل در این نسخه وجود ندارد.

## Audio

```text
نت بنواز با ۲۶۲ و ۰٫۰۲
نت بنواز با ۲۹۴ و ۰٫۰۲
نت بنواز با ۳۳۰ و ۰٫۰۲
```

```bash
tirotir run examples/audio/scale.t
tirotir run examples/audio/scale.t --play-audio
```

تولید WAV مستقل از backend پخش سیستم‌عامل است.

## GUI

```text
پنجره بساز با -برنامهٔ من- و ۶۰۰ و ۴۰۰
برچسب بساز با -به تیروتیر خوش آمدید-
دکمه بساز با -اجرا-
ورودی بساز
نمایش پنجره
```

```bash
tirotir gui examples/apps/hello_gui.t
```

GUI فعلی بر پایهٔ Tkinter است و هنوز Framework کامل GUI محسوب نمی‌شود.

---

# VS Code

افزونهٔ:

```text
tirotirLang-1.1.0.vsix
```

را از داخل VS Code با:

```text
Ctrl + Shift + P
Extensions: Install from VSIX
```

نصب کنید.

یا:

```bash
code --install-extension tirotirLang-1.1.0.vsix
```

امکانات فعلی شامل شناسایی `.t`، Syntax Highlighting، اجرای برنامه، Check، AST، خروجی RTL فارسی و Live Scene است.

LSP و DAP کامل، completion پیشرفته، hover و debugger حرفه‌ای هنوز در نسخهٔ 1.1.0 وجود ندارند.

---

# ساخت EXE

Builder:

```bash
tirotir builder
```

ساخت native Windows EXE باید روی Windows انجام شود.

تفاوت سه فایل مهم:

```text
tirotir.exe
```

اجرایی برای خود زبان و CLI.

```text
program.exe
```

خروجی برنامه‌ای که کاربر با Tirotir ساخته است.

```text
Tirotir-1.1.0-Setup.exe
```

نصب‌کنندهٔ خود Tirotir.

---

# نمونه‌های آموزشی

بستهٔ آموزشی مستقل شامل نمونه‌های `.t` برای شروع کار، متغیر، ورودی و خروجی، ریاضی، شرط، حلقه، فهرست، فرهنگ، تابع، GUI، Graphics و Audio است.

در صورت دریافت:

```text
tirotir-examples-education-1.1.0.zip
```

آن را در پوشه‌ای مانند `Documents` استخراج کنید و نمونه‌ها را اجرا کنید:

```bash
tirotir run examples/basics/hello_world.t
```

---

# امنیت و Capabilityها

Tirotir به‌صورت پیش‌فرض دسترسی آزاد به Python، `eval`، `exec`، shell، شبکه و filesystem ندارد.

قابلیت‌های پیرامونی:

```text
graphics
audio
gui
project-files
network
```

حالت پیش‌فرض فقط قابلیت‌های هسته را فعال می‌کند.

این طراحی به معنی sandbox امنیتی کامل در سطح سیستم‌عامل نیست.

---

# محدودیت‌های نسخهٔ 1.1.0

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
- DAP و Debugger کامل

---

# ساختار اصلی پروژه

```text
src/tirotir/core.py       # Lexer، Parser، AST و Interpreter
src/tirotir/semantic.py   # تحلیل معنایی و Diagnostics
src/tirotir/contracts.py  # قراردادهای معماری
src/tirotir/cli.py        # CLI
src/tirotir/audio.py      # Audio و WAV
src/tirotir/builder.py    # Builder و EXE
src/tirotir/modules/      # Project و Module System
vscode-tirotirLang/       # افزونهٔ VS Code
examples/                  # نمونه‌ها
tests/                     # تست‌ها
docs/                      # مستندات فنی
```

---

# توسعه

```bash
python -m pytest -q
tirotir run hello.t
tirotir check hello.t
tirotir ast hello.t
tirotir format hello.t
```

مستندات فنی در `docs/` قرار دارند.

---

# Tirotir 1.1.0

**یک زبان برنامه‌نویسی فارسی برای یادگیری، ساخت و خلاقیت.**

شروع کنید:

```text
چاپ -سلام دنیا-
```

🌐 https://tirotir.ir  
🌐 https://tirotir.com
