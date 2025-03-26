# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI tests configuration.

Note: need to call python setup.py compile_catalog to compile the translations before
running the tests.
"""
import json
from pathlib import Path

import pytest
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_app as _create_app
from invenio_i18n import lazy_gettext as _


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app


@pytest.fixture(scope="module")
def app_config(app_config):
    """Override pytest-invenio app_config fixture.

    Set languages for the app.
    """
    app_config["I18N_LANGUAGES"] = [
        ("cs", _("Czech")),
    ]
    return app_config


@pytest.fixture()
def admin_identity(admin):
    """Identity of the admin user."""
    return admin.identity


@pytest.fixture()
def admin_client(db, client, admin):
    """Log in a user to the client."""

    login_user(admin.user, remember=True)
    login_user_via_session(client, email=admin.user.email)

    return client


def add_to_manifest(manifest, filename):
    manifest.setdefault("assets", {})[filename] = {"publicPath": filename}
    filename_without_ext = filename.rsplit(".", 1)[0]
    manifest.setdefault("chunks", {}).setdefault(filename_without_ext, []).append(
        filename
    )


@pytest.fixture()
def fake_manifest(app, instance_path):
    app.static_folder = str(Path(instance_path) / "static")

    manifest_path = Path(instance_path) / "static" / "dist" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "status": "done",
        "publicPath": "/static/dist/",
    }
    add_to_manifest(manifest, "base.js")
    add_to_manifest(manifest, "base-admin-theme.js")

    add_to_manifest(manifest, "i18n_app.js")
    add_to_manifest(manifest, "invenio-administration-details.js")
    add_to_manifest(manifest, "invenio-administration-search.js")

    add_to_manifest(manifest, "theme.css")
    add_to_manifest(manifest, "theme.js")

    manifest_path.write_text(json.dumps(manifest))
    return manifest_path


@pytest.fixture()
def clear_babel_context():

    # force babel reinitialization when language is switched
    def _clear_babel_context():
        try:
            from flask import g
            from flask_babel import SimpleNamespace

            g._flask_babel = SimpleNamespace()
        except ImportError:
            return

    return _clear_babel_context
