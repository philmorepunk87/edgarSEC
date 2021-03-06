from bs4 import BeautifulSoup
import re
import requests
import sys



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

