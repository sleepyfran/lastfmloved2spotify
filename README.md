# LastFMLoved2Spotify
This script allows you to easily sync your *loved* tracks from **LastFM** into a **Spotify** playlist. 🎧

## Usage
In order to use *lastfmloved2spotify* you'll need Python 3 or higher installed in your system with these libraries:

- [spotipy](https://github.com/plamere/spotipy)
- [pylast](https://github.com/pylast/pylast)

Once you have everything ready simply clone this repository or download one of the releases. 

After that you'll need to define the *api keys* that well be used by the application in order to work. To do so, create a Python file in the *lfml2sp* folder with the name *api_keys.py* with this content:

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
