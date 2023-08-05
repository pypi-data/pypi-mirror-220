import operator
import numpy as np
import numba
from numba import types, njit, i8, u8, i4, u1,u2,u4,  i8, literally, generated_jit, objmode
from numba.typed import List
from numba.core.types import ListType, unicode_type, void, Tuple
from numba.experimental import structref
from numba.experimental.structref import new, define_attributes, _Utils
from numba.extending import SentryLiteralArgs, lower_cast, overload_method, intrinsic, overload_attribute, intrinsic, lower_getattr_generic, overload, infer_getattr, lower_setattr_generic
from numba.core.typing.templates import AttributeTemplate
from cre.context import cre_context, get_cre_context_data
from cre.structref import define_structref, define_boxing, define_structref_template, CastFriendlyStructref
from cre.fact import define_fact, BaseFact, cast_fact, DeferredFactRefType, Fact, _standardize_type
from cre.utils import cast, PrintElapse, ptr_t, decode_idrec, lower_getattr,  lower_setattr, lower_getattr, _decref_ptr, _incref_ptr, _incref_structref, _ptr_from_struct_incref
from cre.utils import assign_to_alias_in_parent_frame, encode_idrec, _obj_cast_codegen
from cre.vector import VectorType
from cre.obj import cre_obj_field_dict,CREObjType, CREObjTypeClass, CREObjProxy, set_chr_mbrs
from cre.type_conv import ptr_to_var_name
# from cre.predicate_node import BasePredicateNode,BasePredicateNodeType, get_alpha_predicate_node_definition, \
# get_beta_predicate_node_definition, deref_attrs, define_alpha_predicate_node, define_beta_predicate_node, AlphaPredicateNode, BetaPredicateNode
from numba.core import imputils, cgutils
from numba.core.datamodel import default_manager, models
from numba.experimental.structref import StructRefProxy


from operator import itemgetter
from copy import copy
from os import getenv
from cre.utils import deref_info_type, DEREF_TYPE_ATTR, DEREF_TYPE_LIST, listtype_sizeof_item, _obj_cast_codegen
from cre.core import T_ID_VAR, register_global_default
# import inspect



token_fields_dict = {
    "t_id" : u4,
    "length" : u4,
    "value" : unicode_type,
}

class TokenTypeClass(CREObjTypeClass):
    t_id = T_ID_VAR
    type_cache = {}

    

# @lower_cast(VarTypeClass, CREObjType)
# def upcast(context, builder, fromty, toty, val):
#     return _obj_cast_codegen(context, builder, val, fromty, toty,incref=False)



# Manually register the type to avoid automatic getattr overloading 
default_manager.register(VarTypeClass, models.StructRefModel)

VarType = VarTypeClass()
register_global_default("Var", VarType)

# Allow typed Var instances to be upcast to VarType
@lower_cast(VarTypeClass, VarType)
def upcast(context, builder, fromty, toty, val):
    return _obj_cast_codegen(context, builder, val, fromty, toty,incref=False)

class Var(StructRefProxy):
    t_id = T_ID_VAR
    def __new__(cls, typ, alias="", skip_assign_alias=False):
        # if(not isinstance(typ, types.StructRef)): typ = typ.fact_type
        typ = _standardize_type(typ, cre_context())
        # base_type_name = str(typ)
        # print(base_type_name)
                
        base_t_id = cre_context().get_t_id(_type=typ)

        if(getenv("CRE_SPECIALIZE_VAR_TYPE",default=False)):
            raise ValueError("THIS SHOULDN'T HAPPEN")
            typ_ref = types.TypeRef(typ)
            struct_type = VarTypeClass(typ_ref,typ_ref)
            st = var_ctor(struct_type, base_t_id, alias)
        else:
            st = var_ctor_generic(base_t_id, alias)
        
        st._base_type = typ
        st._head_type = typ
        st._derefs_str = ""

        # if(alias):
            # import inspect, ctypes
            # if(alias is not None): 
            #     # Binds this instance globally in the calling python context 
            #     #  so that it is bound to a variable named whatever alias was set to
            #     # print(inspect.stack()[2][0].f_locals)
            #     # Get the calling frame
            #     frame = inspect.stack()[2][0] 
            #     # Assign the Var to it's alias
            #     frame.f_locals[alias] = st
            #     # Update locals()
            #     ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(1))
            # # assign_to_alias_in_parent_frame(st, alias)

        return st
        
   

# Manually define the boxing to avoid constructor overloading
define_boxing(VarTypeClass, Var)
