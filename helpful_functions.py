import tweepy
import tweepy.errors
from all_keys import *
import datetime
from re import match

class SQLQueries():

    def __init__(self, mysql_app):
        self.mysql = mysql_app
        self.cursor = mysql_app.connection.cursor()

    def selectUser(self, username):
        query = ''' SELECT id, name, last_check from users WHERE name =\'''' + username + '''\''''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getUserID(self, username):
        query = ''' SELECT id from users WHERE name =\'''' + username + '''\''''
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    def insertUser(self, username):
        query = '''INSERT INTO users(id, name, last_check) VALUES(NULL, \'''' + username +'''\', NULL)'''
        self.cursor.execute(query)
        self.mysql.connection.commit()

    def updateDate(self, id):
        query = '''UPDATE users SET last_check = NULL WHERE id =\'''' + str(id) + '''\''''
        self.cursor.execute(query)
        self.mysql.connection.commit()

    def insertFollower(self, name, username, user_id):
        name = MyTwitter.twitter_name_escape(name)
        username = MyTwitter.twitter_name_escape(username)
        query = '''INSERT INTO followers(id, name, username, user_id) VALUES(NULL, \'''' + name +'''\', \'''' + username +'''\', \'''' + str(user_id) +'''\')'''
        self.cursor.execute(query)
        self.mysql.connection.commit()

    def deleteFollower(self, username, user_id):
        query = '''DELETE FROM followers WHERE username =\'''' + username + '''\' AND user_id =\'''' + str(user_id) + '''\''''
        self.cursor.execute(query)
        self.mysql.connection.commit()
    
    def selectFollowersOfUser(self, user_id):
        query = ''' SELECT name, username from followers WHERE user_id =\'''' + str(user_id) + '''\''''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def closeCursor(self):
        self.cursor.close()


class MyTwitter:

    @staticmethod
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

    @staticmethod
    def twitter_username_regex(username):
        return True if match("^(\w){1,15}$", username) else False

    @staticmethod
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
    answer = "Follow Tracker - " + user[1] + " since " + str(user[2]) + ": <br/><br/>" + str(len(followed)) + " new users followed you:<br/>"
    for follow in followed:
        answer += follow[0] + " (@" + follow[1] + ")<br/>"
    answer += "<br/>"+ str(len(unfollowed)) + " new users unfollowed you:<br/>"
    for unfollow in unfollowed:
        answer += unfollow[0] + " (@" + unfollow[1] + ")<br/>"
    return answer