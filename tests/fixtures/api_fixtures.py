import pytest
import unittest.mock

import helpers


@pytest.fixture
@unittest.mock.patch('sputils.auth.spotipy')
def sp_mock(sp_mock, api_album_collected, api_playlist):
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
            'items': [api_album_collected['album']]
        }
    }

    return sp_mock


@pytest.fixture
def api_track():
    return helpers.mock_json('mocks/api/track_collected.json')


@pytest.fixture
def api_album_collected():
    return helpers.mock_json('mocks/api/album_collected.json')


@pytest.fixture
def api_album_searched():
    return helpers.mock_json('mocks/api/album_searched.json')


@pytest.fixture
def api_playlist():
    return helpers.mock_json('mocks/api/playlist.json')
