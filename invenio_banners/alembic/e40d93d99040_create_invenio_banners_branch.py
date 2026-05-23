# SPDX-FileCopyrightText: 2016-2018 CERN.
# SPDX-License-Identifier: MIT

"""Create invenio-banners branch."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e40d93d99040"
down_revision = None
branch_labels = ("invenio_banners",)
depends_on = "dbdbc1b19cf2"


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
