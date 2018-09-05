# Import pandas
import pandas as pd
import os


def parse_files(dl_path):
    result = []
    for xls in os.listdir(dl_path):
        # Assign spreadsheet filename to `file`
        file = dl_path + '/' + xls
        try:
            # Load spreadsheet, rename index (first) column for later reference
            df = pd.read_excel(file, sheet_name=1, header=[0, 1])
            df.index.rename("Measure", True)

            # Update for other measures
            research = df[df.index.str.contains('research', case=False)]
            # Current company
            company = xls.split('.')[0]
            # Report Dates
            dates = [x[1] for x in list(research.columns.values)]
            # Measure
            values = research.iloc[0].tolist()
            # Units of Measure
            units_text = df.columns.names[0].split()[-1]
            # Convert textual units of measure to integers
            if units_text.lower() == "thousands":
                units_num = 1000
            elif units_text.lower() == "millions":
                units_num = 1000000
            elif units_text.lower() == "billions":
                units_num = 1000000000
            else:
                units_num = 1
            if(len(values) > 0):
                # Create formatted df to be appended
                newd = {'Company': company,
                        'Report Date': dates,
                        'R&D Cost': [x * units_num for x in values]}
            newdf = pd.DataFrame(data=newd)
            # append current xls data to result
            result.append(newdf)
        except:
            pass
    return pd.concat(result, axis=0)
