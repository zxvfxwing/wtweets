"""
Wipe all your tweets.

2018
zxvfxwing
"""
import csv
import toml
import time
import twitter
import argparse

# TOML filename:
toml_fname = "credentials.toml"

# CSV default filename:
csv_fname = "tweets.csv"

def arguments():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--csv', nargs=1, default=csv_fname, help='use a csv file for mass removal of tweets', metavar='FILENAME')
    group.add_argument('-s', '--soft', action='store_true', default=False, help='wipe your 3200 newer tweets')
    group.add_argument('-n', '--none', action='store_true', default=False, help='do not proceed to tweets deletion')

    parser.add_argument('-f', '--fav', action='store_true', default=False, help='wipe your favorites/likes')
    parser.add_argument('-d', '--dm', action='store_true', default=False, help='wipe your direct messages')

    return parser.parse_args()


def build_api(conf):
    user = toml.load(conf)
    return twitter.Api( consumer_key=user['consumer']['key'],
                        consumer_secret=user['consumer']['secret'],
                        access_token_key=user['access']['token'],
                        access_token_secret=user['access']['token_secret'] )

def doit():
     # Ensure that user is aware of what is going on
    cin = input("> Do you really want to proceed ? (y/N) : ")
    if( cin != "y" and "Y" != cin ):
        return False
    return True

def wipe_csv(api, args):
    ntweets = 0
    ndeleted = 0
    stime = time.monotonic()

    with open(args.csv, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Get total number of tweets inside csv file
        for row in csv_reader:
            ntweets += 1

        # Reset iter
        csv_file.seek(0)
        csv_reader.__init__(csv_file)

        print("\n{} tweets found in csv file.".format(ntweets))
        print("We are going to delete them one by one.")
        print("It may take a long time, you should make yourself some coffee.")

        if not doit(): return

        for index, row in enumerate(csv_reader):
            tweet_id = row['tweet_id']
            print("Deleting tweet [{0}/{1}] ... ".format(index+1, ntweets), end='')
            try:
                api.DestroyStatus(tweet_id)
                print("[DONE]", end='\r')
                ndeleted += 1
            except twitter.error.TwitterError as e:
                print("[FAILED] ->", e, end='\r')

    etime = time.monotonic() - stime
    print("\n>>", ndeleted, "/", ntweets, "tweets deleted in", etime, "seconds.")

def wipe_soft(api):
    print("\nYou made the choice to use 'soft deletion'.")
    print("Twitter API limits us to your 3200 newer tweets.")
    print("We are going to wipe your tweets (200 by 200)")

    if not doit(): return

    tweets = api.GetUserTimeline()
    nb = len(tweets)

    while nb > 0:
        for index, tweet in enumerate(tweets):
            try:
                print("Deleting tweet [{0}/{1}] ... ".format(index+1, nb), end='')
                api.DestroyStatus(tweet.id)
                print("[DONE]", end='\r')
            except twitter.error.TwitterError as e:
                print("[FAILED] ->", e, end='\r')

        print("\n10 seconds break before fetching tweets again")
        time.sleep(10)
        tweets = api.GetUserTimeline()
        nb = len(tweets)

def wipe_fav(api):
    print("\nWe are going to wipe your favorites/likes (200 by 200)")

    if not doit(): return

    favs = api.GetFavorites()
    nb = len(favs)

    while nb > 0:
        for index, fav in enumerate(favs):
            try:
                print("Deleting favorite [{0}/{1}] ... ".format(index+1, nb), end='')
                api.DestroyFavorite(fav)
                print("[DONE]", end='\r')
            except twitter.error.TwitterError as e:
                print("[FAILED] ->", e, end='\r')

        print("\n10 seconds break before fetching favorites again")
        time.sleep(10)
        fav = api.GetFavorites()
        nb = len(fav)

def wipe_dm(api):
    print("\nDM deletion not implemented yet")

def wipe(api, args):
    if args.soft:
        wipe_soft(api)
    elif not args.none:
        wipe_csv(api, args)

    if args.fav:
        wipe_fav(api)

    if args.dm:
        wipe_dm(api)

def main():
    args = arguments()
    api = build_api(toml_fname)
    wipe(api, args)

if __name__ == "__main__":
    main()
