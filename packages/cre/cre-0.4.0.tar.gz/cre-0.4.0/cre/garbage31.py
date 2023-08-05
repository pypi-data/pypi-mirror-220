import numpy as np
from numba.core import types
from numba import njit, float64, f8
from numba.experimental import structref
from numba.core.extending import overload_method, overload

@structref.register
class MyClassType(types.StructRef):
    pass

MyType = MyClassType([("x",f8[::1])])


class MyClass(structref.StructRefProxy):
    def __new__(cls, x):
        self = my_class_ctor(x)
        return self

    @property
    def x(self):
        return _x(self)

@njit(cache=True)
def _x(self):
    return self.x

@overload(MyClass)
def overload_MyClass(x):
    def impl(x):
        return my_class_ctor(x)
    return impl

structref.define_boxing(MyClassType, MyClass)

@njit(MyType(f8[::1]))
def my_class_ctor(x):
    st = structref.new(MyType)
    st.x = x
    return st

# This works...
@njit
def test():
    my_instance = MyClass(np.array([1.0, 2.0, 3.0]))
    print(my_instance.x) # prints [1. 2. 3.]
test()

# But this gets:
# TypeError: cannot convert native 
# numba.MyClassType(('x', array(float64, 1d, A)),) to Python object
my_instance = MyClass(np.array([1.0, 2.0, 3.0]))
