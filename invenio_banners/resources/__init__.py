# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Invenio Resources module to create REST APIs."""

from .config import BannerResourceConfig
from .resource import BannerResource

__all__ = (
    "BannerResource",
    "BannerResourceConfig",
)
