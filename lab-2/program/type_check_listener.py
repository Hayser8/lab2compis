from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):
    def __init__(self):
        self.errors = []
        self.types = {}

    # === EQ / NEQ ===
    def exitEqNeq(self, ctx: SimpleLangParser.EqNeqContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        if type(lt) is not type(rt):
            self.errors.append(f"Incompatible types for '{ctx.op.text}': {lt} and {rt}")
        self.types[ctx] = BoolType()

    # === MUL / DIV / MOD ===
    def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        op = ctx.op.text

        if op == '%':
            if not isinstance(lt, IntType) or not isinstance(rt, IntType):
                self.errors.append(f"Unsupported operand types for '%': {lt} and {rt}")
            self.types[ctx] = IntType()
            return

        if not isinstance(lt, (IntType, FloatType)) or not isinstance(rt, (IntType, FloatType)):
            self.errors.append(f"Unsupported operand types for '{op}': {lt} and {rt}")
            # asignamos algo para continuar
            self.types[ctx] = FloatType() if op == '/' else IntType()
        else:
            # división siempre float; si alguno es float→float; else int
            if op == '/' or isinstance(lt, FloatType) or isinstance(rt, FloatType):
                self.types[ctx] = FloatType()
            else:
                self.types[ctx] = IntType()

    # === ADD / SUB ===
    def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        if not isinstance(lt, (IntType, FloatType)) or not isinstance(rt, (IntType, FloatType)):
            self.errors.append(f"Unsupported operand types for '{ctx.op.text}': {lt} and {rt}")
        else:
            self.types[ctx] = FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()

    # === LITERALS & PARENS ===
    def exitInt(self, ctx: SimpleLangParser.IntContext):
        self.types[ctx] = IntType()

    def exitFloat(self, ctx: SimpleLangParser.FloatContext):
        self.types[ctx] = FloatType()

    def exitString(self, ctx: SimpleLangParser.StringContext):
        self.types[ctx] = StringType()

    def exitBool(self, ctx: SimpleLangParser.BoolContext):
        self.types[ctx] = BoolType()

    def exitParens(self, ctx: SimpleLangParser.ParensContext):
        self.types[ctx] = self.types[ctx.expr()]
