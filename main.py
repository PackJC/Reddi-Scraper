import plotly.express as px
from TokenObject import create_tickers
import pandas_datareader as pdr
import pandas
import praw
import datetime as dt
import re

blacklist_words = [
      "YOLO", "TOS", "CEO", "CFO", "CTO", "DD", "BTFD", "WSB", "OK", "RH",
      "KYS", "FD", "TYS", "US", "USA", "IT", "ATH", "RIP", "BMW", "GDP",
      "OTM", "ATM", "ITM", "IMO", "LOL", "DOJ", "BE", "PR", "PC", "ICE",
      "TYS", "ISIS", "PRAY", "PT", "FBI", "SEC", "GOD", "NOT", "POS", "COD",
      "AYYMD", "FOMO", "TL;DR", "EDIT", "STILL", "LGMA", "WTF", "RAW", "PM",
      "LMAO", "LMFAO", "ROFL", "EZ", "RED", "BEZOS", "TICK", "IS", "DOW"
      "AM", "PM", "LPT", "GOAT", "FL", "CA", "IL", "PDFUA", "MACD", "HQ",
      "OP", "DJIA", "PS", "AH", "TL", "DR", "JAN", "FEB", "JUL", "AUG",
      "SEP", "SEPT", "OCT", "NOV", "DEC", "FDA", "IV", "ER", "IPO", "RISE"
      "IPA", "URL", "MILF", "BUT", "SSN", "FIFA", "USD", "CPU", "AT",
      "GG", "ELON" , "DFV" , "A" , "I" , "THE" , "TO" , "YOU" , "FOR" , "AND",
      "MY", "Y", "WE", "THIS", "JPOW", "NO", "DIP", "IN", "ALL", "HOLD", "BUY"
   ]
   
def get_tokens(posts, subredditName):
    redditObject = praw.Reddit(client_id = 'qZwrzSmQ6F-7Kg',
                         client_secret = '6bxmPxFlzpVT4SYUWXH6FdT1jbJrMw',
                         username = 'DabCam',
                         password = 'cole45',
                         user_agent= 'SubReddit Sraper')
    print("Successfully Authenticated... ... ...")
    selectedSubreddit = redditObject.subreddit(subredditName)
    #Sorts by new and pulls the last (n) posts of (subreddit)
    new_posts = selectedSubreddit.hot(limit = posts)
    commentList =[]
    titleList =[]
    for submission in new_posts:
        #Appends submission to titleList
        titleList.append(submission.title)
        #Defines how many child comments are held in the data to be analyzed
        submission.comments.replace_more(limit=20)
        for comment in submission.comments.list():
            #Appends comment and time to commentList. YYYY/MM/DD HH/MM/SS Date Formatting
            commentList.append([str(comment.body), dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')])
    return commentList


pullLimit = input("How many posts? : ") 
subReddit = input("Which subreddit? : ")
numPullLimit = int(pullLimit)
#Get the comments by calling the get_tokens function from the WSBreader module
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
            #clean_tick = str(j[1:])
            #tickerlist.append(clean_tick.upper())
            if j and j not in blacklist_words:
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
        'text': "Wall Street Bets Top 15",
        'x' : .5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show() #initiates graph

