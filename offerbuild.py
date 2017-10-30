url = 'https://www.tesco.com/groceries/en-GB/promotions/alloffers?page='
for x in range(1,331):
	tempurl = '\t\t"'+url+str(x)+'",'
	print(tempurl)