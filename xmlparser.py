# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 18:45:32 2018

@author: jcopelan
"""

import xml.etree.ElementTree as eTree
import pandas as pd
e = eTree.parse('C:\\Users\\jcopelan\\OneDrive - Agilent Technologies\\Documents\\Ad Hoc Presentations_Analysis\\Edgar SEC Data\\Downloaded_Filings\\AMGN\\amgn-20161231.xml').getroot()
print(e.tag)

#newlist = []
#for child in e:
#    newlist.append(child.tag + str(child.attrib))
#    


lists = []
newlists = {}
for child in e:
    lists.append(child.tag)
    if 'ResearchAndDevelopmentExpense' in child.tag:
        newlists.append(child.tag + ' | ' + child.attrib['contextRef'] + ' | ' + child.text)

#df = pd.DataFrame(lists)
#df.to_excel('columnnames.xlsx')
#  
#for atype in e.findall(newlists):
#    print(atype.text, atype.attrib['contextRef'])