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

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .storage import DBDataStorage, DataStorage

db = None # type: SQLAlchemy
ma = None # type: Marshmallow
tesla_db = None # type: TeSLADB
tesla_storage = None # type: DataStorage
tep_db = None # type: TEP_DB

def init_tesla_db(app):
    global db
    global ma
    global tesla_db
    global tesla_storage
    global tesla_db
    global tep_db

    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    from .database import TeSLADB
    tesla_db = TeSLADB(app.logger)

    tesla_storage = DBDataStorage(app.logger, tesla_db)
    from .tep_database import TEP_DB
    if 'TEP_SQLALCHEMY_DATABASE_URI' in app.config:
        tep_db = TEP_DB(app.config, app.logger, tesla_db, tesla_storage)

    return tesla_db # type: TeSLADB
