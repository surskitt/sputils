import concurrent.futures
import itertools

from . import common


def track_to_dict_collected(api_track):
    common_dict = common.track_to_dict_common(api_track)

    return common_dict


def album_to_dict_collected(api_album):
    common_dict = common.album_to_dict_common(api_album['album'])

    collected = {
        'added': api_album['added_at'],
        'tracks': [track_to_dict_collected(t)
                   for t in api_album['album']['tracks']['items']],
    }

    return {**common_dict, **collected}


def collect_albums(sp, limit, offset):
    api_albums = sp.current_user_saved_albums(limit, offset)

    albums = [album_to_dict_collected(a) for a in api_albums['items']]

    return albums


def collect_playlists(sp, limit, offset):
    api_playlists = sp.current_user_playlists(limit, offset)

    playlists = [common.playlist_to_dict(p) for p in api_playlists['items']]

    return playlists


def collect_all_albums(sp, limit=50, workers=50):
    total_albums = sp.current_user_saved_albums(1)['total']

    args = common.limit_split(total_albums, 0, limit)

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


def collect_all_artists(sp, limit=50, workers=50):
    albums = collect_all_albums(sp, limit, workers)
    albums_sorted = sorted(albums, key=lambda x: x['artist'])

    g = itertools.groupby(albums_sorted,
                          key=lambda x: (x['artist'], x['artist_uri']))

    def artist_gen(k, a):
        return {
            'name': k[0],
            'uri': k[1],
            'albums': list(a)
        }

    return [artist_gen(k, a) for k, a in g]


def collect_all_playlists(sp, limit=50, workers=50):
    total_playlists = sp.current_user_playlists(1)['total']

    args = common.limit_split(total_playlists, 0, limit)

    def collector_helper(sp):
        def f(args):
            return collect_playlists(sp, *args)
        return f

    helper = collector_helper(sp)
    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        playlist_map = executor.map(helper, args)

    playlists = [i for s in playlist_map for i in s]
    return playlists


def collector(sp, resource):
    if resource == 'albums':
        return collect_all_albums(sp)
    if resource == 'tracks':
        return collect_all_tracks(sp)
    if resource == 'playlists':
        return collect_all_playlists(sp)
    if resource == 'artists':
        return collect_all_artists(sp)

    raise ValueError(f'{resource} is not a valid collector resource')
