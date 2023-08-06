#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/21 18:16
Desc: To test intention, just write test code here!
"""
import sys

sys.path.append("../marketwatchdata")
# print(sys.path)

# from marketwatchdata.MarketWatch import *
import marketwatchdata.MarketWatch as mw


def test_ohlc():
    """
    just for test aim
    :return: assert result
    :rtype: assert
    """
    df = mw.ohlc('TMUBMUSD03M', 'P1D', 'P1Y')
    print(df)
    assert df.shape[0] > 0


if __name__ == "__main__":
    test_ohlc()
