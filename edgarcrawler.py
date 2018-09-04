# -*- coding: utf-8 -*-
"""
The purpose of this script is to navigate to the SEC's edgar portal and 
download 10-K's for the companies of interest sepecified in the ticker list

Originally created on Thu Aug 30 20:09:26 2018

@author: Jamey Copeland
"""


#import the urllib and BeautifulSoup library
import urllib.request as urllib2
from bs4 import BeautifulSoup as BeautifulSoup
import pandas as pd
import os

# Step 1: Define funtions to download filings
def get_list(ticker):
    
    url_part1 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
    url_part2 = '&type=10-K&dateb=&owner=exclude&count=1'
    secpath = 'https://www.sec.gov/'
    
    #make the url to go out to the SEC website, bring in the ticker as well
    base_url = url_part1 + ticker + url_part2 
    
    #open the url and parse it with BeautifulSoup
    data_page = urllib2.urlopen(base_url)
    data_soup = BeautifulSoup(data_page,"lxml")

    #find all of the a tags with the id = interactiveDataBtn
    filings = data_soup.find_all('a',id = 'interactiveDataBtn')
    
    #loop through and store the hyperlinks in a list    
    dllink = []
    for filing in filings:
        if filing is not None:
            dllink.append(secpath + filing['href'])
        else:
            continue
    
    return dllink

def download_report(url_list,dl_path):
    
    secpath = 'https://www.sec.gov/'
    
    #loop through the url_list created in the get_list function and find
    #a tags that have content that say "View Excel Document", this occurs
    #only once on each webpage thats why the find method is used
    excelpaths = []
    for report_url in url_list:
        excellink = urllib2.urlopen(report_url)
        excelsoup = BeautifulSoup(excellink, "lxml")
        paths = excelsoup.find('a', string = 'View Excel Document')
        if paths is not None:
            excelpaths.append(secpath + paths['href'])
        else:
            continue
     
    #only look at the first path to get the last three years of info, can modify
    #this line if more data is needed
    try:
        target_url = excelpaths[0]
        print("Target URL found!")
        print("Target URL is:", target_url)
                            
        file_name = ticker + target_url.split('/')[-2] + '.xlsx'
        print(file_name)
                           
        xlsx_report = urllib2.urlopen(target_url)
        data = xlsx_report.read()
        os.chdir(dl_path)
        with open(file_name, 'wb') as output:
            output.write(data)
    except:
        pass

#supply a list of tickers
NYSE = pd.read_csv('NYSETickers.csv')
tickers = list(NYSE['Symbol'])

#change dl_path to desired path wherever, make sure directory is created 
#behorehand else the files wont get written (and the script will keep running
#because of the exception set up on line 61)
dl_path = 'C:\\Users\\jcopelan\\OneDrive - Agilent Technologies\\Documents\\Ad Hoc Presentations_Analysis\\edgarSEC\\Downloads\\NYSE\\'

#loop through all of the tickers and get the .xlsx files (utilizing the functions
#above)
for ticker in tickers:
    url_list= get_list(ticker)
    if url_list is not None:
        download_report(url_list,dl_path)
    else:
        continue