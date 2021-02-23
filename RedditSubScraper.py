import praw
import pandas as pd
import datetime as dt

def get_data(posts, subreddit):
    secret = '6bxmPxFlzpVT4SYUWXH6FdT1jbJrMw' #developer key
    app_id = 'qZwrzSmQ6F-7Kg' #developer id
    user = 'DabCam' #username
    pw = 'cole45' #password
    
    redditObject = praw.Reddit(client_id = app_id,
                         client_secret = secret ,
                         username = user,
                         password = pw,
                         user_agent= 'SubReddit Sraper')

    sub = redditObject.subreddit(subreddit) #select subreddit

    new_posts = sub.hot(limit = posts) #sorts by new and pulls the last (n) posts of r/wallstreetbets

    commentlist =[]
    titlelist =[]
    for submission in new_posts:
        titlelist.append(submission.title)   #creates list of post subjects, elements strings

        submission.comments.replace_more(limit=1)
        for comment in submission.comments.list():
            commentlist.append([str(comment.body), dt.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')]) #creates list of comments, elements strings
    
    return commentlist
    print("Scrape completed")


