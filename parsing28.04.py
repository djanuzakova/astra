




import requests
import csv
from bs4 import BeautifulSoup 


HOST = "https://www.kivano.kg/"
URL = "https://www.kivano.kg/noutbuki"
CSV = "computers.csv"
HEADERS = {
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9",
"user-agent":"image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def get_html(url, params = ""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
# print(get_html(URL).text)






def get_content(html):
    computers = []
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("div", class_ = "item product_listbox oh")
#     print(items)

    for item in items:
        computers.append(
            {
                 "title": item.find('div', class_ = "listbox_title oh").get_text(strip=True),
                "price" : item.find('div', class_ = "listbox_price text-center").get_text(strip=True),
                "link": HOST + item.find('div', class_ = "listbox_img pull-left").find('img').get('src')
            }
            )
    return computers

# html = get_html(URL).text
# print(get_content(html))





def save_info(items, file_name):
    with open(file_name, "w") as file:
        writer = csv.writer(file, delimiter = ",")
        writer.writerow(["Name of product", "Price", "Link"])
        for item in items:
            writer.writerow([item['title'], item['price'],])


def parser():
    PAGINATION = int(input("How  many pages to parse: "))
    html = get_html(URL)
    if html.status_code == 200:
        computers = []
        for page in range(1, PAGINATION+1):
            print(f"Parsing page {page}")
            html = get_html(URL, params={"page":page})
            computers.extend(get_content(html.text))
            save_info(computers, CSV)
        print("Successfully finished")
    else:
        print("Page not found or server error")
parser()
