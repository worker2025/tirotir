# گزارش پذیرش KI-5 — Capability Enforcement

## مبنا و commitها

- base development: `e333c670f1b9b20b147900b5131a2fe73c99cc80`
- execution-path audit: `4cbee2400f8a44828918764b4829bde66a528f90`
- runtime implementation: `20f01ab5cb8eb998fd12fa215977baa994f87e51`

## قرارداد اجرا

`RuntimeContext` policy اجرای جاری را نگه می‌دارد و به‌صورت پیش‌فرض فقط `core` را فعال می‌کند. عملیات بیرونی با API زیر فقط با اجازهٔ صریح اجرا می‌شوند:

```python
execute(source, capabilities=["graphics"])
execute(source, runtime_context=RuntimeContext.from_capabilities(["audio"]))
```

ارسال هم‌زمان `capabilities` و `runtime_context` خطاست. نبود policy بیرونی هرگز graphics، audio یا GUI را خودکار فعال نمی‌کند.

## ماتریس پذیرش

| مسیر | حالت | نتیجهٔ مورد انتظار | نتیجهٔ واقعی |
|---|---|---|---|
| `execute()` | graphics بدون مجوز | `CapabilityError`، بدون SVG | تأیید شد |
| `execute()` | graphics با مجوز | تولید SVG | تأیید شد |
| `execute()` | audio بدون مجوز | `CapabilityError`، بدون WAV | تأیید شد |
| `execute()` | audio با context | تولید WAV | تأیید شد |
| `execute()` | GUI بدون مجوز | `CapabilityError` پیش از ساخت backend | تأیید شد |
| CLI `run FILE` | source دارای graphics بدون مجوز | رد و بدون artifact | تأیید شد |
| CLI `graphics FILE` | command صریح | graphics فعال و SVG تولید شود | تأیید شد |
| CLI project | `graphics=true` در `tirotir.toml` | اجرای graphics | تأیید شد |
| CLI project | `graphics=false` | رد و بدون SVG | تأیید شد |
| CLI project | capability ناشناخته | خطای تنظیمات | تأیید شد |
| module/project execution | context مشترک | policy در اجرای moduleها حفظ شود | تأیید شد با release/module suite |
| builder launcher | بدون policy | core-only | تأیید شد |
| builder launcher | `capabilities=["audio"]` | تولید WAV | تأیید شد |

## نتایج تست

```text
Dedicated KI-5: 14 passed
Module/release integration: 28 passed
Full regression suite: 273 passed
```

## corpus مثال‌ها

این اعداد از اجرای مستقل روی commit `d32f97a` به‌دست آمده‌اند و با full suite مخلوط نشده‌اند:

```text
parse-only: 51 مثال؛ 45 موفق، 6 ناموفق
اجرای واقعیِ مثال‌های غیر-GUI و غیر-input: 38 مورد؛ 30 موفق، 8 ناموفق
GUI/desktop: 13 مورد BLOCKED در محیط headless
```

هر ۶ خطای parse-only مربوط به نیم‌فاصله در identifierهاست و به‌صورت `NOT FIXED` باقی می‌ماند. در اجرای واقعی، ۲ مورد به `input()` و نبود ورودی تعاملی مربوط بود؛ ۶ مورد همان خطاهای identifier هستند. این اعداد ادعای اجرای موفق همهٔ مثال‌ها نیستند.

## مسیرهای enforcement

- graphics: ابتدای `Interpreter.graphics()`؛ قبل از ساخت `Scene` یا ذخیرهٔ SVG؛
- audio: ابتدای `Interpreter.audio_note()`؛ قبل از افزودن note و تولید WAV؛
- GUI: ابتدای `Interpreter.gui_command()`؛ قبل از ساخت شیء Tkinter؛
- CLI: تبدیل command صریح، `--capability` و project config به `RuntimeContext`؛
- builder: launcher تولیدشده با policy صریح؛ پیش‌فرض آن core-only است.

## محدودیت ادعای امنیتی

این milestone sandbox کامل سیستم‌عامل نیست و ادعا نمی‌کند همهٔ filesystem، network، subprocess یا importهای خارجی را کنترل می‌کند. `ModuleLoader` sandbox مسیر خود را دارد، اما enforcement مستقل `project-files` و `network` در این milestone پیاده‌سازی نشده است.

موارد زیر در این محیط تأیید نشده‌اند:

- ساخت و اجرای واقعی EXE با PyInstaller روی Windows؛
- بازشدن پنجرهٔ واقعی Tkinter روی desktop؛
- پخش موفق صدا از دستگاه صوتی واقعی؛
- enforcement capability در هر launcher خارجی که خارج از مسیرهای repository باشد.

این موارد باید پیش از هر ادعای release یا sandbox کامل، جداگانه بررسی شوند.
