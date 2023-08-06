import requests
from bs4 import BeautifulSoup
url = "https://www.sharesansar.com/live-trading"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
table = soup.find('table', id='headFixed')
body = table.find('tbody')

class LiveData:

    def __init__(self, symbl):
        self.symbl = symbl

    def repl(self, data):
        return float(data.text.strip().replace(',', ''))

    def datum(self):
        tickr = []
        symbl = self.symbl
        Symbol = symbl.upper()
        for tr in body.find_all('tr'):
            i = 0
            for data in tr.find_all('td'):
                i += 1
                if i == 2:
                    ticker = data.text.strip()
                    tickr.append(data.text.strip())
                if i == 3:
                    ltp = self.repl(data)
                if i == 4:
                    change = self.repl(data)
                if i == 5:
                    change_in_percentage = self.repl(data)
                if i == 6:
                    opens = self.repl(data)
                if i == 7:
                    high = self.repl(data)
                if i == 8:
                    low = self.repl(data)
                if i == 9:
                    volume = self.repl(data)

            if Symbol == ticker:
                return ({"ticker": ticker},
                        {"last_transaction_price": ltp},
                        {"Change in Points": change},
                        {"Percentage_Change": change_in_percentage},
                        {"Opening Price": opens},
                        {"High": high},
                        {"Low": low},
                        {"Volume": volume},
                        )
        if Symbol not in tickr:
            print("None")

def get_data(symbl):
    return LiveData(symbl).datum()