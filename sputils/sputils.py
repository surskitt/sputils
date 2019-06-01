# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys
import concurrent.futures
import textwrap
import json
from argparse import RawTextHelpFormatter

import spotipy
import spotipy.util
import configargparse
import yaml


def parse_args(args):
    desc = 'A collection of spotify utilities for use with other shell utils.'
    cfgfiles = ['/etc/sputils.d/*.conf', '~/.config/sputils/*.conf']
    parser = configargparse.ArgParser(default_config_files=cfgfiles,
                                      description=desc,
                                      formatter_class=RawTextHelpFormatter)
    parser.add('-c', '--config', is_config_file=True,
               help='config file path')

    parser.add('-u', '--user', type=str, required=True,
               help='spotify user')
    parser.add('--client_id', type=str, required=True,
               help='spotify client id')
    parser.add('--client_secret', type=str, required=True,
               help='spotify client secret')

    actions = ['collect', 'search', 'query', 'save', 'delete', 'reccomend',
               'follow', 'following']
    actions_desc = '''\
                   collect: collect resources from saved collection
                   search: search spotify for resources
                   query: query a set of resource on their uris
                   add: add resource to collection
                   delete: delete resource from collection
                   reccomend: return reccomendations based on given uris
                   follow: follow artist
                   following: query resources based on followed artists
                   '''
    parser.add('-a', '--action', choices=actions, default='collect',
               help=textwrap.dedent(actions_desc))

    resources = ['artists', 'albums', 'tracks', 'playlists']
    parser.add('-r', '--resource', choices=resources, default='albums',
               help='resource to query')

    format_choices = ['json', 'lines', 'yaml']
    parser.add('-f', '--format', choices=format_choices, default='json',
               help='output format')
    parser.add('-l', '--line_format', default='{name}', type=str,
               help='format for outputting lines, accepts json keys')

    query_help = 'query (valid for search, add, delete, reccomend and follow)'
    parser.add('query', nargs='*', help=query_help)

    args = parser.parse_args(args)

    if args.action in ['search', 'query', 'save', 'delete', 'reccomend',
                       'follow'] and args.query == []:
        parser.error('a query is needed for this action')

    return args


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


def album_to_dict_common(api_album):
    return {
        'artist': ', '.join(a['name'] for a in api_album['artists']),
        'name': api_album['name'],
        'uri': api_album['uri'],
        'art_url': api_album['images'][0]['url']
    }


def album_to_dict_collected(api_album):
    common = album_to_dict_common(api_album['album'])

    collected = {
        'added': api_album['added_at'],
        'tracks': [track_to_dict(t)
                   for t in api_album['album']['tracks']['items']],
    }

    return {**common, **collected}


def playlist_to_dict(api_playlist):
    return {
        'name': api_playlist['name'],
        'uri': api_playlist['uri'],
        'art_url': api_playlist['images'][0]['url'],
        'length': api_playlist['tracks']['total']
    }


def limit_split(lmax, start=0, limit=50):
    return [(limit, offset) for offset in range(start, lmax, limit)]


def collect_albums(sp, limit, offset):
    api_albums = sp.current_user_saved_albums(limit, offset)

    albums = [album_to_dict_collected(a) for a in api_albums['items']]

    return albums


def collect_playlists(sp, limit, offset):
    api_playlists = sp.current_user_playlists(limit, offset)

    playlists = [playlist_to_dict(p) for p in api_playlists['items']]

    return playlists


def collect_all_albums(sp, limit=50, workers=50):
    total_albums = sp.current_user_saved_albums(1)['total']

    args = limit_split(total_albums, 0, limit)

    def collector_helper(sp):
        def f(args):
            return collect_albums(sp, *args)
        return f

    helper = collector_helper(sp)
    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        album_map = executor.map(helper, args)

    albums = [i for s in album_map for i in s]
    return sorted(albums, key=lambda x: x['added'], reverse=True)


def collect_all_tracks(sp, limit=50, workers=50):
    albums = collect_all_albums(sp, limit, workers)

    def album_tracks(album):
        album_dict = {
            'albumartist': album['artist'],
            'album': album['name'],
            'added': album['added'],
            'art_url': album['art_url']
        }
        return [{**t, **album_dict} for t in album['tracks']]

    tracks = [i for s in albums for i in album_tracks(s)]

    return tracks


def collect_all_playlists(sp, limit=50, workers=50):
    total_playlists = sp.current_user_playlists(1)['total']

    args = limit_split(total_playlists, 0, limit)

    def collector_helper(sp):
        def f(args):
            return collect_playlists(sp, *args)
        return f

    helper = collector_helper(sp)
    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        playlist_map = executor.map(helper, args)

    playlists = [i for s in playlist_map for i in s]
    return playlists


def format_dict(d, format_string):
    return format_string.format(**d)


def format_lines(items, line_format):
    return '\n'.join(format_dict(line, line_format) for line in items)


def collector(sp, resource):
    if resource == 'albums':
        return collect_all_albums(sp)
    if resource == 'tracks':
        return collect_all_tracks(sp)
    if resource == 'playlists':
        return collect_all_playlists(sp)


def formatter(items, output_format, line_format):
    if output_format == 'json':
        return json.dumps(items, indent=4)
    if output_format == 'lines':
        return format_lines(items, line_format)
    if output_format == 'yaml':
        return yaml.dump(items)


def album_to_dict_searched(api_dict):
    return album_to_dict_common(api_dict)


def search_albums(sp, qry):
    search = sp.search(qry, type='album', limit=50)

    return [album_to_dict_searched(a) for a in search['albums']['items']]


def searcher(sp, qry, resource):
    if resource == 'albums':
        return search_albums(sp, qry)


def main():
    args = parse_args(sys.argv[1:])

    # Create cache dir
    try:
        os.makedirs(os.path.expanduser('~/.cache/sputils'))
    except FileExistsError:
        pass

    sp = get_spotify_client(args.user, args.client_id, args.client_secret)

    if args.action == 'collect':
        items = collector(sp, args.resource)
    elif args.action == 'search':
        qry = ' '.join(args.query)
        items = searcher(sp, qry, args.resource)

    if args.action in ['collect', 'search']:
        out = formatter(items, args.format, args.line_format)
        print(out)
