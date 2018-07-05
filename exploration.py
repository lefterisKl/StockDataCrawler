import requests
from bs4 import BeautifulSoup
from bs4 import element

page = requests.get("https://www.dataquest.io/blog/web-scraping-tutorial-python/")

#html_code = page.content.decode("utf-8") .split("\n")

#for line in html_code:
#    print(line)



soup = BeautifulSoup(page.content, 'html.parser')

#prettify how to view HTML
#print(soup.prettify())

#hierarchy of elements
#soup.children

#for child in soup.children:
#    print(child)




#print( isinstance(list(soup.children)[2],element.Tag) )

#elements = list(soup.children)

# how to get types of elements
#element_types = [type(e) for e in elements]

#tags  = [e for e in elements if isinstance(e,element.Tag)]

#################################################################


#links = soup.find_all('a')

#show all links
#for counter,link in enumerate(links):
#    print(counter)
#    print(list(link.children))

'''
for counter,link in enumerate(links):
    print(counter)
    l = list((link.children))
    if len(l)==1:
        if(l[0]=="more posts"):
            print( link)
'''
#the_link =  list( links)[1]
#print( the_link["href"])
#print( str( list(the_link.children)[0]))

#link = list(links)[5]


#print(str(link))
#print()

#print(  link["href"])
#print(  link["class"])



#####################ID AND CLASS

data = list()

domain = "https://finviz.com/"
location = "screener.ashx?v=111"



#e<a href="screener.ashx?v=111&r=21" class="tab-link"><b>next</b></a>


for  i in range(369):
    print("Crawling page ",str(i))
    page = requests.get(domain + location)
    soup = BeautifulSoup(page.content, "html.parser")



    #trs = list( soup.find_all("tr",class_='table-dark-row-cp')) + list(soup.find_all("tr",class_='table-light-row-cp'))

    trs = list( soup.find_all("tr",class_='table-dark-row-cp')) + list(soup.find_all("tr",class_='table-light-row-cp'))


    for tr in trs:

        tds = list( tr.children)

        number =    list( list(tds[1].children)[0].children)[0]
        ticker = list(list(tds[2].children)[0].children)[0]
        name = list(list(tds[3].children)[0].children)[0]
        sector = list(list(tds[4].children)[0].children)[0]
        industry = list(list(tds[5].children)[0].children)[0]
        country = list(list(tds[6].children)[0].children)[0]
        market_cap = list(list(tds[7].children)[0].children)[0]
        #p_e =  list(list(list(tds[8].children)[0].children)[0].children)[0]
        #price =  list(list(list(tds[9].children)[0].children)[0].children)[0]
        #change =  list(list(list(tds[10].children)[0].children)[0].children)[0]
        volume = list(list(tds[11].children)[0].children)[0]

        #print(number,ticker,name,sector,industry,country,market_cap,volume)

        row_data = [number,ticker,name,sector,industry,country,market_cap,volume]
        data.append(row_data)

    tablinks = list(soup.find_all("a", class_="tab-link"))

    next_page_location = ""
    for x in tablinks:
        c = str(list(x.children)[0])
        if c == "<b>next</b>":
            next_page_location = x["href"]

    location = next_page_location

with open('metadata_all.csv', 'w') as file:
    for row in data:
        row = [x.replace(",",".") for x in row]
        file.write(str(row).replace("[","").replace("]","") + "\n")




