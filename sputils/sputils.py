# -*- coding: utf-8 -*-

"""Main module."""

import os

import spotipy
import spotipy.util


def get_api_dict(user, client_id, client_secret):
    """ Retrieve an api dictionary with params for spotify client object """
    return {
        'username': user,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost',
        'scope': 'user-library-read',
        'cache_path': os.path.expanduser('~/.cache/sputils/user_cache')
    }


def get_spotify_client(user, client_id, client_secret):
    """ Retrieve a token using api details and return client object """

    api = get_api_dict(user, client_id, client_secret)

    # retrieve token, asking user to auth in browser if necessary
    token = spotipy.util.prompt_for_user_token(**api)
    if not token:
        raise RuntimeError('Unable to retrieve authentication token')

    return spotipy.Spotify(auth=token)


def track_to_dict(api_track):
    return {
        'artist': ', '.join(a['name'] for a in api_track['artists']),
        'track': float('{}.{:02d}'.format(api_track['disc_number'],
                                          api_track['track_number'])),
        'name': api_track['name'],
        'uri': api_track['uri']
    }


def album_to_dict(api_album):
    return {
        'artist': ', '.join(a['name'] for a in api_album['album']['artists']),
        'name': api_album['album']['name'],
        'added': api_album['added_at'],
        'tracks': [track_to_dict(t)
                   for t in api_album['album']['tracks']['items']],
        'uri': api_album['album']['uri'],
        'art_url': api_album['album']['images'][0]['url']
    }
