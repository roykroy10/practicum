# Based on ScrapeHero's script:
# https://github.com/scrapehero/zillow_real_estate/blob/master/zillow.py
# WARNING: Use this code at your own risk, scraping is against Zillow's TOC

from lxml import html
import requests
import csv
import time
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#url = "https://www.zillow.com/westwood-ca/sold/"
#url_w_zip = "https://www.zillow.com/berkeley-ca-94705/sold/1_p"
#url_w_zip_newest_first = "https://www.zillow.com/berkeley-ca-94705/sold/days_sort/1_p/"
#url = "https://www.zillow.com/homes/recently_sold/%s/%d_p"%(nei,page)
#berkley_zip_codes = ['94702','94703','94704','94705','94706','94707','94708','94709','94710']

def getPage(nei,zipc,page):
    try:
        #url = "https://www.zillow.com/homes/recently_sold/%s/%d_p"%(nei,page)
        url = "https://www.zillow.com/%s-%s/sold/days_sort/%d_p/"%(nei,zipc,page)
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        ''' headers= {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'cache-control':'max-age=0',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }'''
        response = requests.get(url, headers=headers, verify=False)
        parser = html.fromstring(response.text)
        search_results = parser.xpath("//div[@id='search-results']//article")

    except:
        print("Failed to process the page",url)
    return search_results if search_results else None


def parseResults(search_results,file_path,page):
	try:
		properties_list = []
		for properties in search_results:
			try:
				prop = {}
				raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
				raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
				raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
				raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
				raw_lat = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='latitude']//@content")
				raw_lon = properties.xpath(".//span[@itemprop='geo']//meta[@itemprop='longitude']//@content")
				raw_price = properties.xpath(".//text()[contains(.,'SOLD: ')]")[0][7:]
				raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
				raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
				url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
				raw_title = properties.xpath(".//h4//text()")
				raw_dateSold = properties.xpath(".//text()[contains(.,'Sold ')]")[0][5:]
				raw_zpid = properties.xpath(".//@data-zpid")

				address = ' '.join(' '.join(raw_address).split()) if raw_address else None
				city = ''.join(raw_city).strip() if raw_city else None
				state = ''.join(raw_state).strip() if raw_state else None
				postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
				price = ''.join(raw_price).strip() if raw_price else None
				info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
				broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
				title = ''.join(raw_title) if raw_title else None
				property_url = "https://www.zillow.com"+url[0] if url else None
				dateSold = raw_dateSold.strip() if raw_dateSold else None
				price_sqft = raw_info[0][13:] if raw_info else None
				sqft = raw_info[-1][1:-5] if raw_info else None
				zpid = raw_zpid[0].strip() if raw_zpid else None
				lat = ''.join(raw_lat[0]) if raw_lat else None
				lon = ''.join(raw_lon[0]) if raw_lon else None
				if(len(price_sqft)<2):
					continue
                #is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
				prop = {
                                'zpid':zpid,
                                'title':title,
                                'address':address,
                                'city':city,
                                'state':state,
                                'postal_code':postal_code,
                                'price':price,
                                'facts':info,
                                'provider':broker,
                                'url':property_url,
                                'dateSold':dateSold,
                                'price_sqft':price_sqft,
                                'sqft':sqft,
								'lat':lat,
								'lon':lon
                }
				properties_list.append(prop)
                #print(properties)
                #return properties_list
				with open(file_path,'a')as csvfile:
					fieldnames = ['zpid','title','address','city','state','postal_code','price','facts','provider','url','dateSold','price_sqft','sqft','lat','lon']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					for row in properties_list:
						writer.writerow(row)
			except Exception as e:
				print(e.args)
				pass
	except:
		print("Failed to process the page",url)


def main():
    start=datetime.now()

    #neighborhoods = ['Westwood-CA','Brentwood-CA','Albany-CA','Berkeley-CA','Evanston-IL','Rogers-Park-IL']
    neighborhoods = ['San-Jose-CA']
    berkley_zip_codes = ['94702','94703','94704','94705','94706','94707','94708','94709','94710']
    sj_zip_codes = ['95110','95111','95112','95116','95117','95118','95119',\
	'95120','95121','95122','95123','95124','95125','95126','95127','95128','95129','95130','95131','95132','95133','95135','95136','95138','95139','95148','']
    pages = list(range(1,21)) # 1 to 20
    nei = neighborhoods[0]
    ts = datetime.now().strftime("%d_%m_%Y_%H%M")
	ans = []
    for z in sj_zip_codes:
		#for nei in neighborhoods:
		print('Starting neighborhood: '+nei+' zipcode: '+z)
		file_path = '%s_%s'%(nei,ts)
		ans.append(file_path)
		with open(file_path,'a')as csvfile:
			fieldnames = ['zpid','title','address','city','state','postal_code','price','facts','provider','url','dateSold','price_sqft','sqft','lat','lon']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()

		for p in pages:
			print('Starting Page: %d in neighborhood: %s in zip: %s'%(p,nei,z))
			res = getPage(nei,z,p)
			parseResults(res,file_path,p)
			time.sleep(15.0)
			print('Saved results for: %s, page %d'%(nei,p))

		print('Finished neighborhood: '+nei+' zipcode: '+z)

    print('Finished! It took: '+str(datetime.now()-start))
	return ans


def afterScrape(fpath):
	import pandas as pd
	for p in fpath:
		df = pd.read_csv(p)
		df1 = df.drop_duplicates('zpid').reset_index(drop=True).copy() # Removes duplicate zpids
		df1 = df1.apply(lambda x: x.str.replace(',','')) # Removes all commas
		df1 = df1.loc[df1["sqft"]!='--'].copy() # Remove rows w/o sqft
		df1['sqft']=df1['sqft'].apply(lambda x: float(x[0:-2].replace(',',''))*43560 if " a" in str(x) else x)  # Replaces acres with sq.ft calculation
		df1['sqft']=df1['sqft'].apply(lambda x: x.split(' ')[0] if " sqf" in str(x) else x) # replaces string ending with sqf
		df2 = df1[df1['price'].map(len) > 1].copy() # Removes rows w/o price
		df2 = df2[df2['price_sqft'].map(len) < 6].copy() # Removes rows with price per sqft larger than 6 digits
		df2['price'] = df2['price'].str.replace('price', '0')
		df2.price = (df2.price.replace(r'[KM]+$', '', regex=True).astype(float) * \
		df2.price.str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1)\
		.replace(['K','M'], [10**3, 10**6]).astype(int))
		df2 = df2[df2['price'] > 50000]
		df2 = df2[~df2['price_sqft'].str.contains("-").fillna(False)]
		#df2['sqft'] = df2['sqft'].str.replace(',', '')
		# z['c'] = z.apply(lambda x: math.log(x.b) if x.b > 0 else 0, axis=1)
		# z['c'] = z.apply(lambda row: 0 if row['b'] in (0,1) else row['a'] / math.log(row['b']), axis=1)
		df2['price_sqft'] = df2['price_sqft'].str.replace(',', '')
		df2=df2.drop_index(drop=True)
		df2.to_csv(p, encoding='utf-8')



if __name__=="__main__":
    main()


'''
script to replace 1.00M -> 1000000
import pandas as pd
df = pd.read_csv('/home/ubuntu/Downloads/Berkeley_houses.csv')
df['price'] = df['price'].str.replace(',', '')
df.price= (df.price.replace(r'[KM]+$', '', regex=True).astype(float) * \
df.price.str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1).replace(['K','M'], [10**3, 10**6]).astype(int))
'''
