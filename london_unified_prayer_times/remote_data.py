import urllib.request
from bs4 import BeautifulSoup


def get_html_data(url, css_class):
    r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(r) as data:
        response = data.read()
        soup = BeautifulSoup(response, 'html.parser')
        prayerdata = soup.find("section", class_=css_class).table

        headings = [th.get_text()
                    for th in prayerdata.thead.tr.find_all("th")]

        web_data = []
        for row in prayerdata.tbody.find_all("tr"):
            day = zip(headings, [td.get_text() for td in row.find_all("td")])
            web_data.append(dict(day))

        return web_data
