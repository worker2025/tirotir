const vscode = require('vscode');
const cp = require('child_process');

function activeFile() {
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.languageId !== 'tirotirLang') {
    vscode.window.showWarningMessage('یک فایل .t را باز کنید.'); return null;
  }
  if (editor.document.isDirty) editor.document.save();
  return editor.document.fileName;
}
function cli() { return vscode.workspace.getConfiguration('tirotirLang').get('command', 'tirotir'); }
function runTerminal(command) {
  const file=activeFile(); if (!file) return;
  const terminal=vscode.window.createTerminal('TirotirLang'); terminal.show(true);
  terminal.sendText(`${cli()} ${command} "${file}"`);
}
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function safeSvg(s) { return String(s||'').replace(/<script[\s\S]*?<\/script>/gi,''); }
function webviewHtml(payload, errorText) {
  const error=Boolean(errorText); const svg=error ? '' : safeSvg(payload && payload.svg);
  const text=error ? errorText : ((payload && payload.stdout) || 'خروجی‌ای وجود ندارد.');
  const status=error ? 'خطای اجرای برنامه' : 'اجرای برنامه با موفقیت انجام شد';
  const missing=!error && !svg ? '<div class="missing">صحنه‌ای در اجرای جدید تولید نشد.</div>' : '';
  return `<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'"><style>
  body{direction:rtl;background:#1e1e1e;color:#ddd;font-family:Tahoma,"Vazirmatn",sans-serif;padding:24px;line-height:1.8}
  h2{color:#7dd3fc}.status{color:${error?'#fca5a5':'#86efac'}}.missing{color:#fbbf24}.scene{direction:ltr;background:#fff;border-radius:8px;padding:12px;margin:16px 0;text-align:center}.scene svg{max-width:100%;height:auto}pre{direction:rtl;unicode-bidi:plaintext;white-space:pre-wrap;background:#111827;padding:18px;border-radius:8px}
  </style></head><body><h2>خروجی تیروتیر</h2><div class="status">${esc(status)}</div>${svg?`<div class="scene">${svg}</div>`:missing}<pre>${esc(text)}</pre></body></html>`;
}
function runLiveScene() {
  const file=activeFile(); if (!file) return;
  const panel=vscode.window.createWebviewPanel('tirotirLive','خروجی زندهٔ تیروتیر',vscode.ViewColumn.Beside,{enableScripts:false});
  panel.webview.html=webviewHtml(null,'در حال اجرای برنامه...');
  cp.execFile(cli(),['run',file,'--live-scene'],{encoding:'utf8',windowsHide:true},(error,stdout,stderr)=>{
    if (error) { panel.webview.html=webviewHtml(null,`خطای اجرای برنامه\n${stderr||error.message}`); return; }
    try { panel.webview.html=webviewHtml(JSON.parse(stdout),null); }
    catch (_) { panel.webview.html=webviewHtml(null,'خطای پروتکل خروجی live scene؛ JSON معتبر دریافت نشد.'); }
  });
}
function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('tirotirLang.runFile',()=>runTerminal('run')),
    vscode.commands.registerCommand('tirotirLang.checkFile',()=>runTerminal('check')),
    vscode.commands.registerCommand('tirotirLang.showAst',()=>runTerminal('ast')),
    vscode.commands.registerCommand('tirotirLang.runRTL',runLiveScene),
    vscode.commands.registerCommand('tirotirLang.runGraphics',runLiveScene),
    vscode.commands.registerCommand('tirotirLang.runAudio',()=>runTerminal('audio')),
    vscode.commands.registerCommand('tirotirLang.runGui',()=>runTerminal('gui'))
  );
}
function deactivate() {}
module.exports={activate,deactivate};
