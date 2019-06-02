from . import common


def album_to_dict_searched(api_dict):
    return common.album_to_dict_common(api_dict)


def search_albums(sp, qry):
    searched = sp.search(qry, type='album', limit=50)

    return [album_to_dict_searched(a) for a in searched['albums']['items']]


def searcher(sp, qry, resource):
    if resource == 'albums':
        return search_albums(sp, qry)
