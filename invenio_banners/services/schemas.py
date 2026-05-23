# SPDX-FileCopyrightText: 2022-2023 CERN.
# SPDX-License-Identifier: MIT

"""Banners schema."""

from datetime import datetime, timezone

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import fields, pre_load
from marshmallow_utils.fields import SanitizedHTML, TZDateTime


class BannerSchema(BaseRecordSchema):
    """Schema for banners."""

    message = SanitizedHTML(required=True)
    url_path = fields.String(allow_none=True)
    category = fields.String(required=True, metadata={"default": "info"})
    start_datetime = fields.DateTime(
        required=True,
        metadata={"default": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")},
    )
    end_datetime = fields.DateTime(allow_none=True)
    active = fields.Boolean(required=True, metadata={"default": True})
    created = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
    updated = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)

    @pre_load
    def change_none_to_string(self, data, **kwargs):
        """Fix for empty strings not in line with allow_none=True."""
        for field in data:
            if field == "end_datetime" or field == "category":
                if data[field] == "":
                    data[field] = None
        return data
