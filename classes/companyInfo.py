import requests


class Info:
    def __init__(self):
        return

    def get_summary(self, symbol, stock_url):
        """Takes 2 arguments: symbol[stock_symbol], 
        stock_url[IEX API endpoint] -> Returns summary of
        article that mentions that stock.
        """
        try: 
            # get latest summary of latest article
            response = requests.get(stock_url + symbol + '/news/last/1')
            json - response.json()
            return json[0]['summary']
        except Exception as e:
            print(str(e))

    def get_articles(self, symbol, stock_url):
        """Takes 2 arguments: symbol[stock_symbol], 
        stock_url[IEX API endpoint] -> Returns link to
        latest article that mentions that stock.
        """
        try: 
            # get latest article
            response = requests.get(stock_url + symbol + '/news/last/1')
            json = response.json()
            return json[0]['url']
        except Exception as e:
            print(str(e))

    def get_company_name(self, symbol, stock_url):
        """Takes 2 arguments: symbol[stock_symbol], 
        stock_url[IEX API endpoint] -> Returns company
        name based on stock symbol.
        """        
        try:
            response = requests.get(stock_url + symbol + '/company')
            json = response.json()
            return json['companyName']
        except Exception as e:
            print(str(e))
            
    def get_exchange(self, symbol, stock_url):
        """Takes 2 arguments: symbol[stock_symbol], 
        stock_url[IEX API endpoint] -> Returns stock exchange
        stock belongs to.
        """
        try:
            response = requests.get(stock_url + symbol + '/company')
            json = response.json()
            return json['exchange']
        except Exception as e:
            print(str(e))