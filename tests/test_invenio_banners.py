# SPDX-FileCopyrightText: 2020-2023 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

from flask import Flask

from invenio_banners import InvenioBanners


def test_version():
    """Test version import."""
    from invenio_banners import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    InvenioBanners(app)
    assert "invenio-banners" in app.extensions

    app = Flask("testapp")
    ext = InvenioBanners()
    assert "invenio-banners" not in app.extensions
    ext.init_app(app)
    assert "invenio-banners" in app.extensions
