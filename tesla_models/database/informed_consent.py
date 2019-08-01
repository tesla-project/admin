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

from tesla_models.models import InformedConsent, InformedConsentDocument
from sqlalchemy import asc, desc, or_
from flask_security.utils import hash_password
from flask_security import current_user


class InformedConsentDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def get_informed_consents(self, q=None, limit=None, offset=0, sort='id', order='asc'):
        # todo: add valid_from in search query
        results = []
        try:
            if sort is '' or sort is None:
                sort = 'id'

            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = InformedConsent.query.filter(or_(InformedConsent.version.like(q)))
            else:
                query = InformedConsent.query

            if order == 'asc':
                query = query.order_by(asc(sort))
            else:
                query = query.order_by(desc(sort))

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            results = query.all()

        except Exception:
            self.logger.exception("Error getting list informed consent")

        return results

    def count_informed_consents(self, q=None, limit=None, offset=0):
        # todo: add valid_from in search query
        result = 0
        try:
            if q is not None and q is not '':
                q = '%'+str(q)+'%'
                query = InformedConsent.query.filter(or_(InformedConsent.version.like(q)))
            else:
                query = InformedConsent.query

            query = query.offset(offset)

            if limit is not None:
                query = query.limit(limit)

            result = query.count()

        except Exception:
            self.logger.exception("Error getting count informed consent")

        return result

    def get_informed_consent(self, id):
        result = None
        try:
            result = InformedConsent.query.filter(InformedConsent.id == id).first()
        except Exception:
            self.logger.exception("Error getting informed consent")

        return result

    def informed_consent_addedit(self, id, form):
        result = False
        try:
            if id is 0:
                informed_consent = InformedConsent(version=form.data.get('version'), valid_from=form.data.get('valid_from'))
                self.db.session.add(informed_consent)
                self.db.session.commit()

                id = informed_consent.id
            else:
                self.db.session.query(InformedConsent).filter(InformedConsent.id == id).update(
                    {
                        InformedConsent.version: form.data.get('version'),
                        InformedConsent.valid_from: form.data.get('valid_from'),
                    })
                self.db.session.commit()

            result = True
        except Exception:
            self.logger.exception("Error getting addedit informed_consent")

        return result

    def get_informed_consent_documents(self, id):
        result = []
        try:
            result = InformedConsentDocument.query.filter(InformedConsentDocument.consent_id == id).all()
        except Exception:
            self.logger.exception("Error getting informed consent documents")

        return result

    def get_informed_consent_document(self, id, language):
        result = None
        try:
            result = InformedConsentDocument.query.filter(InformedConsentDocument.consent_id == id,
                                                          InformedConsentDocument.language == language).first()
        except Exception:
            self.logger.exception("Error getting informed consent document")

        return result

    def informed_consent_document_addedit(self, id, language, html, pdf):
        result = False
        try:
            result = InformedConsent.query.filter(InformedConsentDocument.consent_id == id, InformedConsentDocument.language == language).first()

            if result:
                self.db.session.query(InformedConsentDocument).filter(InformedConsentDocument.consent_id == id, InformedConsentDocument.language == language).update(
                    {
                        InformedConsentDocument.html: html,
                        InformedConsentDocument.pdf: pdf,
                        InformedConsentDocument.language: language
                    })
                self.db.session.commit()
            else:
                informed_consent_document = InformedConsentDocument(language=language, html=html, pdf=pdf, consent_id=id)
                self.db.session.add(informed_consent_document)
                self.db.session.commit()

                id = informed_consent_document.consent_id


            result = True
        except Exception:
            self.logger.exception("Error getting addedit informed_consent_document")

        return result
