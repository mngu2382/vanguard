Scraping and plotting Vanguard fund prices. To checkout the figures,
in `./figures`, run in terminal:

    python -m http.server 8000

and check `http://localhost:8000` in your favourite web browser.

## ./fundInfo.txt
A dictionary of fundID and corresponding fund name

## ./getVanguardPrices.py
Defines a function which retrieves a fund's price history from 
https://www.vanguardinvestments.com.au/retail/ret/investments/price-history-rtl.jsp

    getVanguardPrices(fundId, startDate, endDate)

## ./VanguardPrices.py
A command-line utility for ./getVanguardPrices

    ./VanguardPrices.py --help

## ./updateVanguardPrices.py
A script to update prices in ./fundData

## ./mergeNAV.py
A script to merge separate funds csv into a single file

## ./fundData/
Data files

## ./figures/
Figures using [D3.js](www.d3js.org).


