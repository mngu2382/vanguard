import datetime
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class _fundPriceHistHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_fundPriceHistTab = False
        self.in_fundPriceHistBody = False
        self.raw_data = []

    def handle_starttag(self, tag, attrs):
        if self.in_fundPriceHistTab:
            if tag == "tbody":
                self.in_fundPriceHistBody = True
        elif ("id", "fundPriceHist") in attrs:
            self.in_fundPriceHistTab = True

    def handle_endtag(self, tag):
        if self.in_fundPriceHistBody and tag == "tbody":
            self.in_fundPriceHistBody = False
        elif self.in_fundPriceHistTab and tag == "table":
            self.in_fundPriceHistTab = False
    
    def handle_data(self, data):
        if self.in_fundPriceHistBody and data.strip():
            self.raw_data.append(data.strip())

def getVanguardPrices(fundId, startDate, endDate):
    """
    Retreives fund prices from Vanguard website.

    Parameters:
    fundId: int or string representation of int
        Vanguard fund ID. Should one of 1,..9, 28, 29
    startDate, endDate: datetime.date or datetime.datetime objects

    Returns:
    Four lists of strings, all of the same length: date, purchase
    price, net asset value, withdrawal price.
    """

    url = "https://www.vanguardinvestments.com.au/retail/ret/investments/price-history-rtl.jsp"
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0"
    header = { 'User-Agent' : user_agent }

    url_values = {}
    url_values["fundId"] = fundId
    if startDate:
        url_values["startDate1"] = "{:02d}".format(startDate.day)
        url_values["startMonth1"] = "{:02d}".format(startDate.month)
        url_values["startYear1"] = "{}".format(startDate.year)
    if endDate:
        url_values["endDate1"] = "{:02d}".format(endDate.day)
        url_values["endMonth1"] = "{:02d}".format(endDate.month)
        url_values["endYear1"] = "{}".format(endDate.year)
    url_values = urllib.parse.urlencode(url_values)
    url_values = url_values.encode("utf-8")

    req = urllib.request.Request(url, url_values, header)
    response = urllib.request.urlopen(req)
    page = response.read()
    page = page.decode()

    parserHTML = _fundPriceHistHTMLParser()
    parserHTML.feed(page)

    if len(parserHTML.raw_data) > 3: # at least one row of data
        raw_data = parserHTML.raw_data[::-1]
        Withdrawal, NAV, Purchase, Date = map(lambda i: raw_data[i::4], range(4))
        Date = [datetime.datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d")
                for d in Date]
    else:
        raise Exception(print(parserHTML.raw_data))

    return Date, Purchase, NAV, Withdrawal
