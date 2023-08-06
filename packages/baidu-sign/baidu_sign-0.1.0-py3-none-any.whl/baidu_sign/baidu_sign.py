"""Gen baidu sign.

%timeit js2py_sign('test ' * 2)
11.2 ms ± 215 µs per loop

%timeit google_sign('test ' * 2, GTK)
39.4 µs ± 1.29 µs per loop
about 30 times faster than js2py_sign

"""
from google_sign import google_sign

from .js2py_sign import js2py_sign

GTK = "320305.131321201"


def baidu_sign(
    text: str,
) -> str:
    r"""Gen baidu sign for text.

    len(text) > 30: js2py_sign(text)
    google_sign(text, GTK)
    """
    if len(text) < 31:
        _ = google_sign(text, GTK)
    else:
        _ = js2py_sign(text)

    return _
