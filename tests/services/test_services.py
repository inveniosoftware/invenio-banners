# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service level tests for Banners."""

from datetime import datetime, timedelta

import pytest
from invenio_records_resources.services.errors import PermissionDeniedError

from invenio_banners.proxies import current_banners_service as service
from invenio_banners.records import BannerModel
from invenio_banners.services.errors import BannerNotExistsError

banners = {
    "active": {
        "message": "active",
        "url_path": "/active",
        "category": "info",
        "end_datetime": datetime.utcnow() + timedelta(days=1),
        "active": True,
    },
    "inactive": {
        "message": "inactive",
        "url_path": "/inactive",
        "category": "info",
        "active": False,
    },
    "other": {
        "message": "other",
        "url_path": "/other",
        "category": "warning",
        "active": True,
    },
    "expired": {
        "message": "expired",
        "url_path": "/expired",
        "category": "info",
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
}


def test_banner_creation(app, superuser_identity):
    """Create a banner."""
    banner_data = banners["active"]
    banner = service.create(superuser_identity, banner_data)

    assert banner["message"] == banner_data["message"]
    assert banner["url_path"] == banner_data["url_path"]
    assert banner["category"] == banner_data["category"]
    assert banner["active"] == banner_data["active"]


def test_create_is_forbidden(app, simple_user_identity):
    """Test that the simple user cannot create a new banner."""
    with pytest.raises(PermissionDeniedError):
        service.create(simple_user_identity, banners["active"])


def test_update_banner(app, superuser_identity):
    """Update a banner."""
    # create banner first
    banner = BannerModel.create(banners["active"])

    new_data = {
        "message": "New banner message",
        "category": "info",
    }

    updated_banner = service.update(superuser_identity, banner.id, new_data)

    assert updated_banner["message"] == new_data["message"]
    assert updated_banner["category"] == new_data["category"]
    assert updated_banner["url_path"] == banner.url_path
    assert updated_banner["active"] == banner.active


def test_update_is_forbidden(app, simple_user_identity):
    """Test that the simple user cannot update a banner."""
    # create banner first
    banner = BannerModel.create(banners["active"])

    new_data = {"message": "New banner message"}

    with pytest.raises(PermissionDeniedError):
        service.update(simple_user_identity, banner.id, new_data)


def test_update_non_existing_banner(app, superuser_identity):
    """Update a non-existing banner."""
    new_data = {"message": "New banner message"}

    with pytest.raises(BannerNotExistsError) as ex:
        service.update(superuser_identity, 1, new_data)

    assert ex.value.description == "Banner with id 1 is not found."


def test_delete_banner(app, superuser_identity):
    """Delete a banner."""
    # create banner first
    banner = BannerModel.create(banners["active"])

    service.delete(superuser_identity, banner.id)

    # check that it's not present in db
    assert BannerModel.query.filter_by(id=banner.id).one_or_none() is None


def test_delete_is_forbidden(app, simple_user_identity):
    """Test that the simple user cannot delete a banner."""
    # create banner first
    banner = BannerModel.create(banners["active"])

    with pytest.raises(PermissionDeniedError):
        service.delete(simple_user_identity, banner.id)


def test_delete_non_existing_banner(app, superuser_identity):
    """Delete a non-existing banner."""
    with pytest.raises(BannerNotExistsError) as ex:
        service.delete(superuser_identity, 1)

    assert ex.value.description == "Banner with id 1 is not found."


def test_read_banner(app, simple_user_identity):
    """Read a banner by id."""
    # create banner first
    banner = BannerModel.create(banners["active"])

    banner_result = service.read(simple_user_identity, banner.id)

    assert banner_result["message"] == banner.message
    assert banner_result["url_path"] == banner.url_path
    assert banner_result["category"] == banner.category
    assert banner_result["active"] == banner.active


def test_read_non_existing_banner(app, simple_user_identity):
    """Read a non-existing banner."""
    with pytest.raises(BannerNotExistsError) as ex:
        service.read(simple_user_identity, 1)

    assert ex.value.description == "Banner with id 1 is not found."


def test_search_banner_with_limit(app, simple_user_identity):
    """Search for banners limited (return 2 out of 3)."""
    # create banners first
    BannerModel.create(banners["active"])
    BannerModel.create(banners["other"])
    BannerModel.create(banners["inactive"])

    banner_list = service.search(simple_user_identity, limit=2)

    assert banner_list.total == 2
    result_hits = banner_list.to_dict()["hits"]
    result_list = result_hits["hits"]
    assert len(result_list) == 2
    assert result_list[0]["message"] == "active"
    assert result_list[1]["message"] == "other"


def test_search_banner_with_params(app, simple_user_identity):
    """Search for banners with parameters."""
    # create banners first
    BannerModel.create(banners["active"])
    BannerModel.create(banners["other"])
    BannerModel.create(banners["inactive"])

    search_params = {
        "facets": {
            "active": [True],
            "category": ["info"],
        }
    }

    banner_list = service.search(simple_user_identity, params=search_params)

    assert banner_list.total == 1
    result_hits = banner_list.to_dict()["hits"]
    result_list = result_hits["hits"]
    assert len(result_list) == 1
    assert result_list[0]["message"] == "active"


def test_search_banner_empty_list(app, simple_user_identity):
    """Search for banners (no banner found)."""
    banner_list = service.search(simple_user_identity)

    assert banner_list.total == 0
    result_list = banner_list.to_dict()["hits"]
    assert len(result_list["hits"]) == 0


def test_read_active_banners(app, simple_user_identity):
    """Search for active banners"""
    # create banners first
    BannerModel.create(banners["active"])
    BannerModel.create(banners["other"])
    BannerModel.create(banners["inactive"])

    banner_list = service.read_active_banners(simple_user_identity, "/active")

    assert banner_list.total == 1
    result_hits = banner_list.to_dict()["hits"]
    result_list = result_hits["hits"]
    assert len(result_list) == 1
    assert result_list[0]["url_path"] == "/active"
    assert result_list[0]["active"] is True


def test_read_active_banners_empty_list(app, simple_user_identity):
    """Search for active banners (no banner found)."""
    # create banners first
    BannerModel.create(banners["other"])
    BannerModel.create(banners["inactive"])

    banner_list = service.read_active_banners(simple_user_identity, "/active")

    assert banner_list.total == 0
    result_list = banner_list.to_dict()["hits"]
    assert len(result_list["hits"]) == 0


def test_disable_expired_banners(app, superuser_identity):
    """Disable expired banners."""
    # create banner first
    BannerModel.create(banners["expired"])
    BannerModel.create(banners["active"])

    assert BannerModel.query.filter(BannerModel.active.is_(True)).count() == 2

    service.disable_expired(superuser_identity)

    _banners = BannerModel.query.filter(BannerModel.active.is_(True)).all()

    assert len(_banners) == 1
    assert _banners[0].message == "active"


def test_disable_expired_is_forbidden(app, simple_user_identity):
    """Test that the simple user cannot disable a banner."""
    with pytest.raises(PermissionDeniedError):
        service.disable_expired(simple_user_identity)
