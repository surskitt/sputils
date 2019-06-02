from argparse import RawTextHelpFormatter
import textwrap

import configargparse


def parse_args(args):
    desc = 'A collection of spotify utilities for use with other shell utils.'
    cfgfiles = ['/etc/sputils.d/*.conf', '~/.config/sputils/*.conf']
    parser = configargparse.ArgParser(default_config_files=cfgfiles,
                                      description=desc,
                                      formatter_class=RawTextHelpFormatter)
    parser.add('-c', '--config', is_config_file=True,
               help='config file path')

    parser.add('-u', '--user', type=str, required=True,
               help='spotify user')
    parser.add('--client_id', type=str, required=True,
               help='spotify client id')
    parser.add('--client_secret', type=str, required=True,
               help='spotify client secret')

    actions = ['collect', 'search', 'query', 'save', 'delete', 'reccomend',
               'follow', 'following']
    actions_desc = '''\
                   collect: collect resources from saved collection
                   search: search spotify for resources
                   query: query a set of resource on their uris
                   add: add resource to collection
                   delete: delete resource from collection
                   reccomend: return reccomendations based on given uris
                   follow: follow artist
                   following: query resources based on followed artists
                   '''
    parser.add('-a', '--action', choices=actions, default='collect',
               help=textwrap.dedent(actions_desc))

    resources = ['artists', 'albums', 'tracks', 'playlists']
    parser.add('-r', '--resource', choices=resources, default='albums',
               help='resource to query')

    format_choices = ['json', 'lines', 'yaml']
    parser.add('-f', '--format', choices=format_choices, default='json',
               help='output format')
    parser.add('-l', '--line_format', default='{name}', type=str,
               help='format for outputting lines, accepts json keys')

    query_help = 'query (valid for search, add, delete, reccomend and follow)'
    parser.add('query', nargs='*', help=query_help)

    args = parser.parse_args(args)

    if args.action in ['search', 'query', 'save', 'delete', 'reccomend',
                       'follow'] and args.query == []:
        parser.error('a query is needed for this action')

    return args
