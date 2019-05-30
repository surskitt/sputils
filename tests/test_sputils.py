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
        sputils.get_spotify_client(*sp_params)


@pytest.fixture
def api_track():
    return {
        'artists': [{'name': 'artist1'}, {'name': 'artist2'}],
        'track_number': 1,
        'disc_number': 1,
        'name': 'track',
        'uri': 'uri'
    }


@pytest.fixture
def track_dict():
    return {
        'artist': 'artist1, artist2',
        'track': 1.01,
        'name': 'track',
        'uri': 'uri'
    }


@pytest.fixture
def api_album():
    return {
        'added_at': 'mtime',
        'album': {
            'artists': [{'name': 'artist1'}, {'name': 'artist2'}],
            'name': 'album',
            'tracks': {
                'items': [
                    {
                        'artists': [{'name': 'artist1'}, {'name': 'artist2'}],
                        'track_number': 1,
                        'disc_number': 1,
                        'name': 'track',
                        'uri': 'uri'
                    }
                ]
            },
            'uri': 'uri',
            'images': [{'url': 'art_url'}]
        }
    }


@pytest.fixture
def album_dict():
    return {
        'artist': 'artist1, artist2',
        'name': 'album',
        'added': 'mtime',
        'tracks': [
            {
                'artist': 'artist1, artist2',
                'track': 1.01,
                'name': 'track',
                'uri': 'uri'
            }
        ],
        'uri': 'uri',
        'art_url': 'art_url'
    }


def test_track_to_dict(api_track, track_dict):
    track = sputils.track_to_dict(api_track)

    assert deepdiff.DeepDiff(track, track_dict) == {}


def test_album_to_dict(api_album, album_dict):
    album = sputils.album_to_dict(api_album)

    assert deepdiff.DeepDiff(album, album_dict) == {}


def test_limit_split():
    expected = [(50, 100), (50, 150), (50, 200), (50, 250)]

    splits = sputils.limit_split(290, 100, 50)

    assert splits == expected


@pytest.fixture
@unittest.mock.patch('sputils.sputils.spotipy')
def sp_mock(sp_mock, api_album, api_playlist):
    sp_mock.Spotify.return_value.current_user_saved_albums.return_value = {
        'items': [api_album],
        'total': 2
    }

    sp_mock.Spotify.return_value.current_user_playlists.return_value = {
        'items': [api_playlist],
        'total': 2
    }

    return sp_mock


def test_get_albums(sp_mock, album_dict):
    expected = [album_dict]

    sp = sp_mock.Spotify()
    albums = sputils.get_albums(sp, 1, 0)

    assert deepdiff.DeepDiff(albums, expected) == {}


def test_collect_albums(sp_mock, album_dict):
    expected = [album_dict, album_dict]

    sp = sp_mock.Spotify()
    albums = sputils.collect_albums(sp, 1)

    assert deepdiff.DeepDiff(albums, expected) == {}


def test_collect_tracks(sp_mock, track_dict):
    ad = {
        'albumartist': 'artist1, artist2',
        'album': 'album',
        'added': 'mtime',
        'art_url': 'art_url',
    }
    td = {**track_dict, **ad}

    expected = [td, td]

    sp = sp_mock.Spotify()
    tracks = sputils.collect_tracks(sp, 1)

    assert deepdiff.DeepDiff(tracks, expected) == {}


def test_format_dict(album_dict):
    format_string = '{artist} - {name}'
    expected = 'artist1, artist2 - album'
    formatted = sputils.format_dict(album_dict, format_string)

    assert formatted == expected


@pytest.fixture
def required_args():
    return '--user testuser --client_id a --client_secret b'


@pytest.mark.parametrize('f', ['json', 'lines', 'yaml'])
def test_parse_args_format(f, required_args):
    args = sputils.parse_args(f'--format {f} {required_args}')

    assert args.format == f


@pytest.mark.parametrize('a', ['albums', 'tracks'])
def test_parse_args_action(a, required_args):
    args = sputils.parse_args(f'--action {a} {required_args}')

    assert args.action == a


def test_parse_args_user_args(required_args):
    args = sputils.parse_args(required_args)

    assert args.user == 'testuser'
    assert args.client_id == 'a'
    assert args.client_secret == 'b'


@pytest.fixture
def api_playlist():
    return {
        'images': [{'url': 'playlist_img_url'}],
        'name': 'playlist',
        'uri': 'playlist_uri',
        'tracks': {'total': 10}
    }


@pytest.fixture
def playlist_dict():
    return {
        'name': 'playlist',
        'uri': 'playlist_uri',
        'art_url': 'playlist_img_url',
        'length': 10
    }


def test_playlist_to_dict(api_playlist, playlist_dict):
    playlist = sputils.playlist_to_dict(api_playlist)

    assert deepdiff.DeepDiff(playlist, playlist_dict) == {}


def test_get_playlists(sp_mock, playlist_dict):
    expected = [playlist_dict]

    sp = sp_mock.Spotify()
    playlists = sputils.get_playlists(sp, 1, 0)

    assert deepdiff.DeepDiff(playlists, expected) == {}


def test_collect_playlists(sp_mock, playlist_dict):
    expected = [playlist_dict, playlist_dict]

    sp = sp_mock.Spotify()
    playlists = sputils.collect_playlists(sp, 1)

    assert deepdiff.DeepDiff(playlists, expected) == {}
