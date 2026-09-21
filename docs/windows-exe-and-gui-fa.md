# رابط گرافیکی و ساخت EXE در Windows

## API رابط گرافیکی

نسخهٔ ۱٫۱ یک backend اختیاری Tkinter دارد. این backend فقط زمانی فعال می‌شود که برنامه یکی از فرمان‌های GUI را اجرا کند و جزء هستهٔ lexer یا parser نیست.

نمونهٔ کامل:

```text
پنجره بساز با -برنامهٔ من- و ۶۰۰ و ۴۰۰
برچسب بساز با -به تیروتیر خوش آمدید-
دکمه بساز با -اجرا-
ورودی بساز
نمایش پنجره
```

فرمان‌های پشتیبانی‌شده عبارت‌اند از `پنجره بساز`، `برچسب بساز`، `دکمه بساز`، `ورودی بساز` و `نمایش پنجره`. این نسخهٔ اولیهٔ GUI برای ساخت پنجره و عناصر پایه است. رویدادهای دکمه، اتصال متغیر به ورودی و layout پیشرفته در نسخهٔ بعدی تکمیل می‌شوند.

## نصب روی Windows

Python را با گزینهٔ **Add Python to PATH** نصب کنید. سپس در PowerShell در ریشهٔ پروژه اجرا کنید:

```powershell
py -m pip install .
tirotir version
tirotir run examples\gui\hello_window.t
```

فرمان صریح `gui` نیز وجود دارد:

```powershell
tirotir gui examples\gui\hello_window.t
```

اگر Python نصب‌شدهٔ شما Tkinter نداشته باشد، خطای فارسی دریافت می‌کنید. در Windows رسمی Python معمولاً Tkinter همراه نصب ارائه می‌شود.

## ساخت فایل EXE

برای ساخت فایل اجرایی مستقل، PyInstaller را نصب و اسکریپت پروژه را اجرا کنید:

```powershell
py -m pip install pyinstaller
py -m pip install .
pyinstaller --clean --onefile --name tirotir --paths src tools\tirotir_launcher.py
```

خروجی در این مسیر ایجاد می‌شود:

```text
dist\tirotir.exe
```

یا از اسکریپت آماده استفاده کنید:

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_windows_exe.ps1
```

برای نسخهٔ گرافیکی می‌توانید یک میانبر یا فایل batch بسازید:

```powershell
.\dist\tirotir.exe run examples\gui\hello_window.t
```

ساخت EXE باید روی خود Windows انجام شود، زیرا PyInstaller به‌طور معمول برای سیستم‌عامل مقصد بسته می‌سازد. برای Linux و macOS باید build جداگانه روی همان سیستم‌عامل انجام شود.

## محدودیت GUI نسخهٔ ۱٫۱

این backend به Tkinter وابستهٔ اختیاری است و هنوز سیستم رویدادمحور کامل، callback فارسی برای دکمه، canvas مشترک با SVG، designer بصری و package installer مستقل ندارد. برای اجرای بدون dependency سنگین، GUI در هستهٔ پایه اجباری نشده است.
