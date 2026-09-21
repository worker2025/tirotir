# راهنمای نصب Tirotir 1.1.0 در Windows

به بستهٔ Tirotir خوش آمدید. این پوشه شامل نصب‌کنندهٔ زبان و افزونهٔ VS Code است.

## فایل‌های این پوشه

ساختار پیشنهادی پوشه باید شبیه این باشد:

```text
Tirotir-1.1.0-Windows\
│
├── Tirotir-1.1.0-Setup.exe
├── tirotirLang-1.1.0.vsix
└── README-fa.md
```

اگر فایل نمونه‌های آموزشی نیز ارائه شده است، می‌توانید آن را کنار این فایل قرار دهید:

```text
├── tirotir-examples-education-1.1.0.zip
```

## نیازمندی‌های کاربر

برای نصب معمولی به Python، pip، Git، PyInstaller یا Inno Setup نیاز ندارید. فقط یک Windows دسکتاپ لازم است. برای استفاده از افزونه، VS Code نیز باید جداگانه نصب شده باشد.

## مرحلهٔ اول: نصب خود Tirotir

روی فایل زیر دوبار کلیک کنید:

```text
Tirotir-1.1.0-Setup.exe
```

اگر Windows پیام دسترسی نمایش داد، روی **Yes** کلیک کنید. مراحل نصب را با **Next** و سپس **Install** ادامه دهید.

اگر Windows SmartScreen هشدار داد، ابتدا نام فایل و منبع دریافت آن را بررسی کنید. در صورت اطمینان از سالم‌بودن فایل، روی **More info** و سپس **Run anyway** کلیک کنید. این هشدار معمولاً به‌دلیل نداشتن امضای دیجیتال شناخته‌شده برای فایل Setup نمایش داده می‌شود.

پس از پایان نصب، یک پنجرهٔ جدید PowerShell یا Command Prompt باز کنید. پنجرهٔ قدیمی ممکن است تغییرات PATH را نشناسد.

## مرحلهٔ دوم: بررسی نصب

در PowerShell یا Command Prompt اجرا کنید:

```text
tirotir version
```

باید نسخهٔ زیر نمایش داده شود:

```text
Tirotir 1.1.0
```

اگر فرمان `tirotir` شناخته نشد، از مسیر کامل نصب استفاده کنید. مسیر معمول نصب این است:

در PowerShell:

```powershell
& "C:\Program Files\Tirotir\tirotir.exe" version
```

در Command Prompt:

```cmd
"C:\Program Files\Tirotir\tirotir.exe" version
```

اگر مسیر نصب شما متفاوت است، مسیر واقعی نصب را جایگزین کنید.

## مرحلهٔ سوم: اجرای اولین برنامه

یک پوشهٔ کاری بسازید؛ برای نمونه:

```text
Documents\Tirotir\
```

در این پوشه فایلی با نام زیر بسازید:

```text
hello.t
```

محتوای آن را دقیقاً این قرار دهید:

```text
چاپ -سلام دنیا-
```

سپس در همان پوشه یک Terminal باز کنید و اجرا کنید:

```text
tirotir run hello.t
```

خروجی مورد انتظار:

```text
سلام دنیا
```

برای بررسی فایل بدون اجرای آن:

```text
tirotir check hello.t
```

## مرحلهٔ چهارم: نصب افزونهٔ VS Code

این مرحله اختیاری است، اما برای ویرایش فایل‌های `.t` پیشنهاد می‌شود.

### روش گرافیکی

1. VS Code را باز کنید.
2. کلیدهای `Ctrl + Shift + P` را بزنید.
3. عبارت زیر را جست‌وجو کنید:

```text
Extensions: Install from VSIX
```

4. فایل زیر را از همین پوشه انتخاب کنید:

```text
tirotirLang-1.1.0.vsix
```

5. پس از نصب، در صورت درخواست VS Code را Reload کنید.

### روش Terminal

اگر فرمان `code` در PATH نصب شده است، در همان پوشه اجرا کنید:

```cmd
code --install-extension tirotirLang-1.1.0.vsix
```

پس از نصب افزونه، یک فایل `hello.t` را در VS Code باز کنید. فایل باید با زبان Tirotir شناسایی شود و امکانات افزونهٔ موجود مانند اجرای فایل، بررسی فایل و خروجی فارسی را در اختیار داشته باشد.

## استفاده از نمونه‌های آموزشی

اگر فایل زیر در بسته وجود دارد:

```text
tirotir-examples-education-1.1.0.zip
```

آن را در پوشه‌ای خارج از `Program Files`، مانند Documents، Extract کنید. سپس نمونه‌ها را از آنجا اجرا کنید. برای نمونه:

```text
tirotir run examples\basics\hello_world.t
```

ذخیرهٔ فایل‌های قابل ویرایش در Documents بهتر از ویرایش مستقیم داخل `C:\Program Files\Tirotir` است.

## اجرای قابلیت‌های پیرامونی

### GUI

برای اجرای نمونهٔ GUI روی Windows دسکتاپ:

```text
tirotir gui examples\gui\hello_window.t
```

### Audio

برای تولید WAV:

```text
tirotir run examples\audio\scale.t
```

برای درخواست پخش مستقیم:

```text
tirotir run examples\audio\scale.t --play-audio
```

### Graphics

برای تولید صحنهٔ SVG:

```text
tirotir graphics examples\graphics\hello_shape.t --scene scene.svg
```

Graphics در نسخهٔ 1.1.0 قابلیت static SVG و live scene دارد و Known Limitation آن شامل نبود animation کامل و حرکت پیشرفته است.

### ساخت EXE

اگر Builder در نصب شما قرار دارد، آن را با این فرمان باز کنید:

```text
tirotir builder
```

Builder برای ساخت فایل اجرایی Windows از برنامهٔ `.t` استفاده می‌شود. ساخت EXE باید روی خود Windows انجام شود.

## خطاهای متداول

### پیام `tirotir is not recognized`

یک Terminal جدید باز کنید. اگر همچنان خطا وجود داشت، از مسیر کامل استفاده کنید:

```cmd
"C:\Program Files\Tirotir\tirotir.exe" version
```

اگر این دستور کار کرد، مشکل فقط PATH است.

### پیام Windows Defender SmartScreen

این پیام معمولاً به امضانشدن یا تازه‌بودن فایل Setup مربوط است. قبل از اجرای فایل، مطمئن شوید آن را از منبع رسمی دریافت کرده‌اید و در صورت انتشار checksum، مقدار SHA-256 را بررسی کنید.

### افزونه در VS Code نصب نمی‌شود

بررسی کنید فایل انتخاب‌شده دقیقاً `tirotirLang-1.1.0.vsix` باشد و VS Code نصب شده باشد. سپس از مسیر `Extensions: Install from VSIX` دوباره تلاش کنید.

### GUI نمایش داده نمی‌شود

GUI به desktop واقعی Windows نیاز دارد. آن را در Windows معمولی اجرا کنید، نه در محیط headless یا session بدون رابط گرافیکی.

## خلاصهٔ سریع

```text
۱. روی Tirotir-1.1.0-Setup.exe دوبار کلیک کنید.
۲. نصب را کامل کنید.
۳. یک Terminal جدید باز کنید.
۴. tirotir version را اجرا کنید.
۵. فایل hello.t را بسازید.
۶. tirotir run hello.t را اجرا کنید.
۷. در صورت نیاز tirotirLang-1.1.0.vsix را در VS Code نصب کنید.
```

**Tirotir 1.1.0 — زبان برنامه‌نویسی فارسی برای یادگیری، ساخت و خلاقیت**

وب‌سایت‌ها:

```text
tirotir.ir
tirotir.com
```
