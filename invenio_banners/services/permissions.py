# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Banners permissions."""

from invenio_administration.generators import Administration
from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess
from invenio_banners.generators import BannersAdministration


class BannersPermissionPolicy(BasePermissionPolicy):
    """Permission policy for banners."""

    can_create = [Administration(), SystemProcess(), BannersAdministration()]
    can_read = [AnyUser(), SystemProcess(), BannersAdministration()]
    can_search = [AnyUser(), SystemProcess(), BannersAdministration()]
    can_update = [Administration(), SystemProcess(), BannersAdministration()]
    can_delete = [Administration(), SystemProcess(), BannersAdministration()]
    can_disable = [Administration(), SystemProcess(), BannersAdministration()]
