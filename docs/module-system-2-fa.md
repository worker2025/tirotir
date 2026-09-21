# Module System تیروتیر ۲٫۰

این milestone پس از Contract Freeze و Semantic Layer، یک سیستم ماژول کوچک، deterministic و sandbox‌شده فراهم می‌کند. هدف package manager یا registry خارجی نیست؛ هدف ساخت graph پروژه پیش از اجرا است.

## قراردادهای اصلی

### ModuleId

هر ماژول با `project_root` و `canonical_path` شناخته می‌شود. مسیر نسبی فقط ورودی resolve است و هویت نهایی نیست. namespace از مسیر نسبی canonical ساخته می‌شود؛ برای نمونه `lib/tools.tirotir` دارای namespace `lib.tools` است.

### ModuleLoader

`ModuleLoader` فقط سه مسئولیت دارد:

```text
resolve(import)
load(module_id)
parse(module_id)
```

این loader هیچ semantic analysis، interpreter یا side effectی اجرا نمی‌کند. تشخیص importها برای graph از متن source انجام می‌شود و parse فقط AST می‌سازد.

### Sandbox

مسیر با `Path.resolve()` canonicalize می‌شود و سپس با project root مقایسه می‌شود. بنابراین مسیرهایی مانند `../../secret.tirotir` حتی اگر با بررسی رشته‌ای ساده پنهان شوند، پذیرفته نمی‌شوند. فقط فایل‌های داخل project root قابل resolve هستند.

### ModuleGraph

graph پیش از execution ساخته می‌شود. هر node یک `ModuleSpec` و هر edge یک import به `ModuleId` canonical است. چرخه با diagnostic `TIR3001` گزارش می‌شود. خطاهای module not found و مسیر نامعتبر به‌ترتیب با `TIR3002` و `TIR3003` گزارش می‌شوند.

### Namespace

نسخهٔ نخست namespace صریح را انتخاب می‌کند. import یک فایل، نام‌های آن را بی‌قاعده وارد scope جاری نمی‌کند. دسترسی dotted مانند `ابزار.جمع` در مرحلهٔ Object/Module integration به semantic resolver اضافه خواهد شد؛ این milestone عمداً parsing، identity، graph و امنیت مسیر را جدا نگه می‌دارد.

### ModuleCache

هر module در یک اجرای پروژه فقط یک بار load یا initialize می‌شود. cache از اجرای تکراری side effectهای سطح module جلوگیری می‌کند.

## tirotir.toml

نمونهٔ حداقلی:

```toml
[project]
name = "my-project"
entry = "main.tirotir"
language = "2.0"

[capabilities]
graphics = false
audio = false
gui = false
project-files = false
network = false
```

در این مرحله package manager، dependency خارجی، registry و نصب package وجود ندارد.

## نمونهٔ پروژهٔ دوماژوله

ساختار:

```text
my-project/
    tirotir.toml
    main.tirotir
    lib/
        tools.tirotir
```

`main.tirotir`:

```text
وارد کن -lib/tools-
چاپ -main-
```

`lib/tools.tirotir`:

```text
چاپ -tools-
```

ساخت graph از API Python:

```python
from tirotir.modules import ModuleGraphBuilder, ModuleLoader

loader = ModuleLoader("my-project")
entry = loader.sandbox.module_id("my-project/main.tirotir")
graph, diagnostics = ModuleGraphBuilder(loader).build(entry)
```

در این عملیات هیچ `چاپ` اجرا نمی‌شود؛ فقط source خوانده، importها resolve و graph ساخته می‌شوند.

## تست‌های milestone

تست‌های مستقل در `tests/test_modules.py` موارد زیر را پوشش می‌دهند:

- هویت canonical؛
- resolve مسیر ساده و nested؛
- جلوگیری از `..` و خروج از root؛
- load و parse؛
- graph و topological order؛
- تشخیص cycle؛
- cache یک‌باره؛
- خواندن `tirotir.toml`؛
- عدم اجرای source در graph construction.

مرحلهٔ بعدی، اتصال namespace ماژول‌ها به Semantic Layer و سپس اجرای graph با ترتیب topological است. Event Runtime و Object Model عمداً وارد این milestone نشده‌اند.
