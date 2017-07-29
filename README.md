# LastFMLoved2Spotify 
![](http://forthebadge.com/images/badges/built-with-swag.svg)
![](http://forthebadge.com/images/badges/made-with-python.svg)

A simple script that allows you to easily sync your *loved* tracks from **LastFM** into a **Spotify** playlist. 🎧

## How to run the script

### Requirements
In order to use *lastfmloved2spotify* you'll need Python 3 or higher installed in your system with these libraries:

- **[spotipy](https://github.com/plamere/spotipy)**
- **[pylast](https://github.com/pylast/pylast)**

You'll also need a **LastFM API Account** that you can make over [here](https://www.last.fm/api/account/create) and a **Spotify Web API Application** which you can create [here](https://developer.spotify.com/my-applications/#!/applications/create). Be sure to save the account/application details for later, you're going to need them!

### Aaaaand there we go!

Once you have everything ready simply **clone** this repository or grab one of the **latests [releases](https://github.com/spaceisstrange/lastfmloved2spotify/releases)**.

After that you'll need to define the *api keys* that will be used by the application in order to work. Remember those nice keys you got when creating the account and the application? Now it's their moment of glory! Create a Python file in the *lfml2sp* folder with the name *api_keys.py* and this content:

```
LAST_FM_API_KEY = '<Your LastFM API Key>'
LAST_FM_SHARED_SECRET = '<Yout LastFM Shared Secret>'

SPOTIFY_CLIENT_ID = '<Your Spotify Client ID>'
SPOTIFY_CLIENT_SECRET = '<Your Spotify Client Secret>'

```

Then navigate through the terminal to the folder in which you downloaded the project, enter the *lfml2sp* folder and execute:

```
python3 lfml2sp.py
```

After that simply follow the on-screen instructions and enjoy your music! 

## Hacking & requests
This is basically a quick script I made to solve my lazyness of syncing my LastFM favorites with Spotify, so don't expect any pretty code! If you feel that anything should be changed I'm open to any changes. Be sure to open an issue if you miss something too!