# -*-coding:utf-8-*-
# Project:  Lihang
# Filename: unit_test
# Date: 8/16/18
# Author: 😏 <smirk dot cao at gmail dot com>
import unittest
import pandas as pd
import nb


class TestnbMethods(unittest.TestCase):

    def test_e41(self):
        data = pd.read_csv("./Input/data_4_1.txt", header=None, sep=",")
        x = data[data.columns[0:2]]
        y = data[data.columns[2]]
        clf = nb.NB(1)
        clf.fit(x, y)
        rst = clf.predict([2, "S"])
        self.assertEqual(rst, -1)

    def _test_e42(self):
        data = pd.read_csv("./Input/data_4_1.txt", header=None, sep=",")
        x = data[data.columns[0:2]].values
        y = data[data.columns[2]].values
        clf = nb.NB(1)
        clf.fit(x, y)
        rst = clf.predict([2, "S"])
        self.assertEqual(rst, -1)


if __name__ == '__main__':
    unittest.main()