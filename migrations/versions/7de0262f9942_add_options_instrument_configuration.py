"""Add options to instrument configuration

Revision ID: 7de0262f9942
Revises: c6a5ccd22a0b
Create Date: 2018-05-31 10:45:52.164195

"""
#  TeSLA Admin
#  Copyright (C) 2019 Universitat Oberta de Catalunya
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7de0262f9942'
down_revision = 'c6a5ccd22a0b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('activity_instrument', sa.Column('alternative_options', sa.LargeBinary(), nullable=True))
    op.add_column('activity_instrument', sa.Column('options', sa.LargeBinary(), nullable=True))


def downgrade():
    op.drop_column('activity_instrument', 'options')
    op.drop_column('activity_instrument', 'alternative_options')

