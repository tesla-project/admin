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

from tesla_models import db
from sqlalchemy.exc import OperationalError
from .learners import LearnerDB
from .users import UserDB
from .instruments import InstrumentDB
from .requests import RequestDB
from .activities import ActivityDB
from .course import CourseDB
from .config import ConfigDB
from .tasks import TaskDB
from .statistics import StatisticsDB
from .informed_consent import InformedConsentDB
from .vle import VleDB
from .reports import ReportsDB
from .ties import TiesDB

class TeSLADB(object):

    def __init__(self, logger):
        self.db = db
        self.logger = logger
        self.learners = LearnerDB(db, logger)
        self.users = UserDB(db, logger)
        self.instruments = InstrumentDB(db, logger)
        self.requests = RequestDB(db, logger)
        self.activities = ActivityDB(db, logger)
        self.courses = CourseDB(db, logger)
        self.config = ConfigDB(db, logger)
        self.tasks = TaskDB(db, logger)
        self.statistics = StatisticsDB(db, logger)
        self.informed_consent = InformedConsentDB(db, logger)
        self.vle = VleDB(db, logger)
        self.reports = ReportsDB(db, logger)
        self.ties = TiesDB(db, logger)

    def is_alive(self):
        try:
            result = db.session.execute('select 1 as is_alive;').scalar()
        except OperationalError as e:
            return 0

        return result

    def valid_schema(self):
        # TODO: Check if the database tables are up to date (alembic ? )
        return 1
