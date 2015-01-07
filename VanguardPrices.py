#! /usr/bin/env python3

# TODO: add argument for verbose switch

import argparse
import datetime
import re
import textwrap

from getVanguardPrices import getVanguardPrices

notDigit = re.compile("[^0-9]")

def strToDate(s):
    try:
        s1 = notDigit.sub("", s)
        d = datetime.datetime.strptime(s1, "%Y%m%d")
    except:
        msg = "{} is not a vaild date".format(s)
        raise argparse.ArgumentTypeError(msg)
    return d

def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
                Retrives the historical prices of Vanguard funds from
                https://www.vanguardinvestments.com.au/retail/ret/investments/price-history-rtl.jsp
    
                If no arguments supplied, returns prices for the past month
                of 'Vanguard Index Australian Shares Fund' (fundId=1).
                '''))
    parser.add_argument("-f", "--fundId", default="1", metavar="fundId",
            choices=[str(j) for j in [i for i in range(9)] + [28, 29]])
    parser.add_argument("-s", "--startDate", type=strToDate, metavar="yyyy-mm-dd")
    parser.add_argument("-e", "--endDate", type=strToDate, metavar="yyyy-mm-dd")
    args = parser.parse_args()
    
    if args.endDate:
        if args.startDate:
            if args.endDate < args.startDate:
                msg = "End date not after start date"
                raise argparse.ArgumentTypeError(msg)
        else:
            msg = "Start date needed"
            raise argparse.ArgumentTypeError(msg)
    
    Date, Purchase, NAV, Withdrawal = \
        getVanguardPrices(args.fundId, args.startDate, args.endDate)
    
    print("Date,Purchase,NAV,Withdrawal")
    for i in zip(Date, Purchase, NAV, Withdrawal):
        print(",".join(i))

if __name__ == "__main__":
    main()
