from bs4 import BeautifulSoup as soup
import pandas as pd
# import numpy as np
from urllib.request import urlopen as uReq
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

my_url = "https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nepal"
uClient = uReq(my_url)
page_html = uClient.read()

uClient.close()
page_soup = soup(page_html, "html.parser")

table = page_soup.findAll('table', {'class': "wikitable sortable"})


# print(table[0])


def get_timeline():
    # ROWS
    body = table[0].findAll('tr')  # getting all rows
    arr = []

    for i in range(2, len(body)):
        cell = body[i].findAll('td')  # getting all table cells
        req_cell = []
        for j in [1, 4, 6]:  # 0-dates, 1= totalcases, 4=totalrecovery, 6= totaldeaths
            num = cell[j].text
            num = num.replace(",", "")
            if j != 0:
                req_cell.append(int(num))
            else:
                req_cell.append(num.replace("\n", ""))
        arr.append(req_cell)  # making two dimensional list for making dataframe
    #         print(arr)
    df = pd.DataFrame(arr, columns=['TotalCases', 'Recovered', 'Deaths'])  # dataframe

    dates = []
    start_date = datetime.date(2020, 1, 23)
    length = len(df['TotalCases'])

    for i in range(length):
        a = start_date.strftime("%d")  # date
        b = start_date.strftime("%b")  # month
        c = a + " " + b

        dates.append(c)
        start_date = start_date + timedelta(days=1)

    # print(dates)
    # print(start_date)
    date = pd.DataFrame(dates, columns=['Date'])
    df = pd.concat([date, df], axis=1)
    df.dropna(axis=0)
    return (df, start_date)


# x,date=get_timeline()
# print(x)
# xd=x['TotalCases']
# plt.plot(xd)
# plt.show()
