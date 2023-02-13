from tests import server


def test_get_installed_list():
    r = server.plugin.get_installed_list()
    print(r)
