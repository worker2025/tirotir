# Historical baseline — KI-1

این پوشه evidence رفتار تاریخی KI-1 را نگه می‌دارد و بخشی از candidate acceptance suite نیست.

## رفتار تاریخی

```text
Commit: a6dd5dec1b4b9e2a304fec0a6cf06aecac7b417a
Input: چاپ ۵-۳+۲-۱
Output: 5
```

Assertion اصلی با معنای تاریخی، بدون تغییر معنایی، در `tests/baseline/ki1_historical_behavior.py` نگه‌داری شده است. فایل baseline عمداً وارد collection عادی candidate نمی‌شود؛ candidate contract خروجی `3` را تصویب کرده است.

## بازتولید

برای بازتولید واقعی baseline، یک checkout مستقل از commit بالا بسازید و همان تست را در آن اجرا کنید؛ source candidate را تغییر ندهید:

```bash
git worktree add /tmp/tirotir-ki1-baseline \
  a6dd5dec1b4b9e2a304fec0a6cf06aecac7b417a
cd /tmp/tirotir-ki1-baseline
PYTHONPATH=src python3 -m pytest -q \
  tests/test_known_issues.py::test_ki1_legacy_text_and_arithmetic_tokenization_are_characterized
```

در baseline باید خروجی تاریخی `5` بازتولید شود. در integration candidate، تست baseline جداگانه اجرا نمی‌شود؛ full candidate suite فقط acceptance contract جدید را بررسی می‌کند.

این سند test اجرایی نیست و برای جلوگیری از اشتباه گرفتن evidence تاریخی با acceptance candidate در collection عادی قرار نگرفته است.
