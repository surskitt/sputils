import unittest.mock

import deepdiff

from sputils import search


def test_album_to_dict_searched(api_album_searched, album_dict_searched):
    album = search.album_to_dict_searched(api_album_searched)

    assert deepdiff.DeepDiff(album, album_dict_searched) == {}


def test_search_album(sp_mock, api_album_searched, album_dict_searched):
    sp = sp_mock.Spotify()

    expected = [album_dict_searched]

    searched = search.search_albums(sp, 'test')

    assert deepdiff.DeepDiff(searched, expected) == {}


@unittest.mock.patch('sputils.search.search_albums')
def test_searcher(mock_sa, sp_mock):
    sp = sp_mock.Spotify()

    search.searcher(sp, 'test', 'albums')
    mock_sa.assert_called_once()
