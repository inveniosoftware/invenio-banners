# SPDX-FileCopyrightText: 2022-2025 CERN.
# SPDX-License-Identifier: MIT

"""Banner Resource Configuration."""

import marshmallow as ma
from flask_resources import JSONDeserializer, RequestBodyParser
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)


class BannerServerSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Banner request parameters."""

    sort_direction = ma.fields.Str()
    active = ma.fields.Bool()
    url_path = ma.fields.Str()


class BannerResourceConfig(RecordResourceConfig):
    """Banner resource config."""

    # Blueprint configuration
    blueprint_name = "banners"
    url_prefix = "/banners"
    routes = {
        "item": "/<banner_id>",
        "list": "/",
    }

    request_view_args = {
        "banner_id": ma.fields.Integer(),
    }

    request_search_args = BannerServerSearchRequestArgsSchema

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}
    default_content_type = "application/json"

    response_handlers = {
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }
