
## ممیزی امنیت و CI پس از گزارش اولیه

در commit بعدی، `tests/test_security_boundaries.py` پنج آزمون واقعی برای موارد زیر اضافه کرد:

- deny-by-default برای `network` و `project-files`؛
- اثبات اینکه فعال‌کردن این enumها به‌تنهایی backend زبانی ایجاد نمی‌کند؛
- رد مسیر مطلق و parent traversal در ModuleSandbox؛
- رد symlink escape از project root؛
- بارگذاری موفق فایل داخل project root.

نتیجهٔ این تست‌ها `5 passed` و full suite جدید `291 passed` است.

فایل `.github/workflows/ci.yml` نیز matrix لینوکس برای Python 3.11 و 3.12، نصب package، نصب pytest، اجرای suite و CLI smoke را تعریف می‌کند. این workflow در این session روی GitHub runner اجرا نشده و صرفاً contract آن به‌صورت محلی بررسی شده است.

برای `network` و `project-files` در زبان فعلی primitive یا backend عمومی وجود ندارد؛ بنابراین آن‌ها عمداً «قابلیت عملیاتی» اعلام نشده‌اند. افزودن API فایل یا شبکه بدون قرارداد مسیر، policy و تست end-to-end امن، تغییر پرخطر و خارج از این patch کوچک است.
