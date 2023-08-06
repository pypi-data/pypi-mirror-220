#!/usr/bin/env python3
# encoding: utf-8
#
# +--------------------------------------------------------------------------+
# | Endian Firewall                                                          |
# +--------------------------------------------------------------------------+
# | Copyright (c) 2004-2023 Endian SRL <info@endian.com>                     |
# |         Endian SRL                                                       |
# |         via Ipazia 2                                                     |
# |         39100 Bolzano (BZ)                                               |
# |         Italy                                                            |
# |                                                                          |
# | This program is free software; you can redistribute it and/or modify     |
# | it under the terms of the GNU General Public License as published by     |
# | the Free Software Foundation; either version 2 of the License, or        |
# | (at your option) any later version.                                      |
# |                                                                          |
# | This program is distributed in the hope that it will be useful,          |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of           |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |
# | GNU General Public License for more details.                             |
# |                                                                          |
# | You should have received a copy of the GNU General Public License along  |
# | with this program; if not, write to the Free Software Foundation, Inc.,  |
# | 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              |
# +--------------------------------------------------------------------------+


from typing import Union


NoneType = type(None)


class StrictObject:
    """
    A base class for validating simple subclass instances according to their class attributes' type annotations.

    Works with all built-in types, and with special types `List`, `Union`, `Optional`.

    Examples:

    1. Simple validation
        ```
        from eos.validators.object import StrictObject

        class A(StrictObject):
            num: int
        
        A(num=0)  # ok
        A(num=42)  # ok
        A(num="not an int")  # will throw a TypeError
        ```
    2. Custom validation
        ```
        from eos.validators.object import StrictObject

        class B(StrictObject):
            fortytwo: Union[int|str]
            # custom validators must by named by "validate_" followed by
            # the class attribute name, and they should return a bool
            def validate_fortytwo(self, val) -> bool:
                return int(val) == 42
        
        B(num=42)  # ok
        B(num="42")  # ok
        B(num=123)  # will throw a TypeError
        ```
    """
    def __init__(self, **kwargs) -> None:
        # validate all kwargs mapping them to class attributes with equal name
        for k,v in kwargs.items():
            # in all cases: the declared type must match
            _type = self.__class__.__annotations__[k]
            if self.__class__._validate_type(v, _type) is False:
                raise TypeError(f"{self.__class__.__name__}.{k} must be of type {_type} and {v} is not an allowed value")

            # special case: a custom validator function is defined
            validator = getattr(self, f"validate_{k}", None)
            if callable(validator):
                if validator(v) is False:
                    raise TypeError(f"{self.__class__.__name__}.{k} has value {v} and does not satisfy custom validation rules")

            setattr(self, k, v)

        # make sure that all non-Optional class attributes have been defined
        for name, _type in self.__class__.__annotations__.items():
            if (getattr(self, name, None) is None):
                if (
                    hasattr(_type, "__origin__") and
                    NoneType in _type.__args__
                ):
                    pass
                else:
                    raise TypeError(f"{self.__class__.__name__}.{k} must be of type {_type} and {v} is not an allowed value")

    @classmethod
    def _validate_type(cls, element, _type) -> bool:
        if hasattr(_type, "__origin__"):
            # type is Union or Optional (a special case of Union)
            if _type.__origin__ is Union:
                # validate an Optional attribute which is None
                if NoneType in _type.__args__ and element is None:
                    return True
                
                # validate a normal Union types
                return any(
                    cls._validate_type(element, t) 
                    for t in _type.__args__
                )
            # type List
            elif _type.__origin__ is list:
                # an empty list is a valid list of any types
                if len(element) == 0:
                    return True
                # if all list items can be validated with any type, the list is valid
                return any(
                    cls._validate_type(
                        i,
                        Union[_type.__args__] # type: ignore
                    )
                    for i in element
                )
            else:
                raise RuntimeError(f"Trying to validate an unknown type: {_type}")
        else:
            return _type is type(element)
