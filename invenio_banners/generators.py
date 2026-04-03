# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# invenio-banners is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-Administration Permissions Generators."""

from invenio_records_permissions.generators import Generator

from invenio_banners.permissions import banners_administration_access_action


class BannersAdministration(Generator):
    """Allows administration-access in Banners Administration dashboard."""

    def __init__(self):
        """Constructor."""
        super(BannersAdministration, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [banners_administration_access_action]
