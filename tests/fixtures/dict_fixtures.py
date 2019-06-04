import pytest

import helpers


@pytest.fixture
def track_dict_collected():
    return helpers.mock_json('mocks/dicts/track_collected.json')


@pytest.fixture
def track_dict_searched():
    return helpers.mock_json('mocks/dicts/track_searched.json')


@pytest.fixture
def album_dict_common():
    return helpers.mock_json('mocks/dicts/album_common.json')


@pytest.fixture
def album_dict_collected():
    return helpers.mock_json('mocks/dicts/album_collected.json')


@pytest.fixture
def album_dict_searched():
    return helpers.mock_json('mocks/dicts/album_searched.json')


@pytest.fixture
def playlist_dict():
    return helpers.mock_json('mocks/dicts/playlist.json')


@pytest.fixture
def artist_dict_searched():
    return helpers.mock_json('mocks/dicts/artist_searched.json')
