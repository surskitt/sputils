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


def test_album_to_dict_common(api_album_collected, album_dict_common):
    album = sputils.album_to_dict_common(api_album_collected['album'])

    assert deepdiff.DeepDiff(album, album_dict_common) == {}
