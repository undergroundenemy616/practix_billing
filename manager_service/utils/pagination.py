from collections import OrderedDict
from typing import Union

from config.settings.base import (MAX_PAGE_SIZE, PAGE_QUERY_PARAM,
                                  PAGE_SIZE_QUERY_PARAM)
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class DynamicPageNumberPagination(PageNumberPagination):
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    page_query_param = PAGE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE
    page_size = None

    def get_page_metadata(self):
        return {
            'total_pages': self.page.paginator.num_pages,
            'page': self.page.number,
            'per_page': self.get_page_size(self.request)
        }

    def get_paginated_data(self, data: Union[ReturnDict, ReturnList]) -> OrderedDict:
        meta = self.get_page_metadata()
        if isinstance(data, list):
            data = OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
                ('meta', meta)
            ])
        else:
            if 'meta' in data:
                data['meta'].update(meta)
            else:
                data['meta'] = meta
        return data
