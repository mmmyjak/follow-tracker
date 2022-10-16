# follow-tracker

Flask + MySQL app that tracks new follows / unfollows with Twitter Api + Tweepy.

1. Create 'all_keys.py' file in this directory and set 'bearer_token' variable to your https://developer.twitter.com/en token.

![image](https://user-images.githubusercontent.com/84145031/169515827-da8eee7f-d977-48f9-bcc5-9fcbbe57950a.png)

![image](https://user-images.githubusercontent.com/84145031/169515867-785e2398-9ee6-42f9-a179-f6af7fe5d245.png)

Due to TwitterAPI rate limits (GET followers/list - 15 requests per 1 window {15 minutes}) and 1000 followers per one request, I set the limit to check only last 7000 followers, so for accounts that has more than 7k followers the app doesn't find 100% unfollows.

Python 3.9.3
