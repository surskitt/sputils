import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils

import helpers


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
