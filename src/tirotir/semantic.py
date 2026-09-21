"""تحلیل معنایی تیروتیر؛ مستقل از interpreter و بدون side effect."""
from dataclasses import dataclass, field
from typing import Any
from .contracts import Diagnostic, NodeId, SourceSpan, node_id
from .core import (Assign, Bin, Break, Call, Continue, Decl, DictNode, ExprStmt,
                   For, Func, If, Index, ListNode, Lit, Node, Print, Program,
                   Repeat, Return, Unary, Var, While)

@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str
    scope: str
    span: SourceSpan = field(default_factory=SourceSpan)
    node_id: NodeId = field(default_factory=lambda: NodeId("unknown"))

@dataclass
class Scope:
    name: str
    parent: 'Scope|None' = None
    symbols: dict[str, Symbol] = field(default_factory=dict)
    children: list['Scope'] = field(default_factory=list)

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> Symbol|None:
        if name in self.symbols:
            return self.symbols[name]
        return self.parent.lookup(name) if self.parent else None

@dataclass
class SymbolTable:
    global_scope: Scope
    scopes: list[Scope] = field(default_factory=list)

@dataclass
class SemanticResult:
    symbols: SymbolTable
    diagnostics: list[Diagnostic]

BUILTINS = {
    'طول','افزودن','حذف','به_عدد','به_متن','بخوان',
    'پنجره_بازکن','پنجره_ببند','پاک_کن','حرکت','عقب_برو','چرخش',
    'به_سمت','قلم_پایین','قلم_بالا','رنگ_قلم','ضخامت_قلم',
    'مربع','مستطیل','دایره','مثلث','پر_کن','نت_بنواز','موسیقی_پخش_کن',
    'پنجره_بساز','برچسب_بساز','دکمه_بساز','ورودی_بساز',
    'چک_باکس_بساز','لیست_بساز','منوی_انتخاب_بساز','متن_چندخطی_بساز',
    'نوار_لغزش_بساز','نمایش_پنجره',
}
RUNTIME_ASSIGNMENTS = {'رنگ_قلم', 'ضخامت_قلم'}

class SemanticAnalyzer:
    """AST را می‌خواند و فقط SymbolTable و Diagnostic تولید می‌کند."""
    def __init__(self, source: str = '<متن>'):
        self.source = source
        self.diagnostics: list[Diagnostic] = []
        self.ordinal = 0
        self.global_scope = Scope('global')
        self.table = SymbolTable(self.global_scope)
        self.current = self.global_scope
        self.function_depth = 0
        self.loop_depth = 0
        self.functions: dict[str, Func] = {}

    def _span(self) -> SourceSpan:
        # تا زمان اتصال کامل span به همهٔ AST nodeها، مکان امن و معتبر منبع
        return SourceSpan(source=self.source)

    def _diagnostic(self, code: str, typ: str, message: str, suggestion: str|None=None) -> None:
        self.diagnostics.append(Diagnostic(code, 'error', typ, message, self._span(), suggestion))

    def _new_id(self, kind: str) -> NodeId:
        self.ordinal += 1
        return node_id(self.source, self.ordinal, kind)

    def analyze(self, program: Program) -> SemanticResult:
        # توابع پیش از عبور از بدنه ثبت می‌شوند تا فراخوانی forward و recursion مجاز باشد.
        for statement in program.body:
            if isinstance(statement, Func):
                self.functions[statement.name] = statement
                self._define(statement.name, 'function')
        self._statements(program.body)
        return SemanticResult(self.table, self.diagnostics)

    def _define(self, name: str, kind: str) -> None:
        symbol = Symbol(name, kind, self.current.name, self._span(), self._new_id(kind))
        if not self.current.define(symbol):
            old = self.current.symbols[name]
            if kind == 'constant' or old.kind == 'constant' or kind == 'function':
                self._diagnostic('TIR2002','duplicate_definition',f'نام «{name}» در این scope قبلاً تعریف شده است.', 'نام دیگری انتخاب کن.')

    def _statements(self, statements: list[Node]) -> None:
        for statement in statements:
            self._statement(statement)

    def _statement(self, statement: Node) -> None:
        if isinstance(statement, Decl):
            kind = 'constant' if statement.const else 'variable'
            # «بگذار» برای مقداردهی دوباره نیز syntax رسمی است.
            if statement.const or not self.current.lookup(statement.name):
                self._define(statement.name, kind)
            self._expression(statement.expr)
        elif isinstance(statement, Assign):
            if isinstance(statement.target, Var):
                symbol = self.current.lookup(statement.target.name)
                if not symbol and statement.target.name not in RUNTIME_ASSIGNMENTS:
                    self._undefined(statement.target.name)
                elif symbol and symbol.kind == 'constant':
                    self._diagnostic('TIR2003','constant_assignment',f'ثابت «{statement.target.name}» قابل تغییر نیست.')
            else:
                self._expression(statement.target)
            self._expression(statement.expr)
        elif isinstance(statement, (Print, ExprStmt)):
            self._expression(statement.expr)
        elif statement.__class__.__name__ == 'Input':
            return
        elif isinstance(statement, If):
            for condition, body in statement.branches:
                self._expression(condition); self._statements(body)
            self._statements(statement.otherwise)
        elif isinstance(statement, While):
            self._expression(statement.cond)
            self.loop_depth += 1; self._statements(statement.body); self.loop_depth -= 1
        elif isinstance(statement, For):
            self._expression(statement.expr)
            self._define_if_missing(statement.name, 'variable')
            self.loop_depth += 1; self._statements(statement.body); self.loop_depth -= 1
        elif isinstance(statement, Repeat):
            self._expression(statement.count)
            self.loop_depth += 1; self._statements(statement.body); self.loop_depth -= 1
        elif isinstance(statement, Func):
            self.function_depth += 1
            child = Scope(f'function:{statement.name}', self.current)
            self.current.children.append(child); self.table.scopes.append(child)
            old = self.current; self.current = child
            for argument in statement.args: self._define_if_missing(argument, 'parameter')
            self._statements(statement.body)
            self.current = old; self.function_depth -= 1
        elif isinstance(statement, Return):
            if self.function_depth == 0:
                self._diagnostic('TIR2004','return_outside_function','«بازگردان» فقط داخل تابع مجاز است.')
            if statement.expr: self._expression(statement.expr)
        elif isinstance(statement, Break):
            if self.loop_depth == 0:self._diagnostic('TIR2005','break_outside_loop','«بیرون» فقط داخل حلقه مجاز است.')
        elif isinstance(statement, Continue):
            if self.loop_depth == 0:self._diagnostic('TIR2006','continue_outside_loop','«ادامه» فقط داخل حلقه مجاز است.')

    def _define_if_missing(self, name: str, kind: str) -> None:
        if not self.current.lookup(name): self._define(name, kind)

    def _undefined(self, name: str) -> None:
        self._diagnostic('TIR2001','undefined_name',f'متغیر «{name}» پیدا نشد.', 'ابتدا آن را با «بگذار» تعریف کن.')

    def _expression(self, expression: Node) -> None:
        if isinstance(expression, (Lit,)): return
        if isinstance(expression, Var):
            if not self.current.lookup(expression.name) and expression.name not in BUILTINS and expression.name not in self.functions:
                self._undefined(expression.name)
        elif isinstance(expression, (ListNode,)):
            for item in expression.items:self._expression(item)
        elif isinstance(expression, DictNode):
            for _, value in expression.items:self._expression(value)
        elif isinstance(expression, Index):
            self._expression(expression.obj)
            # در «شخص[سن]»، نام ناشناخته می‌تواند کلید متنی فرهنگ باشد؛
            # نام‌های شناخته‌شده همچنان به‌عنوان expression تحلیل می‌شوند.
            if not (isinstance(expression.key, Var) and not self.current.lookup(expression.key.name)):
                self._expression(expression.key)
        elif isinstance(expression, Unary):self._expression(expression.expr)
        elif isinstance(expression, Bin):self._expression(expression.left);self._expression(expression.right)
        elif isinstance(expression, Call):
            if expression.name not in BUILTINS and expression.name not in self.functions:
                self._undefined(expression.name)
            if expression.name in self.functions:
                expected=len(self.functions[expression.name].args); actual=len(expression.args)
                if expected != actual:
                    self._diagnostic('TIR2007','argument_count_mismatch',f'تعداد آرگومان‌های تابع «{expression.name}» نادرست است.',f'{expected} آرگومان لازم است.')
            for argument in expression.args:self._expression(argument)
