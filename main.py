from edgarcrawler import get_link, download_report
from xlsparser import parse_files
import pandas as pd
import os

# supply a list of tickers

NYSE = pd.read_csv('NYSETickers.csv')
tickers = list(NYSE['Symbol'])

# change dl_path to desired path, create folder if it doesn't already exist, 
# then set folder as active directory
dl_path = os.path.join("C:", os.sep, "Users", "jephilli", "Documents", "Data", "SEC Data", "NYSE")
if not os.path.exists(dl_path):
    os.makedirs(dl_path)
os.chdir(dl_path)

# loop through all of the tickers and get the .xlsx files 
# (utilizing the functions above)
for ticker in tickers:
    url = get_link(ticker)
    if url is not None:
        download_report(url, dl_path, ticker)
    else:
        continue

# create and store final data table

final = parse_files(dl_path)

print(final)