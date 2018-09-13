# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:53:02 2018

@author: jcopelan
"""

# -*- coding: utf-8 -*-
"""
Leveraging Yahoo Finance to get the  headcount at a company

Originally created on Thu Aug 30 20:09:26 2018

@author: Jamey Copeland
"""


from bs4 import BeautifulSoup
import urllib.request as urllib2
import http.client as http
import pandas as pd


def get_headcount(ticker):
    try:
        values = []
        pattern = 'Full Time Employees'
    
        url_part1 = 'https://finance.yahoo.com/quote/'
        url_part2 = '/profile?p=A'
    
    
        # make the url to go out to the SEC website, bring in the ticker as well
        base_url = url_part1 + ticker + url_part2
    
    
        data_page = urllib2.urlopen(base_url)
        data_soup = BeautifulSoup(data_page, "lxml")
        
        # get the data-reactid of the pattern string and add 3 to it
        reactid = str(int(str(data_soup.find_all( 'span', text = pattern)).split('>')[0][-3:-1]) + 3)
    
        # look for the values
        count = data_soup.find('span', {'data-reactid':reactid}).text
        values.append(count)
        
        return values
    
    except (urllib2.HTTPError,urllib2.URLError, AttributeError, ValueError, http.IncompleteRead) as e:
        print(e)

AMEX = pd.read_csv('AMEXTickers.csv')
tickers = list(AMEX['Symbol'])

financials = []

for ticker in tickers:
    print(ticker)
    headcount = get_headcount(ticker)
    if headcount is not None:
        newd = {'Ticker': ticker, 'EmployeeCount': headcount}
        newdf = pd.DataFrame(data=newd)
        financials.append(newdf)
    else:
        continue
    

result = pd.concat(financials, axis=0)

result.to_csv('AMEX_Headcount.csv', index=False)       



