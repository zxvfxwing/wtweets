# Wipe all your tweets.
> More delete options will come.

## How to ?
__mass delete tweets :__
* Go into your [twitter account settings](https://twitter.com/settings/account) and ask for your tweets archive (bottom of the page).
* Check your mailbox (the one associated with your twitter account) and download the zip archive.
* Now extract `tweets.csv` from the downloaded archive into __wtweets__'s directory.

__make the script work :__
* Create your own twitter application [here](https://apps.twitter.com/)
    1. Permissions tab :
        - Set "__Read and Write__" access.
    2. Keys and Access Tokens tab :
        - Generate __consumer key__ & __consumer secret__ (normally done at app creation) ;
        - Generate __access token__ & __access token secret__.
* Once generated, copy these four credentials in their respective places in the `credentials.toml` file.
* You are ready to go.

## Why are we using a csv file to proceed mass deletion ?
The twitter API sets a limit of 3200 tweets recovered per user.  
By parsing csv file, we can retrieve tweets ID (and more) directly and without worries.

## Dependancies :
```
# pip install -r requirements.txt
```

## Usage :
```
usage: wtweets.py [-h] [--csv [FILENAME] | -s | -n] [-f] [-d]

optional arguments:
  -h, --help        show this help message and exit
  --csv [FILENAME]  use csv file for mass removal of tweets
  -s, --soft        wipe your 3200 newer tweets
  -n, --none        do not proceed to tweets deletion
  -f, --fav         wipe your favorites/likes
  -d, --dm          wipe your direct messages
```

## Run examples :

1. Mass delete tweets using `tweets.csv` :
```
python3 wtweets.py
```
2. Mass delete tweets + favorites deletion
```
python3 wtweets.py -f
```
3. Only delete your favorites :
```
python3 wtweets.py -n -f
```

