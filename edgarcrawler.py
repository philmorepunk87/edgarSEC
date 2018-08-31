# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 20:09:26 2018

@author: copel
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 18:15:15 2018
@author: jcopelan
"""
#import the urllib and BeautifulSoup library
import urllib.request as urllib2
from bs4 import BeautifulSoup as BeautifulSoup


# Step 1: Define funtions to download filings
def get_list(ticker):
    
    url_part1 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
    url_part2 = '&type=10-K&dateb=&owner=exclude&count=40'
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
        dllink.append(secpath + filing['href'])
    
    return dllink

def download_report(url_list):
    
    secpath = 'https://www.sec.gov/'
    
    #loop through the url_list created in the get_list function and find
    #a tags that have content that say "View Excel Document", this occurs
    #only once on each webpage thats why the find method is used
    excelpaths = []
    for report_url in url_list:
        excellink = urllib2.urlopen(report_url)
        excelsoup = BeautifulSoup(excellink, "lxml")
        paths = excelsoup.find('a', string = 'View Excel Document')
        excelpaths.append(secpath + paths['href'])
     
    #loop through the excelpaths and then download the .xlsx files,
    #it is setup to download files to the same directory that the script
    #is executed in
        for path in excelpaths:
            target_url = path
            print("Target URL found!")
            print("Target URL is:", target_url)
                    
            file_name = target_url.split('/')[-2] + '.xlsx'
            print(file_name)
                   
            xlsx_report = urllib2.urlopen(target_url)
            data = xlsx_report.read()
            with open(file_name, 'wb') as output:
                output.write(data)


#supply a list of tickers
tickers = ['A','AMGN']

#loop through all of the tickers and get the .xlsx files (utilizing the functions
#above)
for ticker in tickers:
    url_list= get_list(ticker)
    download_report(url_list)