# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# invenio-banners is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for banners module."""

from invenio_access import action_factory
from invenio_access.permissions import Permission

banners_administration_access_action = action_factory("banners-administration-access")
banners_administration_permission = Permission(banners_administration_access_action)
