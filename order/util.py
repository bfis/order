# -*- coding: utf-8 -*-

"""
Helpful utilities.
"""


__all__ = ["typed", "make_list", "multi_match"]


import functools
import types
import re
import fnmatch


class typed(property):
    """
    Shorthand for the most common property definition. Can be used as a decorator to wrap around
    a single function. Example:

    .. code-block:: python

         class MyClass(object):

            def __init__(self):
                self._foo = None

            @typed
            def foo(self, foo):
                if not isinstance(foo, str):
                    raise TypeError("not a string: '%s'" % foo)
                return foo

        myInstance = MyClass()
        myInstance.foo = 123   -> TypeError
        myInstance.foo = "bar" -> ok
        print(myInstance.foo)  -> prints "bar"

    In the exampe above, set/get calls target the instance member ``_foo``, i.e. "_<function_name>".
    The member name can be configured by setting *name*. If *setter* (*deleter*) is *True* (the
    default), a setter (deleter) method is booked as well. Prior to updating the member when the
    setter is called, *fparse* is invoked which may implement sanity checks.
    """

    def __init__(self, fparse=None, setter=True, deleter=True, name=None):
        self._flags = (setter, deleter)

        # only register the property if fparse is set
        if fparse is not None:
            self.fparse = fparse

            # build the default name
            if name is None:
                name = "_" + fparse.__name__

            # call the super constructor with generated methods
            property.__init__(self,
                functools.wraps(fparse)(self._fget(name)),
                self._fset(name) if setter else None,
                self._fdel(name) if deleter else None
            )

    def __call__(self, fparse):
        return self.__class__(fparse, *self._flags)

    def _fget(self, name):
        """
        Build and returns the property's *fget* method for the member defined by *name*.
        """
        def fget(inst):
            return getattr(inst, name)
        return fget

    def _fset(self, name):
        """
        Build and returns the property's *fdel* method for the member defined by *name*.
        """
        def fset(inst, value):
            # the setter uses the wrapped function as well
            # to allow for value checks
            value = self.fparse(inst, value)
            setattr(inst, name, value)
        return fset

    def _fdel(self, name):
        """
        Build and returns the property's *fdel* method for the member defined by *name*.
        """
        def fdel(inst):
            delattr(inst, name)
        return fdel


def make_list(obj, cast=True):
    """
    Converts an object *obj* to a list and returns it. Objects of types *tuple* and *set* are
    converted if *cast* is *True*. Otherwise, and for all other types, *obj* is put in a new list.
    """
    if isinstance(obj, list):
        return list(obj)
    if isinstance(obj, types.GeneratorType):
        return list(obj)
    if isinstance(obj, (tuple, set)) and cast:
        return list(obj)
    else:
        return [obj]


def multi_match(name, patterns, mode=any, func="fnmatch", *args, **kwargs):
    """
    Compares *name* to multiple *patterns* and returns *True* in case of at least one match (*mode*
    = *any*, the default), or in case all patterns matched (*mode* = *all*). Otherwise, *False* is
    returned. *func* determines the matching function and accepts ``"fnmatch"``, ``"fnmatchcase"``,
    and ``"re"``. All *args* and *kwargs* are passed to the actual matching function.
    """
    if func == "re":
        return mode(re.match(pattern, name, *args, **kwargs) for pattern in patterns)
    elif func in ("fnmatch", "fnmatchcase"):
        _func = getattr(fnmatch, func)
        return mode(_func(name, pattern, *args, **kwargs) for pattern in patterns)
    else:
        raise ValueError("unknown matching function: %s" % func)