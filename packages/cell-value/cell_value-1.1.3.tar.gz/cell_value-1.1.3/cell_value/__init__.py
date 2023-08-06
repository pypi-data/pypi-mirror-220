import json
from enum import Enum

import jsonschema


class FilterMethod(Enum):
    FILTER_ALL_EXACT = 'all_exact'  # 精确匹配，args 完全相等
    FILTER_ALL_FUZZY = 'all_fuzzy'  # 模糊匹配，当前.args 均与对比的 CellValue.args 模糊匹配
    FILTER_ANY_EXACT = 'any_exact'  # 精确匹配, 当前.args 至少存在一个与对比的 CellValue.args 一样
    FILTER_ANY_FUZZY = 'any_fuzzy'  # 模糊匹配，当前.args 至少存在一个与对比的 CellValue.args 模糊匹配


RevertFilterMethod = {member.value: member for member in FilterMethod}


class CellValue:
    SCHEMA = {
        "type": "object",
        "properties": {
            "data_list": {
                "type": "array",
                "minItems": 1,
                "maxItems": 99,
                "prefixItems": [
                    {"type": "string"}
                ]
            },
            "trace_id": {
                "type": ["string", "null", "integer"]
            },
            "filter_method": {
                "type": "string",
                "enum": [member.value for member in FilterMethod]
            }

        },
        "required": ["data_list", "filter_method", "trace_id"]
    }

    def __init__(self, args: str or tuple or list or set, filter_method: FilterMethod = '',
                 filter_ext='', trace_id=None):
        """

        :param trace_id:  可携带上下文id，在不同应用流通
        :param args:
        """
        self.filter_method = filter_method if filter_method else FilterMethod.FILTER_ALL_EXACT  # 默认全精确匹配
        if isinstance(args, str):
            self.args = [args]
        elif isinstance(args, (tuple, list, set)):
            self.args = list(args)
        else:
            raise ValueError(f'args 参数类型不合法')
        self.trace_id = trace_id

    def __str__(self):
        if not self.trace_id:
            return f'{self.args}'
        return f'trace_id={self.trace_id} {self.args}'

    def tag_trace(self, trace_id):
        self.trace_id = trace_id

    @classmethod
    def loads(cls, json_string: str or dict):
        if isinstance(json_string, str):
            data = json.loads(json_string)
        elif isinstance(json_string, dict):
            data = json_string
        else:
            raise ValueError(f'json_string 必须为 str or dict ,不允许{type(json_string)}')
        jsonschema.validate(data, cls.SCHEMA)
        obj = cls(args=json_string['data_list'],
                  filter_method=RevertFilterMethod.get(data['filter_method']))
        obj.tag_trace(json_string.get('trace_id'))
        return obj

    def dumps(self, as_json=False) -> dict or json:
        d = {
            'data_list': [],
            'trace_id': None
        }

        d['data_list'] = self.args
        d['trace_id'] = self.trace_id
        d['filter_method'] = self.filter_method.value
        jsonschema.validate(d, self.SCHEMA)

        if as_json:
            return json.dumps(d)
        return d

    def __eq__(self, other: 'self'):
        current_data = set(self.args)
        compare_data = set(other.args)
        if self.filter_method == FilterMethod.FILTER_ALL_EXACT:
            return current_data == compare_data
        if self.filter_method == FilterMethod.FILTER_ALL_FUZZY:
            return check_all_substring_match(current_data, compare_data)
        if self.filter_method == FilterMethod.FILTER_ANY_EXACT:
            return current_data.issubset(compare_data)
        if self.filter_method == FilterMethod.FILTER_ANY_FUZZY:
            return check_any_substring_match(current_data, compare_data)
        return False


def check_all_substring_match(a_list, b_list):
    for a in a_list:
        found_match = False
        for b in b_list:
            if a in b:
                found_match = True
                break
        if not found_match:
            return False
    return True


def check_any_substring_match(a_list, b_list):
    for a in a_list:
        for b in b_list:
            if a in b:
                return True
    return False
