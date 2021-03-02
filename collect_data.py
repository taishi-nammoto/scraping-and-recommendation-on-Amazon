import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# type page number and search words
page_num = 100
search_term = 'chair'

# activate webdriver and build an empty dataframe
path = '/Users/taishi/Documents/chromedriver'
driver = webdriver.Chrome(path)

# check if the data exists
def find_data(item):
    try:
        atag = item.h2.a
        description = atag.text.strip()
        rating = item.i.text
        price = item.find('span','a-price')
        price = item.find('span','a-offscreen').text
        num_reviews = item.find('span', {'class':'a-size-base','dir':'auto'}).text
        item_url = 'https://www.amazon.com/' + atag.get('href')
        item_img = item.find('img', 's-image')
        img_url = item_img.get('src')
        return (description, rating, price, num_reviews, item_url, img_url)
    except AttributeError:
        return None


# collect data on every page
def collect_data(page, search_term):
    url = 'https://www.amazon.com/s?k='+search_term+'&page='+str(page)+'&ref=sr_pg_'+str(page)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type':'s-search-result'})
    for item in results:
        data_tuple = find_data(item)
        if data_tuple:
            data_list.append(data_tuple)


# loop number of pages and search words
data_list = []
for i in range(page_num):
    search_term = search_term.strip().split()
    search_term = '+'.join(search_term)
    collect_data(i, search_term)

driver.close()

# save the list in dataframe
df = pd.DataFrame(data_list, columns=['description', 'rating', 'price', 'num_reviews', 'item_url', 'img_url'])

# remove empty rows
df = df.dropna()

# save data in an excel file
df.to_excel('Data/table_data.xlsx',sheet_name='Item_info',index=False)
