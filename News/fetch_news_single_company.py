# importing requests package
import requests     
 
def TopCompanyNews():
     
    # Top 5 headlines api
    news_url = "https://financialmodelingprep.com/api/v3/stock_news?tickers=AAPL,FB,GOOG,AMZN&apikey=demo"
 
    # fetching data in json format
    res = requests.get(news_url)
    open_news_page = res.json()
 
    # getting all articles in a string article
    article = open_news_page["articles"]
 
    # empty list which will 
    # contain all trending news for the company
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    for i in range(len(results)):
         
        # printing all trending news
        print(i + 1, results[i])
 
# Driver Code
if __name__ == '__main__':
     
    # function call
    TopCompanyNews() 