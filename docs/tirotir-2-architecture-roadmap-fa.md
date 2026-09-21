# نقشهٔ معماری Tirotir 2.0

**وضعیت مبنا:** Tirotir 1.1.0  
**هدف:** تبدیل هستهٔ واقعی موجود به یک زبان کامل‌تر با ماژول، رویداد، مدل شیء، debugger، پروژهٔ چندفایلی و محیط توسعهٔ مدرن، بدون بازنویسی بی‌دلیل هسته.

## تصمیم اصلی

تیروتیر باید از صفر بازنویسی نشود. lexer، parser، AST، interpreter، runtime امن، API گرافیک SVG، صدا، GUI اختیاری و پنل RTL موجود سرمایهٔ معماری هستند. تغییر اصلی باید اضافه‌کردن لایه‌های مستقل و قراردادهای پایدار باشد.

> **اصل معماری ۲٫۰:** سادگی در سطح نحو و آموزش؛ تفکیک و قدرت در زیرساخت.

هدف این نیست که تیروتیر به مجموعه‌ای از فرمان‌های نمایشی تبدیل شود. گرافیک، صدا و GUI باید clientهای runtime باشند؛ زبان همچنان یک زبان متنی با scope، تابع، داده، خطا، ماژول و ابزار توسعه باقی می‌ماند.

## معماری هدف

```text
Source
  ↓
Unicode Normalizer
  ↓
Lexer + Source Spans
  ↓
Parser
  ↓
AST
  ↓
Semantic Analyzer
  ├── Symbol Table
  ├── Scope Resolution
  ├── Module Graph
  ├── Type Hints اختیاری
  └── Diagnostics
  ↓
Execution IR اختیاری
  ↓
Interpreter / Bytecode VM آینده
  ↓
Capability Sandbox
  ↓
Runtime Services
  ├── Core
  ├── Text / List / Dictionary
  ├── Graphics
  ├── Audio
  ├── GUI
  ├── Events
  ├── Time / Random
  └── Limited Files
  ↓
CLI / VS Code / WebView / Desktop Launcher
```

هیچ backend نباید lexer یا parser را بشناسد. AST و قراردادهای runtime نقطهٔ اتصال زبان با امکانات بیرونی هستند.

## وضعیت کنونی و فاصله تا ۲٫۰

نسخهٔ ۱٫۱٫۰ متغیر، ثابت، نوع‌های پایه، فهرست، فرهنگ، شرط، حلقه، تابع، recursion، ورودی و خروجی، AST JSON، CLI، formatter، REPL، Creative Mode، SVG، تولید WAV، Tkinter پایه و خروجی RTL VS Code دارد. این قابلیت‌ها با ۲۰۲ تست و ۷۱ مثال اعتبارسنجی شده‌اند.

فاصلهٔ اصلی با ۲٫۰ در چهار بخش است: تحلیل معنایی مستقل، سیستم ماژول، event loop و ابزار توسعهٔ سطح IDE. object model و debugger نیز باید قبل از بزرگ‌شدن APIهای GUI و بازی طراحی شوند.

## لایهٔ اول: Source Model و Diagnostics

هر token و هر node باید `line`، `column`، `start_offset` و `end_offset` داشته باشد. خطاها باید به‌جای رشتهٔ ساده، یک شیء ساختاریافته باشند:

```text
Diagnostic {
    code: "TIR1003"
    severity: خطا | هشدار | اطلاعات
    type: "نام_تعریف_نشده"
    message: "متغیر «تعداد» پیدا نشد."
    line: 6
    column: 12
    span: {start, end}
    suggestion: "ابتدا با «بگذار» آن را تعریف کن."
}
```

CLI باید بتواند خطا را به شکل انسانی و JSON چاپ کند:

```text
tirotir check program.t --format human
tirotir check program.t --format json
```

این قرارداد پایهٔ diagnostics در VS Code، formatter و debugger خواهد بود.

## لایهٔ دوم: Semantic Analyzer

قبل از اجرا، analyzer باید symbol table و scopeها را بسازد. این مرحله باید موارد زیر را بررسی کند:

- تعریف تکراری نام در scope نامعتبر؛
- استفاده از نام تعریف‌نشده؛
- تغییر ثابت؛
- تعداد نادرست آرگومان؛
- `بازگردان` خارج از تابع؛
- `بیرون` و `ادامه` خارج از حلقه؛
- import چرخه‌ای؛
- capability استفاده‌نشده یا ممنوع؛
- ناسازگاری نوعی در حالت type checking اختیاری.

Dynamic typing در حالت پیش‌فرض حفظ می‌شود. type annotation باید بعداً اختیاری باشد، نه اینکه شروع سادهٔ زبان را دشوار کند:

```text
نوع سن برابر ۲۰
تابع جمع با عدد الف و عدد ب
    بازگردان الف + ب
```

## لایهٔ سوم: سیستم ماژول

نحو پیشنهادی:

```text
وارد کن -کتابخانه-
وارد کن -کتابخانه- با نام ابزار
```

ساختار پروژه:

```text
my-project/
    tirotir.toml
    main.t
    کتابخانه.t
    assets/
        images/
        sounds/
```

`tirotir.toml` باید نقطهٔ ورود، نسخهٔ زبان و capabilityها را مشخص کند:

```toml
[project]
name = "my-project"
entry = "main.t"
language = "2.0"

[capabilities]
graphics = true
audio = false
filesystem = "project-assets"
network = false
```

loader فقط فایل‌های داخل ریشهٔ پروژه و stdlib امضاشده را می‌پذیرد. مسیرها باید canonicalize شوند تا خروج از پوشهٔ پروژه با `..` ممکن نباشد. import آزاد Python مطلقاً وجود نخواهد داشت.

ماژول باید namespace مستقل داشته باشد و از اجرای دوبارهٔ فایل جلوگیری شود. graph ماژول پیش از اجرا ساخته و چرخه‌ها با diagnostics مشخص گزارش شوند.

## لایهٔ چهارم: مدل شیء

در نسخهٔ ۲٫۰ بهتر است object model کوچک و روشن باشد. پیشنهاد اولیه:

```text
شیء دانش‌آموز
    سازنده با نام
        بگذار خود.نام برابر نام

    تابع معرفی
        چاپ خود.نام
```

اما ورود کلاس‌ها نباید قبل از مشخص‌شدن قرارداد زیر انجام شود:

| موضوع | تصمیم پیشنهادی |
|---|---|
| هویت | هر نمونه identity مستقل دارد |
| field | قابل دسترسی فقط طبق visibility پیش‌فرض ساده |
| method | تابعی با receiver آشکار `خود` |
| inheritance | در نسخهٔ نخست ۲٫۰ حذف شود یا فقط single inheritance باشد |
| mutation | صریح و قابل ردیابی باشد |
| magic methods | محدود به چند مورد مانند متن و مقایسه |
| serialization | فقط برای objectهای داده‌ای مجاز باشد |

هدف object model پشتیبانی از پروژه‌های واقعی است، نه ساخت یک سیستم پیچیدهٔ کلاس‌ها برای خودش. composition باید قبل از inheritance قرار بگیرد.

## لایهٔ پنجم: Event Loop

event loop باید بخشی از runtime باشد، نه hack مخصوص Tkinter یا WebView. مدل پیشنهادی event queue، handler registry و clock کنترل‌شده دارد:

```text
وقتی شروع شد
    چاپ -بازی آغاز شد-

وقتی کلید -space- فشرده شد
    ارسال پیام -پرش-

وقتی پیام -پرش- دریافت شد
    حرکت با ۲۰

تکرار کن
    به‌روزرسانی
    صحنه را نمایش بده
```

در سطح runtime:

```text
Event {
    name
    payload
    timestamp
    source
}

EventLoop {
    register(handler)
    emit(event)
    tick(delta)
    stop()
}
```

handlerها باید در یک صف اجرا شوند و ترتیب آن‌ها deterministic باشد. callback Python نباید مستقیماً در اختیار برنامه قرار گیرد. backend GUI، بازی و WebView فقط eventهای ثبت‌شده را تولید می‌کنند.

برای جلوگیری از قفل برنامه، هر tick سقف گام دارد. loop باید حالت `run`، `pause`، `step` و `stop` داشته باشد تا debugger بتواند به آن متصل شود.

## لایهٔ ششم: همزمانی سبک

قبل از thread واقعی، taskهای cooperative پیشنهاد می‌شوند:

```text
همزمان اجرا کن
    حرکت با ۵
```

هر task فقط در نقاط yield یا پایان tick کنترل را پس می‌دهد. این روش با sandbox، توقف، debugger و اجرای deterministic سازگارتر است. thread و process در نسخهٔ نخست ۲٫۰ نباید وارد زبان شوند.

## لایهٔ هفتم: Debugger

Debugger باید از AST و interpreter instrumentation ساخته شود و هرگز برای ارزیابی عبارت از Python `eval` یا `exec` استفاده نکند.

هر statement قابل اجرا باید یک `node_id` و source span داشته باشد. interpreter رویدادهای زیر را منتشر کند:

```text
before_statement(node_id, frame)
after_statement(node_id, frame)
function_enter(name, frame)
function_exit(name, frame)
exception(diagnostic)
```

حالت‌های لازم:

- ادامه؛
- توقف؛
- مرحلهٔ بعد؛
- ورود به تابع؛
- خروج از تابع؛
- breakpoint روی source span؛
- نمایش locals و globals؛
- call stack؛
- restart؛
- ارزیابی محدود expression فقط از AST تیروتیر.

برای اتصال به VS Code، استفاده از Debug Adapter Protocol مناسب است؛ DAP دقیقاً برای ارتباط editor با debugger و runtime طراحی شده است [2].

## لایهٔ هشتم: Language Server و VS Code

اکستنشن فعلی باید از syntax highlighting به Language Server واقعی ارتقا یابد. Language Server Protocol برای استانداردسازی ارتباط ابزار توسعه و سرور زبان طراحی شده است [1].

قابلیت‌های مرحلهٔ نخست:

1. diagnostics لحظه‌ای؛
2. completion کلیدواژه، متغیر و API؛
3. hover فارسی؛
4. go to definition؛
5. find references؛
6. rename symbol؛
7. document symbols؛
8. semantic highlighting؛
9. formatter؛
10. code actions.

بعد از آماده‌شدن debugger، اکستنشن از DAP استفاده کند. خروجی همچنان در WebView با `dir="rtl"` نمایش داده شود. source code نباید reorder شود؛ RTL فقط لایهٔ نمایش خروجی و توضیحات است.

## کتابخانهٔ استاندارد و capabilityها

stdlib باید interface فارسی و backend مستقل داشته باشد:

| ماژول | نمونهٔ API | capability پیش‌فرض | backend |
|---|---|---:|---|
| متن | `طول`، `به_متن` | core | runtime |
| فهرست | `افزودن`، `حذف` | core | runtime |
| ریاضی | `توان`، `ریشه`، `کف` | core | math محدود |
| زمان | `اکنون`، `خواب` | زمان | clock کنترل‌شده |
| تصادفی | `تصادفی` | core | PRNG قابل seed |
| گرافیک | `حرکت`، `مربع` | graphics | SVG/WebView/Tk |
| صدا | `نت بنواز` | audio | WAV یا backend اختیاری |
| رابط | `پنجره بساز` | gui | Tkinter/WebView |
| فایل | خواندن asset پروژه | project-files | sandbox |
| شبکه | در نسخهٔ ۲٫۰ پیش‌فرض خاموش | network | آینده |

هر API باید signature، نوع ورودی، خروجی، خطا، محدودیت امنیتی و تست مشخص داشته باشد. backendهای خارجی dependency اختیاری باشند.

## سطوح آموزشی

تیروتیر باید progression مشخص داشته باشد:

| سطح | هدف | امکانات |
|---|---|---|
| ۱ | نتیجهٔ فوری | چاپ، متن، عدد، ایموجی |
| ۲ | تفکر الگوریتمی | متغیر، شرط، حلقه، فهرست |
| ۳ | abstraction | تابع، scope، فرهنگ، recursion |
| ۴ | خلاقیت | گرافیک، صدا، GUI، event |
| ۵ | پروژهٔ واقعی | ماژول، object، تست، debugger |

برای سطح اول، APIهای سطح‌بالا مانند `مربع بکش با ۱۰۰` می‌توانند روی primitiveهای Logo قرار بگیرند. primitiveها نیز باید معتبر باقی بمانند تا کاربر بتواند از abstraction به کنترل دقیق برسد.

## سازگاری نسخه‌ای

برنامه‌های نسخهٔ ۱ باید در ۲٫۰ با کمترین تغییر اجرا شوند. قواعد زیر لازم است:

- `-متن-` حفظ شود؛ quotation جدید فقط افزوده شود؛
- `بگذار نام برابر مقدار` و `نام = مقدار` حفظ شوند؛
- nodeهای AST موجود حذف نشوند؛
- runtime API با adapter نسخه‌ای نگهداری شود؛
- migration tool برای syntaxهای deprecate شده ارائه شود؛
- `tirotir check --target 1.0` سازگاری را بررسی کند.

هر قابلیت ناسازگار باید feature flag و پیام مهاجرت داشته باشد.

## امنیت و sandbox

قابلیت‌های بیرونی باید capability-based باشند. حالت پیش‌فرض فقط `core` را فعال کند. graphics، audio و gui با permission جدا فعال شوند. filesystem فقط به `assets` یا مسیرهای project-scoped محدود شود. network، subprocess، environment secrets، import آزاد Python، eval و exec ممنوع باقی بمانند.

برای اجرای امن‌تر، CLI باید محدودیت‌های زیر را قابل تنظیم کند:

```text
tirotir run main.t --max-steps 100000 --timeout 3 --memory 128
```

محدودیت حافظه و timeout واقعی باید در سطح process supervisor پیاده‌سازی شوند، نه فقط با شمارندهٔ داخل interpreter.

## برنامهٔ پیاده‌سازی مرحله‌ای

### مرحلهٔ ۰: تثبیت قراردادها

Source span، Diagnostic، Runtime API، capability registry و node id اضافه شوند. این مرحله باید بدون تغییر محسوس در syntax نسخهٔ ۱ انجام شود.

### مرحلهٔ ۱: تحلیل معنایی و formatter

Symbol table، scope resolver، semantic diagnostics و formatter AST-based پیاده‌سازی شوند. تست خطاهای پیش از اجرا باید اضافه شود.

### مرحلهٔ ۲: پروژه و ماژول

`tirotir.toml`، module loader sandbox‌شده، namespace، import graph و CLI چندفایلی اضافه شوند.

### مرحلهٔ ۳: event loop

event queue، handler، timer، message و حالت‌های run/pause/step ساخته شوند. گرافیک و GUI فقط به این runtime service متصل شوند.

### مرحلهٔ ۴: object model

object، method، constructor و field با composition ساده اضافه شوند. inheritance تا بعد از تثبیت semantics به تعویق بیفتد.

### مرحلهٔ ۵: debugger و LSP

instrumentation interpreter، protocol داخلی debug، DAP adapter و Language Server توسعه یابند.

### مرحلهٔ ۶: VM آینده

پس از تثبیت semantics، AST به IR و سپس bytecode اختیاری تبدیل شود. interpreter مرجع برای تست و حالت آموزشی باقی بماند.

## معیارهای پذیرش Tirotir 2.0

نسخهٔ ۲٫۰ فقط زمانی آماده اعلام شود که:

- یک پروژهٔ چندفایلی با import sandbox‌شده اجرا شود؛
- import چرخه‌ای و مسیر خارج پروژه با خطای فارسی رد شود؛
- event loop با timer و پیام deterministic باشد؛
- برنامهٔ GUI و بازی از event API استفاده کنند، نه hack backend؛
- object و method دارای scope و diagnostics روشن باشند؛
- breakpoint، step، continue، call stack و locals در VS Code کار کنند؛
- LSP diagnostics و completion روزمره قابل استفاده باشد؛
- خروجی RTL اکستنشن پایدار بماند؛
- capabilityها قابل مشاهده و قابل محدودسازی باشند؛
- برنامه‌های نسخهٔ ۱ بدون اصلاح اجباری اجرا شوند؛
- حداقل ۳۰۰ تست خودکار، تست cross-platform و چند پروژهٔ واقعی نمونه وجود داشته باشد.

## چیزهایی که در هستهٔ ۲٫۰ نباید وارد شوند

compiler native، inheritance پیچیده، package manager بزرگ، شبکهٔ آزاد، database، AI اجباری، سه‌بعدی، multiplayer و دسترسی مستقیم به سیستم‌عامل نباید زودتر از تثبیت semantics، event loop، module system و debugger وارد شوند.

## جمع‌بندی

پیشنهاد اصلی این است که مسیر بعدی با عنوان **Tirotir 2.0 Architecture Track** تعریف شود، نه مجموعه‌ای از patchهای جدا برای GUI و بازی. هستهٔ فعلی حفظ می‌شود؛ اما قبل از بزرگ‌شدن قابلیت‌های خلاقانه، قراردادهای diagnostics، capability، event، module، object و debug تثبیت می‌شوند.

این طراحی اجازه می‌دهد یک کودک با `چاپ -سلام جهان-` شروع کند، یک دانش‌آموز با `تکرار` شکل بسازد، یک کاربر متوسط تابع و فهرست بنویسد و یک کاربر پیشرفته پروژهٔ چندفایلی و رویدادمحور بسازد؛ همه در یک زبان واحد و با امنیت قابل کنترل.

## منابع

[1]: https://microsoft.github.io/language-server-protocol/ "Language Server Protocol — Official Site"

[2]: https://microsoft.github.io/debug-adapter-protocol/specification.html "Debug Adapter Protocol — Official Specification"
