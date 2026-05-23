# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Banner services conftest."""

import pytest


@pytest.fixture()
def superuser_identity(admin):
    """Superuser identity fixture."""
    identity = admin.identity
    return identity


@pytest.fixture()
def simple_user_identity(user):
    """Simple identity fixture."""
    identity = user.identity
    return identity
