# SPDX-FileCopyrightText: 2016-2018 CERN.
# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Alter datetime columns to utc aware datetime columns."""

from invenio_db.utils import (
    update_table_columns_column_type_to_datetime,
    update_table_columns_column_type_to_utc_datetime,
)

# revision identifiers, used by Alembic.
revision = "3bfaeb3d8eff"
down_revision = "5e02314da32e"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    for table_name in ["banners"]:
        update_table_columns_column_type_to_utc_datetime(table_name, "created")
        update_table_columns_column_type_to_utc_datetime(table_name, "updated")
    update_table_columns_column_type_to_utc_datetime("banners", "start_datetime")
    update_table_columns_column_type_to_utc_datetime("banners", "end_datetime")


def downgrade():
    """Downgrade database."""
    for table_name in ["banners"]:
        update_table_columns_column_type_to_datetime(table_name, "created")
        update_table_columns_column_type_to_datetime(table_name, "updated")
    update_table_columns_column_type_to_datetime("banners", "start_datetime")
    update_table_columns_column_type_to_datetime("banners", "end_datetime")
