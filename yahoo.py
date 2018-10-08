from bs4 import BeautifulSoup
import re
import requests
import sys
import pandas as pd


def periodic_figure_values(soup, yahoo_figure):
    values = []
    pattern = re.compile(yahoo_figure)

    title = soup.find("strong", text=pattern)
    # works for the figures printed in bold
    if title:
        row = title.parent.parent
    else:
        title = soup.find("td", text=pattern)
        # works for any other available figure
        if title:
            row = title.parent
        else:
            return None

    cells = row.find_all("td")[1:]
    # exclude the <td> with figure name
    for cell in cells:
        if cell.text.strip() != yahoo_figure:
            # needed because some figures are indented
            str_value = cell.text.strip().replace(",", "").replace("(", "-").replace(")", "")
            if str_value == "-":
                str_value = 0
            try:
                value = int(str_value) * 1000
            except:
                value = str_value
            values.append(value)
    return values


def financials_soup(ticker_symbol, statement="is", quarterly=False):
    if statement == "is" or statement == "bs" or statement == "cf":
        url = "https://finance.yahoo.com/q/" + statement + "?s=" + ticker_symbol
        if not quarterly:
            url += "&annual"
        return BeautifulSoup(requests.get(url).text, "html.parser")
    return sys.exit("Invalid financial statement code '" + statement + "' passed.")

AMEX = pd.read_csv('Tickers/AMEXTickers.csv')
tickers = list(AMEX['Symbol'])

financials = []

for ticker in tickers:
    print(ticker)
    incomestatment_soup = financials_soup(ticker, "is")
    date = periodic_figure_values(incomestatment_soup, "Revenue")
    research = periodic_figure_values(incomestatment_soup, "Research Development")
    opex = periodic_figure_values(incomestatment_soup,"Total Operating Expenses")
    revenue = periodic_figure_values(incomestatment_soup,"Total Revenue")
    if(date != None):
        newd = {'Ticker': ticker,
                'Date': date,
                'Research & Development Cost': research,
                'Total Operating Expences': opex,
                'Revenue': revenue}
        newdf = pd.DataFrame(data=newd)
        financials.append(newdf)

result = pd.concat(financials, axis=0)

result.to_csv('Data/AMEX_RD.csv', index=False)