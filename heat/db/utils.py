#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class LazyPluggable(object):
    """A pluggable backend loaded lazily based on some value."""

    def __init__(self, pivot, **backends):
        self.__backends = backends
        self.__pivot = pivot
        self.__backend = None

    def __get_backend(self):
        if not self.__backend:
            backend_name = 'sqlalchemy'
            backend = self.__backends[backend_name]
            if isinstance(backend, tuple):
                name = backend[0]
                fromlist = backend[1]
            else:
                name = backend
                fromlist = backend

            self.__backend = __import__(name, None, None, fromlist)
        return self.__backend

    def __getattr__(self, key):
        backend = self.__get_backend()
        return getattr(backend, key)


IMPL = LazyPluggable('backend',
                     sqlalchemy='heat.db.sqlalchemy.api')


def purge_deleted(age, granularity='days', project_id=None, batch_size=20):
    IMPL.purge_deleted(age, granularity, project_id, batch_size)


def encrypt_parameters_and_properties(ctxt, encryption_key, verbose):
    IMPL.db_encrypt_parameters_and_properties(ctxt, encryption_key,
                                              verbose=verbose)


def decrypt_parameters_and_properties(ctxt, encryption_key, verbose):
    IMPL.db_decrypt_parameters_and_properties(ctxt, encryption_key,
                                              verbose=verbose)
