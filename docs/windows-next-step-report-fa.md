# گزارش گام بعدی Windows — Tirotir 1.1.0

## نتیجه

```text
Tests: 240 passed
Examples: 71 passed
Move/Rotate: PASS
.t in VS Code manifest: PASS
GUI primitives: PASS (parser/runtime API added)
Builder prototype: PASS (module and CLI command available)
Audio Windows: PASS (manual verification retained)
RTL: PASS (manual verification retained)
```

## حرکت و چرخش

سناریوی دستی چهار حرکت ۱۰۰ و سه چرخش ۹۰ بررسی شد. runtime چهار line واقعی زیر را تولید می‌کند:

```text
(0,0) -> (100,0)
(100,0) -> (100,100)
(100,100) -> (0,100)
(0,100) -> (0,0)
```

تست regression مختصات lineهای SVG را دقیقاً بررسی می‌کند؛ بنابراین فقط parse شدن دستورها تست نشده است. اصلاح viewport قبلی نیز bounding box همین مسیر را در viewBox قرار می‌دهد.

## پسوند `.t` در VS Code

Manifest اکستنشن اکنون فقط `.t` را associate می‌کند:

```json
"extensions": [".t"]
```

همهٔ نمونه‌ها و مستندات اصلی `.t` هستند. CLI و ModuleLoader پسوند قدیمی `.tirotir` را برای compatibility می‌پذیرند.

## GUI primitiveهای اضافه‌شده

این primitiveها به‌صورت API Tkinter اضافه شدند:

```text
چک‌باکس بساز
لیست بساز
منوی انتخاب بساز
متن چندخطی بساز
نوار لغزش بساز
```

برای مواردی که آرگومان لازم دارند، فرم `با` پشتیبانی می‌شود. event/binding هنوز عمداً اضافه نشده است تا parser، semantic و runtime آن در یک milestone مستقل کامل شوند.

## Tirotir EXE Builder

فرمان مستقل زیر اضافه شد:

```bash
tirotir builder
```

Builder با Tkinter طراحی شده و این گزینه‌ها را دارد:

- انتخاب فایل اصلی `.t`؛
- نام برنامه؛
- One File یا Folder؛
- حالت console یا windowed؛
- آیکون `.ico`؛
- مسیر خروجی؛
- اجرای PyInstaller؛
- نمایش log و خطا در همان پنجره.

Builder در محیط headless بدون import شکست‌خوردهٔ هسته کار می‌کند، ولی بازکردن UI نیازمند desktop و Tkinter است. اجرای native روی Windows باید manual acceptance شود.

## وضعیت Audio و RTL

Audio و RTL مطابق تست دستی Windows کار می‌کنند و در این گام تغییر داده نشدند، جز حفظ regressionهای قبلی.

## فایل‌های release

- `dist/tirotir-1.1.0-py3-none-any.whl`
- `dist/tirotir-1.1.0.tar.gz`
- `/home/ubuntu/tirotirLang-1.1.0.vsix`
- `/home/ubuntu/tirotir-1.1.0-release.tar.gz`
