from bs4 import BeautifulSoup
import requests as req
import pandas as pd

url = "https://www.list.am/category/23?bid=76&price1=&price2=&crc=-1&_a27=0&_a2_1=0&_a2_2=0&_a1_1=0&_a1_2=0&_a15=0&_a28_1=0&_a28_2=0&_a13=0&_a16=0&_a17=0&_a23=0&_a22=0&n=0"

resp = req.get(url)
soup = BeautifulSoup(resp.content, 'lxml')
pages_span = soup.find("span", { "class" : "pp" })
pages = pages_span.find_all("a")
page_links = [url]
for pages_a in pages_span.find_all("a"):
    page_links.append("https://www.list.am"+pages_a["href"])

def toyotas_from_listam(page_link):
    all_page = req.get(page_link)
    page_content = BeautifulSoup(all_page.content, 'lxml')
    cars_div = page_content.find_all("div", { "class" : "gl" })[1]
    car_rows = []
    for car_a in cars_div.find_all("a"):
        car_row = {}
        name = car_a.find("div", {"class" : "l"})
        clear_name = name.text.replace(';','')
        car_row["Car_Name"] = clear_name
        price = car_a.find("div", {"class" : "p"})
        if not price:
            car_row["Car_Price"] = "N/A"
        else:
            car_row["Car_Price"] = price.text
        car_row["Car_URL"] = "https://list.am"+car_a["href"]
        car_rows.append(car_row)
    all_pages_car_rows.extend(car_rows)
    return all_pages_car_rows

all_pages_car_rows = []
for page_link in page_links:
    toyotas_from_listam(page_link)
list_for_csv = pd.DataFrame(all_pages_car_rows)
list_for_csv.to_csv('list.csv')