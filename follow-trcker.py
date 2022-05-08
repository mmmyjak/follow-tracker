import tweepy
from all_keys import *
from sys import exit
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import datetime

def get_followers(username):
    try:
        client = tweepy.Client(bearer_token)
        user_id = client.get_user(username=username).data.id
    except AttributeError:
        return None
    else:
        response = client.get_users_followers(user_id).data
        followers = []
        for user in response:
            followers.append([user.name, user.username])
        return followers


def time_from_lastcheck(time):
    _now = datetime.datetime.now()
    _time = _now - time
    return(_time.seconds/3600)

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'twitter_follows'
mysql = MySQL(app)

@app.route('/', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        username = request.form['name']
        cursor = mysql.connection.cursor()
        query = ''' SELECT name, last_check from users WHERE name =\'''' + username + '''\''''
        _response = cursor.execute(query)
        if _response == 0:
            query = '''INSERT INTO users(id, name, last_check) VALUES(NULL, \'''' + username +'''\', NULL)'''
            cursor.execute(query)
            mysql.connection.commit()
            query = ''' SELECT id from users WHERE name =\'''' + username + '''\''''
            cursor.execute(query)
            id = cursor.fetchall()[0][0]
            followers = get_followers(username)
            for follower in followers:
                query = '''INSERT INTO followers(id, name, username, user_id) VALUES(NULL, \'''' + follower[0] +'''\', \'''' + follower[1] +'''\', \'''' + str(id) +'''\')'''
                cursor.execute(query)
                mysql.connection.commit()
            cursor.close()
            return('You were added database. Check in 24 hours if anyone followed or unfollowed you')
        else:
            our_user = cursor.fetchall()
            if time_from_lastcheck(our_user[0][1]) > 0:
                query = ''' SELECT id from users WHERE name =\'''' + username + '''\''''
                cursor.execute(query)
                id = cursor.fetchall()[0][0]
                query = ''' SELECT username from followers WHERE user_id =\'''' + str(id) + '''\''''
                cursor.execute(query)
                old_followers = cursor.fetchall()
                fllwrs = get_followers(username)
                followers = [[fllwr[1], False] for fllwr in fllwrs]
                for old in old_followers:
                    if old in followers:
                        pass
                answer = str(old_followers) + " vs " + str(followers)
                return(answer)
            else:
                return('Your last check was less than 24 hours ago!')



    else:
        return render_template('form.html')
    
    # query = '''INSERT INTO users(id, name, last_check) VALUES(NULL, \'''' + username +'''\', NULL)'''
    # cursor.execute(query)
    # # resp = cursor.fetchall()
    # mysql.connection.commit()
    # cursor.close()
    # # return(str(resp[0][0]))
    # return("udidit")

if __name__ == "__main__":
    app.run(debug=True)