# type_check_visitor.py
from SimpleLangVisitor import SimpleLangVisitor
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

INT = IntType(); FLOAT = FloatType(); STRING = StringType(); BOOL = BoolType()

class TypeCheckVisitor(SimpleLangVisitor):
    def __init__(self):
        self.errors = []

    # --- Recorre todo el programa ---
    def visitProg(self, ctx: SimpleLangParser.ProgContext):
        for st in ctx.stat():
            self.visit(st)
        return None

    def visitStat(self, ctx: SimpleLangParser.StatContext):
        return self.visit(ctx.expr())

    # === EQ / NEQ ===
    def visitEqNeq(self, ctx: SimpleLangParser.EqNeqContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        if type(lt) is not type(rt):
            self.errors.append(f"Incompatible types for '{ctx.op.text}': {lt} and {rt}")
        return BoolType()

    # === MUL / DIV / MOD ===
    def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        op = ctx.op.text

        if op == '%':
            if not isinstance(lt, IntType) or not isinstance(rt, IntType):
                self.errors.append(f"Unsupported operand types for '%': {lt} and {rt}")
            return IntType()

        if not isinstance(lt, (IntType, FloatType)) or not isinstance(rt, (IntType, FloatType)):
            self.errors.append(f"Unsupported operand types for '{op}': {lt} and {rt}")
            return FloatType() if op == '/' else IntType()

        if op == '/' or isinstance(lt, FloatType) or isinstance(rt, FloatType):
            return FloatType()
        return IntType()

    # === ADD / SUB ===
    def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        if not isinstance(lt, (IntType, FloatType)) or not isinstance(rt, (IntType, FloatType)):
            self.errors.append(f"Unsupported operand types for '{ctx.op.text}': {lt} and {rt}")
            return FloatType()
        return FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()

    # === LITERALS & PARENS ===
    def visitInt(self, ctx: SimpleLangParser.IntContext):   return IntType()
    def visitFloat(self, ctx: SimpleLangParser.FloatContext): return FloatType()
    def visitString(self, ctx: SimpleLangParser.StringContext): return StringType()
    def visitBool(self, ctx: SimpleLangParser.BoolContext):   return BoolType()
    def visitParens(self, ctx: SimpleLangParser.ParensContext):
        return self.visit(ctx.expr())
