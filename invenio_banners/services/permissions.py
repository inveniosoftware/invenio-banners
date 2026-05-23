# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Banners permissions."""

from invenio_administration.generators import Administration
from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class BannersPermissionPolicy(BasePermissionPolicy):
    """Permission policy for banners."""

    can_create = [Administration(), SystemProcess()]
    can_read = [AnyUser(), SystemProcess()]
    can_search = [AnyUser(), SystemProcess()]
    can_update = [Administration(), SystemProcess()]
    can_delete = [Administration(), SystemProcess()]
    can_disable = [Administration(), SystemProcess()]
