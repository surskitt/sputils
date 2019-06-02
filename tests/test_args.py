import pytest

from sputils import commandline


@pytest.mark.parametrize('f', ['json', 'lines', 'yaml'])
def test_parse_args_format(f, required_args):
    args = commandline.parse_args(f'--format {f} {required_args}')

    assert args.format == f


@pytest.mark.parametrize('r', ['albums', 'tracks'])
def test_parse_args_resource(r, required_args):
    args = commandline.parse_args(f'--resource {r} {required_args}')

    assert args.resource == r


@pytest.mark.parametrize('a', ['collect'])
def test_parse_args_action(a, required_args):
    args = commandline.parse_args(f'--action {a} {required_args}')

    assert args.action == a


def test_parse_args_user_args(required_args):
    args = commandline.parse_args(required_args)

    assert args.user == 'testuser'
    assert args.client_id == 'a'
    assert args.client_secret == 'b'


def test_parse_args_no_query(required_args):
    exception_msg = 'error: a query is needed for this action'
    with pytest.raises(SystemExit, message=exception_msg) as e:
        commandline.parse_args(f'-a search {required_args}')
    assert e.value.code == 2
