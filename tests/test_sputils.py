#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sputils` package."""

import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils


def rel_fn(fn):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_name, fn)


def mock_json(fn):
    with open(rel_fn(fn)) as f:
        return json.load(f)


@pytest.fixture
def api_track():
    return mock_json('mocks/api/track.json')


@pytest.fixture
def track_dict():
    return mock_json('mocks/dicts/track.json')


@pytest.fixture
def api_album_collected():
    return mock_json('mocks/api/album_collected.json')


@pytest.fixture
def album_dict_collected():
    return mock_json('mocks/dicts/album_collected.json')


@pytest.fixture
def api_album_searched():
    return mock_json('mocks/api/album_searched.json')


@pytest.fixture
def album_dict_searched():
    return mock_json('mocks/dicts/album_searched.json')


@pytest.fixture
def api_playlist():
    return mock_json('mocks/api/playlist.json')


@pytest.fixture
def playlist_dict():
    return mock_json('mocks/dicts/playlist.json')


@unittest.mock.patch('sputils.sputils.os')
def test_get_api_dict(mock_os):
    def mock_os_lambda(x):
        return x.replace('~', '/home/test')
    mock_os.path.expanduser.side_effect = mock_os_lambda

    expected = mock_json('mocks/dicts/spotify_api_params.json')

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


def test_track_to_dict(api_track, track_dict):
    track = sputils.track_to_dict(api_track)

    assert deepdiff.DeepDiff(track, track_dict) == {}


def test_album_to_dict_collect(api_album_collected, album_dict_collected):
    album = sputils.album_to_dict_collect(api_album_collected)

    assert deepdiff.DeepDiff(album, album_dict_collected) == {}


def test_limit_split():
    expected = [(50, 100), (50, 150), (50, 200), (50, 250)]

    splits = sputils.limit_split(290, 100, 50)

    assert splits == expected


@pytest.fixture
@unittest.mock.patch('sputils.sputils.spotipy')
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


def test_collect_albums(sp_mock, album_dict_collected):
    expected = [album_dict_collected]

    sp = sp_mock.Spotify()
    albums = sputils.collect_albums(sp, 1, 0)

    assert deepdiff.DeepDiff(albums, expected) == {}


def test_collect_all_albums(sp_mock, album_dict_collected):
    expected = [album_dict_collected, album_dict_collected]

    sp = sp_mock.Spotify()
    albums = sputils.collect_all_albums(sp, 1)

    assert deepdiff.DeepDiff(albums, expected) == {}


def test_collect_all_tracks(sp_mock, track_dict):
    ad = {
        'albumartist': 'artist1, artist2',
        'album': 'album',
        'added': 'mtime',
        'art_url': 'art_url',
    }
    td = {**track_dict, **ad}

    expected = [td, td]

    sp = sp_mock.Spotify()
    tracks = sputils.collect_all_tracks(sp, 1)

    assert deepdiff.DeepDiff(tracks, expected) == {}


def test_format_dict(album_dict_collected):
    format_string = '{artist} - {name}'
    expected = 'artist1, artist2 - album'
    formatted = sputils.format_dict(album_dict_collected, format_string)

    assert formatted == expected


@pytest.fixture
def required_args():
    return '--user testuser --client_id a --client_secret b'


@pytest.mark.parametrize('f', ['json', 'lines', 'yaml'])
def test_parse_args_format(f, required_args):
    args = sputils.parse_args(f'--format {f} {required_args}')

    assert args.format == f


@pytest.mark.parametrize('r', ['albums', 'tracks'])
def test_parse_args_resource(r, required_args):
    args = sputils.parse_args(f'--resource {r} {required_args}')

    assert args.resource == r


@pytest.mark.parametrize('a', ['collect'])
def test_parse_args_action(a, required_args):
    args = sputils.parse_args(f'--action {a} {required_args}')

    assert args.action == a


def test_parse_args_user_args(required_args):
    args = sputils.parse_args(required_args)

    assert args.user == 'testuser'
    assert args.client_id == 'a'
    assert args.client_secret == 'b'


def test_parse_args_no_query(required_args):
    exception_msg = 'error: a query is needed for this action'
    with pytest.raises(SystemExit, message=exception_msg) as e:
        sputils.parse_args(f'-a search {required_args}')
    assert e.value.code == 2


def test_playlist_to_dict(api_playlist, playlist_dict):
    playlist = sputils.playlist_to_dict(api_playlist)

    assert deepdiff.DeepDiff(playlist, playlist_dict) == {}


def test_collect_playlists(sp_mock, playlist_dict):
    expected = [playlist_dict]

    sp = sp_mock.Spotify()
    playlists = sputils.collect_playlists(sp, 1, 0)

    assert deepdiff.DeepDiff(playlists, expected) == {}


def test_collect_all_playlists(sp_mock, playlist_dict):
    expected = [playlist_dict, playlist_dict]

    sp = sp_mock.Spotify()
    playlists = sputils.collect_all_playlists(sp, 1)

    assert deepdiff.DeepDiff(playlists, expected) == {}


@unittest.mock.patch('sputils.sputils.collect_all_albums')
@unittest.mock.patch('sputils.sputils.collect_all_tracks')
@unittest.mock.patch('sputils.sputils.collect_all_playlists')
def test_collector(mock_cp, mock_ct, mock_ca, sp_mock):
    sp = sp_mock.Spotify()

    sputils.collector(sp, 'albums')
    mock_ca.assert_called_once()

    sputils.collector(sp, 'tracks')
    mock_ct.assert_called_once()

    sputils.collector(sp, 'playlists')
    mock_cp.assert_called_once()


def test_format_lines(album_dict_collected):
    expected = 'album\nalbum'
    albums = [album_dict_collected, album_dict_collected]
    lines = sputils.format_lines(albums, '{name}')

    assert lines == expected


@unittest.mock.patch('sputils.sputils.json.dumps')
@unittest.mock.patch('sputils.sputils.format_lines')
@unittest.mock.patch('sputils.sputils.yaml.dump')
def test_formatter(mock_yaml, mock_lines, mock_json, sp_mock):
    sp = sp_mock.Spotify()

    sputils.formatter(sp, 'json', None)
    mock_json.assert_called_once()

    sputils.formatter(sp, 'lines', None)
    mock_lines.assert_called_once()

    sputils.formatter(sp, 'yaml', None)
    mock_yaml.assert_called_once()


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
