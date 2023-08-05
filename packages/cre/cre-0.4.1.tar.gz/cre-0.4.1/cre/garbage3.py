from numba import njit, f8
import cre
from cre import Var
from cre import define_fact
from cre.obj import CREObjType
from cre.utils import cast
from numba.typed import Dict

BOOP1 = define_fact("BOOP1", {"A" : "string", "B" : "number"})

@njit()
def baz():
    b = BOOP1("A",1)
    print(hash(b))
    c = cast(b, CREObjType)
    print(hash(c))
    # d = Dict.empty(BOOP1, f8)
    # # d[c] = 1.0
    
    # if(c not in d):
    #     print("HI")
    # return d

print(baz())

@njit(cache=True)
def foo(x):
    return str(x)

@njit(cache=True)
def bar(x):
    return float(x)

print(foo(True))
print(foo(1.0))
print(foo(1))

print(bar("1.0"))
print(bar("1"))
