#NOTE: you must create oauth_tokens your self... It must include the constants
#shown below
from oauth_tokens import *
import twitter

if __name__=="__main__":
    a = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, USER_ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET)
    followers = a.GetFollowers()
    for f in followers:
        print f.name
        
    for u in a.GetFriendsTimeline():
        print u.user.name + u" -- " + u.GetText()