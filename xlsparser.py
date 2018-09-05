# Import pandas
import pandas as pd
import os
import numpy as np

def parse_files(dl_path):
    result = []

    # Subroutine used to help with conditional breaking. i.e. can be modfied to
    # 'find_first_research'
    def find_research(df):
        # Get the company name from the xls file name
        company = xls.split('.')[0]
        # Attempt to get column and row names of data table
        rows = list(df.iloc[:, 0])
        cols = list(df)
        # Loop through row names
        for i in range(0, len(rows)):
            # Check to see if 'research' appears in the row name
            if 'research' in str(rows[i]).lower():
                # Since the tables are often formattted differently,
                # this if statement provides a cushion of a column
                # in case there is padding. It extracts the R&D values,
                # dates, and corresponding period. Uses the first 13 chars
                # of date because of weird parsing issue
                values_initial = list(df.iloc[i, 1:])
                dates_initial = list(df.iloc[0, 1:])
                data_exists = [not (pd.isnull(a) or pd.isnull(b)) for a, b in zip(values_initial, dates_initial)]

                if(len(list(np.where(data_exists)[0])) > 0):
                    period = cols[list(np.where(data_exists)[0])[0] + 1]
                    values = [values_initial[x] for x in np.where(data_exists)[0]]
                    dates = [str(dates_initial[i])[:13] for i in np.where(data_exists)[0]]

                    # Figure out the units of measure. 
                    # If none given, it's a miss
                    units_text = cols[0].split()[-1]
                    if units_text.lower() == "thousands":
                        units_num = 1000
                    elif units_text.lower() == "millions":
                        units_num = 1000000
                    elif units_text.lower() == "billions":
                        units_num = 1000000000
                    else:
                        return None

                    # Get the current measure from the row name
                    measure = rows[i]
                    # Make sure there's a value and that it's not a percentage
                    if(len(values) > 0 and '%' not in ''.join(str(values))):
                        # Create formatted df to be appended
                        newd = {'Company': company,
                                'Report Date': dates,
                                'R&D Cost': [x * units_num for x in values],
                                'Period': period,
                                'Measure': measure}
                        newdf = pd.DataFrame(data=newd)
                        return newdf
        return None

    for xls in os.listdir(dl_path):
        # Assign spreadsheet filename to `file`
        file = dl_path + '/' + xls
        #  Load workbook into different sheets. Sometimes (rarely) this fails
        try:
            wb = pd.read_excel(file, sheet_name=None)
        except Exception as e:
            print(xls.split('.')[0] + e)
            pass
        # Loop through each sheet to find 'research' terms
        for sheet, df in wb.items():
            newdf = find_research(df)
            if newdf is not None:
                result.append(newdf)
                break  # comment this out to get all R&D Data
    return pd.concat(result, axis=0)
