#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sputils` package."""

import pytest
import unittest.mock

import deepdiff


from sputils import sputils


@unittest.mock.patch('sputils.sputils.os')
def test_get_api_dict(mock_os):
    def mock_os_lambda(x):
        return x.replace('~', '/home/test')
    mock_os.path.expanduser.side_effect = mock_os_lambda

    expected = {
        'username': 'testuser',
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'redirect_uri': 'http://localhost',
        'scope': 'user-library-read',
        'cache_path': '/home/test/.cache/sputils/user_cache'
    }

    api_dict_params = ('testuser', 'test_client_id', 'test_client_secret')
    api_dict = sputils.get_api_dict(*api_dict_params)

    assert deepdiff.DeepDiff(api_dict, expected) == {}


@unittest.mock.patch('sputils.sputils.spotipy')
def test_get_spotify_client(spotipy_mock):
    expected = spotipy_mock.Spotify()

    sp_params = ('testuser', 'test_client_id', 'test_client_secret')
    sp = sputils.get_spotify_client(*sp_params)

    assert sp == expected


@unittest.mock.patch('sputils.sputils.spotipy')
def test_get_spotify_client_token_failed(spotipy_mock):
    spotipy_mock.util.prompt_for_user_token.return_value = None

    exception_msg = 'Unable to retrieve authentication token'
    with pytest.raises(RuntimeError, match=exception_msg):
        sp_params = ('testuser', 'test_client_id', 'test_client_secret')
        sp = sputils.get_spotify_client(*sp_params)
