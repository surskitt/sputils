import pytest

import helpers


@pytest.fixture
def api_track():
    return helpers.mock_json('mocks/api/track.json')


@pytest.fixture
def api_album_collected():
    return helpers.mock_json('mocks/api/album_collected.json')


@pytest.fixture
def api_album_searched():
    return helpers.mock_json('mocks/api/album_searched.json')


@pytest.fixture
def api_playlist():
    return helpers.mock_json('mocks/api/playlist.json')
