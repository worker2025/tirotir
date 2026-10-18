
## افزونهٔ VS Code و بسته‌بندی

در این محیط `code`/VS Code CLI نصب نیست، بنابراین نصب و فعال‌سازی واقعی extension در VS Code انجام نشد. بااین‌حال VSIX با `npx @vscode/vsce package` واقعاً ساخته و با `unzip -t` بررسی شد:

```text
/tmp/tirotirlang-2.0.0-dev.vsix
SHA-256: 0009a74b8787a5e3003c286d8ee749c53ab2827a9ede607dd7bff6a69b20d16c
```

هشدار اولیهٔ vsce دربارهٔ نبودن `.vscodeignore` با افزودن این فایل رفع شد و repository metadata افزونه به `https://github.com/worker2025/tirotir` اصلاح شد. این نتیجه فقط package integrity و manifest را ثابت می‌کند، نه اجرای واقعی VS Code.

## event syntax

زیرساخت Python برای event وجود دارد و GUI callback واقعی smoke شده است، اما syntax عمومی event هنوز به زبان اضافه نشده است. افزودن syntax بدون قرارداد پایدار برای scope، lifetime، callback و ارتباط با event loop، در این مرحله تغییر پرخطر محسوب می‌شود؛ بنابراین قابلیت صوری یا نیمه‌کاره اضافه نشده است.
