# Contract Freeze معماری تیروتیر ۲٫۰

این سند قراردادهای پایه‌ای را ثبت می‌کند که باید پیش از توسعهٔ Semantic Layer، ماژول، event loop، object model و debugger پایدار بمانند.

## SourceSpan

هر token، diagnostic و در آینده هر AST node باید بتواند محدودهٔ منبع خود را ارائه کند:

```python
SourceSpan(source, start_line, start_column, end_line, end_column)
```

شمارهٔ خط و ستون از یک شروع می‌شوند. `to_dict()` برای خروجی JSON و LSP در نظر گرفته شده است.

## Diagnostic

تشخیص‌ها دارای `code`، `severity`، `type`، `message`، `span` و در صورت امکان `suggestion` هستند. نمایش انسانی CLI و JSON باید از همین شیء ساخته شوند و پیام‌های backend نباید قرارداد مستقل بسازند.

## NodeId

شناسهٔ node در قرارداد فعلی با `node_id(source, ordinal, kind)` تولید می‌شود. پیش از debugger باید شناسه به AST nodeها متصل شود؛ اما مقدار آن باید برای یک source و parse یکسان تکرارپذیر باشد.

## RuntimeService

سرویس‌هایی مانند graphics، audio، GUI و events باید قرارداد `name`، `capability` و `call(operation, args)` را رعایت کنند. parser نباید به Tkinter، SVG یا pygame وابسته شود.

## Capability

capabilityهای رسمی فعلی عبارت‌اند از `core`، `graphics`، `audio`، `gui`، `project-files` و `network`. `CapabilityRegistry` در حالت پیش‌فرض فقط `core` را فعال می‌کند. هر backend باید پیش از عملیات `require()` را فراخوانی کند.

## سازگاری نسخهٔ ۱

قرارداد `v1_contract()` قواعد حیاتی را ثبت می‌کند: متن `-...-`، انتساب فارسی و `=`، تورفتگی، شناسهٔ Unicode و ممنوعیت import آزاد Python. هر تغییر آینده باید تست سازگاری این قرارداد را حفظ کند.

## دسته‌بندی تست‌ها

تست‌های آینده در چهار گروه نگهداری می‌شوند:

| دسته | هدف |
|---|---|
| unit | رفتار یک تابع، token، node یا service |
| semantic/diagnostic | name resolution، scope و پیام‌های خطا |
| integration | ارتباط parser، runtime، module و backend |
| cross-platform acceptance | نصب و اجرای واقعی روی Windows، Linux و macOS |

## وضعیت پیاده‌سازی

نسخهٔ فعلی قراردادهای immutable پایه، serializable و دارای تست مستقل دارد. این گام عمداً رفتار زبان را تغییر نمی‌دهد؛ گام بعدی باید Semantic Layer را روی همین قراردادها بنا کند.
