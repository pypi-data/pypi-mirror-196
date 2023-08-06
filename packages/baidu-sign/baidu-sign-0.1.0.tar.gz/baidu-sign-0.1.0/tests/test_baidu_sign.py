"""Check sanity."""
from baidu_sign import baidu_sign

# from bdtr_async import baidu_sign
# from bdtr_async import baidu_sign
# from bdtr_async.baidu_sign import baidu_sign


def test_baidu_sign():
    """Check sanity."""
    assert baidu_sign("test") == "431039.159886"
    # GTK = '320305.131321201'
    # google_sign('test', GTK)

    assert baidu_sign("test " * 10) == "403909.183028"
    # js2py_sign('test ' * 10, GTK)
    # '403909.183028'
