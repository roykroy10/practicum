'''
Zip Codes in Manhattan:
Manhattan	Central Harlem	10026, 10027, 10030, 10037, 10039
Chelsea and Clinton	10001, 10011, 10018, 10019, 10020, 10036
East Harlem	10029, 10035
Gramercy Park and Murray Hill	10010, 10016, 10017, 10022
Greenwich Village and Soho	10012, 10013, 10014
Lower Manhattan	10004, 10005, 10006, 10007, 10038, 10280
Lower East Side	10002, 10003, 10009
Upper East Side	10021, 10028, 10044, 10065, 10075, 10128
Upper West Side	10023, 10024, 10025
Inwood and Washington Heights	10031, 10032, 10033, 10034, 10040

zipcodes source: https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm
pandas read html: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_html.html

medium guide to get table from website: https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58

streets from zipcodes site: http://w10.melissadata.com/lookups/zipstreet.asp?InData=10012&c=1&l=U

sorting: http://www.compciv.org/guides/python/fundamentals/sorting-collections-with-sorted/
nice printing: import json  print(json.dumps(dictionary, indent=4, sort_keys=True))

'''


import pandas as pd
import pprint
from difflib import SequenceMatcher as SM
import csv

def zipandstreets():

    listaddr = {}
    #zip_codes = [10026, 10027, 10030, 10037, 10039,10001, 10011, 10018, 10019, 10020, 10036,10029, 10035,10010, 10016, 10017, 10022,10012, 10013, 10014,
    #10004, 10005, 10006, 10007, 10038, 1028,10002, 10003, 10009, 10021, 10028, 10044, 10065, 10075, 10128, 10023, 10024, 10025, 10031, 10032, 10033, 10034, 10040]
    zip_codes = [10037, 10039,10001]
    for zip in zip_codes:
        tables = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5="+str(zip))
    #   calls_df, = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5="+str(zip), attrs = {'class': 'Tableresultborder'})
        tmp = []
        print zip,tables[5][0]
        for row in tables[5][1]:
            tmp.append(row)
        listaddr[zip] = tmp


    with open("dict2csv.csv", 'w') as outfile:
       csv_writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

       for k,v in listaddr.items():
           csv_writer.writerow([k] + v)
    #calls_df, = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5=10012")
    #print(calls_df.to_json(orient="records", date_format="iso"))
    #pprint.pprint(listaddr)
    #l1 = sorted(listaddr[10039],key=lambda x: SM(None, x, b).ratio())



a = '27th'
a1 = '27th Street'
b = 'Avenue Of The Amer'
b1 = 'Avenue Of The Americas'
c = 'Hudson Yards'
c1 = 'Hudsonyards'
d = '27th'
d1 = '28th'
f = '10'
f1 = '10th'
g = 'Adam C Powell'
g1 = 'Adam Clayton Powell Jr'

#SM(None, a, a1).ratio()
import time
start_time = time.time()
zipandstreets()
print("--- %s seconds ---" % (time.time() - start_time))
