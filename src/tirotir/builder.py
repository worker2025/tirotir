"""رابط گرافیکی مستقل برای ساخت EXE تیروتیر؛ هستهٔ زبان را تغییر نمی‌دهد."""
from pathlib import Path
import os, subprocess, sys, tempfile, threading

def resolve_launcher():
    """Resolve a real launcher from development repo or installed package."""
    candidates=[]
    configured=os.environ.get('TIROTIR_LAUNCHER')
    if configured: candidates.append(Path(configured).expanduser())
    package_root=Path(__file__).resolve().parent
    repo_root=package_root.parents[1]
    candidates.extend([repo_root/'tools'/'tirotir_launcher.py', package_root/'launcher.py'])
    for candidate in candidates:
        if candidate.is_file(): return candidate
    raise FileNotFoundError('Launcher تیروتیر پیدا نشد؛ مسیرهای بررسی‌شده: '+', '.join(str(x) for x in candidates))

def make_entry_launcher(entry, work):
    target=Path(work)/'tirotir_entry_launcher.py'
    source=Path(entry).read_text(encoding='utf8')
    target.write_text(
        'import os\n'
        'from tirotir.core import execute, parse\n'
        'from tirotir.semantic import SemanticAnalyzer\n'
        'os.environ["TIROTIR_ENTRY"]='+repr(str(Path(entry).resolve()))+'\n'
        'source='+repr(source)+'\n'
        'result=SemanticAnalyzer(os.environ["TIROTIR_ENTRY"]).analyze(parse(source))\n'
        'if result.diagnostics:\n'
        '    raise SystemExit("\\n".join(d.message for d in result.diagnostics))\n'
        'execute(source)\n',
        encoding='utf8')
    return target

class BuilderApp:
    def __init__(self, root):
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
        self.tk=tk; self.filedialog=filedialog; self.messagebox=messagebox; self.ttk=ttk
        self.root=root; root.title('Tirotir EXE Builder'); root.geometry('680x520')
        self.file=tk.StringVar(); self.name=tk.StringVar(value='MyTirotirApp'); self.mode=tk.StringVar(value='onefile')
        self.console=tk.BooleanVar(value=True); self.icon=tk.StringVar(); self.out=tk.StringVar(value=str(Path.cwd()/'dist'))
        ttk=self.ttk
        form=ttk.Frame(root,padding=16); form.pack(fill='both',expand=True)
        self._row(form,0,'فایل اصلی (.t):',self.file,self.pick_file)
        self._row(form,1,'نام برنامه:',self.name,None)
        ttk.Label(form,text='حالت خروجی:').grid(row=2,column=0,sticky='w',pady=6)
        ttk.Radiobutton(form,text='One File',variable=self.mode,value='onefile').grid(row=2,column=1,sticky='w')
        ttk.Radiobutton(form,text='Folder',variable=self.mode,value='onedir').grid(row=2,column=2,sticky='w')
        ttk.Checkbutton(form,text='نمایش کنسول',variable=self.console).grid(row=3,column=1,sticky='w',pady=6)
        self._row(form,4,'آیکون (.ico):',self.icon,self.pick_icon)
        self._row(form,5,'مسیر خروجی:',self.out,self.pick_out)
        self.build=ttk.Button(form,text='Build EXE',command=self.start); self.build.grid(row=6,column=1,sticky='w',pady=14)
        ttk.Button(form,text='باز کردن پوشهٔ خروجی',command=self.open_output).grid(row=6,column=2,sticky='w',pady=14)
        self.status=tk.Text(form,height=14,wrap='word'); self.status.grid(row=7,column=0,columnspan=3,sticky='nsew')
        form.columnconfigure(1,weight=1); form.rowconfigure(7,weight=1)
    def _row(self,box,row,label,var,command):
        ttk=self.ttk; ttk.Label(box,text=label).grid(row=row,column=0,sticky='w',pady=5); ttk.Entry(box,textvariable=var).grid(row=row,column=1,columnspan=2,sticky='ew',padx=6)
        if command: ttk.Button(box,text='انتخاب',command=command).grid(row=row,column=3)
    def pick_file(self):
        p=self.filedialog.askopenfilename(filetypes=[('Tirotir files','*.t'),('All files','*.*')]);
        if p:self.file.set(p)
    def pick_icon(self):
        p=self.filedialog.askopenfilename(filetypes=[('Icon','*.ico')]);
        if p:self.icon.set(p)
    def pick_out(self):
        p=self.filedialog.askdirectory();
        if p:self.out.set(p)
    def open_output(self):
        out=Path(self.out.get()).resolve(); out.mkdir(parents=True,exist_ok=True)
        if sys.platform.startswith('win'):
            os.startfile(str(out))
        elif sys.platform=='darwin':
            subprocess.Popen(['open',str(out)])
        else:
            subprocess.Popen(['xdg-open',str(out)])
    def log(self,text):
        self.root.after(0,lambda:(self.status.insert('end',text+'\n'),self.status.see('end')))
    def start(self):
        if not self.file.get().lower().endswith('.t') or not Path(self.file.get()).is_file():
            self.messagebox.showerror('خطا','یک فایل اصلی معتبر با پسوند .t انتخاب کنید.'); return
        self.build.configure(state='disabled'); threading.Thread(target=self.build_exe,daemon=True).start()
    def build_exe(self):
        out=Path(self.out.get()).resolve(); out.mkdir(parents=True,exist_ok=True); work=out/'_tirotir_build'; work.mkdir(exist_ok=True)
        cmd=['pyinstaller','--clean','--noconfirm','--name',self.name.get() or 'TirotirApp','--distpath',str(out),'--workpath',str(work/'build'),'--specpath',str(work),'--paths',str(Path(__file__).resolve().parent.parent),'--onefile' if self.mode.get()=='onefile' else '--onedir']
        if not self.console.get():cmd.append('--windowed')
        if self.icon.get():cmd += ['--icon',self.icon.get()]
        # launcher اجراگر زبان است و source انتخاب‌شده به‌عنوان آرگومان به آن داده می‌شود.
        try: launcher=make_entry_launcher(self.file.get(),work); cmd.append(str(launcher))
        except FileNotFoundError as exc:
            self.log('خطای launcher: '+str(exc)); self.root.after(0,lambda:self.build.configure(state='normal')); return
        self.log('در حال ساخت: '+' '.join(cmd))
        try:
            p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
            for line in p.stdout:self.log(line.rstrip())
            code=p.wait()
            artifact=out/(self.name.get() or 'TirotirApp')
            if self.mode.get()=='onefile' and sys.platform.startswith('win'):artifact=artifact.with_suffix('.exe')
            if code==0:
                self.log('ساخت موفق شد: '+str(artifact))
                if artifact.is_file() or artifact.is_dir():
                    self.log('در حال اجرای EXE ساخته‌شده...')
                    run=subprocess.run([str(artifact)],cwd=str(out),capture_output=True,text=True,encoding='utf-8',errors='replace')
                    if run.stdout:self.log(run.stdout.rstrip())
                    if run.stderr:self.log(run.stderr.rstrip())
                    self.log('اجرای EXE با code='+str(run.returncode))
                else:self.log('هشدار: artifact خروجی پیدا نشد؛ log ساخت را بررسی کنید.')
            else:self.log(f'ساخت ناموفق بود؛ code={code}')
        except FileNotFoundError:self.log('PyInstaller پیدا نشد؛ ابتدا pip install pyinstaller را اجرا کنید.')
        finally:self.root.after(0,lambda:self.build.configure(state='normal'))

def main():
    import tkinter as tk
    root=tk.Tk(); BuilderApp(root); root.mainloop()
