'''
author: nlama
date: 06.10.2020
secret	L1_Qa744mf6CE8saktD5OUGRoUU
jIEqjrL-p8JvSg
Foid_Bot

Just using this to casually scrap data and then visualize it 

'''


#import dependencies
import praw
import pandas as pd
import datetime as dt
#import Text_Mining_Utils
# import numpy as np

#Functions
def get_date(created):
    return dt.datetime.fromtimestamp(created)

def DumpFile(df):
    import pickle
    with open('reddit_users_subreddits.pickle', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

def RedditAPI():
    reddit = praw.Reddit(client_id='jIEqjrL-p8JvSg', \
                     client_secret='L1_Qa744mf6CE8saktD5OUGRoUU', \
                     user_agent='Foid_Bot', \
                     username='The_Coding_Lama', \
                     password='R3ddiT_st@rtUPn0w!!')
    return reddit

def ObtainRedditInfo(df):
    '''
It takes a long time to load up this data. I savad this dictionary as a pickle called reddit_users_subreddits.pickle 
'''
    reddit = RedditAPI()
    contributers_dict = {} #key = subreddit, value = set of all contributers 
    # for sub,t in zip(df['Subreddit'], df['Status']):
    for sub,t in df.items():
        if t == "Quarantined":
            subreddit = reddit.subreddit(sub)
            subreddit.quaran.opt_in() #need this if entering a quarantined subreddit
        else:
            subreddit = reddit.subreddit(sub)
            
        contributers_set = set()
    
        for comment in subreddit.comments(limit=1000):
            try:
                contributers_set.add(comment.author.name)
            except:
                print("Error. Continue")
                continue
        for submission in subreddit.new(limit=1000):
            try:
                contributers_set.add(submission.author)
            except:
                print("Could not parse author from {0}'s post".format(sub))
                
        contributers_dict[sub] = contributers_set
    
    return contributers_dict



df = pd.read_csv("NSFW_Quarantined_Subreddits.csv")
df = {"LGBDropTheT": "NSFW","futanari" : "NSFW"}
subreddit_df = ObtainRedditInfo(df)

#Make edge list for network graph
elist = []
for k_1 in subreddit_df.keys():
    for k_2 in subreddit_df.keys():
        if k_1 != k_2:
            edge_weight = len(subreddit_df[k_1].intersection(subreddit_df[k_2]))
            if edge_weight > 0: 
                elist.append((k_1,k_2,edge_weight))
                
                
import pickle                
with open('reddit_users_subreddits_edgelist.pickle', 'wb') as handle:
    pickle.dump(elist, handle, protocol=pickle.HIGHEST_PROTOCOL)






