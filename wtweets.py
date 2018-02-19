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
    """Build twitter API from user credentials.
    
    Arguments:
        conf {string} -- relative or absolute pathname of the toml configuration file.
    
    Returns:
        tweepy.API -- python twitter API.
    """

    user = toml.load(conf)
    auth = tweepy.OAuthHandler(user['consumer']['key'], user['consumer']['secret'])
    auth.set_access_token(user['access']['token'], user['access']['token_secret'])
    return tweepy.API(auth)

def wipe(twitter_api):
    """Main process, wipe tweets found into .csv.
    
    Arguments:
        twitter_api {tweepy.API} -- python twitter API.
    """

    ntweets = 0
    ndeleted = 0
    stime = time.monotonic()

    with open(csv_fname, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Get total number of tweets inside csv file
        for row in csv_reader:
            ntweets += 1
        
        # Reset iter
        csv_file.seek(0)
        csv_reader.__init__(csv_file)
        
        print(ntweets, "tweets found in csv file.")
        print("We are going to delete them one by one.")
        print("It may take a long time, you should make yourself some coffee.")
        
        # Ensure that user is aware of what is going on
        cin = input("\nDo you really want to proceed ? (y/N) : ")
        if( cin != "y" and "Y" != cin ): 
            exit(0)
        
        # Last chance to cancel
        print("\nStarts in 5 seconds.\n\n")
        time.sleep(5)

        for index, row in enumerate(csv_reader):
            tweet_id = row['tweet_id']
            print("Deleting tweet [{0}/{1}] ... ".format(index+1, ntweets), end="")
            try:
                twitter_api.destroy_status(tweet_id)
                print("[DONE]", end="\r")
                ndeleted += 1
            except Exception as e:
                print("[FAILED] ->", e, end="\r")

    etime = time.monotonic() - stime
    print("\n>>", ndeleted, "/", ntweets, "tweets deleted in", etime, "seconds.")

def main():
    tapi = build_api(toml_fname)
    wipe(tapi)

if __name__ == "__main__":
    main()