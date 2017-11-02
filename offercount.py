import requests
import lxml.html
import math
categoryId=[12518,13343,267396,267397,12320,218831,12422,12192,12448,11651,12564,12298,281806]
#categoryId=[12518,13343,12422]
urlstring='https://www.sainsburys.co.uk/shop/gb/groceries/home/CategorySeeAllView?langId=44&storeId=10151&catalogId=10123&pageSize=108&facet=88&categoryId=%d&categoryFacetId1=%d&beginIndex=%d'
start_url = []
for n in categoryId:
	r  = requests.get(urlstring%(n,n,0))
	data = lxml.html.fromstring(r.text)
	output = data.xpath('//h1[@id="resultsHeading"]/text()')
	item = output[0].replace('  ','').replace('\r\n','').split('(')[0]
	itemcount = output[0].replace('  ','').replace('\r\n','').split('(')[1].split(' ')[0]
	print(item,':',itemcount)
	for i in range(0,math.ceil(int(itemcount.replace(',',''))/108)):
		start_url.append(urlstring%(n,n,i*108))
		print(urlstring%(n,n,i*108))
print(start_url)

#itemcount = output[0].split(' ')
#print(math.ceil(int(itemcount[0])/24))