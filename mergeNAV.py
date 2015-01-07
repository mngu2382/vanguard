import os
import os.path
import pandas as pd

NAV = None
for fund_filename in os.listdir("./fundData/"):
    if fund_filename.startswith("fund"):
        fundID = fund_filename[:6]
        dat = pd.read_csv(os.path.join("fundData", fund_filename))
        dat.rename(columns={"NAV": fundID}, inplace=True)
        if NAV is None:
            NAV = dat[["Date", fundID]]
        else:
            NAV = NAV.merge(dat[["Date", fundID]], how="outer", copy=False)
NAV.to_csv("./fundData/NAV.csv", index=False, na_rep="NA")

