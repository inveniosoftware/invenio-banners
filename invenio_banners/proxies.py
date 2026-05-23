# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Proxies for accessing the current Banners extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_banners = LocalProxy(lambda: current_app.extensions["invenio-banners"])
"""Proxy for the instantiated Banners extension."""

current_banners_service = LocalProxy(
    lambda: current_app.extensions["invenio-banners"].banners_service
)
"""Proxy for the currently instantiated banners service."""
