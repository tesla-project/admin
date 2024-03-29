"""Change type of html column in informed consent

Revision ID: 33978b6f064b
Revises: 705f2cce1981
Create Date: 2018-04-09 16:59:06.609526

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
revision = '33978b6f064b'
down_revision = '705f2cce1981'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('informed_consent_document', 'html',
               existing_type=postgresql.BYTEA(),
               type_=postgresql.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('informed_consent_document', 'html',
               existing_type=postgresql.TEXT(),
               type_=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###
#, postgresql_using='html::varchar'