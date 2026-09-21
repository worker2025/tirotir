# TirotirLang برای VS Code

اکستنشن مستقل VS Code برای زبان فارسی **تیروتیر** با شناسهٔ `tirotirLang` است. پسوند رسمی فایل‌ها `.t` است؛ فایل‌های قدیمی `.tirotir` در CLI برای سازگاری پذیرفته می‌شوند.

## امکانات

- شناسایی فایل‌های `.t` به‌عنوان پسوند رسمی
- رنگ‌بندی کلیدواژه‌ها، اعداد فارسی، متن و کامنت
- تنظیم تورفتگی بلوک‌ها
- فرمان اجرای فایل
- فرمان بررسی نحوی
- نمایش AST در ترمینال VS Code
- پنل خروجی فارسی راست‌به‌چپ با WebView
- نمایش زندهٔ SVG در WebView پس از هر اجرا، بدون ساخت فایل دائمی کنار source
- اجرای برنامه‌های Creative Mode و تولید SVG
- فرمان‌های جداگانهٔ Graphics، Audio و GUI
- پشتیبانی از شناسه‌های فارسی

## نصب از کد منبع

در پوشهٔ این اکستنشن اجرا کنید:

```powershell
npm install -g @vscode/vsce
vsce package
```

سپس فایل `.vsix` ساخته‌شده را در VS Code نصب کنید:

1. `Ctrl+Shift+P`
2. انتخاب `Extensions: Install from VSIX...`
3. انتخاب فایل `tirotirLang-1.1.0.vsix`

یا از خط فرمان:

```powershell
code --install-extension tirotirLang-1.1.0.vsix
```

## پیش‌نیاز اجرای برنامه

باید CLI تیروتیر نصب و در PATH باشد:

```powershell
py -m pip install .
tirotir version
```

اگر فرمان `tirotir` در PATH نیست، در تنظیمات VS Code مقدار زیر را به مسیر کامل فایل اجرایی تغییر دهید:

```json
{
  "tirotirLang.command": "C:\\Users\\YOUR_USER\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\tirotir.exe"
}
```

روی فایل `.t` راست‌کلیک کنید و یکی از فرمان‌های زیر را انتخاب کنید:

- `TirotirLang: اجرای فایل`
- `TirotirLang: بررسی فایل`
- `TirotirLang: نمایش AST`
- `TirotirLang: اجرای زنده در پنل فارسی راست‌به‌چپ`
- `TirotirLang: نمایش Graphics زنده`
- `TirotirLang: پخش Audio`
- `TirotirLang: اجرای GUI`

فرمان RTL خروجی برنامه را در پنل WebView با `dir="rtl"` و `lang="fa"` نمایش می‌دهد. Graphics با پروتکل JSON داخلی `--live-scene` از اجرای همان لحظه دریافت می‌شود و SVG مستقیماً در WebView render می‌شود؛ در اجرای معمول، فایل SVG کنار source ساخته نمی‌شود. فایل export فقط با اجرای CLI و گزینهٔ `--scene` تولید می‌شود.
