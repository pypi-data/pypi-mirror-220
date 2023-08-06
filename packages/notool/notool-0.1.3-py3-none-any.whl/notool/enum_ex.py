import types
import typing as t
from collections import ChainMap
from enum import EnumMeta, Enum, IntEnum, Flag, IntFlag


_T = t.TypeVar('_T')
_acceptable_enum_classes = (Enum, IntEnum, Flag, IntFlag)


def _get_enum_base(cls):
    if cls in _acceptable_enum_classes:
        return cls

    for base in cls.__bases__:
        if base not in _acceptable_enum_classes:
            return _get_enum_base(base)
        else:
            return base


# TODO implement specifying str2member_map or repr2member_map, when str and loaded values is not the same
def enum_str(cls: _T = None, *,
             member2str_map: t.Optional[dict] = None,
             make_inverse_map=False,
             default_value=None) -> _T:

    def _enum_str(_cls):
        def __str__(self):
            return getattr(self.__class__, '_member2str_map_', lambda: {}).get(self) or\
                   super_str(self)

        def __new__(_cls, value, *args, **kw):
            if isinstance(value, str):
                if (member := getattr(_cls, '_str2member_map_', lambda: {}).get(value)) is not None:
                    return member
            try:
                if not isinstance(value, member_type):
                    value = member_type(value)
                return super_call(_cls, value, *args, **kw)
            except ValueError:
                if default_value is not None:
                    return super_call(_cls, default_value, *args, **kw)
                else:
                    raise

        member2str = member2str_map or getattr(_cls, '_member2str_map', lambda: None)()
        member_type = _cls._member_type_ if not object else int
        if member2str:
            super_str = getattr(_cls, '__str__')
            setattr(_cls, '__str__', __str__)
            setattr(_cls, '_member2str_map_', member2str)
            if make_inverse_map:
                super_call = getattr(_cls, '__new__')
                setattr(_cls, '__new__', __new__)
                str2member = {val: key for key, val in member2str.items()}
                if len(str2member) != len(member2str):
                    raise ValueError('Values in str_map must be unique')
                setattr(_cls, '_str2member_map_', str2member)
        return _cls

    return _enum_str if cls is None else _enum_str(cls)


class EnumChain(EnumMeta):
    @classmethod
    def __prepare__(mcs, cls_name, bases, **kw):
        enum_type = None
        for cls in bases:
            if (cls_enum_type := _get_enum_base(cls)) is None:
                raise TypeError('Can\'t inherit from not enum classes')
            if enum_type and enum_type is not cls_enum_type:
                raise TypeError('Can\'t inherit from different enum classes')
            enum_type = cls_enum_type
        return EnumMeta.__prepare__(cls_name, (enum_type, ), **kw)

    def __new__(mcs, cls_name, bases: tuple, cls_dict):
        if getattr(cls_dict, '_member_names'):
            raise ValueError

        ensure_unique = cls_dict.get('__ensure_unique__', True)
        new_cls = EnumMeta.__new__(mcs, cls_name, (_get_enum_base(bases[0]),), cls_dict)

        _enum_chain_ = list()
        names, values, strs = set(), set(), set()
        for cls in bases:
            if cls in _acceptable_enum_classes:
                continue
            _enum_chain_.append(cls)
            _names = set(getattr(cls, '_member_map_'))
            _strs = set(getattr(cls, '_str2member_map_', {}))

            if strs_intersection := strs.intersection(_strs):
                raise ValueError(f'Values in str_map of parent classes repeated {strs_intersection}')

            if names_intersection := names.intersection(_names):
                raise ValueError(f'Members names of parent classes repeated {names_intersection}')

            strs.update(_strs)
            names.update(_names)
            values.update(set(getattr(cls, '_value2member_map_')))

            if ensure_unique and len(names) != len(values):
                raise ValueError('Members values must be unique, setting attribute '
                                 '__ensure_unique__ to False will disable this Error')

        setattr(new_cls, '_enum_chain_', _enum_chain_)
        setattr(new_cls, '_T', t.Union[(new_cls, *_enum_chain_)])
        return new_cls

    def __call__(cls, value, names=None, *, module=None, qualname=None, type_=None, start=1):
        if names:
            return cls._create_(value, names, module=module, qualname=qualname, type=type_, start=start)
        else:
            for enum_cls in cls._enum_chain_:
                try:
                    return enum_cls.__new__(enum_cls, value)
                except (ValueError, TypeError):
                    pass
            raise ValueError(f'{value} is not a valid {cls.__class__.__qualname__} <{cls.__qualname__}>')

    def __dir__(self):
        return NotImplementedError()

    def __getattr__(cls, name):
        for enum_cls in cls._enum_chain_:
            if result := enum_cls._member_map_.get(name):
                return result
        raise AttributeError(name)

    def __setattr__(cls, name, value):
        if _enum_chain_ := cls.__dict__.get('_enum_chain_'):
            for enum_cls in _enum_chain_:
                if enum_cls.__dict__['_member_map_'].get(name):
                    raise AttributeError('Cannot reassign members.')
        super().__setattr__(name, value)

    def __delattr__(cls, attr):
        raise AttributeError(f'Deleting attribute in {cls.__class__.__qualname__} not allowed')

    def __getitem__(cls, name):
        for enum_cls in cls._enum_chain_:
            if result := enum_cls._member_map_.get(name):
                return result
        raise KeyError(name)

    @property
    def __members__(cls):
        return ChainMap(
            *(types.MappingProxyType(enum_cls._member_map_)
              for enum_cls in cls._enum_chain_))

    def __contains__(cls, member):
        for enum_cls in cls._enum_chain_:
            if isinstance(member, enum_cls):
                return EnumMeta.__contains__(enum_cls, member)
        return False

    def __iter__(cls):
        for enum_cls in cls._enum_chain_:
            yield from enum_cls.__iter__()

    def __reversed__(cls):
        for enum_cls in reversed(cls._enum_chain_):
            yield from enum_cls.__reversed__()

    def __len__(cls):
        len_ = 0
        for enum_cls in cls._enum_chain_:
            len_ += len(enum_cls._member_names_)
        return len_

    def __repr__(cls):
        return f'{cls.__class__.__qualname__}(' \
               f'{", ".join(repr(enum_cls) for enum_cls in cls._enum_chain_)})'


if __name__ == '__main__':

    def _tests():
        from enum import auto
        import orjson

        value = 3
        str_value = '_DATA2A_'

        class Data1(Enum):
            data1a = value
            data1b = auto()

        @enum_str(make_inverse_map=True)
        class Data2(Enum):
            data2a = 16
            data2b = auto()
            data2c = auto()

            @classmethod
            def _member2str_map(cls):
                return {cls.data2a: str_value, cls.data2b: '_DATA2B_'}

        class Data3(Enum):
            data3a = 23
            data3b = 24
            data3c = 255

        enum_str(Data3, member2str_map={Data3.data3a: '_DATA3A_', }, make_inverse_map=True)

        class Data(Data1, Data2, Data3, metaclass=EnumChain):
            ...
        Data._T = t.Union[Data, Data1, Data2, Data3]

        results = (
            Data1.data1a is Data.data1a,
            Data.data1a is not Data1.data1a.value,
            Data.data1a.value is value,
            Data1.data1a is Data(value),
            Data1.data1a.name in Data.__members__,
            Data3.data3a in Data,
            Data(str_value) == Data2.data2a,
            Data.data1a != value,
            ' '.join(map(str, Data)) == 'Data1.data1a Data1.data1b '
                                        '_DATA2A_ _DATA2B_ Data2.data2c '
                                        '_DATA3A_ Data3.data3b Data3.data3c',
            orjson.dumps(list(Data)) == b'[3,4,16,17,18,23,24,255]'
        )

        print(*results)
        print(*Data)
        print(orjson.dumps(list(Data)))
        assert all(results)

    _tests()
