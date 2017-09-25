# -*- coding: utf-8 -*-


__all__ = ["VariableTest"]


import unittest

from order import Variable


class VariableTest(unittest.TestCase):

    def make_var(self, name, **kwargs):
        kwargs.setdefault("expression", "myBranchA * myBranchB")
        kwargs.setdefault("selection", "myBranchC > 0")
        kwargs.setdefault("binning", (20, 0., 10.))
        kwargs.setdefault("x_title", "p_{T}")
        kwargs.setdefault("unit", "GeV")
        return Variable(name, **kwargs)

    def test_constructor(self):
        v = self.make_var("constructor_var")
        self.assertEqual(v.name, "constructor_var")
        self.assertEqual(v.expression, "myBranchA * myBranchB")
        self.assertEqual(v.selection, "(myBranchC > 0)")
        self.assertEqual(v.binning, (20, 0., 10.))
        self.assertEqual(v.full_title(), "constructor_var;p_{T} [GeV];Entries / 0.5 GeV")

    def test_parsing(self):
        v = self.make_var("parsing_var")

        v.expression = "foo"
        self.assertEqual(v.expression, "foo")
        with self.assertRaises(TypeError):
            v.expression = 1

        v.selection = "foo"
        self.assertEqual(v.selection, "(foo)")

        v.binning = (10, 0., 1.)
        self.assertEqual(v.binning, (10, 0., 1.))
        with self.assertRaises(TypeError):
            v.binning = {}
        with self.assertRaises(ValueError):
            v.binning = (10, 0.)

        v.x_title = "foo"
        self.assertEqual(v.x_title, "foo")
        with self.assertRaises(TypeError):
            v.x_title = 1

        v.y_title = "foo"
        self.assertEqual(v.y_title, "foo")
        with self.assertRaises(TypeError):
            v.y_title = 1

        v.x_title_short = "bar"
        self.assertEqual(v.x_title_short, "bar")
        with self.assertRaises(TypeError):
            v.x_title_short = 1
        v.x_title_short = None
        self.assertEqual(v.x_title_short, "foo")

        v.y_title_short = "bar"
        self.assertEqual(v.y_title_short, "bar")
        with self.assertRaises(TypeError):
            v.y_title_short = 1
        v.y_title_short = None
        self.assertEqual(v.y_title_short, "foo")

        v.log_x = True
        self.assertTrue(v.log_x)
        with self.assertRaises(TypeError):
            v.log_x = {}

        v.log_y = True
        self.assertTrue(v.log_y)
        with self.assertRaises(TypeError):
            v.log_y = {}

        v.unit = "GeV"
        self.assertEqual(v.unit, "GeV")
        with self.assertRaises(TypeError):
            v.unit = {}
        v.unit = None
        self.assertIsNone(v.unit)

    def test_titles(self):
        v = self.make_var("foo",
            x_title       = "Muon transverse momentum",
            x_title_short = r"$\mu p_{T}$",
            y_title       = "Entries",
            y_title_short = "N",
            binning = (40, 0., 10.),
        )

        self.assertEqual(v.full_x_title(), "Muon transverse momentum [GeV]")
        self.assertEqual(v.full_x_title(short=True), "$\\mu p_{T}$ [GeV]")
        self.assertEqual(v.full_x_title(short=True, root=True), "#mu p_{T} [GeV]")
        self.assertEqual(v.full_y_title(), "Entries / 0.25 GeV")
        self.assertEqual(v.full_y_title(bin_width=0.2), "Entries / 0.2 GeV")
        self.assertEqual(v.full_y_title(short=True), "N / 0.25 GeV")
        self.assertEqual(v.full_title(), "foo;Muon transverse momentum [GeV];Entries / 0.25 GeV")
        self.assertEqual(v.full_title(short=True), "foo;#mu p_{T} [GeV];N / 0.25 GeV")

    def test_copy(self):
        v = self.make_var("copy_var").copy(name="otherVar", expression="otherExpression")

        self.assertEqual(v.name, "otherVar")
        self.assertEqual(v.expression, "otherExpression")
        self.assertEqual(v.selection, "(myBranchC > 0)")
