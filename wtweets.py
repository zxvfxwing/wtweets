"""
Wipe all your tweets.

2018
zxvfxwing
v0.1

Dependencies:
https://pypi.python.org/pypi/tweepy
https://pypi.python.org/pypi/toml
https://docs.python.org/3.8/library/csv.html
https://docs.python.org/3.8/library/time.html
"""
import csv
import toml
import time
import tweepy

# CSV filename:
csv_fname = "tweets.csv"

# TOML filename:
toml_fname = "credentials.toml"

def build_api(conf):
    user = toml.load(conf)
    auth = tweepy.OAuthHandler(user['consumer']['key'], user['consumer']['secret'])
    auth.set_access_token(user['access']['token'], user['access']['token_secret'])
    return tweepy.API(auth)

def wipe(twitter_api):
    ntotal = 0
    ndeleted = 0
    stime = time.monotonic()

    with open(csv_fname, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            ntotal += 1
            tweet_id = row['tweet_id']
            print("Deleting tweet", tweet_id ,"... ",end="")
            try:
                twitter_api.destroy_status(tweet_id)
                print("[DONE]")
                ndeleted += 1
            except Exception as e:
                print("[FAILED] ->", e)

    etime = time.monotonic() - stime
    print("\n>>", ndeleted, "/", ntotal, "tweets deleted in", etime, "seconds.")

def main():
    tapi = build_api(toml_fname)
    wipe(tapi)

if __name__ == "__main__":
    main()