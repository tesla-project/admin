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

from tesla_models.models import VLE, Configuration


class VleDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def get_vle(self, id):
        try:
            vle = VLE.query.filter_by(id=id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting VLE for id {}".format(id))
            vle = None

        return vle

    def get_vles(self):
        try:
            vles = VLE.query.all()
        except Exception:
            self.logger.exception("Error getting VLEs")
            vles = None

        return vles

    def get_vle_by_vle_id(self, vle_id):
        try:
            vle = VLE.query.filter_by(vle_id=vle_id).one_or_none()
        except Exception:
            self.logger.exception("Error selecting VLE for vle_id {}".format(id))
            vle = None

        return vle

    def get_configured_vles(self):
        try:
            vles = VLE.query.filter(VLE.url!=None, VLE.token!=None).all()
        except Exception:
            self.logger.exception("Error selecting configured VLEs")
            vles = None

        return vles

    def create_vle(self, name, vle_id=None, url=None, token=None):
        try:
            new_vle = VLE(name=name, vle_id=vle_id, url=url, token=token)

            self.db.session.add(new_vle)
            self.db.session.commit()
            self.db.session.refresh(new_vle)
        except Exception:
            self.logger.exception("Error creating new VLE {}".format(name))
            new_vle = None

        return new_vle

    def update_vle(self, id, name, vle_id=None, url=None, token=None):
        try:
            VLE.query.filter_by(id=id) \
                .update({
                    'name': name,
                    'vle_id': vle_id,
                    'url': url,
                    'token': token})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating VLE with Id={}".format(id))
            return False

        return True

    def update_vle_access(self, id, url=None, token=None):
        try:
            VLE.query.filter_by(id=id) \
                .update({
                'url': url,
                'token': token})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating VLE access data with Id={}".format(id))
            return False

        return True
