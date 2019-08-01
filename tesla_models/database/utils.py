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

import pickle
from sqlalchemy import asc, desc, or_


def encode_data(json_data):
    if json_data is None:
        return None
    return pickle.dumps(json_data, pickle.HIGHEST_PROTOCOL)


def decode_data(encoded_data):
    if encoded_data is None:
        return None
    return pickle.loads(encoded_data)


class ResultsPagination():

    def __init__(self, request, search_fields=None):
        self.search = request.args.get('search')
        self.sort = request.args.get('sort')
        self.order = request.args.get('order')
        self.search_fields = search_fields
        self.page = request.args.get('page')
        self.per_page = request.args.get('page')
        self.max_per_page = None
        self.limit = request.args.get('limit')
        self.offset = request.args.get('offset')

        if self.search is '':
            self.search = None
        if self.sort is '':
            self.sort = None
        if self.order is not 'asc' and self.order is not 'desc':
            self.order = 'asc'

        if self.page is not None:
            self.page = int(self.page)
        if self.per_page is not None:
            self.per_page = int(self.per_page)
        if self.offset is not None:
            self.offset = int(self.offset)
        if self.limit is not None:
            self.limit = int(self.limit)

        if self.per_page is None and self.limit is not None:
            self.per_page = self.limit
        if self.page is None and self.offset is not None and self.per_page is not None:
            self.page = int(self.offset/self.per_page) + 1

    def get_results(self, query):
        # Set the sorting field
        if self.sort is None:
            if query._group_by != False:
                self.sort = list(query._group_by)[0].description
            else:
                self.sort = list(query._primary_entity.entity_zero._all_pk_props)[0].description

        # Apply search query
        if self.search is not None and self.search_fields is not None and len(self.search_fields) > 0:
            # TODO: Apply filtering
            if len(self.search_fields) > 1:
                for i in range(1, len(self.search_fields)):
                    pass
            else:
                query.filter_by(self.search_fields[0]=='%' + str(q) + '%')

        # Apply results sorting
        if self.order == 'asc':
            query = query.order_by(asc(self.sort))
        else:
            query = query.order_by(desc(self.sort))

        return query.paginate(page=self.page, per_page=self.per_page, max_per_page=self.max_per_page)

