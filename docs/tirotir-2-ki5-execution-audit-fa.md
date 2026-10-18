# ممیزی مسیر اجرای KI-5 و طراحی enforcement

## مبنا

- branch: `feature/ki5-capability-enforcement`
- base commit: `e333c670f1b9b20b147900b5131a2fe73c99cc80`
- هدف: اعمال capability در عملیات واقعی graphics، audio و GUI، بدون بازطراحی parser، AST، interpreter یا module system.

## وضعیت واقعی پیش از اصلاح

`CapabilityRegistry` در `src/tirotir/contracts.py` وجود دارد و به‌صورت پیش‌فرض فقط `core` را فعال می‌کند، اما context آن به مسیر اجرای برنامه منتقل نمی‌شود.

مسیرهای واقعی فعلی:

```text
CLI
 ├─ run FILE / graphics / audio / gui
 ├─ project runner → load_project → ModuleLoader/ModuleGraphBuilder
 └─ builder → make_entry_launcher
        ↓
parse → SemanticAnalyzer (در CLI)
        ↓
execute(source, scene_path, play_audio)
        ↓
Interpreter
 ├─ graphics() → Scene.command() → SVG
 ├─ audio_note() → WAV generation / optional playback
 └─ gui_command() → Gui.command() → Tkinter
```

یافته‌های قطعی:

- `execute()` هیچ registry یا RuntimeContext دریافت نمی‌کند؛
- `Interpreter.__init__()` capability policy ندارد؛
- `graphics()` پیش از ساخت SVG هیچ `require()` انجام نمی‌دهد؛
- `audio_note()` و مسیر playback هیچ `require()` انجام نمی‌دهند؛
- `gui_command()` پیش از ساخت Tkinter هیچ `require()` انجام نمی‌دهد؛
- project config در `load_project()` خوانده می‌شود، اما capabilities به `execute()` منتقل نمی‌شوند؛
- builder launcher نیز `execute(source)` را بدون policy اجرا می‌کند؛
- ModuleLoader فقط sandbox مسیر و graph را کنترل می‌کند؛ اجرای backendها باید از context مشترک استفاده کند.

## طراحی محدود و سازگار

### RuntimeContext

یک `RuntimeContext` کوچک در contracts اضافه می‌شود که شامل `CapabilityRegistry` و در صورت نیاز project root است. مقدار پیش‌فرض فقط `core` است. این context در `execute()` و `Interpreter` قابل دریافت است.

API پیشنهادی:

```python
execute(source, ..., capabilities=None, runtime_context=None)
```

- نبود هر دو آرگومان به معنی اجرای core-only است؛
- `capabilities=["graphics"]` قابلیت graphics را به‌صورت صریح فعال می‌کند و core همچنان فعال می‌ماند؛
- ارسال `runtime_context` برای CLI، project runner و builder ممکن است؛
- ارسال هم‌زمان policy و context باید خطای واضح بدهد.

این انتخاب ممکن است بعضی callerهای قدیمی را که graphics/audio را از `execute()` مستقیم و بدون policy اجرا می‌کردند متوقف کند؛ این تغییر امنیتیِ عمدی است و در migration note ثبت می‌شود، نه اینکه bypass سازگاری ساخته شود.

### نقاط enforcement

مجوز دقیقاً پیش از اثر جانبی بررسی می‌شود:

| عملیات | capability | نقطهٔ الزام | اثر رد شدن |
|---|---|---|---|
| ساخت/تغییر Scene و SVG | `graphics` | ابتدای `Interpreter.graphics()` | `CapabilityError` و بدون SVG |
| افزودن note و تولید WAV | `audio` | ابتدای `Interpreter.audio_note()` | `CapabilityError` و بدون WAV |
| ساخت یا اجرای Tkinter | `gui` | ابتدای `Interpreter.gui_command()` | `CapabilityError` و بدون import/پنجره |

### CLI و project

- `graphics`، `audio` و `gui` به‌ترتیب capability متناظر را به context اضافه می‌کنند؛
- گزینهٔ صریح `--capability` برای اجرای مستقیم قابل استفاده است؛
- project runner capabilityهای فعال `tirotir.toml` را با اعتبارسنجی enum و مقدار boolean/string به context تبدیل می‌کند؛
- project config بدون capability بیرونی، core-only باقی می‌ماند؛
- config نامعتبر یا capability ناشناخته با خطای تشخیصی رد می‌شود؛
- ModuleLoader همچنان sandbox مسیر خود را حفظ می‌کند؛ این مرحله ادعای enforcement کامل `project-files` یا network ندارد.

### Builder و launcher

launcher تولیدشده policy صریح دریافت می‌کند و در حالت پیش‌فرض core-only است. builder بدون انتخاب capability جدید، bypass ایجاد نمی‌کند. تست positive builder فقط با capability صریح همان backend اجرا می‌شود.

## محدوده و محدودیت امنیتی

این تغییر sandbox سیستم‌عامل نیست و ادعای جلوگیری از همهٔ filesystem، network، subprocess یا importهای خارجی ندارد. scope این milestone فقط اتصال end-to-end capabilityهای graphics، audio و GUI به مسیرهای پشتیبانی‌شدهٔ موجود است.

KI-1، KI-2، KI-9، module graph و release integration باید بدون regression بمانند. GUI headless و audio playback واقعی همچنان به محیط وابسته‌اند؛ تست‌های منفی باید بدون ایجاد اثر جانبی قابل اجرا باشند.
