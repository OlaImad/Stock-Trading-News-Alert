import requests
from twilio.rest import Client

STOCK_API_KEY = "************************"
STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"
NEWS_API_KEY = "***************************************"
account_sid = '************************************'
auth_token = '***************************************'
STOCK_NAME = "Nu Bank"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "SYMBOL": "NU",
    "apikey": STOCK_ENDPOINT,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()
# to create a list from the data dict with only the values without the keys
# it will be a list containing a dictionary of VALUES
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

# Python abs() 

# difference = abs(float(yesterday_closing_price - day_before_yesterday_closing_price))
# or to use an emoji that shows if difference is up or down
difference = round(float(yesterday_closing_price - day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"


diff_percent = float(difference / yesterday_closing_price) * 100
# we use again the abs in case we did not use it previous for ex when we took it out to do the emoji
if abs(diff_percent) > 5:
    news_params = {
        "apikey": NEWS_API_KEY,
         "q": "NU bank",
        "searchIn": "description",
    }
    new_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = new_response.json()["articles"]
    # use Python slice operator to create a list that contain the first 3 articles
    three_articles = articles[:3]

    formatted_articles_list = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}." \
                               f" \nBrief: {article['description']}"
                               for article in three_articles]

    client = Client(account_sid, auth_token)
    for article in formatted_articles_list:
        message = client.messages \
            .create(
            body=article,
            from_ ='#################',
            to='###############'
        )

    print(message.status)

