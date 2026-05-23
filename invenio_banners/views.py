# SPDX-FileCopyrightText: 2020-2023 CERN.
# SPDX-License-Identifier: MIT

"""Invenio module providing management APIs for banners."""


def create_banners_api_bp(app):
    """Create the banners resource api blueprint."""
    ext = app.extensions["invenio-banners"]
    return ext.banners_resource.as_blueprint()
