import tweepy
from all_keys import *
import datetime

def get_followers(username):
    try:
        client = tweepy.Client(bearer_token)
        user_id = client.get_user(username=username).data.id
    except AttributeError:
        return None
    else:
        response = tweepy.Paginator(client.get_users_followers, user_id, max_results=1000).flatten(limit=6001)
        followers = []
        for user in response:
            followers.append([user.name, user.username])
        return followers

def time_from_lastcheck(time):
    _now = datetime.datetime.now()
    _time = _now - time
    return(_time.seconds/3600)

def printAnswer(user, followed, unfollowed):
    answer = "Follow Tracker - " + user[0] + " since " + str(user[1]) + ": <br/><br/>" + str(len(followed)) + " new users followed you:<br/>"
    for follow in followed:
        answer += follow[0] + " (@" + follow[1] + ")<br/>"
    answer += "<br/>"+ str(len(unfollowed)) + " new users unfollowed you:<br/>"
    for unfollow in unfollowed:
        answer += unfollow[0] + " (@" + unfollow[1] + ")<br/>"
    return answer
