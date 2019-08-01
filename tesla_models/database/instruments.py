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

from tesla_models.models import Instrument, InstrumentQueue, InstrumentThresholds


class InstrumentDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def get_instruments(self):
        try:
            instruments = Instrument.query.all()
        except Exception:
            self.logger.exception("Error finding instruments")
            instruments = []

        return instruments

    def get_instruments_queues(self):
        try:
            instruments = InstrumentQueue.query.all()
        except Exception:
            self.logger.exception("Error finding instrument queues")
            instruments = []

        return instruments

    def get_instrument_status(self):
        try:
            instruments = self.db.session.query(Instrument, InstrumentQueue).filter(Instrument.id == InstrumentQueue.instrument_id).all()
        except Exception:
            self.logger.exception("Error finding instrument status")
            instruments = []

        return instruments

    def get_instrument_by_id(self, id):
        try:
            instrument = Instrument.query.filter_by(id=id).one_or_none()
        except Exception:
            self.logger.exception("Error finding instrument with id {}".format(id))
            instrument = None

        return instrument

    def get_num_instruments(self):
        try:
            num_instruments = Instrument.query.count()
        except Exception:
            self.logger.exception("Error finding number of instruments")
            num_instruments = 0

        return int(num_instruments)

    def get_instrument_by_acronym(self, acronym):
        try:
            instrument = Instrument.query.filter_by(acronym=acronym).one_or_none()
        except Exception:
            self.logger.exception("Error finding instrument with acronym {}".format(acronym))
            instrument = None

        return instrument

    def get_instrument_queue(self, instrument_id):
        try:
            instrument = InstrumentQueue.query.filter_by(instrument_id=instrument_id).one_or_none()
        except Exception:
            self.logger.exception("Error finding instrument queue for instrument_id {}".format(instrument_id))
            instrument = None

        return instrument

    def create_instrument(self, id, name, acronym, url, port, active, require_enrollment, has_licence):
        if id is None or id <=0:
            self.logger.error("Invalid instrument id")
            return None
        try:
            new_instrument = Instrument(id=id, name=name, acronym=acronym, url=url, port=port, active=active,
                                        requires_enrollment=require_enrollment, has_licence=has_licence)

            self.db.session.add(new_instrument)
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error creating new instrument {}".format(new_instrument))
            new_instrument = None

        return new_instrument

    def create_instrument_queue(self, instrument_id, queue):
        try:
            new_instrument_queue = InstrumentQueue(instrument_id=instrument_id, queue=queue)
            self.db.session.add(new_instrument_queue)
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error creating new instrument {}".format(new_instrument_queue))
            new_instrument_queue = None

        return new_instrument_queue

    def update_instrument(self, id, name, acronym, url, port, active, require_enrollment, has_licence):
        try:
            Instrument.query.filter_by(id=id).update({"name": name, "acronym": acronym, "url": url,
                                                                   "port": port, "active": active,
                                                                   "requires_enrollment": require_enrollment,
                                                                   "has_licence": has_licence})
            self.db.session.commit()
            instrument = Instrument.query.filter_by(id=id).one_or_none()

        except Exception:
            self.logger.exception("Error updating instrument {}".format(instrument))
            instrument = None

        return instrument

    def update_instrument_queue(self, instrument_id, queue):
        try:
            InstrumentQueue.query.filter_by(instrument_id=instrument_id).update({"queue": queue})
            self.db.session.commit()
            instrument_queue = InstrumentQueue.query.filter_by(instrument_id=instrument_id).one_or_none()

        except Exception:
            self.logger.exception("Error updating instrument queue for instrument {}".format(instrument_id))
            instrument_queue = None

        return instrument_queue

    def update_instrument_queue_stats(self, instrument_id, pending_tasks, consumers, service=None, service_info=None):
        try:
            instrument_queue=self.db.session.query(InstrumentQueue).filter(InstrumentQueue.instrument_id==instrument_id).with_for_update().one_or_none()
            if instrument_queue is not None:
                velocity = pending_tasks - instrument_queue.pending_tasks
                acceleration = velocity - instrument_queue.tendency1
                instrument_queue.consumers = consumers
                instrument_queue.pending_tasks = pending_tasks
                instrument_queue.tendency1 = velocity
                instrument_queue.tendency2 = acceleration
                instrument_queue.service = service
                instrument_queue.service_info = service_info

            self.db.session.commit()
            self.db.session.refresh(instrument_queue)

        except Exception:
            self.logger.exception("Error updating instrument queue statistics for instrument {}".format(instrument_id))
            instrument_queue = None

        return instrument_queue

    def get_instrument_thresholds(self, instrument_id):
        try:
            instrument = InstrumentThresholds.query.filter_by(instrument_id=instrument_id).one_or_none()
        except Exception:
            self.logger.exception("Error finding instrument thresholds for instrument_id {}".format(instrument_id))
            instrument = None

        return instrument

    def create_or_update_instrument_thresholds(self, instrument_id, low, medium, high, audit_level):
        try:
            inst_thresholds = self.db.session.query(InstrumentThresholds).filter(
                InstrumentThresholds.instrument_id == instrument_id).with_for_update().one_or_none()

            if inst_thresholds is None:
                inst_thresholds = InstrumentThresholds(instrument_id=instrument_id, low=low, medium=medium,
                                                       high=high, audit_level=audit_level)
                self.db.session.add(inst_thresholds)
            else:
                inst_thresholds.low = low
                inst_thresholds.medium = medium
                inst_thresholds.high = high
                inst_thresholds.audit_level = audit_level
            self.db.session.commit()
            self.db.session.refresh(inst_thresholds)

        except Exception:
            self.logger.exception("Error creating or updating instrument threshodls for instrument {}".format(instrument_id))
            inst_thresholds = None

        return inst_thresholds
