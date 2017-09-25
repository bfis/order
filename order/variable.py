# -*- coding: utf-8 -*-

"""
Tools to work with variables.
"""


__all__ = ["Variable"]


import six

from .unique import UniqueObject
from .mixins import CopyMixin, AuxDataMixin, TagMixin, SelectionMixin
from .util import typed, to_root_latex


class Variable(UniqueObject, CopyMixin, AuxDataMixin, TagMixin, SelectionMixin):
    """
    Class that provides simplified access to plotting variables.

    *expression* and *selection* can be used for projection statements. When empty, *expression*
    defaults to *name*. Other options that are relevant for plotting are *binning*, *x_title*,
    *x_title_short*, *y_title*, *y_title_short*, and *unit*. *selection* and *selection_mode* are
    passed to the :py:class:`SelectionMixin`, *tags* to the :py:class:`TagMixin`, *aux* to the
    :py:class:`AuxDataMixin`, and *name*, *id* (defaulting to an auto id) and *context* to the
    :py:class:`UniqueObject` constructor.

    .. code-block:: python

        v = Variable("myVar",
            expression = "myBranchA * myBranchB",
            selection = "myBranchC > 0",
            binning   = (20, 0., 10.),
            x_title   = r"$\mu p_{T}$",
            unit      = "GeV"
        )

        v.x_title_root
        # -> "#mu p_{T}"

        v.full_title()
        # -> "myVar;$\mu p_{T}$" [GeV];Entries / 0.5 GeV'"

    .. py:attribute:: expression
       type: string, None

       The expression of this variable. Defaults to name if *None*.

    .. py:attribute:: binning
       type: tuple

       Number of bins, minimum bin and maximum bin.

    .. py:attribute:: x_title
       type: string

       The title of the x-axis.

    .. py:attribute:: x_title_root
       type: string
       read-only

       The title of the x-axis, converted to *proper* ROOT latex.

    .. py:attribute:: x_title_short
       type: string

       Short version for the title of the x-axis. Defaults to *x_title* when not explicitely set.

    .. py:attribute:: x_title_short_root
       type: string
       read-only

       The short version of the title of the x-axis, converted to *proper* ROOT latex.

    .. py:attribute:: y_title
       type: string

       The title of the y-axis.

    .. py:attribute:: y_title_root
       type: string
       read-only

       The title of the y-axis, converted to *proper* ROOT latex.

    .. py:attribute:: y_title_short
       type: string

       Short version for the title of the y-axis. Defaults to *y_title* when not explicitely set.

    .. py:attribute:: y_title_short_root
       type: string
       read-only

       The short version of the title of the y-axis, converted to *proper* ROOT latex.

    .. py:attribute:: unit
       type: string, None

       The unit to be shown on both, x- and y-axis. When *None*, no unit is shown.

    .. py:attribute:: log_x
       type: boolean

       Whether or not the x-axis should be drawn logarithmically.

    .. py:attribute:: log_y
       type: boolean

       Whether or not the y-axis should be drawn logarithmically.

    .. py:attribute:: bin_width
       type: float
       read-only

       The bin width, evaluated from *binning*.
    """

    copy_attrs = ["expression", "binning", "x_title", "x_title_short", "y_title", "y_title_short",
                  "log_x", "log_y", "unit", "selection", "selection_mode", "tags", "aux"]

    def __init__(self, name, id="+", expression=None, binning=(1, 0., 1.), x_title="",
                 x_title_short=None, y_title="Entries", y_title_short=None, log_x=False,
                 log_y=False, unit="1", selection=None, selection_mode=None, tags=None, aux=None,
                 context=None):
        UniqueObject.__init__(self, name, id, context=context)
        AuxDataMixin.__init__(self, aux=aux)
        TagMixin.__init__(self, tags=tags)
        SelectionMixin.__init__(self, selection=selection, selection_mode=selection_mode)

        # instance members
        self._expression = None
        self._binning = None
        self._x_title = None
        self._x_title_short = None
        self._y_title = None
        self._y_title_short = None
        self._log_x = None
        self._log_y = None
        self._unit = None

        # set initial values
        self._expression = expression
        self._binning = binning
        self._x_title = x_title
        self._x_title_short = x_title_short
        self._y_title = y_title
        self._y_title_short = y_title_short
        self._log_x = log_x
        self._log_y = log_y
        self._unit = unit

    @property
    def expression(self):
        # expression getter
        if self._expression is None:
            return self.name
        else:
            return self._expression

    @expression.setter
    def expression(self, expression):
        # expression setter
        if expression is None:
            # reset on None
            self._expression = None
            return

        if not isinstance(expression, six.string_types):
            raise TypeError("invalid expression type: %s" % (expression,))
        elif not expression:
            raise ValueError("expression must not be empty")

        self._expression = str(expression)

    @typed
    def binning(self, binning):
        # binning parser
        if not isinstance(binning, (list, tuple)):
            raise TypeError("invalid binning type: %s" % (binning,))
        elif len(binning) != 3:
            raise ValueError("binning must have length 3: %s" % (binning,))

        return tuple(binning)

    @typed
    def x_title(self, x_title):
        # x_title parser
        if not isinstance(x_title, six.string_types):
            raise TypeError("invalid x_title type: %s" % (x_title,))

        return str(x_title)

    @property
    def x_title_root(self):
        # x_title_root getter
        return to_root_latex(self.x_title)

    @property
    def x_title_short(self):
        # x_title_short getter
        return self.x_title if self._x_title_short is None else self._x_title_short

    @x_title_short.setter
    def x_title_short(self, x_title_short):
        # x_title_short setter
        if x_title_short is None:
            self._x_title_short = None
        elif isinstance(x_title_short, six.string_types):
            self._x_title_short = str(x_title_short)
        else:
            raise TypeError("invalid x_title_short type: %s" % (x_title_short,))

    @property
    def x_title_short_root(self):
        # x_title_short_root getter
        return to_root_latex(self.x_title_short)

    @typed
    def y_title(self, y_title):
        # y_title parser
        if not isinstance(y_title, six.string_types):
            raise TypeError("invalid y_title type: %s" % (y_title,))

        return str(y_title)

    @property
    def y_title_root(self):
        # y_title_root getter
        return to_root_latex(self.y_title)

    @property
    def y_title_short(self):
        # y_title_short getter
        return self.y_title if self._y_title_short is None else self._y_title_short

    @y_title_short.setter
    def y_title_short(self, y_title_short):
        # y_title_short setter
        if y_title_short is None:
            self._y_title_short = None
        elif isinstance(y_title_short, six.string_types):
            self._y_title_short = str(y_title_short)
        else:
            raise TypeError("invalid y_title_short type: %s" % (y_title_short,))

    @property
    def y_title_short_root(self):
        # y_title_short_root getter
        return to_root_latex(self.y_title_short)

    @typed
    def log_x(self, log_x):
        # log_x parser
        if not isinstance(log_x, bool):
            raise TypeError("invalid log_x type: %s" % (log_x,))

        return log_x

    @typed
    def log_y(self, log_y):
        # log_y parser
        if not isinstance(log_y, bool):
            raise TypeError("invalid log_y type: %s" % (log_y,))

        return log_y

    @typed
    def unit(self, unit):
        if unit is None:
            return None
        elif isinstance(unit, six.string_types):
            return str(unit)
        else:
            raise TypeError("invalid unit type: %s" % (unit,))

    @property
    def bin_width(self):
        return (self.binning[2] - self.binning[1]) / float(self.binning[0])

    def full_x_title(self, short=False, root=False):
        """
        Returns the full title (i.e. with unit string) of the x-axis. When *short* is *True*, the
        short version is returned. When *root* is *True*, the title is converted to *proper* ROOT
        latex.
        """
        title = self.x_title_short if short else self.x_title

        if self.unit not in (None, "1"):
            title += " [%s]" % self.unit

        return to_root_latex(title) if root else title

    def full_y_title(self, bin_width=None, short=False, root=False):
        """
        Returns the full title (i.e. with bin width and unit string) of the y-axis. When not *None*,
        the value *bin_width* instead of the one evaluated from *binning*. When *short* is *True*,
        the short version is returned. When *root* is *True*, the title is converted to *proper*
        ROOT latex.
        """
        title = self.y_title_short if short else self.y_title

        if bin_width is None:
            bin_width = round(self.bin_width, 2)
        title += " / %s" % bin_width

        if self.unit not in (None, "1"):
            title += " %s" % self.unit

        return to_root_latex(title) if root else title

    def full_title(self, name=None, short=False, short_x=None, short_y=None, root=True,
                   bin_width=None):
        """
        Returns the full combined title that is compliant with ROOT's TH1 classes. *short_x*
        (*short_y*) is passed to :py:meth:`full_x_title` (:py:meth:`full_y_title`). Both values
        fallback to *short* when *None*. *bin_width* is forwarded to :py:meth:`full_y_title`. When
        *root* is *False*, the axis titles are not converted to *proper* ROOT latex.
        """
        if name is None:
            name = self.name
        if short_x is None:
            short_x = short
        if short_y is None:
            short_y = short

        x_title = self.full_x_title(short=short_x, root=root)
        y_title = self.full_y_title(bin_width=bin_width, short=short_y, root=root)

        return ";".join([name, x_title, y_title])
