# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 13:06:37 2018

@author: jcopelan
"""

import pandas as pd
from Levenshtein import ratio
import numpy as np
import timeit
from yahoo import financials_soup, periodic_figure_values
from headcount import get_headcount

start = timeit.default_timer()

# read in the tickers and concatenate them all together
NASDAQ =  pd.read_csv('Tickers/NASDAQTickers.csv')
AMEX = pd.read_csv('Tickers/AMEXTickers.csv')
NYSE = pd.read_csv('Tickers/NYSETickers.csv')
tickers = pd.concat([NASDAQ,AMEX,NYSE])

#delete out tickers without a market cap
tickers = tickers[tickers['MarketCap'] != 'n/a']
tickers = list(tickers['Symbol'])
# loop over the tickers and store the financial and headcount data in various
# data frames   
financials = []
headcount = []

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
    headcount = get_headcount(ticker)
    if headcount is not None:
        head = {'Ticker': ticker, 'EmployeeCount': headcount}
        headdf = pd.DataFrame(data=head)
        headcount.append(headdf)
    else:
        continue

financialresult = pd.concat(financials, axis=0)
financialresult.to_csv('Data/Financials_RD.csv', index=False)

headcountresult = pd.concat(headcount, axis=0)
headcountresult.to_csv('Data/Headcount.csv')


# read in the financial data of interest and join to the tickers
financials = pd.read_csv('Data/Financials_RD.csv')
financials = financials.merge(tickers[["Name","Symbol"]], left_on='Ticker', right_on='Symbol', how="outer", copy=False).drop(labels=['Symbol'], axis=1)


#read in the headcount data and join to the rest
headcount = pd.read_csv('Data/Headcount.csv')
financials = financials.merge(headcount, on = "Ticker", how="outer")
financials = financials.drop_duplicates(subset = ["Name","Date"])
financials["Name"] = financials["Name"].apply(lambda x: str(x).upper())

# read in the global party data
globalparties =  list(pd.read_table('Data/GlobalParties.txt')["GlobalPartyName"])
uniquenames_original = [str(x).upper() for x in list(financials.drop_duplicates(subset = ["Name"])["Name"])]

#make a list of corporation titles
corporations = ["INC.", "INCORPORATED", "LIMITED", "LTD.", "CORPORATION", "PLC", "CORP.",
                "SA", "LTD", "INC", "HOLDINGS", "COMPANY", "S.A", "GMBH", "AG", "L.P",
                "NV", "S.A.B", "SAB", "DE", "LLC", "", " ", "LP", "CO", "CO.","HOLDINGS,", "L.P.",
                "HOLDING", "S.A.", "PHARMA", "PHARMACEUTICALS", "THERAPEUTICS", "RESEARCH", "BIOLOGICS",
                "SOLUTIONS","TECHNOLOGIES","SCIENCES", '&', 'L.L.C', 'N.V']

#make globalparties and unique names a list of lists seperated by words
uniquenames = [x.split(' ') for x in uniquenames_original]
globalpartiesfiltered = [x.split(' ')[1:] for x in globalparties]
uniquenames = [[x.replace(',','') for x in corpnames if x not in corporations] for corpnames in uniquenames]
uniquenames = [[x for x in corpnames if x not in corporations] for corpnames in uniquenames]
globalpartiesfiltered  = [[x for x in corpnames if x not in corporations] for corpnames in globalpartiesfiltered]
uniquenames = [" ".join(x) for x in uniquenames]
globalpartiesfiltered  = [" ".join(x) for x in globalpartiesfiltered]

##compute the levenstein ratio
ratiolist = []
for uniquename in uniquenames:
    for globalparty in globalpartiesfiltered:
        if ratio(globalparty, uniquename) >= 0.95:
            ratiolist.append(ratio(globalparty, uniquename))
        else:
            ratiolist.append(-100)
ratiolist = np.reshape(ratiolist, (len(uniquenames),len(globalparties)))
maxindeces = np.argmax(ratiolist, axis = 1)

#make a Global Party list to store the likely global party from the  levenshtein ratios above
GPLList = []
for index in maxindeces:
    GPLList.append(globalparties[index])

matchlists = pd.DataFrame(data={"CompanyName": uniquenames_original, "GlobalParty": GPLList})
#get rid of the no match index which was assigned as '1 Government of the United States'
matchlists = matchlists[matchlists['GlobalParty'] != '1 GOVERNMENT OF THE UNITED STATES']
financials = financials.merge(matchlists, left_on='Name', right_on='CompanyName', how="outer").drop(labels=['CompanyName'], axis=1)
financials =  financials.dropna(subset = ["GlobalParty"], axis = 0)
financials =  financials.dropna(subset = ["Date"], axis = 0)

#add in the global party name to the financial data

stop = timeit.default_timer()

print('Time elapsed: ', (stop - start) / 60, ' minutes' ) 