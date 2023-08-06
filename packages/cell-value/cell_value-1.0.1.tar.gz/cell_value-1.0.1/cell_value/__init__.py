import json

import jsonschema


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
            "trace_id": {"type": "string"}
        },
        "required": ["data_list"]
    }

    def __init__(self, *args):
        """

        :param trace_id:  可携带上下文id，在不同应用流通
        :param args:
        """
        self.args = args
        self.trace_id = None

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
        obj = cls(*json_string['data_list'])
        obj.tag_trace(json_string.get('trace_id'))
        return obj

    def dumps(self, as_json=False) -> dict or json:
        d = {
            'data_list': [],
            'trace_id': None
        }

        d['data_list'] = self.args
        d['trace_id'] = self.trace_id
        jsonschema.validate(d, self.SCHEMA)

        if as_json:
            return json.dumps(d)
        return d
