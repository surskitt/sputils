# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys

from . import commandline, auth, common, collect, search


def main():
    args = commandline.parse_args(sys.argv[1:])

    # Create cache dir
    try:
        os.makedirs(os.path.expanduser('~/.cache/sputils'))
    except FileExistsError:
        pass

    sp = auth.get_spotify_client(args.user, args.client_id, args.client_secret)

    if args.action == 'collect':
        items = collect.collector(sp, args.resource)
    elif args.action == 'search':
        qry = ' '.join(args.query)
        items = search.searcher(sp, qry, args.resource)

    if args.action in ['collect', 'search']:
        out = common.formatter(items, args.format, args.line_format)
        print(out)
