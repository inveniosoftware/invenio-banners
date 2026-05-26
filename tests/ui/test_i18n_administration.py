# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test the i18n of the administration interface.

Note: this does not test the actual translation of the messages, but rather that the
translation kicks in and that some of the labels are localized - so that we know that
the lazy_gettext is working.
"""

from datetime import datetime, timedelta

from invenio_banners.proxies import current_banners_service as service


def test_list_is_localized(app, admin_client, fake_manifest, clear_babel_context):
    """Test that the administration page is localized and that the labels are translated."""

    clear_babel_context()
    resp = admin_client.get("/administration/banners")
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"
    # check that the string "Active" is in the response twice (sort order, column number)
    assert len(resp.text.split('"Active"')) == 3

    clear_babel_context()
    resp = admin_client.get(
        "/administration/banners", headers=[("Accept-Language", "cs")]
    )
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"
    assert '<html lang="cs"' in resp.text

    # checks both sort order and table column name
    assert "Active" not in resp.text


def test_detail_is_localized(
    app, admin, admin_client, fake_manifest, clear_babel_context
):
    """Test that the administration detail page is localized and that the labels are translated."""

    active_banner = {
        "message": "active",
        "url_path": "/active",
        "category": "info",
        "start_datetime": (datetime.now() - timedelta(days=1)).isoformat(),
        "end_datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "active": True,
    }

    banner_id = service.create(admin.identity, active_banner)["id"]

    clear_babel_context()
    resp = admin_client.get(f"/administration/banners/{banner_id}")
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"
    assert '"Active"' in resp.text

    clear_babel_context()
    resp = admin_client.get(
        f"/administration/banners/{banner_id}", headers=[("Accept-Language", "cs")]
    )
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"
    assert '<html lang="cs"' in resp.text

    # checks both sort order and table column name
    assert "Active" not in resp.text
