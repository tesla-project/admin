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

import dotenv
import json
from git import Repo
import os
import errno
import fileinput
import codecs
import io



_git_repo = None
_module_config = None


class FileConfig(object):
    valid = False
    error = None
    __escape_decoder = codecs.getdecoder('unicode_escape')

    def __init__(self, conf_file, force_creation=False):
        self.conf_file = conf_file

        if not os.path.exists(self.conf_file):
            if force_creation is True:
                try:
                    os.makedirs(os.path.dirname(self.conf_file))
                except FileExistsError:
                    pass

                f = open(self.conf_file, "w")
                f.close()
            else:
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), self.conf_file)

    def get_value(self, key, default=None):
        value = dotenv.get_key(self.conf_file, key)
        if value is None:
            return default
        return value

    def set_value(self, key, value):
        dotenv.set_key(self.conf_file, key, value)

    def get_values(self):
        values = dotenv.dotenv_values(self.conf_file)
        return values

    def set_values(self, values):
        for key in values:
            dotenv.set_key(self.conf_file, key, values[key])

    def replaced_set_value(self, key, value):
        self.replaced_function_set_key(self.conf_file, key, value)

    def replaced_function_set_key(self, dotenv_path, key_to_set, value_to_set, quote_mode="always"):
        """
        Adds or Updates a key/value to the given .env

        If the .env path given doesn't exist, fails instead of risking creating
        an orphan .env somewhere in the filesystem
        """
        value_to_set = value_to_set.strip("'").strip('"')

        if " " in value_to_set:
            quote_mode = "always"

        line_template = '{}="{}"\n' if quote_mode == "always" else '{}={}\n'
        line_out = line_template.format(key_to_set, value_to_set)

        replaced = False
        for line in fileinput.input(dotenv_path, inplace=True):
            k, v = self.parse_line(line)
            if k == key_to_set:
                replaced = True
                line = line_out
            print(line, end='')

        if not replaced:
            with io.open(dotenv_path, "a") as f:
                f.write("{}\n".format(line_out))

        return True, key_to_set, value_to_set


    def parse_line(self, line):
        line = line.strip()

        # Ignore lines with `#` or which doesn't have `=` in it.
        if not line or line.startswith('#') or '=' not in line:
            return None, None

        k, v = line.split('=', 1)

        if k.startswith('export '):
            k = k.lstrip('export ')

        # Remove any leading and trailing spaces in key, value
        k, v = k.strip(), v.strip()

        if v:
            v = v.encode('unicode-escape').decode('ascii')
            quoted = v[0] == v[-1] in ['"', "'"]
            if quoted:
                v = self.decode_escaped(v[1:-1])

        return k, v

    def decode_escaped(self, escaped):
        return self.__escape_decoder(escaped)[0]


class ServiceFileConfig(FileConfig):
    def __init__(self, service, base_path='./'):
        self.service = service
        self.conf_path = os.path.join(base_path, 'services', self.service)
        super(ServiceFileConfig, self).__init__(os.path.join(self.conf_path, '.env'))

    def get_config(self):
        return self.get_values()

    def set_config(self, key, value):
        FileConfig(os.path.join(self.conf_path, self.service, '.env')).replaced_function_set_key(key, value)


class ModuleFileConfig(FileConfig):

    def __init__(self, module, base_path='./'):
        self.module = module
        self.conf_path = os.path.join(base_path, 'modules', self.module)
        self.services_path = os.path.join(base_path, 'services')
        super(ModuleFileConfig, self).__init__(os.path.join(self.conf_path, '.env'), force_creation=True)

    def get_service_config(self, service):
        dependencies = None
        if os.path.exists(os.path.join(self.conf_path, 'dependencies.json')):
            dependencies = json.load(open(os.path.join(os.path.join(self.conf_path, 'dependencies.json'))))

        srv_vals = None
        if dependencies is not None:
            if "services" in dependencies:
                if service in dependencies['services']:
                    srv_vals = FileConfig(os.path.join(self.services_path, service, '.env')).get_values()
                    try:
                        srv_mod_vals = FileConfig(os.path.join(self.conf_path, service + '.env')).get_values()
                    except FileNotFoundError:
                        srv_mod_vals = {}
                    srv_vals.update(srv_mod_vals)

        return srv_vals

    def set_service_config(self, service, config):
        dependencies = None
        if os.path.exists(os.path.join(self.conf_path, 'dependencies.json')):
            dependencies = json.load(open(os.path.join(os.path.join(self.conf_path, 'dependencies.json'))))

        if dependencies is not None:
            if "services" in dependencies:
                if service in dependencies['services']:
                    update_vals = {}
                    srv_vals = FileConfig(os.path.join(self.services_path, service, '.env'), force_creation=True).get_values()

                    for key in srv_vals:
                        if key in config.keys() and config[key] != srv_vals[key]:
                            update_vals[key] = config[key]

                    if len(update_vals) == 0:
                        if os.path.exists(os.path.join(self.conf_path, service + '.env')):
                            os.remove(os.path.join(self.conf_path, service + '.env'))
                    else:
                        FileConfig(os.path.join(self.conf_path, service + '.env'), force_creation=True).set_values(update_vals)

    def get_config(self):
        dependencies = None
        if os.path.exists(os.path.join(self.conf_path, 'dependencies.json')):
            dependencies = json.load(open(os.path.join(os.path.join(self.conf_path, 'dependencies.json'))))

        base_config = self.get_values()
        if dependencies is not None:
            if "services" in dependencies:
                for srv in dependencies['services']:
                    srv_vals = FileConfig(os.path.join(self.services_path, srv, '.env')).get_values()
                    try:
                        srv_mod_vals = FileConfig(os.path.join(self.conf_path, srv + '.env')).get_values()
                    except FileNotFoundError:
                        srv_mod_vals = {}
                    srv_vals.update(srv_mod_vals)
                    base_config.update(srv_vals)

        return base_config

    def set_config(self, key, value):
        FileConfig(os.path.join(self.conf_path, self.module, '.env')).replaced_function_set_key(key, value)


    def get_module_dependencies(self):
        dependencies = None
        if os.path.exists(os.path.join(self.conf_path, 'dependencies.json')):
            dependencies = json.load(open(os.path.join(os.path.join(self.conf_path, 'dependencies.json'))))
        return dependencies


class ConfigRepository(object):
    def __init__(self, work_path, domain, git_url=None, git_user=None, git_password=None):
        self.work_path = work_path
        self.git_url = 'https://{}:{}@{}'.format(git_user, git_password, git_url)
        self.domain = domain

        if not os.path.exists(work_path):
            self.repository = Repo.clone_from(self.git_url, self.work_path)
        else:
            self.repository = Repo(self.work_path)

    def pull(self):
        self.repository.remotes['origin'].pull()

    def push(self):
        for new_file in self.repository.untracked_files:
            self.repository.index.add(new_file)
        self.repository.index.commit('Updated configuration')
        self.repository.remotes['origin'].push()

    def get_module_config(self, module):
        return ModuleFileConfig(module, os.path.join(self.work_path, self.domain))

    def get_service_config(self, service):
        return ServiceFileConfig(service, os.path.join(self.work_path, self.domain))

    def get_module_dependencies(self, module):
        return ModuleFileConfig(module, os.path.join(self.work_path, self.domain)).get_module_dependencies()

    def get_service_list(self):
        return ["database", "elasticsearch", "mail", "minio", "portal", "rabbit", "redis", "tep", "tip", "tep_db"]

    def get_module_list(self):
        return ["admin", "api", "beat", "flower", "fr", "lti", "nginx-proxy", "rt", "tep", "tfr", "tip", "vle", "worker"]

    


def get_config_repository():
    global _git_repo

    if _git_repo is None:
        domain = os.getenv("DOMAIN", None)
        git_url = os.getenv("GIT_REPOSITORY", None)
        git_user = os.getenv("GIT_USER", None)
        git_password = os.getenv("GIT_PASSWORD", None)
        working_path = os.getenv("GIT_WORKING_PATH", './data_admin')

        if domain is None:
            print('DOMAIN must be provided as environment variable')
            exit(1)

        if not os.path.exists(working_path):
            if git_url is None:
                print('GIT_REPOSITORY must be provided as environment variable')
                exit(1)

            if git_user is None or git_password is None:
                print('GIT_USER and GIT_PASSWORD must be provided as environment variables')
                exit(1)
        else:
            if git_url is None:
                print('GIT_REPOSITORY must be provided as environment variable to allow changes')

            if git_user is None or git_password is None:
                print('GIT_USER and GIT_PASSWORD must be provided as environment variables to allow changes')

        _git_repo = ConfigRepository(working_path, domain, git_url, git_user, git_password)

    return _git_repo # type: ConfigRepository


def get_config_value(key, default=None):
    global _module_config

    if _module_config is None:
        module = os.getenv('MODULE_NAME', None)

        if module is None:
            print('MODULE_NAME must be provided as environment variable')
            exit(1)

        module = module.lower()
        repo = get_config_repository()
        repo.pull()
        mod_config = repo.get_module_config(module)
        _module_config = mod_config.get_config()

    key_val = default
    if key in _module_config:
        key_val = _module_config[key]

    return key_val
