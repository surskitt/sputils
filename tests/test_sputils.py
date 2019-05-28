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


def api_track():
    return {
        'artists': [{'name': 'artist1'}, {'name': 'artist2'}],
        'track_number': 1,
        'disc_number': 1,
        'name': 'track',
        'uri': 'uri'
    }


def track_dict():
    return {
        'artist': 'artist1, artist2',
        'track': 1.01,
        'name': 'track',
        'uri': 'uri'
    }


def api_album():
    return {
        'added_at': 'mtime',
        'album': {
            'artists': [{'name': 'artist1'}, {'name': 'artist2'}],
            'name': 'album',
            'tracks': {'items': [api_track()]},
            'uri': 'uri',
            'images': [{'url': 'art_url'}]
        }
    }


def album_dict():
    return {
        'artist': 'artist1, artist2',
        'name': 'album',
        'added': 'mtime',
        'tracks': [track_dict()],
        'uri': 'uri',
        'art_url': 'art_url'
    }


def test_track_to_dict():

    track = sputils.track_to_dict(api_track())

    assert deepdiff.DeepDiff(track, track_dict()) == {}


def test_album_to_dict():
    album = sputils.album_to_dict(api_album())

    assert deepdiff.DeepDiff(album, album_dict()) == {}


def test_limit_split():
    expected = [(50, 100), (50, 150), (50, 200), (50, 250)]

    splits = sputils.limit_split(290, 100, 50)

    assert splits == expected


@unittest.mock.patch('sputils.sputils.spotipy')
def test_get_albums(sp_mock):
    sp_mock.Spotify.return_value.current_user_saved_albums.return_value = {
        'items': [api_album()]
    }

    expected = [album_dict()]

    sp = sp_mock.Spotify()
    albums = sputils.get_albums(sp, 1, 0)

    assert deepdiff.DeepDiff(albums, expected) == {}


@unittest.mock.patch('sputils.sputils.spotipy')
def test_collect_albums(sp_mock):
    sp_mock.Spotify.return_value.current_user_saved_albums.return_value = {
        'items': [api_album()],
        'total': 2
    }

    expected = [album_dict(), album_dict()]

    sp = sp_mock.Spotify()
    albums = sputils.collect_albums(sp, 1)

    assert deepdiff.DeepDiff(albums, expected) == {}


@unittest.mock.patch('sputils.sputils.spotipy')
def test_collect_tracks(sp_mock):
    sp_mock.Spotify.return_value.current_user_saved_albums.return_value = {
        'items': [api_album()],
        'total': 2
    }

    expected = [track_dict(), track_dict()]

    sp = sp_mock.Spotify()
    tracks = sputils.collect_tracks(sp, 1)

    assert deepdiff.DeepDiff(tracks, expected) == {}
