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

from tesla_models.models import Configuration, VLE, TEPMigrations
from sqlalchemy import asc, desc, or_

class ConfigDB(object):

    def __init__(self, db, logger):
        self.logger = logger
        self.db = db

    def get_configuration(self, key):
        try:
            config = Configuration.query.filter_by(key=key).one_or_none()
        except Exception:
            self.logger.exception("Error selecting configuration for key {}".format(key))
            config = None

        return config

    def get_configuration_value(self, key):
        try:
            config = Configuration.query.filter_by(key=key).one_or_none()
            value = None
            if config is not None:
                value = config.value
        except Exception:
            self.logger.exception("Error selecting configuration for key {}".format(key))
            value = None

        return value

    def create_configuration(self, key, description, value):
        try:
            new_conf = Configuration(key=key, description=description, value=value)

            self.db.session.add(new_conf)
            self.db.session.commit()
            self.db.session.refresh(new_conf)
        except Exception:
            self.logger.exception("Error creating new configuration {}".format(key))
            new_conf = None

        return new_conf

    def update_configuration_value(self, key, value):
        try:
            Configuration.query.filter_by(key=key) \
                .update({'value': value})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating value for configuration key {}".format(key))
            return False
        return True

    def update_configuration_description(self, key, description):
        try:
            Configuration.query.filter_by(key=key) \
                .update({'description': description})
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating description for configuration key {}".format(key))
            return False
        return True

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
            vle = None

        return vle

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
            Configuration.query.filter_by(id=id) \
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

    def get_migration_offset(self, element):
        try:
            offset = TEPMigrations.query.filter(TEPMigrations.element == element).one_or_none()
            if offset is None:
                new_offset = TEPMigrations(element=element, offset=0)
                self.db.session.add(new_offset)
                self.db.session.commit()
                return 0
        except Exception:
            self.logger.exception("Error selecting offset for TEP migrations for element {}".format(element))
            offset = None

        return int(offset.offset)

    def update_migration_offset(self, element, offset):
        try:
            TEPMigrations.query.filter_by(element=element) \
                .update({
                    'offset': offset
                })
            self.db.session.commit()
        except Exception:
            self.logger.exception("Error updating offset for TEP migrations for element {}".format(element))
            return False

        return True
