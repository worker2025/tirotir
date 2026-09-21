"""هستهٔ نسخهٔ ۱ تیروتیر؛ پیاده‌سازی مستقل و امن زبان فارسی."""
from dataclasses import dataclass, fields, is_dataclass
import html, re, math, wave, struct
from .audio import AudioBackendUnavailable, play_file, render_sequence
from .contracts import SourceSpan

DIGITS=str.maketrans('۰۱۲۳۴۵۶۷۸۹٫٬','0123456789.,')
def norm(s:str)->str:return s.translate(DIGITS).replace('ي','ی').replace('ك','ک').replace('\u200c','_')
class TirotirError(Exception):pass
class SyntaxErrorFa(TirotirError):pass
class RuntimeErrorFa(TirotirError):pass
@dataclass
class Tok:
 kind:str; value:str; line:int; col:int
 @property
 def span(self)->SourceSpan:
  return SourceSpan(start_line=self.line,start_column=self.col,end_line=self.line,end_column=self.col+max(1,len(self.value)))

def tokenize(src:str):
 src=src.replace('\r\n','\n').replace('\r','\n'); out=[]; levels=[0]
 for ln,line in enumerate(src.split('\n'),1):
  raw=line.expandtabs(4); s=raw.lstrip(); ind=len(raw)-len(s)
  if not s or s.startswith('#'):continue
  if ind>levels[-1]:levels.append(ind);out.append(Tok('INDENT','',ln,1))
  while ind<levels[-1]:levels.pop();out.append(Tok('DEDENT','',ln,1))
  if ind!=levels[-1]:raise SyntaxErrorFa(f'خطای تورفتگی در خط {ln}: تورفتگی باید یکنواخت باشد.')
  i=ind
  while i<len(raw):
   c=raw[i]
   if c.isspace():i+=1;continue
   if c=='#':break
   col=i+1
   if c=='-':
    # متن با -...-؛ خط تیرهٔ جدا از دو طرف عملگر تفریق است
    j=i+1; escaped=False; buf=[]
    while j<len(raw):
     if raw[j]=='-' and not escaped:break
     if raw[j]=='\\' and j+1<len(raw) and raw[j+1]=='-':buf.append('-');j+=2;escaped=False;continue
     buf.append(raw[j]);j+=1;escaped=False
    if j<len(raw) and j>i+1 and not raw[i+1].isspace():out.append(Tok('STRING',''.join(buf),ln,col));i=j+1;continue
    out.append(Tok('OP','-',ln,col));i+=1;continue
   if c=='،':out.append(Tok('OP',',',ln,col));i+=1;continue
   if c.isdigit() or c in '۰۱۲۳۴۵۶۷۸۹':
    m=re.match(r'[0-9۰-۹]+(?:[٫.][0-9۰-۹]+)?',raw[i:]);v=norm(m.group());out.append(Tok('NUMBER',v,ln,col));i+=len(m.group());continue
   if c.isalpha() or c=='_' or '\u0600'<=c<='\u06ff':
    m=re.match(r'[\w\u0600-\u06ff]+',raw[i:],re.UNICODE);out.append(Tok('WORD',norm(m.group()),ln,col));i+=len(m.group());continue
   two=raw[i:i+2]
   if two in ('==','>=','<=','!='):out.append(Tok('OP',two,ln,col));i+=2;continue
   if c in '+*/%=<>[](),:':out.append(Tok('OP',c,ln,col));i+=1;continue
   raise SyntaxErrorFa(f'نویسهٔ ناشناخته «{c}» در خط {ln}، ستون {col}')
  out.append(Tok('NEWLINE','',ln,len(raw)+1))
 while len(levels)>1:levels.pop();out.append(Tok('DEDENT','',ln,1))
 out.append(Tok('EOF','',ln,1));return out

@dataclass
class Node:pass
@dataclass
class Program(Node):body:list
@dataclass
class Decl(Node):name:str;expr:Node;const:bool=False
@dataclass
class Assign(Node):target:Node;expr:Node
@dataclass
class ExprStmt(Node):expr:Node
@dataclass
class Print(Node):expr:Node
@dataclass
class Input(Node):pass
@dataclass
class If(Node):branches:list;otherwise:list
@dataclass
class While(Node):cond:Node;body:list
@dataclass
class For(Node):name:str;expr:Node;body:list
@dataclass
class Func(Node):name:str;args:list;body:list
@dataclass
class Call(Node):name:str;args:list
@dataclass
class Return(Node):expr:Node|None
@dataclass
class Break(Node):pass
@dataclass
class Continue(Node):pass
@dataclass
class Repeat(Node):count:Node;body:list
@dataclass
class Lit(Node):value:object
@dataclass
class Var(Node):name:str
@dataclass
class Bin(Node):left:Node;op:str;right:Node
@dataclass
class Unary(Node):op:str;expr:Node
@dataclass
class ListNode(Node):items:list
@dataclass
class DictNode(Node):items:list
@dataclass
class Index(Node):obj:Node;key:Node
@dataclass
class Import(Node):name:str;alias:str|None=None

class Parser:
 def __init__(self,t):self.t=t;self.i=0
 def cur(self):return self.t[self.i]
 def take(self):x=self.cur();self.i+=1;return x
 def accept(self,v):
  if self.cur().value==v:return self.take()
  return None
 def end(self):
  if self.cur().kind=='NEWLINE':self.take()
 def block(self):
  while self.cur().kind=='NEWLINE':self.take()
  if self.cur().kind!='INDENT':raise SyntaxErrorFa(f'خطای نحوی در خط {self.cur().line}: بدنه باید تورفته باشد.')
  self.take();b=self.program('DEDENT')
  if self.cur().kind=='DEDENT':self.take()
  return b
 def program(self,stop='EOF'):
  b=[]
  while self.cur().kind not in (stop,'EOF'):
   if self.cur().kind=='NEWLINE':self.take();continue
   b.append(self.statement())
  return b
 def statement(self):
  t=self.cur();v=t.value
  if v in ('بگذار','ثابت'):
   self.take();n=self.take()
   if n.kind!='WORD':raise SyntaxErrorFa(f'نام متغیر در خط {n.line} معتبر نیست.')
   if not self.accept('برابر') and not self.accept('='):raise SyntaxErrorFa(f'انتظار «برابر» در خط {t.line} داشتم.')
   if self.cur().value=='فرهنگ':
    self.take();return Decl(n.value,self.dict_block(),v=='ثابت')
   e=self.expr();self.end();return Decl(n.value,e,v=='ثابت')
  if v=='چاپ':self.take();e=self.expr();self.end();return Print(e)
  if v=='بخوان':self.take();self.end();return Input()
  if v=='اگر':
   branches=[];self.take();branches.append((self.expr(),self.block()))
   while self.cur().value=='وگرنه':
    self.take()
    if self.cur().value=='اگر':self.take();branches.append((self.expr(),self.block()))
    else:return If(branches,self.block())
   return If(branches,[])
  if v=='تاوقتی':self.take();return While(self.expr(),self.block())
  if v=='برای':
   self.take();n=self.take();self.accept('در');return For(n.value,self.expr(),self.block())
  if v=='تکرار':
   self.take();count=self.expr()
   if self.cur().value=='بار':self.take()
   return Repeat(count,self.block())
  if v=='تابع':
   self.take();n=self.take();self.accept('با');args=[]
   while self.cur().kind=='WORD' and self.cur().value not in ('بازگردان',):
    args.append(self.take().value)
    if not self.accept('و'):break
   return Func(n.value,args,self.block())
  if v=='وارد':
   self.take();self.accept('کن');name=self.take()
   if name.kind!='STRING':raise SyntaxErrorFa('نام ماژول باید در متن نوشته شود.')
   self.end();return Import(name.value)
  if v=='بازگردان':self.take();e=None if self.cur().kind in ('NEWLINE','DEDENT') else self.expr();self.end();return Return(e)
  if v in ('بیرون','ادامه'):self.take();self.end();return Break() if v=='بیرون' else Continue()
  noarg={'پنجره_ببند','پاک_کن','قلم_پایین','قلم_بالا','ورودی_بساز','متن_چندخطی_بساز','نمایش_پنجره'}
  if t.kind=='WORD' and v in noarg:
   self.take();self.end();return ExprStmt(Call(v,[]))
  left=self.expr()
  if self.accept('=') or (isinstance(left,Var) and self.accept('برابر')):
   e=self.expr();self.end();return Assign(left,e)
  self.end();return ExprStmt(left)
 def dict_block(self):
  self.end()
  if self.cur().kind!='INDENT':raise SyntaxErrorFa('بدنهٔ فرهنگ باید تورفته باشد.')
  self.take();items=[]
  while self.cur().kind not in ('DEDENT','EOF'):
   if self.cur().kind=='NEWLINE':self.take();continue
   key=self.take().value
   if not self.accept('برابر'):raise SyntaxErrorFa('هر عضو فرهنگ باید با «برابر» مقداردهی شود.')
   items.append((key,self.expr()));self.end()
  if self.cur().kind=='DEDENT':self.take()
  return DictNode(items)
 def expr(self,minp=0):
  t=self.take()
  if t.kind=='NUMBER':left=Lit(float(t.value) if '.' in t.value else int(t.value))
  elif t.kind=='STRING':left=Lit(t.value)
  elif t.value in ('درست','نادرست','تهی'):left=Lit({'درست':True,'نادرست':False,'تهی':None}[t.value])
  elif t.value in ('نه','-'):left=Unary('نه' if t.value=='نه' else '-',self.expr(6))
  elif t.value=='(':left=self.expr();self.accept(')')
  elif t.value=='[':
   a=[]
   while self.cur().value!=']':
    a.append(self.expr());
    if not self.accept(','):break
   if not self.accept(']'):raise SyntaxErrorFa(f'فهرست در خط {t.line} بسته نشده است.')
   left=ListNode(a)
  elif t.kind=='WORD':
   if t.value=='بخوان':left=Call('بخوان',[])
   elif self.cur().value=='با':
    self.take();args=[]
    while self.cur().kind not in ('NEWLINE','EOF','DEDENT'):
     args.append(self.expr(3))
     if not self.accept('و'):break
    left=Call(t.value,args)
   else:left=Var(t.value)
  else:raise SyntaxErrorFa(f'انتظار یک عبارت داشتم، اما «{t.value}» دریافت شد (خط {t.line}).')
  while self.cur().value=='[':
   self.take();k=self.expr();self.accept(']');left=Index(left,k)
  if isinstance(left,Var) and self.cur().kind=='WORD' and self.cur().value not in ('و','یا','بزرگتر','کوچکتر','از','مساوی','برابر'):
   left=Index(left,Lit(self.take().value))
  prec={'یا':1,'و':2,'==':3,'!=':3,'>':3,'<':3,'>=':3,'<=':3,'بزرگتر':3,'کوچکتر':3,'+':4,'-':4,'*':5,'/':5,'%':5}
  while True:
   op=self.cur().value;p=prec.get(op,-1)
   if p<minp:break
   self.take()
   if op in ('بزرگتر','کوچکتر') and self.cur().value=='از':self.take()
   if op in ('بزرگتر','کوچکتر') and self.cur().value=='یا':
    self.take();self.accept('مساوی');op='>=' if op=='بزرگتر' else '<='
   right=self.expr(p+1);left=Bin(left,op,right)
  return left
 def parse(self):return Program(self.program())

def ast_json(n):
 if is_dataclass(n):return {'نوع':n.__class__.__name__,**{f.name:ast_json(getattr(n,f.name)) for f in fields(n)}}
 if isinstance(n,list):return [ast_json(x) for x in n]
 if isinstance(n,tuple):return [ast_json(x) for x in n]
 return n
class Env:
 def __init__(self,parent=None):self.d={};self.const=set();self.parent=parent
 def get(self,k):
  if k in self.d:return self.d[k]
  if self.parent:return self.parent.get(k)
  raise RuntimeErrorFa(f'متغیر «{k}» تعریف نشده است. پیشنهاد: ابتدا آن را با «بگذار» تعریف کنید.')
 def owner(self,k):return self if k in self.d else self.parent.owner(k) if self.parent else None
 def set(self,k,v):
  e=self.owner(k)
  if not e:raise RuntimeErrorFa(f'متغیر «{k}» تعریف نشده است.')
  if k in e.const:raise RuntimeErrorFa(f'ثابت «{k}» قابل تغییر نیست.')
  e.d[k]=v
class Ret(Exception):
 def __init__(self,v):self.v=v
class Br(Exception):pass
class Cont(Exception):pass
class Interpreter:
 def __init__(self,output=None,input_fn=None,max_steps=100000,play_audio=False):self.env=Env();self.out=print if output is None else output;self.input=input if input_fn is None else input_fn;self.steps=0;self.max_steps=max_steps;self.funcs={};self.play_audio=play_audio;self.audio_notes=[];self.audio_path='tirotir-note.wav'
 def run(self,p):
  for s in p.body:
   if isinstance(s,Func):self.funcs[s.name]=s
  self.execs(p.body,self.env)
  if self.audio_notes:
   render_sequence(self.audio_notes,self.audio_path)
   if self.play_audio:
    try:play_file(self.audio_path)
    except AudioBackendUnavailable:self.out('پخش‌کننده پیدا نشد؛ فایل tirotir-note.wav ذخیره شد.')
 def execs(self,b,e):
  old=self.env;self.env=e
  try:
   for s in b:self.step(s)
  finally:self.env=old
 def step(self,s):
  self.steps+=1
  if self.steps>self.max_steps:raise RuntimeErrorFa('اجرای برنامه بیش از حد طولانی شد؛ حلقهٔ بی‌نهایت متوقف شد.')
  if isinstance(s,Decl):
   val=self.val(s.expr)
   if s.name in self.env.d:self.env.set(s.name,val)
   elif self.env.parent and self.env.parent.owner(s.name):self.env.set(s.name,val)
   else:self.env.d[s.name]=val
   if s.const:self.env.const.add(s.name)
  elif isinstance(s,Assign):self.assign(s.target,self.val(s.expr))
  elif isinstance(s,Print):self.out(self.val(s.expr))
  elif isinstance(s,Input):return self.input()
  elif isinstance(s,ExprStmt):self.val(s.expr)
  elif isinstance(s,If):
   for c,b in s.branches:
    if self.val(c):self.execs(b,self.env);return
   self.execs(s.otherwise,self.env)
  elif isinstance(s,While):
   while self.val(s.cond):
    try:self.execs(s.body,self.env)
    except Br:break
    except Cont:continue
  elif isinstance(s,For):
   it=self.val(s.expr)
   if not isinstance(it,(list,tuple,str)):raise RuntimeErrorFa('حلقهٔ «برای» به فهرست یا متن نیاز دارد.')
   for x in it:
    self.env.d[s.name]=x
    try:self.execs(s.body,self.env)
    except Br:break
    except Cont:continue
  elif isinstance(s,Repeat):
   for _ in range(int(self.val(s.count))):
    try:self.execs(s.body,self.env)
    except Br:break
    except Cont:continue
  elif isinstance(s,Return):raise Ret(self.val(s.expr) if s.expr else None)
  elif isinstance(s,Break):raise Br()
  elif isinstance(s,Continue):raise Cont()
  elif isinstance(s,Func):self.funcs[s.name]=s
 def assign(self,t,v):
  if isinstance(t,Var):
   if t.name in ('رنگ_قلم','ضخامت_قلم'):self.graphics(t.name,[v]);return
   self.env.set(t.name,v);return
  if isinstance(t,Index):
   obj=self.val(t.obj);key=self.val(t.key)
   try:obj[key]=v
   except (TypeError,IndexError,KeyError):raise RuntimeErrorFa('دسترسی یا تغییر عضو نامعتبر است.')
   return
  raise RuntimeErrorFa('سمت چپ انتساب معتبر نیست.')
 def val(self,n):
  if isinstance(n,Lit):return n.value
  if isinstance(n,Var):return self.env.get(n.name)
  if isinstance(n,ListNode):return [self.val(x) for x in n.items]
  if isinstance(n,DictNode):return {k:self.val(v) for k,v in n.items}
  if isinstance(n,Index):
   try:
    key=self.val(n.key)
   except RuntimeErrorFa:
    key=n.key.name if isinstance(n.key,Var) else None
   try:return self.val(n.obj)[key]
   except (IndexError,KeyError,TypeError):raise RuntimeErrorFa('دسترسی به فهرست یا فرهنگ نامعتبر است.')
  if isinstance(n,Unary):
   v=self.val(n.expr)
   if n.op=='نه':return not v
   if n.op=='-':return -v
  if isinstance(n,Bin):
   a=self.val(n.left);o=n.op
   if o=='و':return bool(a and self.val(n.right))
   if o=='یا':return bool(a or self.val(n.right))
   b=self.val(n.right)
   try:return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b,'%':lambda:a%b,'==':lambda:a==b,'!=':lambda:a!=b,'>':lambda:a>b,'<':lambda:a<b,'>=':lambda:a>=b,'<=':lambda:a<=b}[o]()
   except (KeyError,TypeError,ZeroDivisionError):raise RuntimeErrorFa(f'عملیات «{o}» روی این نوع داده مجاز نیست.')
  if isinstance(n,Call):
   args=[self.val(a) for a in n.args]
   if n.name in ('پنجره_بازکن','پنجره_ببند','پاک_کن','حرکت','عقب_برو','چرخش','به_سمت','قلم_پایین','قلم_بالا','رنگ_قلم','ضخامت_قلم','مربع','مستطیل','دایره','مثلث','پر_کن'):
    return self.graphics(n.name,args)
   if n.name in ('پنجره_بساز','برچسب_بساز','دکمه_بساز','ورودی_بساز','چک_باکس_بساز','لیست_بساز','منوی_انتخاب_بساز','متن_چندخطی_بساز','نوار_لغزش_بساز','نمایش_پنجره'):
    return self.gui_command(n.name,args)
   if n.name=='نت_بنواز':
    return self.audio_note(args)
   if n.name=='موسیقی_پخش_کن':
    raise RuntimeErrorFa('پخش فایل موسیقی در نسخهٔ ۱٫۱ آزمایشی است؛ از نت بنواز استفاده کنید.')
   if n.name=='بخوان':return self.input()
   if n.name=='طول':return len(args[0])
   if n.name=='افزودن':args[0].append(args[1]);return None
   if n.name=='حذف':return args[0].pop(args[1])
   if n.name=='به_عدد':return float(args[0])
   if n.name=='به_متن':return str(args[0])
   f=self.funcs.get(n.name)
   if not f:raise RuntimeErrorFa(f'تابع «{n.name}» تعریف نشده است.')
   if len(args)!=len(f.args):raise RuntimeErrorFa(f'تعداد آرگومان‌های تابع «{n.name}» نادرست است.')
   e=Env(self.env);e.d.update(zip(f.args,args))
   try:self.execs(f.body,e)
   except Ret as r:return r.v
   return None
  return None
 def graphics(self,name,args):
  if not hasattr(self,'scene'):self.scene=Scene()
  return self.scene.command(name,args)
 def audio_note(self,args):
  if not args:raise RuntimeErrorFa('نت بنواز به نام نت یا فرکانس نیاز دارد.')
  notes={'دو':261.63,'ر':'293.66','رِ':293.66,'می':329.63,'فا':349.23,'سل':392.00,'لا':440.00,'سی':493.88}
  try:freq=float(args[0])
  except (TypeError,ValueError):
   key=str(args[0]).strip();freq=notes.get(key)
   if freq is None:raise RuntimeErrorFa(f'نت «{key}» شناخته نشد؛ یکی از دو، ر، می، فا، سل، لا یا سی را انتخاب کنید.')
  duration=float(args[1]) if len(args)>1 else 0.25
  self.audio_notes.append((freq,duration))
  return self.audio_path
 def gui_command(self,name,args):
  if not hasattr(self,'gui'):self.gui=Gui()
  return self.gui.command(name,args)

class Scene:
 def __init__(self):self.w=800;self.h=600;self.x=0;self.y=0;self.angle=0;self.pen=True;self.color='black';self.width=2;self.items=[]
 COLOR_MAP={'سیاه':'#000000','سفید':'#ffffff','قرمز':'#dc2626','سبز':'#16a34a','آبی':'#2563eb','زرد':'#eab308','نارنجی':'#f97316','بنفش':'#9333ea'}
 def command(self,name,args):
  if name=='پنجره_بازکن':self.w=int(args[0]) if args else 800;self.h=int(args[1]) if len(args)>1 else 600
  elif name=='پنجره_ببند':pass
  elif name=='پاک_کن':self.items=[]
  elif name in ('قلم_پایین','قلم_بالا'):self.pen=name=='قلم_پایین'
  elif name=='رنگ_قلم':self.color=str(args[0])
  elif name=='ضخامت_قلم':self.width=float(args[0])
  elif name in ('حرکت','عقب_برو'):
   distance=float(args[0]);distance=-distance if name=='عقب_برو' else distance
   nx=self.x+math.cos(math.radians(self.angle))*distance;ny=self.y+math.sin(math.radians(self.angle))*distance
   if self.pen:
    svg_color=self.COLOR_MAP.get(self.color,self.color if re.fullmatch(r'(?:#[0-9a-fA-F]{3,8}|[A-Za-z]+)',self.color) else '#000000')
    source_color=html.escape(str(self.color),quote=True)
    self.items.append(f'<line x1="{self.x:.2f}" y1="{self.y:.2f}" x2="{nx:.2f}" y2="{ny:.2f}" stroke="{svg_color}" data-tirotir-color="{source_color}" stroke-width="{self.width}"/>')
   self.x,self.y=nx,ny
  elif name=='چرخش':self.angle+=float(args[0])
  elif name=='به_سمت':self.angle=float(args[0])
  elif name=='مربع':
   side=float(args[0]);[self.command('حرکت',[side]) or self.command('چرخش',[90]) for _ in range(4)]
  elif name=='مثلث':
   side=float(args[0]);[self.command('حرکت',[side]) or self.command('چرخش',[120]) for _ in range(3)]
  elif name=='مستطیل':
   a,b=float(args[0]),float(args[1]);[(self.command('حرکت',[a if i%2==0 else b]) or self.command('چرخش',[90])) for i in range(4)]
  elif name=='دایره':
   r=float(args[0]);steps=72;[(self.command('حرکت',[2*math.pi*r/steps]) or self.command('چرخش',[360/steps])) for _ in range(steps)]
  elif name=='پر_کن':pass
  return None
 def save(self,path='tirotir-scene.svg'):
  body=''.join(self.items)
  points=[]
  for item in self.items:
   m=re.search(r'x1="([\-0-9.]+)" y1="([\-0-9.]+)" x2="([\-0-9.]+)" y2="([\-0-9.]+)"',item)
   if m:points.extend([(float(m.group(1)),float(m.group(2))),(float(m.group(3)),float(m.group(4)))])
  if points:
   pad=max(12.0,self.width*2); minx=min(p[0] for p in points)-pad; maxx=max(p[0] for p in points)+pad; miny=min(p[1] for p in points)-pad; maxy=max(p[1] for p in points)+pad
   # تبدیل دستگاه منطقی (محور Y رو به بالا) به مختصات صفحهٔ SVG.
   vx=self.w/2+minx; vy=self.h/2-maxy; vw=max(1.0,maxx-minx); vh=max(1.0,maxy-miny)
  else:vx,vy,vw,vh=0,0,self.w,self.h
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}" preserveAspectRatio="xMidYMid meet"><rect width="100%" height="100%" fill="white"/><g transform="translate({self.w/2},{self.h/2}) scale(1,-1)">{body}</g></svg>'
  open(path,'w',encoding='utf8').write(svg);return path

class Gui:
 """رابط گرافیکی اختیاری؛ فقط با فراخوانی API فعال و به Tkinter وابسته است."""
 def __init__(self):
  try:
   import tkinter as tk
   self.tk=tk;self.root=None;self.widgets=[]
  except ImportError:raise RuntimeErrorFa('TIR4001: رابط گرافیکی در این محیط در دسترس نیست؛ Tkinter و desktop لازم است.')
 def command(self,name,args):
  if name=='پنجره_بساز':
   title=str(args[0]) if args else 'تیروتیر';w=int(args[1]) if len(args)>1 else 640;h=int(args[2]) if len(args)>2 else 480
   try:self.root=self.tk.Tk()
   except Exception as exc:raise RuntimeErrorFa('TIR4001: رابط گرافیکی در این محیط در دسترس نیست؛ اجرای GUI به desktop نیاز دارد.') from exc
   self.root.title(title);self.root.geometry(f'{w}x{h}')
  elif self.root is None:raise RuntimeErrorFa('ابتدا با «پنجره بساز» یک پنجره ایجاد کنید.')
  elif name=='برچسب_بساز':
   self.widgets.append(self.tk.Label(self.root,text=str(args[0]) if args else '').pack(padx=12,pady=8))
  elif name=='دکمه_بساز':
   self.widgets.append(self.tk.Button(self.root,text=str(args[0]) if args else 'دکمه').pack(padx=12,pady=8))
  elif name=='ورودی_بساز':self.widgets.append(self.tk.Entry(self.root));self.widgets[-1].pack(padx=12,pady=8)
  elif name=='چک_باکس_بساز':
   var=self.tk.BooleanVar();self.widgets.append(self.tk.Checkbutton(self.root,text=str(args[0]) if args else 'فعال',variable=var));self.widgets[-1].pack(padx=12,pady=8)
  elif name=='لیست_بساز':
   values=[str(x) for x in args];self.widgets.append(self.tk.Listbox(self.root,height=max(3,len(values))));[self.widgets[-1].insert(self.tk.END,x) for x in values];self.widgets[-1].pack(padx=12,pady=8)
  elif name=='منوی_انتخاب_بساز':
   var=self.tk.StringVar(value=str(args[0]) if args else '');self.widgets.append(self.tk.OptionMenu(self.root,var,*[str(x) for x in args]));self.widgets[-1].pack(padx=12,pady=8)
  elif name=='متن_چندخطی_بساز':
   self.widgets.append(self.tk.Text(self.root,height=5,width=40));self.widgets[-1].pack(padx=12,pady=8)
  elif name=='نوار_لغزش_بساز':
   self.widgets.append(self.tk.Scale(self.root,from_=0,to=int(args[0]) if args else 100,orient=self.tk.HORIZONTAL));self.widgets[-1].pack(padx=12,pady=8)
  elif name=='نمایش_پنجره':self.root.mainloop()
  elif name=='پنجره_ببند' and self.root:self.root.destroy();self.root=None
  return None

def parse(src):
 src=src.replace('\u200c','_')
 aliases=[('پنجره بازکن','پنجره_بازکن'),('پنجره ببند','پنجره_ببند'),('پنجره بساز','پنجره_بساز'),('برچسب بساز','برچسب_بساز'),('دکمه بساز','دکمه_بساز'),('ورودی بساز','ورودی_بساز'),('چک_باکس بساز','چک_باکس_بساز'),('چک‌باکس بساز','چک_باکس_بساز'),('چک باکس بساز','چک_باکس_بساز'),('لیست بساز','لیست_بساز'),('منوی انتخاب بساز','منوی_انتخاب_بساز'),('متن چندخطی بساز','متن_چندخطی_بساز'),('نوار لغزش بساز','نوار_لغزش_بساز'),('نمایش پنجره','نمایش_پنجره'),('پاک کن','پاک_کن'),('عقب برو','عقب_برو'),('قلم پایین','قلم_پایین'),('قلم بالا','قلم_بالا'),('رنگ قلم','رنگ_قلم'),('ضخامت قلم','ضخامت_قلم'),('نت بنواز','نت_بنواز'),('موسیقی پخش کن','موسیقی_پخش_کن')]
 for a,b in aliases:src=src.replace(a,b)
 for a,b in [('بزرگتر یا مساوی','>='),('کوچکتر یا مساوی','<='),('برابر با','=='),('نا برابر با','!='),('بزرگتر از','>'),('کوچکتر از','<')]:src=re.sub(r'(?<![\w\u0600-\u06ff])'+re.escape(a)+r'(?![\w\u0600-\u06ff])',b,src)
 return Parser(tokenize(src)).parse()
def execute(src,output=None,input_fn=None,scene_path=None,play_audio=False):
 p=parse(src);runner=Interpreter(output,input_fn,play_audio=play_audio);runner.run(p)
 if hasattr(runner,'scene'):runner.scene.save(scene_path or 'tirotir-scene.svg')
 return p
