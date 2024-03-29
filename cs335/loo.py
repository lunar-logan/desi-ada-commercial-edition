import operator

class ExprType(object):
    def __init__(self, typename, default, 
                 unary_opcodes=None, binary_opcodes=None, 
                 binary_ops=None, unary_ops=None,
                 binary_folds=None, unary_folds=None, rel_folds=None,
                 rel_ops=None, rel_opcodes=None):
        self.typename = typename
        self.binary_ops = binary_ops or set()
        self.unary_ops = unary_ops or set()
        self.default = default
        self.unary_opcodes = unary_opcodes or {}
        self.binary_opcodes = binary_opcodes or {}
        self.unary_folds = unary_folds or set()
        self.binary_folds = binary_folds or set()
        self.rel_ops = rel_ops or set()
        self.rel_opcodes = rel_opcodes or {}
        self.rel_folds = rel_folds or {}

    def __repr__(self):
        return "ExprType({})".format(self.typename)

IntType = ExprType("integer", int(), 
    binary_ops={"+", "-", "*", "/","**","mod","rem"}, 
    unary_ops={"+", "-","abs"},
    binary_opcodes={"+": "add", "-": "sub", "*": "mul", "/": "div","**": "pow","mod": "mod","rem":"rem"},
    unary_opcodes={"+": "uadd", "-": "uneg","abs":"abs"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, "**": operator.pow, "mod": operator.mod},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"=", "/=", "<", ">", "<=", ">=","in","notin"},
    rel_opcodes={"=": "seq", "/=": "sne", ">": "sgt", "<": "slt", ">=": "sge", "<=": "sle","in":"in","notin":"notin"},
    rel_folds={"=": operator.eq, "/=": operator.ne, ">": operator.gt, ">=": operator.ge,
               "<": operator.lt, "<=": operator.le}
)
FloatType = ExprType("float", float(), 
    binary_ops={"+", "-", "*", "/"}, 
    unary_ops={"+", "-","abs"},
    binary_opcodes={"+": "add.s", "-": "sub.s", "*": "mul.s", "/": "div.s"},
    unary_opcodes={"+": "uadd", "-": "uneg","abs":"abs"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"=", "/=", "<", ">", "<=", ">="},
    rel_opcodes={"=": "seq.s", "/=": "sne.s", ">": "sgt.s", "<": "slt.s", ">=": "sge.s", "<=": "sle.s"},
    rel_folds={"=": operator.eq, "/=": operator.ne, ">": operator.gt, ">=": operator.ge,
               "<": operator.lt, "<=": operator.le}
)
StringType = ExprType("string", str(), 
    binary_ops={"&"},
    binary_opcodes={"&":"ampersand"},
    binary_folds={"&": operator.add},
    rel_ops={},
    rel_opcodes={},
    rel_folds={}
)
BoolType = ExprType("bool", bool(),
    unary_ops={"!"},
    rel_ops={"=", "/=", "and", "or","xor","andthen","orelse"},
    rel_opcodes={"=": "seq", "/=": "sne", "and": "land", "or": "lor", "xor": "lxor","andthen":"andthen","orelse":"orelse"},     rel_folds={"=": operator.eq, "/=": operator.ne, "&&": operator.and_, "||": operator.or_},
    unary_opcodes={"!": "not"},
    unary_folds={"!": operator.not_}
)

CharType = ExprType("character",str(),
    unary_ops={},
    rel_ops={},
    rel_opcodes={},
    rel_folds={},
    unary_opcodes={},
    unary_folds={}
)

EnumType = ExprType("enumeration",None,
    unary_ops={},
    rel_ops={},
    rel_opcodes={},
    rel_folds={},
    unary_opcodes={},
    unary_folds={}
)

ArrayType = ExprType("array",list(),
    unary_ops={},
    rel_ops={},
    rel_opcodes={},
    rel_folds={},
    unary_opcodes={},
    unary_folds={}
)

AccessType = ExprType("access",None,
    unary_ops={},
    rel_ops={},
    rel_opcodes={},
    rel_folds={},
    unary_opcodes={},
    unary_folds={}
)

RecordType = ExprType("record",None,
    unary_ops={},
    rel_ops={},
    rel_opcodes={},
    rel_folds={},
    unary_opcodes={},
    unary_folds={}
)
