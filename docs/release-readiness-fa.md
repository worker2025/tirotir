# گزارش آمادگی انتشار عمومی

## نتیجهٔ quality gate

| بخش | نتیجه |
|---|---:|
| تست‌های خودکار | **۲۳۷ موفق** |
| نمونه‌های `.t` | **۷۱ فایل** |
| نمونه‌های non-GUI اجراشده | **۷۱ موفق** |
| Graphics SVG integration | موفق؛ شامل Chromium headless و fit-to-scene |
| Audio WAV fallback | موفق |
| Event Runtime پایه | موفق |
| Module project CLI | موفق |
| Linux smoke test | موفق |
| Windows native build | در Linux اجرا نشده؛ workflow مستقل اضافه شد |
| macOS native build | در این محیط اجرا نشده |

## تفکیک وضعیت اعتبارسنجی

### Verified در sandbox Linux

تولید SVG با UTF-8 واقعی، نبود mojibake، وجود چهار خط مربع، fit شدن viewBox برای viewport، render شدن DOM در Chromium headless، پروتکل JSON live scene، تولید WAV، mapping نت‌های فارسی، diagnostic GUI headless، Event Runtime، Module Graph، اجرای ۷۱ نمونهٔ `.t` و ساخت wheel/sdist/VSIX بررسی شده‌اند.

### CI Verified پس از اجرای GitHub Actions

فایل‌های CI برای Linux، macOS و Windows و workflow مستقل Windows EXE اضافه شده‌اند، اما در این محیط نتیجهٔ runner واقعی GitHub Actions در دسترس نیست. پس موفقیت Windows EXE یا macOS را از پیش ادعا نمی‌کنیم.

### Manual Acceptance Required

اجرای پنجرهٔ واقعی Tkinter، کلیک button، ورود متن، پخش صوت از دستگاه واقعی و نصب/اجرای VS Code WebView باید روی desktop واقعی بررسی شوند.

## قابلیت‌های قابل اجرا

اجرای فایل‌های رسمی `.t`، check معنایی، formatter، AST JSON، اجرای پروژه از `tirotir.toml`، ساخت Scene SVG با fit-to-scene، تولید WAV و درخواست پخش اختیاری صوت در CLI قابل استفاده‌اند. `.tirotir` برای compatibility در CLI پذیرفته می‌شود. اکستنشن VS Code متن را در خروجی RTL و SVG اجرای فعلی را از پروتکل live scene مستقیماً در همان WebView نمایش می‌دهد.

## صدا

تولید WAV بدون dependency خارجی قطعی است. پخش واقعی با backend سیستم‌عامل انجام می‌شود: `aplay`، `paplay` یا `ffplay` در Linux، `afplay` در macOS و `Media.SoundPlayer` در Windows. mapping نام‌های `دو`، `ر`، `می`، `فا`، `سل`، `لا` و `سی` اضافه شده است. چون این sandbox دستگاه صوتی تضمین‌شده ندارد، ادعای پخش موفق در این محیط ثبت نشده است؛ در نبود backend، فایل WAV حفظ می‌شود.

## GUI

Tkinter backend پنجره، label، button و entry را می‌سازد. در محیط headless، خطای ساختاریافتهٔ `TIR4001` به‌جای traceback مبهم ارائه می‌شود. اجرای واقعی پنجره نیازمند محیط desktop و Tkinter است و manual acceptance آن باقی مانده است. callback دکمه، checkbox، listbox، binding ورودی و event syntax سطح زبان هنوز production-complete نیستند.

## Windows EXE

اسکریپت `tools/build_windows_exe.ps1` و workflow مستقل `.github/workflows/windows-exe-release.yml` مسیر رسمی PyInstaller را فراهم می‌کنند. build واقعی Windows در این محیط Linux انجام نشده است؛ بنابراین artifact یا اجرای موفق `.exe` تا زمان اجرای workflow روی Windows ادعا نمی‌شود.

## محدودیت‌های باقی‌مانده قبل از Tirotir 2.0

Namespace dotted مانند `ابزار.جمع` هنوز به semantic resolver و object model متصل نشده است. Module Graph و اجرای topological پروژه وجود دارد، اما export/import نام‌ها هنوز محدود است. Event Runtime داخلی کامل و قابل تست است، ولی syntax رویداد در زبان و اتصال callbackهای GUI هنوز milestone بعدی است. LSP کامل، completion، DAP debugger، object model و VM نیز هنوز تکمیل نشده‌اند.

بنابراین این repository برای انتشار عمومی نسخهٔ ۱٫۱٫۰ به‌عنوان زبان آموزشی/کاربردی با امکانات خلاقانه آماده است، اما نباید به‌عنوان Tirotir 2.0 نهایی یا framework کامل GUI/بازی معرفی شود.
