#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for collection functions."""

import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils

import helpers


def test_album_to_dict_collect(api_album_collected, album_dict_collected):
    album = sputils.album_to_dict_collected(api_album_collected)

    assert deepdiff.DeepDiff(album, album_dict_collected) == {}


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
