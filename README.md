# تیروتیر — Tirotir

<p align="center">
  <img src="assets/logo/tirotir-logo.png" alt="Tirotir Logo" width="180">
</p>

<p align="center">
  <strong>تیروتیر (Tirotir)</strong><br>
  یک زبان برنامه‌نویسی متنی فارسی و مفسری
</p>

<p align="center">
  <a href="https://tirotir.ir/">Website</a> •
  <a href="https://tirotir.com/">Tirotir.com</a> •
  <a href="https://github.com/worker2025/tirotir">GitHub</a> •
  <a href="https://doi.org/10.5281/zenodo.22874866">DOI</a>
</p>

---

## دربارهٔ تیروتیر

**تیروتیر** یک زبان برنامه‌نویسی متنی فارسی و مفسری است که برای **یادگیری برنامه‌نویسی، آموزش مفاهیم محاسباتی و ساخت برنامه‌های واقعی** طراحی شده است.

می‌توان با یک دستور ساده شروع کرد:

```text
چاپ -سلام دنیا-
```

و سپس به مفاهیمی مانند:

* متغیر
* شرط
* حلقه
* تابع
* فهرست
* فرهنگ
* ورودی و خروجی
* پروژه‌های چندفایلی
* Module System

رسید.

تیروتیر همچنین ابزارها و قابلیت‌های پیرامونی برای **Graphics، Audio و GUI** ارائه می‌کند.

🌐 [tirotir.ir](https://tirotir.ir/)
🌐 [tirotir.com](https://tirotir.com/)
💻 [GitHub](https://github.com/worker2025/tirotir)

---

## DOI و استناد

**DOI:**
https://doi.org/10.5281/zenodo.22874866

اگر از تیروتیر در یک مقاله، پژوهش، پروژهٔ دانشگاهی یا آموزشی استفاده می‌کنید، لطفاً به پروژه استناد کنید:

> Alipour, Daryoush. *Tirotir — Persian Programming Language*.
> https://doi.org/10.5281/zenodo.22874866

---

# وضعیت فعلی

## Tirotir 1.1.0 — Frozen Baseline

نسخهٔ **1.1.0** یک baseline پایدار برای توسعه و انتشار پروژه است.

ویژگی‌های اصلی:

* زبان برنامه‌نویسی مفسری فارسی
* پسوند رسمی فایل: `.t`
* پشتیبانی از شناسه‌های فارسی و Unicode
* Lexer
* Parser
* AST
* Semantic Analyzer
* Diagnostics ساختاریافته
* پیام‌های خطای فارسی
* CLI
* REPL
* Project System
* Module System چندفایلی
* Graphics با خروجی SVG
* Audio با تولید WAV
* GUI مبتنی بر Tkinter
* افزونهٔ VS Code
* Builder برای ساخت EXE در Windows
* Runtime با قابلیت‌های کنترل‌شده
* **۲۴۴ تست موفق در baseline**

پسوند قدیمی:

```text
.tirotir
```

نیز برای سازگاری با پروژه‌های قدیمی حفظ شده است.

---

# نصب

## Windows — برای کاربران عادی

اگر فقط می‌خواهید تیروتیر را نصب و استفاده کنید، نصب‌کنندهٔ زیر را اجرا کنید:

```text
Tirotir-1.1.0-Setup.exe
```

در این روش نیازی به نصب موارد زیر ندارید:

* Python
* pip
* Git
* PyInstaller
* Inno Setup

پس از نصب، یک **PowerShell** یا **Command Prompt** جدید باز کنید:

```powershell
tirotir version
```

خروجی:

```text
Tirotir 1.1.0
```

اگر `tirotir` در PATH قرار نگرفته بود:

```powershell
& "C:\Program Files\Tirotir\tirotir.exe" version
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

برای بررسی برنامه بدون اجرای عملیات اصلی:

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

ساختار یک پروژهٔ نمونه:

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

وارد کردن یک ماژول:

```text
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

```text
پنجره بازکن با ۸۰۰ و ۶۰۰
رنگ قلم برابر -آبی-
ضخامت قلم برابر ۳
مربع با ۱۲۰
```

اجرا:

```bash
tirotir graphics examples/graphics/hello_shape.t --scene scene.svg
```

Graphics در نسخهٔ 1.1.0 از renderer مبتنی بر **SVG** استفاده می‌کند.

> Animation کامل در این نسخه هنوز وجود ندارد.

---

## Audio

نمونه:

```text
نت بنواز با ۲۶۲ و ۰٫۰۲
نت بنواز با ۲۹۴ و ۰٫۰۲
نت بنواز با ۳۳۰ و ۰٫۰۲
```

اجرا:

```bash
tirotir run examples/audio/scale.t
```

برای پخش Audio:

```bash
tirotir run examples/audio/scale.t --play-audio
```

تولید WAV مستقل از backend پخش سیستم‌عامل انجام می‌شود.

---

## GUI

نمونه:

```text
پنجره بساز با -برنامهٔ من- و ۶۰۰ و ۴۰۰
برچسب بساز با -به تیروتیر خوش آمدید-
دکمه بساز با -اجرا-
ورودی بساز
نمایش پنجره
```

اجرا:

```bash
tirotir gui examples/apps/hello_gui.t
```

GUI فعلی بر پایهٔ **Tkinter** است.

> GUI در نسخهٔ 1.1.0 هنوز یک Framework کامل GUI محسوب نمی‌شود.

---

# VS Code

افزونهٔ VS Code:

```text
tirotirLang-1.1.0.vsix
```

برای نصب از داخل VS Code:

```text
Ctrl + Shift + P
```

سپس:

```text
Extensions: Install from VSIX
```

یا از خط فرمان:

```bash
code --install-extension tirotirLang-1.1.0.vsix
```

امکانات فعلی شامل:

* شناسایی فایل‌های `.t`
* Syntax Highlighting
* اجرای برنامه
* Check
* AST
* خروجی RTL فارسی
* Live Scene

است.

موارد زیر هنوز در نسخهٔ 1.1.0 کامل نیستند:

* LSP کامل
* Completion پیشرفته
* Hover کامل
* DAP
* Debugger حرفه‌ای

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

### `Tirotir-1.1.0-Setup.exe`

نصب‌کنندهٔ خود Tirotir.

---

# نمونه‌های آموزشی

بستهٔ آموزشی مستقل شامل نمونه‌های `.t` برای موضوعات زیر است:

* شروع کار
* Hello World
* متغیر
* ورودی و خروجی
* ریاضی
* شرط
* حلقه
* فهرست
* فرهنگ
* تابع
* GUI
* Graphics
* Audio

بستهٔ آموزشی:

```text
tirotir-examples-education-1.1.0.zip
```

پس از استخراج، نمونه‌ها را اجرا کنید:

```bash
tirotir run examples/basics/hello_world.t
```

---

# امنیت و Capabilityها

تیروتیر به‌صورت پیش‌فرض دسترسی آزاد به موارد زیر ندارد:

* Python
* `eval`
* `exec`
* shell
* network
* filesystem

قابلیت‌های پیرامونی به‌صورت جداگانه تعریف می‌شوند:

```text
graphics
audio
gui
project-files
network
```

حالت پیش‌فرض فقط قابلیت‌های هسته را فعال می‌کند.

> **توجه:** این طراحی به معنی sandbox امنیتی کامل در سطح سیستم‌عامل نیست.

---

# محدودیت‌های نسخهٔ 1.1.0

موارد زیر هنوز قابلیت کامل محسوب نمی‌شوند:

* Class و Object Model
* Inheritance
* Exception Model عمومی
* Type System کامل
* Generator
* Async/Await
* Animation Runtime کامل
* GUI Event System کامل
* LSP کامل
* DAP
* Debugger کامل

این موارد می‌توانند در نسخه‌های آینده توسعه پیدا کنند.

---

# ساختار اصلی پروژه

```text
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

```text
docs/
```

---

# Tirotir Learning Lab

## 🎓 آزمایشگاه یادگیری تعاملی تیروتیر

**Tirotir Learning Lab** یک پلتفرم آموزشی تعاملی برای یادگیری مفاهیم تیروتیر و تجربهٔ عملی برنامه‌نویسی است.

### ویژگی‌ها

* 📚 محتوای آموزشی ساختارمند
* 🎨 رابط کاربری ساده
* ⚡ بارگذاری سریع
* 📱 طراحی واکنش‌گرا
* 🌐 دسترسی آزاد و رایگان
* 🧪 تجربهٔ عملی و تعاملی

### دسترسی

🌍 **نسخهٔ آنلاین:**
https://worker2025.github.io/tirotir-learning-lab/

💻 **GitHub:**
https://github.com/worker2025

---

# شروع سریع

برای شروع فقط کافی است:

```text
چاپ -سلام دنیا-
```

این اولین قدم شما در دنیای **برنامه‌نویسی فارسی با تیروتیر** است.

---

# Tirotir 1.1.0

<p align="center">
  <img src="assets/logo/tirotir-logo.png" alt="Tirotir" width="120">
</p>

<p align="center">
  <strong>یک زبان برنامه‌نویسی فارسی برای یادگیری، ساخت و خلاقیت.</strong>
</p>

<p align="center">
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
