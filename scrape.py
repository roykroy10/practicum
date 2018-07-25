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
    neighborhoods = ['Berkeley-CA']
    berkley_zip_codes = ['94702','94703','94704','94705','94706','94707','94708','94709','94710']
    pages = list(range(1,21)) # 1 to 20
    nei = neighborhoods[0]
    ts = datetime.now().strftime("%d_%m_%Y_%H%M")
    for z in berkley_zip_codes:
    #for nei in neighborhoods:
		print('Starting neighborhood: '+nei+' zipcode: '+z)
		file_path = '%s_%s'%(nei,ts)
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


if __name__=="__main__":
    main()
