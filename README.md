# Wipe all your tweets.

## __How to__ ?
* Download zip archive of your tweets from [twitter](https://twitter.com/settings/account)
* Extract `tweets.csv` ( into wtweets current dir )
* Create your own twitter application [here](https://apps.twitter.com/)
    1. Permissions tab :
        - Set "Read and Write" access.
    2. Keys and Access Tokens tab :
        - Generate consumer key & secret (if not yet done)
        - Generate access token & access token secret
* Once generated, copy credentials into `credentials.toml` file.

## __Run__ :
__WARNING:__   
_This will delete all your tweets, beyond the 3200 tweets API limitation._
```
# pip install -r requirements.txt
python3 wtweets.py
```

__TODO__
1. Threads support ?
