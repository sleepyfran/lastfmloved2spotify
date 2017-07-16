#!/usr/bin/env python
# Made with <3 by Fran González (@spaceisstrange)
#
# This file belongs to: https://github.com/spaceisstrange/lastfmloved2spotify
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import os
import json
import pylast
import spotipy
import spotipy.util as util
from api_keys import *

# Paths to configuration files
CONFIG_FILE = os.path.expanduser("~") + "/.lastfmloved2spotify.json"


class TerminalColors:
    """
    Prints colors in the terminal. Taken from: https://stackoverflow.com/a/287944/6811219
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Lfml2sp(object):
    """
    Main object of the application. Contains all the interaction necessary with both of the APIs and the core
    functionality of the script.
    """

    def __init__(self):
        """
        Initializes the class with null values to be initialized later.
        """
        self.lastfm = None
        self.spotify = None
        self.saved_config = {}

        if not os.path.exists(CONFIG_FILE):
            self.initial_config()
        else:
            self.load_config()

    def load_config(self) -> None:
        """
        Loads the configuration from the JSON file and initializes the LastFM and Spotify instances.
        """
        with open(CONFIG_FILE, "r") as f:
            self.saved_config = json.loads(f.read())

        # Attempt to login with the saved data
        try:
            self.lastfm = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY,
                                               api_secret=LAST_FM_SHARED_SECRET,
                                               username=self.saved_config['lastfm_username'],
                                               password_hash=self.saved_config['lastfm_password_hash'])

            print(TerminalColors.OKBLUE, end='')
            print('Logged to LastFM as ' + self.saved_config['lastfm_username'])
            print(TerminalColors.ENDC, end='')
        except pylast.WSError:
            print(TerminalColors.FAIL, end='')
            print('There was an error login you into your account with the saved data.')
            print('We will now remove the saved data and ask you to login again.')
            print(TerminalColors.ENDC, end='')
            os.remove(CONFIG_FILE)
            self.initial_config()

        try:
            token = util.prompt_for_user_token(self.saved_config['spotify_username'],
                                               scope='playlist-modify-public',
                                               client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri='http://localhost:8888/callback')

            self.spotify = spotipy.Spotify(auth=token)

            print(TerminalColors.OKBLUE, end='')
            print('Logged to Spotify as ' + self.saved_config['spotify_username'])
            print(TerminalColors.ENDC, end='')
        except spotipy.SpotifyException:
            print(TerminalColors.FAIL, end='')
            print('There was an error login you into your Spotify account. Did you grant access to it?')
            print(TerminalColors.ENDC, end='')
            exit()

    def save_config(self) -> None:
        """
        Saves the configuration into the JSON file given a dictionary containing the information to save.
        """
        with open(CONFIG_FILE, "w") as f:
            f.write(json.dumps(self.saved_config, indent=4))

    def initial_config(self) -> None:
        """
        Guides the user through the app setup. Logs them into LastFM and Spotify.
        """
        print(TerminalColors.OKBLUE)
        print('Let\'s start by login you into LastFM and Spotify.')
        username = input('Enter your LastFM username: ')
        password = input('Enter your LastFM password: ')
        print(TerminalColors.ENDC)
        password_hash = pylast.md5(password)

        # Attempt to log in with the provided data
        try:
            self.lastfm = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY,
                                               api_secret=LAST_FM_SHARED_SECRET,
                                               username=username,
                                               password_hash=password_hash)

            # Let's save the provided data so far
            self.saved_config['lastfm_username'] = username
            self.saved_config['lastfm_password_hash'] = password_hash
        except pylast.WSError:
            print(TerminalColors.FAIL, end='')
            print('There was an error login you into your account.')
            print('Check you entered the correct username and password and try again.')
            print(TerminalColors.ENDC, end='')
            exit()

        # We're logged in!
        print(TerminalColors.OKGREEN, end='')
        print('Successfully logged into your LastFM account. Welcome, ' + username + '. ', end='')
        print('Now let\'s log into Spotify.')
        print(TerminalColors.OKBLUE, end='')
        username = input('Enter your Spotify username: ')
        print(TerminalColors.ENDC, end='')

        try:
            token = util.prompt_for_user_token(username,
                                               scope='playlist-modify-public',
                                               client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri='http://localhost:8888/callback')
        except spotipy.SpotifyException:
            print(TerminalColors.FAIL, end='')
            print('There was an error login you into your Spotify account. Did you grant access to it?')
            print(TerminalColors.ENDC, end='')
            exit()

        self.spotify = spotipy.Spotify(auth=token)

        # Save the username and token
        self.saved_config['spotify_username'] = username

        # Save the configuration file
        self.save_config()

    def new_playlist(self) -> None:
        """
        Creates a new playlist in the user's account and saves its ID to use it later.
        """
        playlist_name = input('Enter the name of the new playlist:')

        while True:
            if playlist_name is None or playlist_name == '':
                playlist_name = input('Enter a valid name:')
            else:
                break

        # Create the new playlist
        self.spotify.user_playlist_create(self.saved_config['spotify_username'],
                                          playlist_name)

    def playlist_definition(self) -> None:
        """
        Asks the user whether the playlist in which the songs are going to be saved will be new or an already
        created playlist. Checks first if we have created a playlist already.
        """
        if 'playlist_id' not in self.saved_config:
            print('You haven\'t defined a playlist to save the songs yet.')
            print('Do you want to save them in a new playlist or an existent one?')
            print('0 -> New playlist')
            print('1 -> Existent playlist')

            while True:
                try:
                    prompt = int(input('Enter your choice: '))

                    if prompt in [0, 1]:
                        break
                except ValueError:
                    pass

                print(TerminalColors.FAIL, end='')
                print('Invalid choice. Please enter either 0 or 1.')
                print(TerminalColors.ENDC, end='')

            if prompt == 0:
                self.new_playlist()
            elif prompt == 1:
                self.new_playlist()

            self.save_config()
        else:
            playlist = self.spotify.user_playlist(self.saved_config['spotify_username'],
                                                  self.saved_config['playlist_id'])


def main():
    print(TerminalColors.BOLD, end='')
    print('Welcome to LastFMLoved2Spotify')
    print(TerminalColors.ENDC, end='')
    print('Your configuration files will be saved in: ' + CONFIG_FILE)

    app = Lfml2sp()
    app.playlist_definition()


if __name__ == '__main__':
    main()
