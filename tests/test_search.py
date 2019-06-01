import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils

import helpers


def test_album_to_dict_searched(api_album_searched, album_dict_searched):
    album = sputils.album_to_dict_searched(api_album_searched)

    assert deepdiff.DeepDiff(album, album_dict_searched) == {}


def test_search_album(sp_mock, api_album_searched, album_dict_searched):
    sp = sp_mock.Spotify()

    expected = [album_dict_searched]

    search = sputils.search_albums(sp, 'test')

    assert deepdiff.DeepDiff(search, expected) == {}


@unittest.mock.patch('sputils.sputils.search_albums')
def test_searcher(mock_sa, sp_mock):
    sp = sp_mock.Spotify()

    sputils.searcher(sp, 'test', 'albums')
    mock_sa.assert_called_once()
