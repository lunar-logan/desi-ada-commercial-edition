# exprtype.py
'''
Expr Type System
================
This file defines classes representing types.  There is a general
class used to represent all types.  Each type is then a singleton
instance of the type class.

class ExprType(object):
      pass

int_type = ExprType("int",...)
float_type = ExprType("float",...)
string_type = ExprType("string", ...)

The contents of the type class is entirely up to you.  However, you
will minimally need to encode some information about:

   a.  What operators are supported (+, -, *, etc.).
   b.  Default values
   c.  ????
   d.  Profit!

Once you have defined the built-in types, you will need to
make sure they get registered with any symbol tables or
code that checks for type names in 'exprcheck.py'.

Note:  This file is expanded in later stages of the compiler project.
'''

import operator

class ExprType(object):
    '''
    Class that represents a type in the Expr language.  Types 
    are declared as singleton instances of this type.
    '''
    def __init__(self, typename, default, 
                 unary_opcodes=None, binary_opcodes=None, 
                 binary_ops=None, unary_ops=None,
                 binary_folds=None, unary_folds=None, rel_folds=None,
                 rel_ops=None, rel_opcodes=None):
        '''
        You must implement yourself and figure out what to store.
        '''
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
    binary_opcodes={"+": "add", "-": "sub", "*": "imul", "/": "idiv","**": "pow","mod": "mod","rem":"rem"},
    unary_opcodes={"+": "uadd", "-": "uneg","abs":"abs"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, "**": operator.pow, "mod": operator.mod},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"=", "/=", "<", ">", "<=", ">=","in","notin"},
    rel_opcodes={"=": "eq", "/=": "ne", ">": "gt", "<": "lt", ">=": "ge", "<=": "le","in":"in","notin":"notin"},
    rel_folds={"=": operator.eq, "/=": operator.ne, ">": operator.gt, ">=": operator.ge,
               "<": operator.lt, "<=": operator.le}
)
FloatType = ExprType("float", float(), 
    binary_ops={"+", "-", "*", "/"}, 
    unary_ops={"+", "-","abs"},
    binary_opcodes={"+": "add", "-": "sub", "*": "fmul", "/": "fdiv"},
    unary_opcodes={"+": "uadd", "-": "uneg","abs":"abs"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"=", "/=", "<", ">", "<=", ">="},
    rel_opcodes={"=": "eq", "/=": "ne", ">": "gt", "<": "lt", ">=": "ge", "<=": "le"},
    rel_folds={"=": operator.eq, "/=": operator.ne, ">": operator.gt, ">=": operator.ge,
               "<": operator.lt, "<=": operator.le}
)
StringType = ExprType("string", str(), 
    binary_ops={"+","&"},
    binary_opcodes={"+": "add","&":"ampersand"},
    binary_folds={"+": operator.add},
    rel_ops={"=", "/="},
    rel_opcodes={"=": "eq", "/=": "ne"},
    rel_folds={"=": operator.eq, "/=": operator.ne}
)
BoolType = ExprType("bool", bool(),
    unary_ops={"!"},
    rel_ops={"=", "/=", "&&", "||","andthen","orelse"},
    rel_opcodes={"=": "eq", "/=": "ne", "&&": "land", "||": "lor","andthen":"andthen","orelse":"orelse"},
    rel_folds={"=": operator.eq, "/=": operator.ne, "&&": operator.and_, "||": operator.or_},
    unary_opcodes={"!": "not"},
    unary_folds={"!": operator.not_}
)
