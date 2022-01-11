## Reddit Scraper +Sentiment
![4f5eea80-766f-11eb-984d-badb1d42c803](https://user-images.githubusercontent.com/34726562/148868595-8e3ad1df-193e-49e0-92af-0edfaa1b8c24.png)
Welcome to my project! I hope you've found everything easily. Although centered around Finance, this tool can be used to guage certain social and political trends.

* Features and Updates
* Dependencies
* Running the script
* About the Sentiment Scoring

## Dependencies

vaderSentiment, os, re
praw, pandas, datetime 
plotly.express

To install the above dependancies, 

>pip3 install vadersSentiment --user

>pip3 install praw --user

>pip3 install pandas --user

>pip3 install plotly.express --user

## Running the script
In order to run this script, you will need to download the Python IDE, IDLE. This project is built with Python 3.9. Once downloaded, open up main.py. Before you run the script you you will need a reddit account with developer features enabled. 

    redditObject = praw.Reddit(client_id = '************',
                         client_secret = ''************',
                         username = ''************',
                         password = '************',
                         user_agent= 'SubReddit Sraper')
                         
     
Once the redditObject is created with your account information you will be able to run the program. Save main.py and press F5 in IDLE. The script may take a while to run depending on how the user has selected their data to be queued. I recommend 5 posts, 15 child comments to verify if the script is working. Expect a couple minutes for the graph to pop up.

About the Sentiment Scoring
To do: Add Sentiment Documents
