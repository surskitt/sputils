#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sputils` package."""

import pytest
import unittest


from sputils import sputils


def test_get_api_dict():
    expected = {
        'username': 'testuser',
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'redirect_uri': 'http://localhost',
        'scope': 'user-library-read'
    }
    api_dict_params = ('testuser', 'test_client_id', 'test_client_secret')
    api_dict = sputils.get_api_dict(*api_dict_params)
