import json
import yaml


def track_to_dict_common(api_track):
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
        'art_url': api_album['images'][0]['url'],
        'artist_uri': api_album['artists'][0]['uri']
    }


def playlist_to_dict(api_playlist):
    return {
        'name': api_playlist['name'],
        'uri': api_playlist['uri'],
        'art_url': api_playlist['images'][0]['url'],
        'length': api_playlist['tracks']['total']
    }


def limit_split(lmax, start=0, limit=50):
    return [(limit, offset) for offset in range(start, lmax, limit)]


def format_dict(d, format_string):
    return format_string.format(**d)


def format_lines(items, line_format):
    return '\n'.join(format_dict(line, line_format) for line in items)


def formatter(items, output_format, line_format):
    if output_format == 'json':
        return json.dumps(items, indent=4)
    if output_format == 'lines':
        return format_lines(items, line_format)
    if output_format == 'yaml':
        return yaml.dump(items)
