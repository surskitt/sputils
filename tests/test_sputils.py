#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sputils` package."""

import pytest
import unittest.mock

import os
import json

import deepdiff

from sputils import sputils

import helpers


def test_format_dict(album_dict_collected):
    format_string = '{artist} - {name}'
    expected = 'artist1, artist2 - album'
    formatted = sputils.format_dict(album_dict_collected, format_string)

    assert formatted == expected


def test_playlist_to_dict(api_playlist, playlist_dict):
    playlist = sputils.playlist_to_dict(api_playlist)

    assert deepdiff.DeepDiff(playlist, playlist_dict) == {}


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
