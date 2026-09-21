$ErrorActionPreference = 'Stop'
py -m pip install --upgrade pyinstaller
py -m pip install .
pyinstaller --clean --onefile --name tirotir --paths src tools/tirotir_launcher.py
Write-Host 'ساخته شد: dist\\tirotir.exe'
