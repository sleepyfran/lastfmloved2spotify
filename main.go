/*
lastfmloved2spotify
Copyright (C) 2018 Fran González (@spaceisstrange)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

package main

import (
	"os"

	"github.com/fatih/color"
	"github.com/urfave/cli"
)

func main() {
	// Vars used to hold the API keys.
	var lastfmAPIKey string
	var lastfmAPISecret string
	var spotifyClientID string
	var spotifyClientSecret string

	// Market that will be used when querying tracks from Spotify.
	var market string

	// CLI app configuration.
	app := cli.NewApp()
	app.Name = "lastfm2spotify"
	app.Version = "2.0"
	app.Usage = "import your LastFM loved tracks to a Spotify playlist"

	// Flags of the program.
	app.Flags = []cli.Flag{
		// Last.fm API Key.
		cli.StringFlag{
			Name:        "lastfm-api-key, lfmkey",
			Value:       "",
			Usage:       "Last.fm API key that will be used to query data from the API",
			EnvVar:      "LASTFM_API_KEY",
			Destination: &lastfmAPIKey,
		},

		// Last.fm API Secret.
		cli.StringFlag{
			Name:        "lastfm-api-secret, lfmsecret",
			Value:       "",
			Usage:       "Last.fm API secret that will be used to query data from the API",
			EnvVar:      "LASTFM_API_SECRET",
			Destination: &lastfmAPISecret,
		},

		// Spotify Client ID.
		cli.StringFlag{
			Name:        "spotify-client-id, scid",
			Value:       "",
			Usage:       "Spotify Client ID that will be used to query data from the API",
			EnvVar:      "SPOTIFY_CLIENT_ID",
			Destination: &spotifyClientID,
		},

		// Spotify Client Secret.
		cli.StringFlag{
			Name:        "spotify-client-secret, scs",
			Value:       "",
			Usage:       "Spotify Client Secret that will be used to query data from the API",
			EnvVar:      "SPOTIFY_CLIENT_SECRET",
			Destination: &spotifyClientSecret,
		},

		// Spotify market flag.
		cli.StringFlag{
			Name:        "market, m",
			Value:       "US",
			Usage:       "market that will be used when querying data from the Spotify API",
			Destination: &market,
		},
	}

	// Action of the app.
	app.Action = func(c *cli.Context) error {
		// Check that the necessary API keys and secrets have been provided.
		if lastfmAPIKey == "" {
			color.Red("No LastFM API Key provided. See lastfmloved2spotify -h for help")
			return nil
		}

		if lastfmAPISecret == "" {
			color.Red("No LastFM API Secret provided. See lastfmloved2spotify -h for help")
			return nil
		}

		if spotifyClientID == "" {
			color.Red("No Spotify Client ID provided. See lastfmloved2spotify -h for help")
			return nil
		}

		if spotifyClientSecret == "" {
			color.Red("No Spotify Client Secret provided. See lastfmloved2spotify -h for help")
			return nil
		}

		return nil
	}

	app.Run(os.Args)
}
