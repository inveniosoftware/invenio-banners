# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2024 Graz University of Technology.
# Copyright (C) 2026 CESNET z.s.p.o.
#
# Invenio-banners is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test invenio-banners alembic."""

import pytest
from invenio_db.utils import alembic_test_context, drop_alembic_version_table


def test_alembic(app, db, extra_entry_points):
    """Test alembic recipes."""
    ext = app.extensions["invenio-db"]

    if db.engine.name == "sqlite":
        raise pytest.skip("Upgrades are not supported on SQLite.")

    app.config["ALEMBIC_CONTEXT"] = alembic_test_context()

    # Check that this package's SQLAlchemy models have been properly registered
    tables = [x for x in db.metadata.tables]
    assert "banners" in tables

    # Check that Alembic agrees that there's no further tables to create.
    assert ext.alembic.compare_metadata() == []

    # Drop everything and recreate tables all with Alembic
    db.drop_all()
    drop_alembic_version_table()
    ext.alembic.upgrade()

    assert ext.alembic.compare_metadata() == []

    ext.alembic.downgrade("dbdbc1b19cf2")
    ext.alembic.upgrade()

    assert ext.alembic.compare_metadata() == []

    drop_alembic_version_table()
