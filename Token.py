from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os #Used to access datetime
import re #Used to find only words with 1-4 characters
import praw #Best Python Reddit API Wrapper Available
import pandas as pd 
import datetime as dt #Used to record comment and submission times

sia = SentimentIntensityAnalyzer() 
#The following code is the procedure to create a list of ticker objects, which carry data for each ticker.
def create_tickers(tickerlist, commentlist):
    obj_list = []
    #Initiate ticker objects
    for ticker in tickerlist:
        obj_list.append(Ticker(ticker))

    for obj in obj_list:
        obj.get_comments(commentlist) #calls get comments method - populates self.comments attribute with list of all comments where ticker was mentioned
        obj.get_count() #length of self.comments, i.e. how many unique comments mentioned the ticker
            

    final_list = [] #we're only going to call the rest of the methods if a stock was mentioned to save time
    for obj in obj_list:
           
        if obj.count>0:
            final_list.append(obj) #creates a final_list that has tickers that have been mentioned at least once

    for obj in final_list: #call the remaining method functions to fully populate the ticker object
        obj.analyzer()
        obj.average_sentiment()
        obj.get_positions()
        if len(obj.comments) > 5: #create a 5 comment moving average of sentiment -- change to variable later!
            obj.get_mv_avg()
    return final_list
        
class Ticker:

    def __init__(self, ticker):
        self.ticker = ticker
        self.comments = []
        self.times = []
        self.sentiment = []
        self.count = 0
        self.avg_sent = 0
        self.positions = []
        self.mv_times = []

  

    def get_comments(self, commentlist): #loops through the comments you pulled and uses regex to see if the ticker is mentioned
        for comment in commentlist:
            if len(re.findall(r'\b{}\b'.format(self.ticker), str(comment))) > 0: #if it is mentioned,
                self.comments.append(comment[0]) #append the ticker's self.comments list with the comment
                self.times.append(comment[1]) #and then append the ticker's self.times list with the time of the comment.
        return self.comments

    # Counts amount of Ticker occurences per Subreddit post, does not count occurences within a single comment
    # i.e. "GME GME GME SUCKS!" = 1
    def get_count(self):
        self.count = len(self.comments)
        return self.count

    #returns a list of each comment's compound score from vaderSentiment
    def analyzer(self): 
        for comment in self.comments:
            #https://towardsdatascience.com/sentimental-analysis-using-vader-a3415fef7664
            score = sia.polarity_scores(comment) 
            sentiment = score['compound']
            self.sentiment.append(sentiment)
    # polarity_scores isn't perfect and if it tries to handle certain things like emojis can be prone to returning 0

    #returns the average sentiment around the stock, but ignores cases where compound is 0
    def average_sentiment(self): 
        counter = 0
        sent = 0
        for sentiment in self.sentiment:
            if sentiment != 0:
                sent += sentiment
                counter += 1
        if counter > 0:
            self.avg_sent = round(sent / counter, ndigits=2)
        return self.avg_sent


    def get_positions(self): #particularly proud of this one :)
        # positions are in form SPY 300c 11/20 for example. On WSB this would mean "Call option on $SPY with a $300 strike expiring 11/20"
        # alt_format is in form 11/20 SPY 300C
        for comment in self.comments:
            position = re.findall(r'{}\s\d+\w\s\d+\S\d+'.format(self.ticker), comment)
            #alt_format = re.findall(r'\d+\S\d+\s{}\s\d+'.format(self.ticker), comment) doesn't fully work yet
            if position != []:
                self.positions.append(position)
            #if alt_format != []:
               # self.positions.append(alt_format)
                                    
        return self.positions
        
    
    def get_mv_avg(self): #creates a 5 comment moving average of sentiment to track it over time. Issue is, time data isn't normalized
         number_series = pd.Series(self.sentiment)
         window_size = 5
         windows  = number_series.rolling(window_size)
         moving_averages = windows.mean()
         moving_avg_list = moving_averages.tolist()
         mv_avg = moving_avg_list[window_size -1 :]

         times = self.times
         clean_times = times[(window_size) - 1:]

         df = pd.DataFrame(list(zip(mv_avg, clean_times)),
                           columns = ['Average Sentiment', 'Time'])

                 
         return df
