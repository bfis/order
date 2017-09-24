# -*- coding: utf-8 -*-

"""
Mixin classes providing common functionality.
"""


__all__ = ["CopyMixin", "AuxDataMixin", "TagMixin", "DataSourceMixin", "SelectionMixin",
           "LabelMixin"]


import copy
import collections

import six

from .util import typed, make_list, multi_match, join_root_selection, join_numexpr_selection, \
    to_root_latex


class CopyMixin(object):
    """
    Mixin-class that adds copy features to inheriting classes.

    .. code-block:: python

        class MyClass(CopyMixin):

            copy_attrs = ["name"]

            def __init__(self, name):
                super(MyClass, self).__init__()
                self.name = name

        a = MyClass("foo")
        a.name
        # -> "foo"

        b = a.copy()
        b.name
        # -> "foo"

        def update_name(inst, kwargs):
            kwargs["name"] += "_updated"

        c = a.copy(callbacks=[update_name])
        c.name
        # -> "foo_updated"

    .. :py:attribute:: copy_attrs
       type: list
       classmember

       The default attributes to copy when *attrs* is *None* in the copy method.

    .. :py:attribute:: copy_callbacks
       type: list
       classmember

       The default callbacks to call when *callbacks* is *None* in the copy method.
    """

    copy_attrs = []
    copy_callbacks = []

    def __init__(self): pass

    def copy(self, cls=None, attrs=None, callbacks=None, **kwargs):
        """
        Returns a copy of this instance via copying attributes defined in *attrs* which default to
        *copy_attrs*. *kwargs* overwrite copied attributes. *cls* is the class of the returned
        instance . When *None*, *this* class is used. *callbacks* can be a list of functions that
        receive the instance to copy and the attributes in a dict, so they can be updated *before*
        the actual copy is created.
        """
        # default args
        if cls is None:
            cls = self.__class__
        if attrs is None:
            attrs = self.copy_attrs
        if callbacks is None:
            callbacks = self.copy_callbacks

        # copy attributes
        for attr in attrs:
            if attr not in kwargs:
                kwargs[attr] = copy.deepcopy(getattr(self, attr))

        # invoke callbacks
        for callback in callbacks:
            if callable(callback):
                callback(self, kwargs)
            elif isinstance(callback, six.string_types):
                getattr(self, str(callback))(self, kwargs)
            else:
                raise TypeError("invalid callback type: %s" % callback)

        return cls(**kwargs)


class AuxDataMixin(object):
    """
    Mixin-class that provides storage of auxiliary data via a simple interface:

    .. code-block:: python

        class MyClass(AuxDataMixin):
            ...

        c = MyClass()
        c.set_aux("foo", "bar")

        c.aux("foo")
        # -> "bar"

    .. :py:attribute:: aux
       type: OrderedDict

       The dictionary of auxiliary data.
    """

    _no_default = object()

    def __init__(self, aux=None):
        super(AuxDataMixin, self).__init__()

        # instance members
        self._aux = collections.OrderedDict()

        # set initial values
        if aux is not None:
            for key, data in dict(aux).items():
                self.set_aux(key, data)

    @typed
    def aux(self, aux):
        # aux parser
        try:
            aux = collections.OrderedDict(aux)
        except:
            raise TypeError("invalid aux type: %s" % aux)

        return aux

    def set_aux(self, key, data):
        """
        Stores auxiliary *data* for a specific *key*. Returns *data*.
        """
        self.aux[key] = data
        return data

    def remove_aux(self, key=None):
        """
        Removes the auxiliary data for a specific *key*, or all data if *key* is *None*.
        """
        if key is None:
            self.aux.clear()
        elif key in self.aux:
            del(self.aux[key])

    def has_aux(self, key):
        """
        Returns *True* when an auxiliary data entry for a specific *key* exists, *False* otherwise.
        """
        return key in self.aux

    def get_aux(self, key, default=_no_default):
        """ get_aux(key, [default])
        Returns the auxiliary data for a specific *key*. If a *default* is given, it is returned in
        case *key* is not found.
        """
        if default != self._no_default:
            return self.aux.get(key, default)
        else:
            return self.aux[key]


class TagMixin(object):
    """
    Mixin-class that allows inheriting objects to be tagged.

    .. code-block:: python

        class MyClass(TagMixin):
            ...

        c = MyClass()
        c.tags = {"foo", "bar"}

        c.has_tag("foo")
        # -> True

        c.has_tag("f*")
        # -> True

        c.has_tag(("foo", "baz"))
        # -> True

        c.has_tag(("foo", "baz"), mode=all)
        # -> False

        c.has_tag(("foo", "bar"), mode=all)
        # -> True

    .. py:attribute:: tags
       type: set

       The set of string tags of this object.
    """

    def __init__(self, tags=None):
        super(TagMixin, self).__init__()

        # instance members
        self._tags = set()

        # set initial tags
        if tags is not None:
            self.tags = tags

    @typed
    def tags(self, tags):
        # tags parser
        if isinstance(tags, six.string_types):
            tags = {tags}
        if not isinstance(tags, (set, list, tuple)):
            raise TypeError("invalid tags type: %s" % tags)

        _tags = set()
        for tag in tags:
            if not isinstance(tag, six.string_types):
                raise TypeError("invalid tag type: %s" % tag)
            _tags.add(str(tag))

        return _tags

    def add_tag(self, tag):
        """
        Adds a new *tag* to the object.
        """
        self._tags.update(self.__class__.tags.fparse(self, tag))

    def remove_tag(self, tag):
        """
        Removes a previously added *tag*.
        """
        self._tags.difference_update(self.__class__.tags.fparse(self, tag))

    def has_tag(self, tag, mode=any, **kwargs):
        """ has_tag(tag, mode=any, **kwargs)
        Returns *True* when this object is tagged with *tag*, *False* otherwise. When *tag* is a
        sequence of tags, the behavior is defined by *mode*. When *any*, the object is considered
        *tagged* when at least one of the provided tags matches. When *all*, all provided tags have
        to match. Each *tag* can be a *fnmatch* or *re* pattern. All *kwargs* are passed to
        :py:func:`util.multi_match`.
        """
        match = lambda tag: any(multi_match(t, [tag], mode=any, **kwargs) for t in self.tags)
        return mode(match(tag) for tag in make_list(tag))


class DataSourceMixin(object):
    """
    Mixin-class that provides convenience attributes for distinguishing between MC and data.

    .. code-block:: python

        class MyClass(DataSourceMixin):
            ...

        c = MyClass()

        c.is_data
        # -> False

        c.data_source
        # -> "mc"

        c.is_data = True
        c.data_source
        # -> "data"

    .. py:attribute:: is_data
       type: boolean

       *True* if this object contains information on real data.

    .. py:attribute:: is_mc
       type: boolean

       *True* if this object contains information on MC data.

    .. py:attribute:: data_source
       type: string

       Either ``"data"`` or ``"mc"``, depending on the source of contained data.
    """

    def __init__(self, is_data=False):
        super(DataSourceMixin, self).__init__()

        # instance members
        self._is_data = None

        # set the initial is_data value
        self.is_data = is_data

    @property
    def is_data(self):
        return self._is_data

    @is_data.setter
    def is_data(self, is_data):
        if not isinstance(is_data, bool):
            raise TypeError("invalid is_data type: %s" % is_data)

        self._is_data = is_data

    @property
    def is_mc(self):
        return not self.is_data

    @is_mc.setter
    def is_mc(self, is_mc):
        if not isinstance(is_mc, bool):
            raise TypeError("invalid is_mc type: %s" % is_mc)

        self._is_data = not is_mc

    @property
    def data_source(self):
        return "data" if self.is_data else "mc"


class SelectionMixin(object):
    """
    Mixin-class that adds attibutes and methods to describe a selection rule.

    .. code-block:: python

        class MyClass(SelectionMixin):
            ...

        c = MyClass(selection="branchA > 0")

        c.add_selection("myBranchB < 100", bracket=True)
        c.selection
        # -> "((myBranchA > 0) && (myBranchB < 100))"

        c.add_selection("myWeight", op="*")
        c.selection
        # -> "((myBranchA > 0) && (myBranchB < 100)) * (myWeight)"

        c = MyClass(selection="branchA > 0", selection_mode="numexpr")

        c.add_selection("myBranchB < 100")
        c.selection
        # -> "(myBranchA > 0) & (myBranchB < 100)"

    .. py:attribute:: default_selection_mode
       type: string
       classmember

       The default *selection_mode* when none is given in the instance constructor.

    .. py:attribute:: selection_mode
       type: string

       The selection mode. Should either be ``"root"`` or ``"numexpr"``.
    """

    MODE_ROOT = "root"
    MODE_NUMEXPR = "numexpr"

    default_selection_mode = MODE_ROOT

    def __init__(self, selection=None, selection_mode=None):
        super(SelectionMixin, self).__init__()

        # instance members
        self._selection = "1"
        self._selection_mode = None

        # fallback to default selection mode
        if selection_mode is None:
            selection_mode = self.default_selection_mode

        # set initial values
        if selection is not None:
            self.selection = selection
        if selection_mode is not None:
            self.selection_mode = selection_mode

    @typed
    def selection(self, selection):
        # selection parser
        if self.selection_mode == self.MODE_ROOT:
            join = join_root_selection
        else:
            join = join_numexpr_selection

        try:
            selection = join(selection)
        except:
            raise TypeError("invalid selection type: %s" % selection)

        return selection

    def add_selection(self, selection, **kwargs):
        """
        Adds a *selection* string to the overall selection. The new string will be logically
        connected via *AND*. All *kwargs* are forwarded to :py:func:`util.join_root_selection` or
        :py:func:`util.join_numexpr_selection`.
        """
        if self.selection_mode == self.MODE_ROOT:
            join = join_root_selection
        else:
            join = join_numexpr_selection

        self.selection = join(self.selection, selection, **kwargs)

    @typed
    def selection_mode(self, selection_mode):
        # selection mode parser
        if not isinstance(selection_mode, six.string_types):
            raise TypeError("invalid selection_mode type: %s" % selection_mode)

        selection_mode = str(selection_mode)
        if selection_mode not in (self.MODE_ROOT, self.MODE_NUMEXPR):
            raise ValueError("unknown selection_mode: %s" % selection_mode)

        return selection_mode


class LabelMixin(object):
    """
    Mixin-class that provides a label, a short version of that label, and some convenience
    attributes.

    .. code-block:: python

        l = LabelMixin(label="Muon", label_short=r"$\mu$")

        l.label
        # -> "Muon"

        l.label_short_root
        # -> "#mu"

        l.label_short = None
        l.label_short_root
        # -> "Muon"

    .. py:attribute:: label
       type: string

       The label. When this object has a *name* (configurable via *_label_fallback_attr*) attribute,
       the label defaults to that value.

    .. py:attribute:: label_root
       type: string
       read-only

       The label, converted to *proper* ROOT latex.

    .. py:attribute:: label_short
       type: string

       A short label, defaults to the normal label.

    .. py:attribute:: label_short_root
       type: string
       read-only

       Short version of the label, converted to *proper* ROOT latex.
    """

    def __init__(self, label=None, label_short=None):
        super(LabelMixin, self).__init__()

        # register empty attributes
        self._label = None
        self._label_short = None

        # set initial values
        if label is not None:
            self.label = label
        if label_short is not None:
            self.label_short = label_short

        # attribute to query for fallback label
        self._label_fallback_attr = "name"

    @property
    def label(self):
        # label getter
        if self._label is not None or self._label_fallback_attr is None:
            return self._label
        else:
            return getattr(self, self._label_fallback_attr, None)

    @label.setter
    def label(self, label):
        # label setter
        if label is None:
            self._label = None
        elif not isinstance(label, six.string_types):
            raise TypeError("invalid label type: %s" % label)
        else:
            self._label = str(label)

    @property
    def label_root(self):
        # label_root getter
        return to_root_latex(self.label)

    @property
    def label_short(self):
        # label_short getter
        return self.label if self._label_short is None else self._label_short

    @label_short.setter
    def label_short(self, label_short):
        # label_short setter
        if label_short is None:
            self._label_short = None
        elif isinstance(label_short, six.string_types):
            self._label_short = str(label_short)
        else:
            raise TypeError("invalid label_short type: %s" % label_short)

    @property
    def label_short_root(self):
        # label_short_root getter
        return to_root_latex(self.label_short)
