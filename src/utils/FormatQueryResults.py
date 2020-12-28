from functools import wraps
from typing import List


def AddFormatterToQuery(field_names: List[str]):
    def format_query(func):
        @wraps(func)
        def formatter(*args, **kwargs):
            def _formatter(result_list):
                returnee = [
                    {
                        field_name: val[index]  for index, field_name in enumerate(field_names) if len(val) - 1 >= index
                    } for val in result_list
                ]
                return returnee
            results = func(*args, **kwargs)
            return results + [_formatter]
        return formatter
    return format_query
