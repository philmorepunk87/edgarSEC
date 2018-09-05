# -*- coding: utf-8 -*-
"""
The purpose of this script is to navigate to the SEC's edgar portal and
download 10-K's for the companies of interest sepecified in the ticker list

Originally created on Thu Aug 30 20:09:26 2018

@author: Jamey Copeland
"""


# import the urllib and BeautifulSoup library
import urllib.request as urllib2
from bs4 import BeautifulSoup as BeautifulSoup
import os


# Step 1: Define funtions to download filings
def get_link(ticker):

    url_part1 = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
    url_part2 = '&type=10-K&dateb=&owner=exclude&count=1'
    secpath = 'https://www.sec.gov/'

    # make the url to go out to the SEC website, bring in the ticker as well
    base_url = url_part1 + ticker + url_part2

    # open the url and parse it with BeautifulSoup
    data_page = urllib2.urlopen(base_url)
    data_soup = BeautifulSoup(data_page, "lxml")

    # find all of the a tags with the id = interactiveDataBtn
    filing = data_soup.find('a', id='interactiveDataBtn')

    if filing is not None:
        dllink = secpath + filing['href']
    else:
        dllink = None
    return dllink


def download_report(url,dl_path, ticker):

    secpath = 'https://www.sec.gov/'

    # get a list of all the files in the directory
    os.chdir(dl_path)
    dirlist = os.listdir(dl_path)

    # loop through the url_list created in the get_list function and find
    # a tags that have content that say "View Excel Document", this occurs
    # only once on each webpage thats why the find method is used
    excellink = urllib2.urlopen(url)
    excelsoup = BeautifulSoup(excellink, "lxml")
    paths = excelsoup.find('a', string='View Excel Document')
    if paths is not None:
        excelpath = secpath + paths['href']

    # only look at the first path to get the last three years of info,
    # can modify this line if more data is needed
    try:
        target_url = excelpath

        file_name = ticker + '.' + target_url.split('/')[-2] + '.xlsx'

        # check to make sure filename is not in directory, if it is ignore
        # to prevent downloaded something that is already there
        if file_name not in dirlist:
            xlsx_report = urllib2.urlopen(target_url)
            data = xlsx_report.read()
            with open(file_name, 'wb') as output:
                output.write(data)
    except:
        pass

    return
