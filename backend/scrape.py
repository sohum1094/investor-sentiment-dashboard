#Get rid of print statements whenever needed

#\Using gnews to source articles and then newspaper3k to scrape them.

from gnews import GNews

num_articles = 10
period = '7d'

# added parameter exclude_websites for articles that can't be parsed by newspaper3k, should probably add a way to auto add websites to this list
# can also add start_date, end_date
google_news = GNews(language='en', country='US', period=period, max_results=num_articles, exclude_websites=['nytimes.com', 'wsj.com', 'axios.com', 'reuters.com'])

#Can do the following to get news: by_site may be useful for our application
#GNews.get_news(keyword)
#GNews.get_news_by_topic(topic)
#GNews.get_top_news()
#GNews.get_news_by_site(site)
search_term = 'techcrunch startups'
articles_info = google_news.get_news(search_term)

"""The format of articles_info is an array of dictionaries. Each dictionary holds the url to an article and other relevant information:"""

print(articles_info)

"""Replacing the 64bit gnews url with the original url so that it can be used with newspaper3k (unfortunately this is quite slow):"""

from googlenewsdecoder import new_decoderv1

for article in articles_info:
  decoded_url = new_decoderv1(article.get('url'), interval=5)
  article['url'] = decoded_url['decoded_url']
  print(article['url'])

from newspaper import Article, ArticleException
from newspaper import Config
import nltk
nltk.download('punkt')

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

failed_articles = []

for article in articles_info:
    url = article['url']
    news = Article(url, config=config)

    try:
        news.download()
        news.parse()
        article['article_text'] = news.text
        news.nlp()
        article['article_keywords'] = news.keywords
        article['article_summary'] = news.summary
    except ArticleException as e:
        print(f"Download failed for {url}: {e}")
        failed_articles.append(article)

for article in failed_articles:
    articles_info.remove(article)

#Add desired values of the dictionary (as displayed below) to Firebase (or process more first and then add to Firebase)

print(article.keys())