from enum import Enum
from functools import partial
from json import JSONEncoder, dumps as json_dumps


class EnumJSONEncoder(JSONEncoder):
    def encode(self, o):
        if isinstance(o, Enum):
            return o.value
        return super().encode(o)


dumps = partial(json_dumps, cls=EnumJSONEncoder)