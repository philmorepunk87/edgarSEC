# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 13:06:37 2018

@author: jcopelan
"""

import pandas as pd
from Levenshtein import ratio
import numpy as np
import timeit

start = timeit.default_timer()


# read in the tickers and concatenate them all together
NASDAQ =  pd.read_csv('Tickers/NASDAQTickers.csv')
AMEX = pd.read_csv('Tickers/AMEXTickers.csv')
NYSE = pd.read_csv('Tickers/NYSETickers.csv')
tickers = pd.concat([NASDAQ,AMEX,NYSE])

# read in the financial data of interest and join to the tickers
NASDAQ_RD =  pd.read_csv('Data/NASDAQ_RD.csv')
AMEX_RD = pd.read_csv('Data/AMEX_RD.csv')
NYSE_RD = pd.read_csv('Data/NYSE_RD.csv')
financials = pd.concat([NASDAQ_RD, AMEX_RD, NYSE_RD])
financials = financials.merge(tickers[["Name","Symbol"]], left_on='Ticker', right_on='Symbol', how="outer", copy=False).drop(labels=['Symbol'], axis=1)


#read in the headcount data and join to the rest
NASDAQ_HC =  pd.read_csv('Data/NASDAQ_Headcount.csv')
AMEX_HC = pd.read_csv('Data/AMEX_Headcount.csv')
NYSE_HC = pd.read_csv('Data/NYSE_Headcount.csv')
headcount = pd.concat([NASDAQ_HC, AMEX_HC, NYSE_HC])
financials = financials.merge(headcount, on = "Ticker", how="outer")
financials = financials.drop_duplicates(subset = ["Name","Date"])

# read in the global party data
globalparties =  list(pd.read_table('Data/GlobalParties.txt')["GlobalPartyName"])
uniquenames_original = [str(x).upper() for x in list(financials.drop_duplicates(subset = ["Name"])["Name"])]

#make a list of corporation titles
corporations = ["INC.", "INCORPORATED", "LIMITED", "LTD.", "CORPORATION", "PLC", "CORP.",
                "SA", "LTD", "INC", "HOLDINGS", "COMPANY", "S.A", "GMBH", "AG", "L.P",
                "NV", "S.A.B", "SAB", "DE", "LLC", "", " ", "LP", "CO", "CO.","HOLDINGS,", "L.P.",
                "HOLDING", "S.A.", "PHARMA", "PHARMACEUTICALS", "THERAPEUTICS", "RESEARCH", "BIOLOGICS",
                "SOLUTIONS","TECHNOLOGIES","SCIENCES"]

#make globalparties and unique names a list of lists seperated by words
uniquenames = [x.split(' ') for x in uniquenames_original]
globalpartiesfiltered = [x.split(' ')[1:] for x in globalparties]
uniquenames = [[x for x in corpnames if x not in corporations] for corpnames in uniquenames]
uniquenames = [[x.replace(',','') for x in corpnames if x not in corporations] for corpnames in uniquenames]
globalpartiesfiltered  = [[x for x in corpnames if x not in corporations] for corpnames in globalpartiesfiltered]
uniquenames = [" ".join(x) for x in uniquenames]
globalpartiesfiltered  = [" ".join(x) for x in globalpartiesfiltered]

##compute the levenstein ratio
ratiolist = []
for uniquename in uniquenames:
    for globalparty in globalpartiesfiltered:
        if ratio(globalparty, uniquename) > 0.90:
            ratiolist.append(ratio(globalparty, uniquename))
        else:
            ratiolist.append(-100)
ratiolist = np.reshape(ratiolist, (len(uniquenames),len(globalparties)))
maxindeces = np.argmax(ratiolist, axis = 1)
#[ratio.max()  for ratio in ratiolist]

GPLList = []
for index in maxindeces:
    GPLList.append(globalparties[index])

matchlists = pd.DataFrame(data={"CompanyName": uniquenames_original, "GlobalParty": GPLList})
#get rid of the no match index which was assigned as '1 Government of the United States'
matchlists = matchlists[matchlists['GlobalParty'] != '1 GOVERNMENT OF THE UNITED STATES']
financials = financials.merge(matchlists, left_on='Name', right_on='CompanyName', how="outer").drop(labels=['CompanyName'], axis=1)
financials.to_csv('/Data/FinancialData.csv')
#add in the global party name to the financial data

stop = timeit.default_timer()

print('Time elapsed: ', (stop - start) / 60, ' minutes' ) 