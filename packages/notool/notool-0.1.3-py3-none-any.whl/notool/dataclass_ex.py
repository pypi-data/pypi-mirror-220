import datetime
import functools
import time
from dataclasses import dataclass
import typing as t
from enum import EnumMeta

import orjson
from dacite import from_dict, core, Config
from dacite.exceptions import DaciteFieldError

_T = t.TypeVar("_T")


def _build_value(type_, data, config):
    origin_type = t.get_origin(type_) or type_
    try:
        if origin_type is dict:
            args = t.get_args(type_)
            if args and (key_type := args[0]):
                if key_type is str:
                    pass
                elif key_type in (int, float):
                    data = {key_type(key): val for key, val in data.items()}
                else:
                    # TODO orjson not supported tuple as dict keys
                    raise NotImplementedError
        elif origin_type is type(data):
            ...
        elif origin_type in (bytes, bytearray, memoryview) and isinstance(data, str):
            data = str.encode(data, 'charmap')
        elif hasattr(origin_type, '_asdict'):  # for namedtuple
            data = origin_type(**data)
        elif origin_type in (int, float) or isinstance(origin_type, EnumMeta) or origin_type is tuple:
            data = origin_type(data if data is not None else '')
        elif origin_type is datetime.datetime:
            data = datetime.datetime.fromisoformat(data)

        return super_build_value(type_, data, config)

    except ValueError:
        raise DaciteFieldError


super_build_value = getattr(core, '_build_value')
setattr(core, '_build_value', _build_value)


def _orjson_default(obj):
    if hasattr(obj, '_asdict'):
        return obj._asdict()
    elif isinstance(obj, (bytes, bytearray, memoryview)):
        return obj.decode('charmap')
    elif isinstance(obj, Exception):
        return str(obj)
    raise TypeError


_encoder = functools.partial(orjson.dumps, default=_orjson_default, option=orjson.OPT_NON_STR_KEYS)
_decoder = orjson.loads
_dacite_default = Config(check_types=False)


# TODO add methods from_dict and asdict or params in loads dumps or autodetect type dict
class Serializable:
    @classmethod
    def loads(cls: t.Type[_T],
              data: t.Union[dict, bytes, bytearray, memoryview, str],
              decoder: t.Callable = None) -> _T:
        dict_ = data if isinstance(data, dict) else (decoder or _decoder)(data)
        return from_dict(cls, dict_, config=_dacite_default)

    def dumps(self, encoder: t.Callable = None, indent=False) -> t.Union[bytes, bytearray, memoryview, str]:
        if encoder:
            return encoder(self)
        else:
            return orjson.dumps(self, default=_orjson_default,
                                option=orjson.OPT_NON_STR_KEYS | int(indent and orjson.OPT_INDENT_2))


if __name__ == '__main__':

    def _tests():
        from notool.enum_ex import EnumChain
        from enum import Enum
        from dataclasses import field

        class Data1(Enum):
            data1a = 1

        class Data2(Enum):
            data2a = 16

        class Data(Data1, Data2, metaclass=EnumChain):
            ...
        Data._T = t.Union[Data, Data1, Data2]

        class EbcParams(t.NamedTuple):
            p1: float
            p2: float
            p3: float

        @dataclass
        class TestForDict:
            d1: EbcParams = EbcParams(1, 1, 1)
            d2: float = 20.20

        @dataclass
        class TestForList:
            f1: Data._T = Data2.data2a
            f2: tuple = (1, 1)
            f3: bool = True
            f4: t.Union[EbcParams, tuple[str, int]] = ('asd', 2)
            f5: dict[int, TestForDict] = field(default_factory=dict)

        @dataclass
        class TestData(Serializable):
            field0: bytes = b'default\n'
            field1: Data._T = Data1.data1a
            field2: float = 2.0
            field3: dict = field(default_factory=lambda: {'test_field': 2})
            field4: list[TestForList] = field(default_factory=list)
            field5: t.Optional[datetime.datetime] = None

        list_ = []
        for i in range(10):
            dict_ = {}
            for j in range(10):
                test_for_dict = TestForDict(EbcParams(i, i, i), j)
                dict_.update({j: test_for_dict})
            a = bool(i % 2)
            tuple_ = EbcParams(i, i, i) if a else (str(i), i)
            list_.append(TestForList(Data1.data1a, (i, i), a, tuple_, dict_))

        for test_data in (TestData(b'default\n', Data2.data2a, 14.2, {'test_field2': 22}),
                          TestData(b'default\n', Data2.data2a, 14.2, {'test_field2': 22},
                                   list_, datetime.datetime.now())):
            test_data_loads = orjson.loads(
                orjson.dumps(test_data, default=_orjson_default, option=orjson.OPT_NON_STR_KEYS))
            assert (test_data
                    == from_dict(TestData, test_data_loads)
                    == TestData.loads(test_data.dumps()))
        else:
            start = time.monotonic()
            for _ in range(1000):
                TestData.loads(test_data_loads)
            print(time.monotonic() - start)

    _tests()
