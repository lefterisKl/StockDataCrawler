import requests
import time
from bs4 import  BeautifulSoup
import datetime
import time


website_url = "https://finance.yahoo.com"
sector_url_prefix = "https://finance.yahoo.com/sector/"
sector_url_suffix = "?offset=0&count=100"

sectors = ["financial","healthcare","services","utilities","industrial_goods","basic_materials","conglomerates",
           "consumer_goods","technology"]

sector_url = {sector:(sector_url_prefix+sector+sector_url_suffix) for sector in sectors }
#print(sector_url['financial'])

data = []

f = open("daily_data.csv", "w")
f.write("Ticker,Date,Close,Volume\n")
f.close()

Date = datetime.datetime.now().strftime ("%Y-%m-%d")
print( "Start crawling at:",time.ctime())

start_time = time.time()

for sector,sector_url in sector_url.items():
    print("Crawling sector",sector,".")
    offset = 0
    next_url = sector_url
    sector_data = []
    while  offset < 100:
        page = requests.get(next_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        urls = soup.find_all(lambda tag: tag.name == 'a' and
                                           tag.get('class') == ['Fw(b)'])
        links = { url.text : website_url + url.get('href')  for url in urls}
        if(len(links)==0):
            break

        for ticker, ticker_link in links.items():
            ticker_page = requests.get(ticker_link)
            ticker_soup = BeautifulSoup(ticker_page.content, 'html.parser')
            ticker_data = ticker_soup.find_all(lambda tag: tag.name == 'td'  and
                                                           tag.get('class') ==["Ta(end)", "Fw(b)", "Lh(14px)"] )
            variables = []
            for x in ticker_data:
                variable =  x.get('data-test')
                if  str(x).find("span") == -1:
                    value =  x.text
                else:
                    value = list( x.children)[0].text
                variables.append((variable,value))
            variables = dict(variables)
            print("\t crawling data for "+ str(ticker))
            sector_data.append((ticker,variables))
        offset = offset + 100
        #sector_url_prefix_predifined = "https://finance.yahoo.com/sector/predifined/"
        sector_url_suffix_predifined = "?offset=" + str(offset) + "&count=100"
        next_url = sector_url_prefix + sector + sector_url_suffix_predifined
    f = open("daily_data2.csv","a")
    for ticker_data in sector_data:
        f.write(ticker_data[0].lower() +","+Date+","+ ticker_data[1]["PREV_CLOSE-value"].replace(",","") +
                ","+ ticker_data[1]["TD_VOLUME-value"].replace(",","") + "\n")
    f.close()
    break
    #data.append((sector,sector_data))
    #time.sleep(1)
# your code
print("End crawling at",time.ctime())
print("Elapsed time:",  time.time() - start_time)







