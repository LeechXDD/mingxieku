import requests
from bs4 import BeautifulSoup
import csv
data = []
url= 'https://www.s.cn/'
attempts=0
success= False

def get_itemdetail(item_url):
    global data
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            req = requests.get(item_url, timeout=10)
            success = True
        except:
            attempts += 1
            if attempts == 3:
                print('网络错误地址：',item_url)
                break
        else:
            t = req.text
            t = t.replace('</body> </html> </div>', '</div>')
            soup = BeautifulSoup(t, 'lxml')
            # print(soup)

            pro = soup.find('div', class_='pro_bg')
            if pro != None:
                for each in pro.find_all('dl'):
                    item_name = each.dd.a.ul.li.string
                    del_price = each.find('i', attrs={'class': 'del_price'}).text
                    price = each.find('i', attrs={'class': 'price'}).text
                    address = 'https:'+ each.dd.a.get('href')
                    if item_name not in data:
                        data.append([item_name,del_price,price,address])
            else:
                pass

                # print('商品： ', each.dd.a.ul.li.string)
                # print('原价：', each.find('i', attrs={'class': 'del_price'}).text)
                # print('折扣价：', each.find('i', attrs={'class': 'price'}).text)
                # print('网址： ', each.dd.a.get('href'))


while attempts<3 and not success:
    try:
        req=requests.get(url,timeout=5)
        success = True
    except:
        attempts+=1
        if attempts == 3:
            print('网络错误')
            break
    else:
        soup=BeautifulSoup(req.content,'lxml')
        #print(soup)

        brands = soup.find('ul',class_='brands').find_all('a')

        for brand in brands:
            print(brand.string, '----->')
            item_url='http:'+brand.get('href')
            get_itemdetail(item_url)



        with open('shoe.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['商品', '原价', '现价','网址'])
            for index in data:
                writer.writerow(index)