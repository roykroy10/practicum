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

'''


import pandas as pd
import pprint
from difflib import SequenceMatcher as SM

listaddr = {}
#zip_codes = [10026, 10027, 10030, 10037, 10039,10001, 10011, 10018, 10019, 10020, 10036,10029, 10035,10010, 10016, 10017, 10022,10012, 10013, 10014
#10004, 10005, 10006, 10007, 10038, 1028,10002, 10003, 10009, 10021, 10028, 10044, 10065, 10075, 10128, 10023, 10024, 10025, 10031, 10032, 10033, 10034, 10040]
zip_codes = [10037, 10039,10001]
for zip in zip_codes:
    tables = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5="+str(zip))
#   calls_df, = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5=10012", attrs = {'class': 'Tableresultborder'})
    tmp = []
    for row in tables[5][1]:
        tmp.append(row)
    listaddr[zip] = tmp

#calls_df, = pd.read_html("http://w10.melissadata.com/lookups/zipstreet.asp?Step5=10012")
#print(calls_df.to_json(orient="records", date_format="iso"))
pprint.pprint(listaddr)
l1 = sorted(listaddr[10039],key=lambda x: difflib.SM(None, x, b).ratio())



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

 SequenceMatcher(None, a, a1).ratio()
