from enum import IntEnum
from enum import Enum

from typing import Type


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class IntEnumSet:
    _enum_type: Type[IntEnum]
    _bit_value: int

    def __init__(self, enum_type, bit_value):
        self._enum_type = enum_type
        self._bit_value = bit_value

    @property
    def enum_type(self):
        return self._enum_type

    @property
    def bit_value(self):
        return self._bit_value

    def values(self):
        return [v for v in self.enum_type if self.bit_value & (1 << v.value)]

    def to_binary(self):
        enums = len(self._enum_type)
        return ('{:0%db}' % enums).format(self._bit_value)

    def __and__(self, other):
        return IntEnumSet(self.enum_type, self.bit_value & other.bit_value)

    def __eq__(self, other):
        return self.enum_type is other.enum_type and self.bit_value == other.bit_value

    def __hash__(self):
        return hash((self.enum_type, self.bit_value))

    def __str__(self):
        type_name = type(self).__name__
        enum_type_name = self.enum_type.__name__
        return f'{type_name}[{enum_type_name}] = {self.bit_value}'


def create_int_enum_set(enum_type: Type[IntEnum], *enums: IntEnum):
    value = 0
    for enum in enums:
        assert enum_type == type(enum)
        value += 1 << enum.value
    return IntEnumSet(enum_type, value)


def get_all_values(enum_type):
    return list(map(int, enum_type))
