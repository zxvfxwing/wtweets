# Wipe all your tweets.
> More delete options will come.

## __How to__ ?
* Go into your [twitter account settings](https://twitter.com/settings/account) and ask for your tweets archive (bottom of the page).
* Check your mailbox (the one associated with your twitter account) and download the zip archive.
* Now extract `tweets.csv` from the downloaded archive into __wtweets__'s directory.
* Create your own twitter application [here](https://apps.twitter.com/)
    1. Permissions tab :
        - Set "Read and Write" access.
    2. Keys and Access Tokens tab :
        - Generate __consumer key__ & __consumer secret__ (normally done at app creation) ;
        - Generate __access token__ & __access token secret__.
* Once generated, copy these four credentials in their respective places in the `credentials.toml` file.
* You are ready to go.

## __Run__ :
__WARNING:__   
_The current version of wtweets will delete __all__ your tweets, beyond the 3200 tweets API limitation._  
No options to choose a specific date yet.
```
# pip install -r requirements.txt
python3 wtweets.py
```

__TODO__
1. Threads support ?
2. CLI options
