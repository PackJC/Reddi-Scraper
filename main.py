import plotly.express as px
from Token import create_tickers
import pandas_datareader as pdr
import pandas
import praw
import datetime as dt
import re
import matplotlib.pyplot as plt

server = "www.nasdaqtrader.com"
directory = "SymbolDirectory"
filename = "nasdaqlisted.txt"
_client_id = ''
_client_secret = ''
_username = ''
_password = ''
_user_agent= 'SubReddit Scraper'
NYSE_Tokens = []
#get file object
f = open("nasdaqlisted.txt", "r")

while(True):
    line = f.readline()
    NYSE_Tokens.append(line.split('|')[0])
    if not line:
        break
#close file
f.close


blacklist_words = [
      "YOLO",  "CFO", "CTO", "DD", "RH", "USA", "IT", "ATH", "GDP",
      "ITM", "IMO", "BE", "ICE", "PT", "LOVE", "EDIT", "PM", "DOW",
      "AM", "PM", "GOAT", "FL", "CA", "IL", "PS", "AH", "TL", "DR",
      "JAN", "FEB", "JUL", "AUG", "OCT", "NOV", "FDA", "IV", "ER",
      "IPO", "RISE", "IPA", "URL", "USD", "AT", "A" , "I" , "THE" ,
      "TO" , "YOU" , "FOR" , "AND", "Y", "WE", "NO", "DIP", "IN",
      "ALL", "HOLD", "BUY", "EOD", "TD", "MOON", "", "ARE", "NOW",
      "UP", "BOYS", "GO", "OF", "ON", "IF", "AM", "ME", "HAS", "CAN",
      "APR", "TECH", "RUN", "GOOD", "OLD", "LIFE", "BBQ"
   ]
   
def get_tokens(posts, subredditName):
    redditObject = praw.Reddit(client_id = _client_id,
                         client_secret = _client_secret,
                         username = _username,
                         password = _password,
                         user_agent= _user_agent)
    selectedSubreddit = redditObject.subreddit(subredditName)
    #Sorts by new and pulls the last (n) posts of (subreddit)
    new_posts = selectedSubreddit.hot(limit = posts)
    commentList =[]
    titleList =[]
    for submission in new_posts:
        #Appends submission to titleList
        titleList.append(submission.title)
        #Defines how many child comments are held in the data to be analyzed
        submission.comments.replace_more(limit=int(childCommentFeathering))
        for comment in submission.comments.list():
            #Appends comment and time to commentList. YYYY/MM/DD HH/MM/SS Date Formatting
            commentList.append([str(comment.body), dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')])
    return commentList

pullLimit = input("How many posts? : ") 
subReddit = input("Which subreddit? : ")       
childCommentFeathering = input("How many child comments to be analyzed?")

numPullLimit = int(pullLimit)
#Adjust this number to pull different amounts of posts, limit 1000
commentList = get_tokens(int(pullLimit), subReddit)
#Sort it by time
commentList.sort(key = lambda x:x[1])
#Think of this as going through every word and adding valid tokens
#Over a large enough amount of data, this is very accurate for picking up the most talked about 'tokens'
tickerList = []

for i in commentList:
    tickers = re.findall('[A-Z]{1,4}', str(i[0])) 
    if len(tickers) > 0:
        for j in tickers:
            if j and j in NYSE_Tokens and j not in blacklist_words:
                tickerList.append(j)

#Removes duplicate tokens             
tickerList = set(tickerList)
#Logs on, scrapes comments, creates ticker objects
final_list = create_tickers(tickerList,commentList) 

graph_list = []
#Creates a nested list that has elements like [GME, 32, .5] for graphing
for obj in final_list:
    graph_list.append([obj.ticker,obj.count,obj.avg_sent])

df = pandas.DataFrame(graph_list, columns = ['Ticker', 'Count', 'Avg_Sentiment']) #creates a dataframe from the graph_list
df = df.sort_values(by = 'Count', ascending = False)#Sorts it by count
df = df.head(10) #Gives us the top 10 rows

fig = px.bar(df, x = df.Ticker, y = df.Count, color = df.Avg_Sentiment) #creates bar graph
fig.update_layout(
    title={
        'text': "The Top 15 Chart",
        'x' : .5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show() #initiates graph