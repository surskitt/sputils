#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for common functions."""

import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils

import helpers


def test_limit_split():
    expected = [(50, 100), (50, 150), (50, 200), (50, 250)]

    splits = sputils.limit_split(290, 100, 50)

    assert splits == expected


def test_track_to_dict(api_track, track_dict):
    track = sputils.track_to_dict(api_track)

    assert deepdiff.DeepDiff(track, track_dict) == {}


def test_playlist_to_dict(api_playlist, playlist_dict):
    playlist = sputils.playlist_to_dict(api_playlist)

    assert deepdiff.DeepDiff(playlist, playlist_dict) == {}


def test_album_to_dict_common(api_album_collected, album_dict_common):
    album = sputils.album_to_dict_common(api_album_collected['album'])

    assert deepdiff.DeepDiff(album, album_dict_common) == {}


def test_format_dict(album_dict_collected):
    format_string = '{artist} - {name}'
    expected = 'artist1, artist2 - album'
    formatted = sputils.format_dict(album_dict_collected, format_string)

    assert formatted == expected


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
