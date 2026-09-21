# گزارش نهایی branch جدید تیروتیر

## نتیجهٔ quality gate

```text
244 passed
9 نمونهٔ اجرایی غیر-GUI بدون خطا
Graphics مربع: 4 line واقعی، رنگ آبی UTF-8
Audio sequence: یک WAV پیوسته با 46,305 frame
Builder: entrypoint مستقل با source جاسازی‌شده تولید و بدون source اصلی اجرا شد
```

## Audio

مشکل نمونه‌های صوتی این بود که `audio_note` در هر فراخوانی همان فایل `tirotir-note.wav` را بازنویسی می‌کرد و در صورت فعال بودن پخش، هر نت جداگانه اجرا می‌شد. در نتیجه sequence به‌صورت یک ملودی پیوسته قابل اتکا نبود. اکنون هر سه نمونهٔ `melody.t`، `render_only.t` و `scale.t` جداگانه اجرا و WAV معتبر تولید کردند.

اکنون Interpreter نت‌ها را در `audio_notes` جمع می‌کند و پس از اجرای برنامه با `render_sequence` یک WAV واحد می‌سازد. اگر `--play-audio` فعال باشد، همان فایل واحد یک‌بار پخش می‌شود. `scale.t` به‌عنوان regression رسمی حفظ و به هفت نت فارسی گسترش داده شد. مثال‌های `melody.t` و `render_only.t` نیز اضافه شدند؛ `render_only.t` صریحاً فقط تولید فایل انجام می‌دهد.

## Graphics

Scene فعلی یک renderer استاتیک است، نه timeline یا animation واقعی. بنابراین ادعای animation زمان‌مند اضافه نشد. حرکت و چرخش state قلم را تغییر می‌دهند و lineهای واقعی در SVG ذخیره می‌شوند.

Regression مسیر زیر را دقیقاً بررسی می‌کند:

```text
(0,0) -> (100,0)
(100,0) -> (100,100)
(100,100) -> (0,100)
(0,100) -> (0,0)
```

رنگ `آبی` در attribute واقعی `stroke` قرار می‌گیرد و viewBox قبلی bounding box صحنه را پوشش می‌دهد.

## پسوند `.t`

نمونه‌های موجود در این branch به `.t` منتقل شدند و referenceهای اصلی مستندات، project default و grammar اصلاح شدند. `extension.js` دیگر کاربر را برای `.tirotir` راهنمایی نمی‌کند. پشتیبانی `.tirotir` در CLI و ModuleLoader برای compatibility باقی است.

## GUI

سه نمونهٔ واقعی در repository حفظ و end-to-end بررسی شدند:

- `examples/gui/hello_window.t` برای پنجره، برچسب، دکمه و ورودی؛
- `examples/gui/widgets.t` برای چک‌باکس، لیست، منوی انتخاب، متن چندخطی و نوار لغزش؛
- `examples/gui/form.t` برای یک فرم ساده.

Regression اصلی این بخش در semantic layer بود. primitiveهای `چک_باکس_بساز`، `لیست_بساز`، `منوی_انتخاب_بساز`، `متن_چندخطی_بساز` و `نوار_لغزش_بساز` در runtime وجود داشتند اما در `BUILTINS` ثبت نشده بودند. اکنون هر سه نمونهٔ GUI از `check` عبور می‌کنند.

هیچ نمونهٔ جعلی event/callback اضافه نشده است؛ event syntax به milestone مستقل parser/semantic/runtime موکول است.

## Builder

ریشهٔ خطا فقط resolver مسیر launcher نبود؛ wrapper قبلی در زمان اجرای EXE فایل launcher توسعه‌ای را با مسیر مطلق باز می‌کرد و source انتخاب‌شده نیز مستقل bundle نمی‌شد. Builder اکنون:

1. `TIROTIR_LAUNCHER` را به‌عنوان مسیر صریح اختیاری بررسی می‌کند؛
2. در development repository، launcher واقعی را فقط برای بررسی compatibility پیدا می‌کند؛
3. source فایل `.t` را در entrypoint موقت جاسازی می‌کند؛
4. entrypoint از `tirotir.core` و `tirotir.semantic` داخل bundle import می‌کند؛
5. پیش از PyInstaller وجود source و package را بررسی می‌کند؛
6. بعد از build، artifact را اجرا می‌کند و stdout، stderr و return code را در UI ثبت می‌کند.

این entrypoint پس از حذف فایل source اصلی در sandbox با موفقیت اجرا شد و WAV تولید کرد. ساخت واقعی one-file EXE باید روی Windows با PyInstaller تأیید شود.

فرمان کاربر:

```text
tirotir builder
```

بازکردن UI به Tkinter و desktop نیاز دارد. اجرای native build روی Windows باید روی خود Windows انجام شود.

## تفکیک محیط تست

| مورد | sandbox/CI | Windows واقعی |
|---|---|---|
| 242 تست Python | تأیید شد | باید در CI یا Windows اجرا شود |
| parsing و runtime صوت | تأیید شد | صدای واقعی طبق سابقهٔ دستی کاربر تأیید شده؛ sequence جدید نیازمند تأیید دستی است |
| پخش WAV با backend Windows | شبیه‌سازی/کد بررسی شد | تست دستی قبلی PASS؛ اجرای sequence جدید هنوز ادعای native نشده است |
| SVG و movement/rotation/color | تأیید شد | نیازمند بازبینی WebView در VS Code Windows |
| `.t` در manifest و grammar | JSON و ساختار تأیید شد | باید با نصب VSIX در VS Code Windows یک‌بار smoke شود |
| GUI primitiveها | parser و import تأیید شد؛ desktop sandbox headless است | باید روی Windows با Tkinter باز شود |
| Builder resolver | مسیر و wrapper تأیید شد | ساخت واقعی EXE باید روی Windows با PyInstaller انجام شود |

بنابراین این branch از نظر کد و regression آمادهٔ تست نهایی Windows است، اما ادعای تست native برای مواردی که در sandbox قابل اجرا نیست، عمداً ثبت نشده است.
