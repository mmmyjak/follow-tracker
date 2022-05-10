from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import helpful_functions
from soupsieve import escape

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
        # first check
        if _response == 0:
            query = '''INSERT INTO users(id, name, last_check) VALUES(NULL, \'''' + username +'''\', NULL)'''
            cursor.execute(query)
            mysql.connection.commit()
            query = ''' SELECT id from users WHERE name =\'''' + username + '''\''''
            cursor.execute(query)
            id = cursor.fetchall()[0][0]
            followers = helpful_functions.get_followers(username)
            for follower in followers:
                follower[0] = escape(follower[0])
                follower[1] = escape(follower[1])
                query = '''INSERT INTO followers(id, name, username, user_id) VALUES(NULL, \'''' + follower[0] +'''\', \'''' + follower[1] +'''\', \'''' + str(id) +'''\')'''
                cursor.execute(query)
                mysql.connection.commit()
            cursor.close()
            return('You were added database. Check in 24 hours if anyone followed or unfollowed you')
        # already in database
        else:
            our_user = cursor.fetchall()
            if helpful_functions.time_from_lastcheck(our_user[0][1]) > 0:
                query = ''' SELECT id from users WHERE name =\'''' + username + '''\''''
                cursor.execute(query)
                id = cursor.fetchall()[0][0]
                query = ''' SELECT name, username from followers WHERE user_id =\'''' + str(id) + '''\''''
                cursor.execute(query)
                old_followers = cursor.fetchall()
                fllwrs = helpful_functions.get_followers(username)
                followers, foll_bool, followed, unfollowed = [], [], [], []
                for fllwr in fllwrs:
                    followers.append(fllwr[1])
                    foll_bool.append(False)
                for old in old_followers:
                    if old[1] in followers:
                        where = followers.index(old[1])
                        foll_bool[where] = True
                    else:
                        unfollowed.append(old)
                        query = '''DELETE FROM followers WHERE username =\'''' + old[1] + '''\''''
                        cursor.execute(query)
                        mysql.connection.commit()
                for i in range(0, len(fllwrs)):
                    if foll_bool[i] == False:
                        followed.append(fllwrs[i])
                        fllwrs[i][0] = escape(fllwrs[i][0])
                        fllwrs[i][1] = escape(fllwrs[i][1])
                        query = '''INSERT INTO followers(id, name, username, user_id) VALUES(NULL, \'''' + fllwrs[i][0] +'''\', \'''' + fllwrs[i][1] +'''\', \'''' + str(id) +'''\')'''
                        cursor.execute(query)
                        mysql.connection.commit()
                # updating last check datatime
                query = '''UPDATE users(last_check) VALUES(NULL) WHERE id =\'''' + str(id) + '''\''''
                cursor.execute(query)
                mysql.connection.commit()
                cursor.close()
                # our_user = (('username', datetime.datetime(y, m, d, h, m, s)),)
                return(helpful_functions.printAnswer(our_user[0], followed, unfollowed))
            else:
                return('Your last check was less than 24 hours ago!')

    else:
        return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)