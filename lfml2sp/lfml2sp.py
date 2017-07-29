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


def prompt(text, possible_values, color=None) -> str:
    """
    Prompts the user for an answer and checks if that answer is in the given possible values.
    :param text: Text shown to the user when asked for the answer.
    :param possible_values: Possible values that can be entered as Strings. Example: ['0', '1']
    :param color: Optional color to be shown when printing the Text.
    :return: A String with the answer given by the user which is one of the possible values.
    """
    while True:
        if color:
            print(color, end='')

        answer = input(text)

        if color:
            print(TerminalColors.ENDC, end='')

        if answer in possible_values:
            return answer

        print(TerminalColors.FAIL, end='')
        print('Invalid choice. Please, enter a valid value.')
        print(TerminalColors.ENDC, end='')


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
        self.playlist = None

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
                                               scope='playlist-modify-public '
                                                     'playlist-modify-private '
                                                     'playlist-read-private',
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
                                               scope='playlist-modify-public '
                                                     'playlist-modify-private '
                                                     'playlist-read-private',
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
        playlist_name = input('Enter the name of the new playlist: ')

        while True:
            if playlist_name is None or playlist_name == '':
                playlist_name = input('Enter a valid name:')
            else:
                break

        # Create the new playlist
        playlist = self.spotify.user_playlist_create(self.saved_config['spotify_username'],
                                                     playlist_name)
        self.saved_config['playlist_id'] = playlist['id']

    def select_playlist(self) -> None:
        """
        Allows the user to select an already existent playlist to use it later.
        """
        print('Here you have the names of all the playlist you can edit:')
        print(TerminalColors.WARNING, end='')
        print('Note: Due to Spotify API\'s restrictions you won\'t be able to select a collaborative playlist.')
        print(TerminalColors.ENDC, end='')

        all_playlists = self.spotify.current_user_playlists(limit=None)
        user_playlists = []
        possible_values = []

        # Iterate through every playlist of the user (the user's username is its owner id)
        # showing an index for the selection and saving those indexes as possible values
        for playlist in all_playlists['items']:
            if playlist['owner']['id'] == self.saved_config['spotify_username']:
                current_item = str(len(user_playlists))
                possible_values.append(current_item)
                print(current_item + ' -> ' + playlist['name'])
                user_playlists.append(playlist)

        # Get the selected playlist and save its ID
        answer = int(prompt('Enter your choice: ', possible_values))
        self.saved_config['playlist_id'] = user_playlists[answer]['id']

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

            answer = int(prompt('Enter your choice: ', ['0', '1']))

            if answer == 0:
                self.new_playlist()
            elif answer == 1:
                self.select_playlist()

            self.save_config()

        self.playlist = self.spotify.user_playlist(self.saved_config['spotify_username'],
                                                   self.saved_config['playlist_id'])

    def save_loved_tracks(self) -> None:
        """
        Fetches every loved track from LastFM and attempts to save it in the Spotify playlist that the user chose.
        """
        print(TerminalColors.OKBLUE, end='')
        print('Fetching your loved tracks from LastFM...')
        print(TerminalColors.ENDC, end='')

        try:
            lastfm_user = self.lastfm.get_user(self.saved_config['lastfm_username'])
            loved_tracks = lastfm_user.get_loved_tracks(limit=None)
        except pylast.LastFMNetwork:
            print(TerminalColors.FAIL, end='')
            print('There was an error fetching your loved tracks. Please, try again.')
            print(TerminalColors.ENDC, end='')
            exit(0)

        print(TerminalColors.OKBLUE, end='')
        print('Retrieved ' + str(len(loved_tracks)) + ' songs from your LastFM account.\n')

        # Here we will save every track ID we come across in Spotify
        spotify_tracks_id = []

        print('Retrieving current tracks from the Spotify playlist to check for duplicates...\n')

        # Get ALL the songs from the playlist. Necessary to use this one instead of the one stored
        # in the Object because the Spotify API limits 100 tracks per request, so the one saved won't
        # actually contain every song of the playlist
        songs_already_added = []
        current_playlist = self.spotify.user_playlist(self.saved_config['spotify_username'],
                                                      self.saved_config['playlist_id'],
                                                      fields="tracks,next")

        tracks = current_playlist['tracks']

        for playlist_track in tracks['items']:
            songs_already_added.append(playlist_track['track']['id'])

        # Keep'em coming!
        while tracks['next']:
            tracks = self.spotify.next(tracks)
            for playlist_track in tracks['items']:
                songs_already_added.append(playlist_track['track']['id'])

        print('Attempting to find the LastFM tracks in Spotify and adding them to the list...\n')

        for track in loved_tracks:
            track_query = track.track.artist.name + ' - ' + track.track.title
            print('Processing: ' + track_query)

            spotify_tracks = self.spotify.search(q=track_query, type='track')['tracks']

            if len(spotify_tracks['items']) > 0:
                track_id = spotify_tracks['items'][0]['id']

                # Check that the track isn't already added to the playlist
                if track_id not in songs_already_added:
                    print('Adding: ' + spotify_tracks['items'][0]['name'] + ' to the playlist.\n')
                    spotify_tracks_id.append(track_id)
                else:
                    print(TerminalColors.WARNING, end='')
                    print(track_query + ' is already on the playlist!\n')
                    print(TerminalColors.OKBLUE, end='')


            else:
                print(TerminalColors.WARNING, end='')
                print('No results found for ' + track_query + '\n')
                print(TerminalColors.OKBLUE, end='')

        # Check if there's anything to add
        if len(spotify_tracks_id) == 0:
            print('Nothing new to add!')
            print(TerminalColors.ENDC, end='')
            return
        else:
            print('Adding ' + str(len(spotify_tracks_id)) + ' tracks to your playlist...')

        # The Spotify API accepts a maximum of 100 tracks per request
        if len(spotify_tracks_id) > 100:
            # Split the list into chunks of 100 items
            chunks = [spotify_tracks_id[x:x + 100] for x in range(0, len(spotify_tracks_id), 100)]

            for chunk in chunks:
                self.spotify.user_playlist_add_tracks(self.saved_config['spotify_username'],
                                                      self.saved_config['playlist_id'],
                                                      chunk)
        else:
            self.spotify.user_playlist_add_tracks(self.saved_config['spotify_username'],
                                                  self.saved_config['playlist_id'],
                                                  spotify_tracks_id)

        print(TerminalColors.ENDC, end='')


def main():
    print(TerminalColors.BOLD, end='')
    print('Welcome to LastFMLoved2Spotify')
    print(TerminalColors.ENDC, end='')
    print('Your configuration files will be saved in: ' + CONFIG_FILE)

    app = Lfml2sp()
    app.playlist_definition()

    print(TerminalColors.WARNING)
    answer = prompt('Are you sure you want to save all your loved tracks from LastFM in the playlist '
                    + app.playlist['name'] + '? (y/n): ', ['y', 'n'], TerminalColors.WARNING)

    if answer == 'n':
        print('No problem! We will now delete the reference to that playlist so you can configure a new one next time.')
        app.saved_config.pop('playlist_id', None)
        app.save_config()
        exit(0)

    app.save_loved_tracks()
    print('All done! Check your playlist and enjoy the music!')


if __name__ == '__main__':
    main()
