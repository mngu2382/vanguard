#! /usr/bin/env python3

import argparse
import datetime
import os.path

from getVanguardPrices import getVanguardPrices

funds = {
    "1"  : "Vanguard\u00ae; Index Australian Shares Fund",
    "2"  : "Vanguard\u00ae; LifeStrategy&reg; Conservative Fund",
    "3"  : "Vanguard\u00ae; Investor Cash Plus Fund",
    "4"  : "Vanguard\u00ae; Index Diversified Bond Fund",
    "5"  : "Vanguard\u00ae; LifeStrategy&reg; Growth Fund",
    "6"  : "Vanguard\u00ae; LifeStrategy&reg; High Growth Fund",
    "7"  : "Vanguard\u00ae; Index Hedged International Shares Fund",
    "8"  : "Vanguard\u00ae; Index International Shares Fund",
    "9"  : "Vanguard\u00ae; Index Australian Property Securities Fund",
    "29" : "Vanguard\u00ae; High Yield Australian Shares Fund",
    "28" : "Vanguard\u00ae; LifeStrategy&reg; Balanced Fund"
}

def updateVanguardPrices(fundId):
    fname = "./fundData/fund{:02d}.csv".format(fundId)

    if os.path.isfile(fname):
        with open(fname, "r") as fin:
            for line in fin: pass
        lastDate = datetime.datetime.strptime(line.split(",", 1)[0], "%Y-%m-%d")
        if lastDate.date() < datetime.date.today():
            startDate = lastDate + datetime.timedelta(days=1)
            try:
                Date, Purchase, NAV, Withdrawal = \
                    getVanguardPrices(fundId, startDate, None)
                with open(fname, "a") as out:
                    for i in zip(Date, Purchase, NAV, Withdrawal):
                        out.write(",".join(i) + "\n")
            except:
                pass
    else:
        startDate = datetime.datetime.strptime("2013-01-01", "%Y-%m-%d")
        Date, Purchase, NAV, Withdrawal = \
            getVanguardPrices(fundId, startDate , None)
        with open(fname, "w") as out:
            out.write("Date,Purchase,NAV,Withdrawal")
            for i in zip(Date, Purchase, NAV, Withdrawal):
                out.write(",".join(i) + "\n")

for key, val in funds.items():
    updateVanguardPrices(int(key))
    print("Updated {} (fund{:02d}.csv)".format(val, int(key)))
