from . import common


def album_to_dict_searched(api_dict):
    return common.album_to_dict_common(api_dict)


def track_to_dict_searched(api_dict):
    common_dict = common.track_to_dict_common(api_dict)

    searched = {
        'album': {
            'name': api_dict['album']['name'],
            'uri': api_dict['album']['uri'],
            'release_date': api_dict['album']['release_date'],
            'art_url': api_dict['album']['images'][0]['url']
        }
    }

    return {**common_dict, **searched}


def search_albums(sp, qry):
    searched = sp.search(qry, type='album', limit=50)

    return [album_to_dict_searched(a) for a in searched['albums']['items']]


def search_tracks(sp, qry):
    searched = sp.search(qry, type='track', limit=50)

    return [track_to_dict_searched(t) for t in searched['tracks']['items']]


def artist_to_dict_searched(api_dict):
    return {
        'name': 'artist1, artist2',
        'uri': 'uri'
    }


def search_artist(sp, qry):
    searched = sp.search(qry, type='artist', limit=50)

    return [artist_to_dict_searched(a) for a in searched['artists']['items']]


def searcher(sp, qry, resource):
    if resource == 'albums':
        return search_albums(sp, qry)
    if resource == 'tracks':
        return search_tracks(sp, qry)
