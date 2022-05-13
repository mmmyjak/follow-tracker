from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import helpful_functions as hf

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'twitter_follows'
mysql_app = MySQL(app)


@app.route('/', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        username = request.form['name']
        if not hf.MyTwitter.twitter_username_regex(username): return("You can't have a username like that on Twitter")
        followers = hf.MyTwitter.get_followers(username)
        if isinstance(followers, str): return followers # returning an error message
        mysql = hf.SQLQueries(mysql_app)
        our_user = mysql.selectUser(username)
        if len(our_user) == 0:
            mysql.insertUser(username)
            id = mysql.getUserID(username)
            for follower in followers:
                mysql.insertFollower(name=follower[0], username=follower[1], user_id=id)
            mysql.closeCursor()
            return('You were added database. Check in 12 hours if anyone followed or unfollowed you')
        else: # already in database
            if hf.time_from_lastcheck(our_user[0][2]) > 12:
                old_followers = mysql.selectFollowersOfUser(user_id=our_user[0][0])
                new_followers, foll_bool, followed, unfollowed = [], [], [], []
                for fllwr in followers:
                    new_followers.append(fllwr[1])
                    foll_bool.append(False)
                for old in old_followers:
                    if old[1] in new_followers:
                        where = new_followers.index(old[1])
                        foll_bool[where] = True
                    else:
                        unfollowed.append(old)
                        mysql.deleteFollower(username=old[1], user_id=our_user[0][0])
                for i in range(0, len(followers)):
                    if foll_bool[i] == False:
                        followed.append(followers[i])
                        mysql.insertFollower(name=followers[i][0], username=followers[i][1], user_id=our_user[0][0])
                mysql.updateDate(id=our_user[0][0])
                mysql.closeCursor()
                # our_user = ((id, 'username', datetime.datetime(y, m, d, h, m, s)),)
                return(hf.printAnswer(our_user[0], followed, unfollowed))
            else:
                return('Your last check was less than 12 hours ago!')
    else:
        return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)