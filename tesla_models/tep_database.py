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

from sqlalchemy import create_engine
from .models import TEPMigrations
from datetime import datetime
from .database.utils import encode_data
from .constants import TESLA_RESULT_STATUS, TESLA_REQUEST_STATUS

class TEP_DB(object):

    def __init__(self, config, logger, database, storage):
        self.engine = create_engine(config['TEP_SQLALCHEMY_DATABASE_URI'])
        self.logger = logger
        self.db = database
        self.storage = storage

    def _sync_activity(self, connection, vle_id, activity_id, activity_type_id):
        # Get the activity configuration
        act_results = connection.execute(
            'SELECT * FROM "ActivityConfigs" a, "ActivityTypes" t WHERE a."ActivityId"=\'{}\' AND a."ActivityTypeId"=t."Id" AND a."VleId"=\'{}\' AND a."ActivityTypeId"={}'.format(
                activity_id, vle_id, activity_type_id))
        if act_results.rowcount == 1:
            for row_act in act_results:
                activity_type = row_act['Description']
                act_conf_id = row_act['Id']
        elif act_results.rowcount == 0:
            act_conf_id = None
            tep_act_type = connection.execute('SELECT * FROM "ActivityTypes" WHERE "Id"={}'.format(activity_type_id))
            if tep_act_type.rowcount == 1:
                for row_tep_act_type in tep_act_type:
                    activity_type = row_tep_act_type['Description']
            else:
                self.logger.error('Activity type missing on TEP during synchronization.')
                return None
        else:
            self.logger.error('Invalid Activity when synchronizing TEP reports. Multiple rows received')
            return None

        # Check if the activity exists in database
        new_activity = self.db.activities.get_activity_by_def(vle_id, activity_type, activity_id)
        if new_activity is None:
            new_activity = self.db.activities.create_activity(vle_id, activity_type, activity_id)
        act_id = new_activity.id

        # Setup instruments
        if act_conf_id is None:
            self.logger.warning('Activity missing on TEP during synchronization. Activity will be created with no alternatives.')
            act_instruments = connection.execute('SELECT "InstrumentId" FROM "Reports" WHERE "ActivityId"=\'{}\' AND "VleId"={} AND "ActivityTypeId"={} GROUP BY "ActivityId", "VleId", "ActivityTypeId", "InstrumentId"'.format(
                activity_id, vle_id, activity_type_id))
            instruments = []
            for inst in act_instruments:
                inst_id = inst['InstrumentId']
                required = True
                alt_id = None
                instruments.append({
                    "instrument_id": inst_id,
                    "required": required,
                    "alternative_code": alt_id,
                    "active": False
                })
        else:
            act_instruments = connection.execute('SELECT * FROM "AlternativeInstruments" WHERE "ActivityConfigId"=\'{}\''.format(
                act_conf_id))

            instruments = []
            active_instrument_id = []
            for inst in act_instruments:
                inst_id = inst['InstrumentId']
                required = inst['Required']
                alt_id = None
                if not required:
                    alt_id = inst['AlternativeId']

                if inst_id == alt_id:
                    required = True
                    alt_id = None

                instruments.append({
                    "instrument_id": inst_id,
                    "required": required,
                    "alternative_code": alt_id,
                    "active": True
                })

                active_instrument_id.append(inst_id)

            # Check for disabled instruments with existing requests
            act_instruments = connection.execute(
                'SELECT "InstrumentId" FROM "Reports" WHERE "ActivityId"=\'{}\' AND "VleId"={} AND "ActivityTypeId"={} GROUP BY "ActivityId", "VleId", "ActivityTypeId", "InstrumentId"'.format(
                    activity_id, vle_id, activity_type_id))

            for inst in act_instruments:
                inst_id = inst['InstrumentId']
                if inst_id in active_instrument_id:
                    continue
                required = True
                alt_id = None
                instruments.append({
                    "instrument_id": inst_id,
                    "required": required,
                    "alternative_code": alt_id,
                    "active": False
                })
        self.db.activities.update_activity_instruments(act_id, instruments)
        return new_activity

    def sync_learner(self, tesla_id):
        connection = self.engine.connect()
        self.logger.info('Synchronizing learner information with TEP database.')

        learner_results = list(connection.execute(
            'SELECT "Id", "PublicKey", "PublicKeyType" FROM "Learners" WHERE "MaskedTeslaId"=\'{}\''.format(
                tesla_id)))

        if len(learner_results) == 1:
            learner_id = learner_results[0][0]
            key = learner_results[0][1]
            key_type = learner_results[0][2]
        else:
            self.logger.error('Learner not found in TEP when synchronizing learner data.')
            connection.close()
            return None

        learner_agreement = list(connection.execute(
            'SELECT "Id", "AgreementVersionId", "Status" FROM "LearnerAgreements" WHERE "LearnerId"=\'{}\''.format(
                learner_id)))

        has_agreement = False
        ic_id = None
        agreement_accepted = None
        if len(learner_agreement) == 1:
            has_agreement = True

        if has_agreement:
            [first_data, last_data] = list(connection.execute(
                'SELECT MIN("Start"), MAX("Start") FROM "Reports" WHERE "LearnerId"=\'{}\''.format(
                    learner_id)))[0]

            if last_data is None:
                agreement_accepted = datetime.now()
                version = "1.3.0"
                valid_from = datetime(2018, 2, 15)
            else:
                agreement_accepted = first_data
                if last_data < datetime(2017, 2, 1):
                    version = "1.0.0"
                    valid_from = datetime(2016, 9, 1)
                elif last_data < datetime(2017, 9, 1):
                    version = "1.1.0"
                    valid_from = datetime(2017, 2, 1)
                elif last_data < datetime(2018, 2, 15):
                    version = "1.2.0"
                    valid_from = datetime(2017, 9, 1)
                else:
                    version = "1.3.0"
                    valid_from = datetime(2018, 2, 15)

            # Create informed consents
            informed_consent = self.db.learners.get_informed_consent_by_version(version)
            if informed_consent is None:
                informed_consent = self.db.learners.create_informed_consent(version, valid_from)
            ic_id = informed_consent.id

        # Create learner
        crypto_data = encode_data({"type": key_type, "key": key})

        connection.close()

        # Create or update learner
        learner = self.db.learners.get_learner(tesla_id)
        if learner is None:
            learner = self.db.learners.create_learner(tesla_id=tesla_id, crypto_data=crypto_data, consent_id=ic_id,
                                             consent_accepted=agreement_accepted, consent_rejected=None)
            if learner is None:
                self.logger.error("Error creating learner")
                connection.close()
                return None
        else:
            consent_rejected = None
            if learner.consent_id is not None:
                ic_id = learner.consent_id
            if learner.consent_accepted is not None:
                agreement_accepted = learner.consent_accepted
            if learner.consent_rejected is not None:
                consent_rejected = learner.consent_rejected

            self.db.learners.update_learner(tesla_id=tesla_id, crypto_data=crypto_data, consent_id=ic_id,
                                             consent_accepted=agreement_accepted, consent_rejected=consent_rejected)

        connection.close()

        # Sync learner enrolment and verification requests
        self.sync_learner_requests(tesla_id)

        return learner

    def sync_reports(self, block_size, sync_data = True, sync_audit = True):
        connection = self.engine.connect()
        self.logger.info('Synchronizing with TEP database. Block size {}'.format(block_size))

        if self.db.instruments.get_num_instruments() < 7:
            self.logger.warning("TEP Synchronization skipped. Instruments are not up to date.")
            connection.close()
            return

        offset = self.db.config.get_migration_offset("REQUESTS")
        if offset is None:
            connection.close()
            return

        result = connection.execute('SELECT * FROM "Reports" ORDER BY "Id" LIMIT {} OFFSET {}'.format(block_size, offset))
        if result.rowcount == 0:
            self.logger.info("TEP and Broker are synchronized")
            connection.close()
            return

        for row_report in result:
            self.db.db.session.query(TEPMigrations).filter(
                TEPMigrations.element == "REQUESTS").with_for_update().one_or_none()

            # Get activity information
            act_id = None
            tesla_id = None
            if row_report['ActivityId'] is not None:
                # Get the activity configuration
                activity = self._sync_activity(connection, row_report['VleId'], row_report['ActivityId'], row_report['ActivityTypeId'])
                if activity is None:
                    self.logger.error('Invalid Activity when synchronizing TEP reports. Aborting.')
                    connection.close()
                    return
                act_id = activity.id

            # Get Learner information
            learner_results = list(connection.execute('SELECT "MaskedTeslaId", "PublicKey", "PublicKeyType" FROM "Learners" WHERE "Id"={}'.format(row_report['LearnerId'])))
            if len(learner_results) == 1:
                tesla_id = learner_results[0][0]
                key = learner_results[0][1]
                key_type = learner_results[0][2]
            else:
                self.logger.error('Invalid Learner when synchronizing TEP reports')
                connection.close()
                return

            learner = self.db.learners.get_learner(tesla_id)
            if learner is None:
                learner_agreement = list(connection.execute(
                    'SELECT "Id", "AgreementVersionId", "Status" FROM "LearnerAgreements" WHERE "LearnerId"=\'{}\''.format(
                        row_report['LearnerId'])))

                has_agreement = False
                ic_id = None
                agreement_accepted = None
                if len(learner_agreement) == 1:
                    has_agreement = True

                if has_agreement:
                    [first_data, last_data] = list(connection.execute('SELECT MIN("Start"), MAX("Start") FROM "Reports" WHERE "LearnerId"=\'{}\''.format(row_report['LearnerId'])))[0]

                    if last_data is None:
                        agreement_accepted = datetime.now()
                        version = "1.3.0"
                        valid_from = datetime(2018, 2, 15)
                    else:
                        agreement_accepted = first_data
                        if last_data < datetime(2017, 2, 1):
                            version = "1.0.0"
                            valid_from = datetime(2016, 9, 1)
                        elif last_data < datetime(2017, 9, 1):
                            version = "1.1.0"
                            valid_from = datetime(2017, 2, 1)
                        elif last_data < datetime(2018, 2, 15):
                            version = "1.2.0"
                            valid_from = datetime(2017, 9, 1)
                        else:
                            version = "1.3.0"
                            valid_from = datetime(2018, 2, 15)

                    # Create informed consents
                    informed_consent = self.db.learners.get_informed_consent_by_version(version)
                    if informed_consent is None:
                        informed_consent = self.db.learners.create_informed_consent(version, valid_from)
                    ic_id = informed_consent.id

                # Create learner
                crypto_data = encode_data({"type": key_type, "key": key})
                learner = self.db.learners.create_learner(tesla_id=tesla_id, crypto_data=crypto_data, consent_id=ic_id, consent_accepted=agreement_accepted, consent_rejected=None)
                if learner is None:
                    self.logger.error("Error creating learner")
                    connection.close()
                    return

            instrument_list = [row_report['InstrumentId']]
            request_id = row_report['Id']

            # Check if request exists
            new_request = self.db.requests.get_request(request_id)
            if new_request is not None:
                # Check values
                if new_request.tesla_id != tesla_id:
                    self.logger.error(
                        "Learner from current request is different from the one in TEP. Aborting. request_id={}".format(
                            request_id))
                    connection.close()
                    return

                if new_request.activity_id is not None and new_request.activity_id != act_id:
                    self.logger.error(
                        "Activity from current request is different from the one in TEP. Aborting. request_id={}".format(
                            request_id))
                    connection.close()
                    return

                if new_request.activity_id is None and act_id is not None:
                    self.db.requests.update_request_activity(request_id, act_id)

            if new_request is None:
                if row_report['IsEnrolmentRequest']:
                    new_request = self.db.requests.create_enrollment_request(tesla_id, instrument_list, id=request_id, activity_id=act_id)
                else:
                    new_request = self.db.requests.create_verification_request(tesla_id, act_id, instrument_list, id=request_id)

            if new_request is None:
                self.logger.error("Error creating request")
                connection.close()
                return

            if sync_audit or sync_data:
                data = list(connection.execute('SELECT "SampleData", "AuditDataIncludeEnrolement", "AuditDataIncludeRequest" FROM "ReportSampleData" WHERE "ReportId"={}'.format(
                        request_id)))

                if len(data)==1:
                    [sample_data, include_enrolment, include_request] = data[0]
                    if sync_data:
                        request_data = self.db.get_request_data(request_id)
                        if request_data is None:
                            self.storage.save_request_data(request_id, sample_data)

                    if sync_audit:
                        self.storage.save_request_audit_data(request_id, row_report['InstrumentId'], include_enrolment,
                                                         include_request, row_report['AuditData'])
            error_id = 0
            if row_report['ErrorId'] is not None:
                error_id = int(row_report['ErrorId'])
                progress = 1.0
                status = TESLA_RESULT_STATUS.FAILED
            else:
                progress = 1.0
                status = TESLA_RESULT_STATUS.DONE
                if row_report['RequestStatus'] == 0:
                    status = TESLA_RESULT_STATUS.PENDING
                    progress = 0.0

            finish_value = row_report['Finish']
            if str(finish_value) == '0001-01-01 00:00:00.000000':
                finish_value = None
            self.db.requests.create_update_result(request_id, row_report['InstrumentId'], row_report['Start'],
                                         finish_value, error_id, row_report['ErrorMsg'],
                                         row_report['Result'], None, status, progress)
            if row_report['IsEnrolmentRequest']:
                self.db.requests.update_enrollment_percentage_from_result(request_id, row_report['InstrumentId'], row_report['Result'])

            # Update the request status
            self.db.requests.fix_request_status(request_id)

            offset = offset + 1
            self.db.config.update_migration_offset("REQUESTS", offset)

        connection.close()

    def sync_learner_requests(self, tesla_id, filter_type=None):
        connection = self.engine.connect()
        self.logger.info('Synchronizing learner requests with TEP database. Filter value = {}'.format(filter_type))

        learner_results = list(connection.execute(
            'SELECT "Id", "PublicKey", "PublicKeyType" FROM "Learners" WHERE "MaskedTeslaId"=\'{}\''.format(
                tesla_id)))

        if len(learner_results) == 1:
            learner_id = learner_results[0][0]
        else:
            connection.close()
            return None

        if filter_type is None:
            learner_requests = connection.execute('SELECT * FROM "Reports" WHERE "LearnerId"=\'{}\''.format(learner_id))
        else:
            if filter_type:
                learner_requests = connection.execute(
                    'SELECT * FROM "Reports" WHERE "LearnerId"=\'{}\' AND "IsEnrolmentRequest"=true'.format(learner_id))
            else:
                learner_requests = connection.execute(
                    'SELECT * FROM "Reports" WHERE "LearnerId"=\'{}\' AND "IsEnrolmentRequest"=false'.format(learner_id))

        for row_report in learner_requests:
            # Get activity information
            act_id = None
            if row_report['ActivityId'] is not None:
                # Get the activity configuration
                activity = self._sync_activity(connection, row_report['VleId'], row_report['ActivityId'],
                                               row_report['ActivityTypeId'])
                if activity is None:
                    self.logger.error('Invalid Activity when synchronizing TEP reports. Aborting.')
                    connection.close()
                    return
                act_id = activity.id

            instrument_list = [row_report['InstrumentId']]
            request_id = row_report['Id']

            # Check if request exists
            new_request = self.db.requests.get_request(request_id)
            if new_request is not None:
                # Check values
                if new_request.tesla_id != tesla_id:
                    self.logger.error("Different request with same ID. TeSLA ID does not match. Aborting. request_id={}, tesla_id={}/{}".format(request_id, new_request.tesla_id, tesla_id))
                    connection.close()
                    return

                if new_request.activity_id != act_id:
                    if new_request.activity_id is None and act_id is not None:
                        self.logger.info("Recovered missing activity in request")
                        self.db.requests.update_request_activity(new_request.id, act_id)
                    else:
                        self.logger.error("Different request with same ID. Activity does not match. Aborting. request_id={}, activity_id={}/{}".format(request_id, new_request.activity_id, act_id))
                        connection.close()
                        return

            if new_request is None:
                if row_report['IsEnrolmentRequest']:
                    new_request = self.db.requests.create_enrollment_request(tesla_id, instrument_list, id=request_id,
                                                                             activity_id=act_id)
                else:
                    new_request = self.db.requests.create_verification_request(tesla_id, act_id, instrument_list,
                                                                               id=request_id)

            if new_request is None:
                self.logger.error("Error creating request")
                connection.close()
                return

            error_id = 0
            if row_report['ErrorId'] is not None:
                error_id = int(row_report['ErrorId'])
                progress = 1.0
                status = TESLA_RESULT_STATUS.FAILED
            else:
                progress = 1.0
                status = TESLA_RESULT_STATUS.DONE
                if row_report['RequestStatus'] == 0:
                    status = TESLA_RESULT_STATUS.PENDING
                    progress = 0.0
            finish_value = row_report['Finish']
            if str(finish_value) == '0001-01-01 00:00:00.000000':
                finish_value = None
            self.db.requests.create_update_result(request_id, row_report['InstrumentId'], row_report['Start'],
                                                  finish_value, error_id, row_report['ErrorMsg'],
                                                  row_report['Result'], None, status, progress)
            if row_report['IsEnrolmentRequest']:
                self.db.requests.update_enrollment_percentage_from_result(request_id, row_report['InstrumentId'],
                                                                          row_report['Result'])
            # Update the request status
            self.db.requests.fix_request_status(request_id)
        connection.close()

    def sync_instrument_thresholds(self):
        connection = self.engine.connect()
        self.logger.info('Synchronizing instrument thresholds with TEP database.')

        instrument_thresholds = list(connection.execute(
            'SELECT i."ShortName", t."low", t."medium", t."high", t."audit_level" FROM "Instruments" i, "InstrumentThresholds" t WHERE i."Id" = t."instrument"'))

        for thr_row in instrument_thresholds:
            acronym = thr_row[0]
            low = thr_row[0]
            medium = thr_row[0]
            high = thr_row[0]
            audit_level = thr_row[0]

            instrument = self.db.instruments.get_instrument_by_acronym(acronym)
            if instrument is not None:
                self.db.instruments.create_or_update_instrument_thresholds(instrument.id, low, medium, high, audit_level)

        connection.close()

    def update_instrument_thresholds(self):
        connection = self.engine.connect()
        self.logger.info('Update instrument thresholds to TEP database.')

        instrument_thresholds = list(connection.execute(
            'SELECT i."ShortName", t."low", t."medium", t."high", t."audit_level" FROM "Instruments" i, "InstrumentThresholds" t WHERE i."Id" = t."instrument"'))

        instruments = self.db.instruments.get_instruments()

        for instrument in instruments:
            instrument_thresholds = self.db.instruments.get_instrument_thresholds(instrument.id)

            for thr_row in instrument_thresholds:
                acronym = thr_row[0]
                low = thr_row[0]
                medium = thr_row[0]
                high = thr_row[0]
                audit_level = thr_row[0]

                #instrument = self.db.instruments.get_instrument_by_acronym(acronym)
                if instrument is not None:
                    inst_thr = self.db.instruments.get_instrument_thresholds(instrument.id)
                    if inst_thr is not None:
                        connection.execute(
                            'REPLACE "InstrumentThresholds" SET "low"={}, "medium"={}, "high"={}, "audit_level"=\'{}\' WHERE "instrument"={}}'.format(
                                inst_thr.low, inst_thr.medium, inst_thr.high, inst_thr.audit_level, inst_thr.instrument_id
                            ))

        connection.close()

    def get_enrolment_samples(self, tesla_id, instrument_id):
        connection = self.engine.connect()
        self.logger.info('Get enrolment samples from TEP database.')

        learner_results = list(connection.execute(
            'SELECT "Id" FROM "Learners" WHERE "MaskedTeslaId"=\'{}\''.format(
                tesla_id)))

        if len(learner_results) == 1:
            learner_id = learner_results[0][0]
        else:
            self.logger.error('Learner not found in TEP when getting learner data.')
            connection.close()
            return None

        enrolment_requests = connection.execute(
            'SELECT * FROM "Reports" WHERE "LearnerId"=\'{}\' AND "IsEnrolmentRequest"=true AND "InstrumentId"={}'.format(learner_id, instrument_id))

        connection.close()

        return list(enrolment_requests)

    def get_failed_enrolment_samples(self, tesla_id, instrument_id):
        connection = self.engine.connect()
        self.logger.info('Get failed enrolment samples from TEP database.')

        learner_results = list(connection.execute(
            'SELECT "Id" FROM "Learners" WHERE "MaskedTeslaId"=\'{}\''.format(
                tesla_id)))

        if len(learner_results) == 1:
            learner_id = learner_results[0][0]
        else:
            self.logger.error('Learner not found in TEP when getting learner data.')
            connection.close()
            return None

        enrolment_requests = connection.execute(
            'SELECT * FROM "Reports" WHERE "LearnerId"=\'{}\' AND "IsEnrolmentRequest"=true AND "InstrumentId"={} AND "RequestStatus"=1'.format(learner_id, instrument_id))

        connection.close()

        return list(enrolment_requests)

    def get_request_data(self, request_id):
        connection = self.engine.connect()
        self.logger.info('Get request data from TEP database.')

        data_row = connection.execute(
            'SELECT "SampleData" FROM "ReportSampleData" WHERE "ReportId"={}'.format(request_id))

        connection.close()

        if data_row.rowcount != 1:
            return None

        return list(data_row)[0][0]

    def update_enrolment(self, tesla_id, inst_p):
        pass

    def update_request_result(self, request_id, result):
        pass

    def update_enrolment_status(self):
        pass

    def get_activity_audit(self, vle_id, activity_type, activity_id, tesla_id, instrument_id):
        connection = self.engine.connect()
        self.logger.info('Get activity audit data from TEP database.')

        # Get the activity configuration
        query = 'SELECT r."Id", r."Result", r."Start", r."Finish", r."AuditData", s."SampleData" FROM "Learners" l, "ActivityConfigs" c, "Reports" r, "ActivityTypes" at, "ReportSampleData" s '
        query += 'WHERE r."ActivityTypeId"=at."Id" AND c."ActivityTypeId"=r."ActivityTypeId" AND c."VleId"=r."VleId" AND c."ActivityId"=r."ActivityId" AND r."LearnerId"=l."Id" AND s."ReportId"=r."Id"'
        query += 'AND l."MaskedTeslaId"=\'{}\' AND r."ActivityId"=\'{}\' AND at."Description"=\'{}\' AND r."VleId"={} AND r."InstrumentId"={}'

        query = query.format(tesla_id, activity_id, activity_type, vle_id, instrument_id)
        audit_results = connection.execute(query)
        audit_data = []

        for r in audit_results:
            finish = r[3]
            if str(finish) == '0001-01-01 00:00:00':
                finish = None
            audit_data.append({
                "id":  r[0],
                "result": r[1],
                "start": r[2],
                "finish": finish,
                "audit": r[4],
                "sample": r[5]
            })

        connection.close()

        return audit_data
