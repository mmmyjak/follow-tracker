import tweepy
import tweepy.errors
from all_keys import *
import datetime
from re import match


def get_followers(username):
    try:
        client = tweepy.Client(bearer_token)
        user_id = client.get_user(username=username).data.id
        response = tweepy.Paginator(client.get_users_followers, user_id, max_results=1000).flatten(limit=6001)
        followers = []
        for user in response:
            followers.append([user.name, user.username])
    except AttributeError:
        return "There is no user named like that"
    except tweepy.errors.TooManyRequests:
        return "Too many requests to Twitter API in last 15 min, try again in some time"
    else:
        return followers

def twitter_username_regex(username):
    return True if match("^(\w){1,15}$", username) else False

def twitter_name_escape(name):
    escaped_name = ""
    for n in name:
        if match("^(\w)|[ #.-]$", n): escaped_name+=n
    return escaped_name

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