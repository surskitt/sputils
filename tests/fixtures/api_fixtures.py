import pytest
import unittest.mock

import helpers


@pytest.fixture
@unittest.mock.patch('sputils.auth.spotipy')
def sp_mock(sp_mock, api_album_searched, api_album_collected, api_playlist,
            api_track_searched, api_artist_searched):
    sp_mock.Spotify.return_value.current_user_saved_albums.return_value = {
        'items': [api_album_collected],
        'total': 2
    }

    sp_mock.Spotify.return_value.current_user_playlists.return_value = {
        'items': [api_playlist],
        'total': 2
    }

    sp_mock.Spotify.return_value.search.return_value = {
        'albums': {
            'items': [api_album_searched]
        },
        'tracks': {
            'items': [api_track_searched]
        },
        'artists': {
            'items': [api_artist_searched]
        }
    }

    return sp_mock


@pytest.fixture
def api_track_collected():
    return helpers.mock_json('mocks/api/track_collected.json')


@pytest.fixture
def api_track_searched():
    return helpers.mock_json('mocks/api/track_searched.json')


@pytest.fixture
def api_album_collected():
    return helpers.mock_json('mocks/api/album_collected.json')


@pytest.fixture
def api_album_searched():
    return helpers.mock_json('mocks/api/album_searched.json')


@pytest.fixture
def api_playlist():
    return helpers.mock_json('mocks/api/playlist.json')


@pytest.fixture
def api_artist_searched():
    return helpers.mock_json('mocks/api/artist_searched.json')
