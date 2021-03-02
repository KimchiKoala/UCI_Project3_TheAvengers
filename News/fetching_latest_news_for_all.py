# importing requests package
import requests     
 
def TopNews():
     
    # Top 20 Business headline api
    main_url = "http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=95a5557a4c5847a4b99933122f558ad2"
 
    # fetching data in json format
    res = requests.get(main_url)
    open_news_page = res.json()
 
    # getting all articles in a string article
    article = open_news_page["articles"]
 
    # empty list which will 
    # contain all trending news
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    for i in range(len(results)):
         
        # printing all trending news
        print(i + 1, results[i])
 
# Driver Code
if __name__ == '__main__':
     
    # function call
    TopNews() 