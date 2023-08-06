import struct
from typing import Any, Literal, cast

from beni import bfunc


def decode(value: bytes):
    import chardet
    data = chardet.detect(value)
    encoding = data['encoding'] or 'utf8'
    return value.decode(encoding)


EndianType = Literal[
    # https://docs.python.org/zh-cn/3/library/struct.html#byte-order-size-and-alignment
    '@',  # 按原字节
    '=',  # 按原字节
    '<',  # 小端
    '>',  # 大端
    '!',  # 网络（=大端）
]


class BytesWriter():

    def __init__(self, endian: EndianType):
        self.endian = endian
        self.formatAry: list[str] = []
        self.valueAry: list[Any] = []

    def toBytes(self):
        return struct.pack(
            f'{self.endian}{"".join(self.formatAry)}',
            *self.valueAry
        )

    def _write(self, format: str, value: int | float | bool | str | bytes):
        self.formatAry.append(format)
        self.valueAry.append(value)

    def _writeAry(self, func: Any, ary: list[Any]):
        self.writeUint(len(ary))
        for value in ary:
            func(value)
        return self

    # ---------------------------------------------------------------------------

    def writeShort(self, value: int):
        'int16'
        self._write('h', bfunc.getValueInside(value, -32768, 32767))
        return self

    def writeUshort(self, value: int):
        'int16'
        self._write('H', bfunc.getValueInside(value, 0, 65535))
        return self

    def writeInt(self, value: int):
        'int32'
        self._write('i', bfunc.getValueInside(value, -2147483648, 2147483647))
        return self

    def writeUint(self, value: int):
        'int32'
        self._write('I', bfunc.getValueInside(value, 0, 4294967295))
        return self

    def writeLong(self, value: int):
        'int64'
        self._write('q', bfunc.getValueInside(value, -9223372036854775808, 9223372036854775807))
        return self

    def writeUlong(self, value: int):
        'int64'
        self._write('Q', bfunc.getValueInside(value, 0, 18446744073709551615))
        return self

    def writeFloat(self, value: float):
        self._write('f', value)
        return self

    def writeDouble(self, value: float):
        self._write('d', value)
        return self

    def writeBool(self, value: bool):
        self._write('?', value)
        return self

    def writeStr(self, value: str):
        valueBytes = value.encode('utf8')
        count = len(valueBytes)
        self.writeUshort(count)
        self._write(f'{count}s', valueBytes)
        return self

    # ---------------------------------------------------------------------------

    def writeAryShort(self, ary: list[int]):
        'int16[]'
        return self._writeAry(self.writeShort, ary)

    def writeAryUshort(self, ary: list[int]):
        'int16[]'
        return self._writeAry(self.writeUshort, ary)

    def writeAryInt(self, ary: list[int]):
        'int32[]'
        return self._writeAry(self.writeInt, ary)

    def writeAryUint(self, ary: list[int]):
        'int32[]'
        return self._writeAry(self.writeUint, ary)

    def writeAryLong(self, ary: list[int]):
        'int64[]'
        return self._writeAry(self.writeLong, ary)

    def writeAryUlong(self, ary: list[int]):
        'int64[]'
        return self._writeAry(self.writeUlong, ary)

    def writeAryFloat(self, ary: list[float]):
        return self._writeAry(self.writeFloat, ary)

    def writeAryDouble(self, ary: list[float]):
        return self._writeAry(self.writeDouble, ary)

    def writeAryBool(self, ary: list[bool]):
        return self._writeAry(self.writeBool, ary)

    def writeAryStr(self, ary: list[str]):
        return self._writeAry(self.writeStr, ary)


class BytesReader():

    offset: int
    data: bytes

    def __init__(self, endian: EndianType, data: bytes):
        self.endian = endian
        self.offset = 0
        self.data = data

    def _read(self, fmt: str):
        result = struct.unpack_from(fmt, self.data, self.offset)[0]
        self.offset += struct.calcsize(fmt)
        return result

    def _readAry(self, func: Any):
        ary: list[Any] = []
        count = self.readUint()
        for _ in range(count):
            ary.append(func())
        return ary

    # ---------------------------------------------------------------------------

    def readShort(self):
        'int16'
        return cast(int, self._read('h'))

    def readUshort(self):
        'int16'
        return cast(int, self._read('H'))

    def readInt(self):
        'int32'
        return cast(int, self._read('i'))

    def readUint(self):
        'int32'
        return cast(int, self._read('I'))

    def readLong(self):
        'int64'
        return cast(int, self._read('q'))

    def readUlong(self):
        'int64'
        return cast(int, self._read('Q'))

    def readFloat(self):
        return cast(float, self._read('f'))

    def readDouble(self):
        return cast(float, self._read('d'))

    def readBool(self):
        return cast(bool, self._read('?'))

    def readStr(self):
        count = self.readUshort()
        return cast(str, self._read(f'{count}s').decode())

    # ---------------------------------------------------------------------------

    def readAryShort(self):
        'int16[]'
        return cast(list[int], self._readAry(self.readShort))

    def readAryUshort(self):
        'int16[]'
        return cast(list[int], self._readAry(self.readUshort))

    def readAryInt(self):
        'int32[]'
        return cast(list[int], self._readAry(self.readInt))

    def readAryUint(self):
        'int32[]'
        return cast(list[int], self._readAry(self.readUint))

    def readAryLong(self):
        'int64[]'
        return cast(list[int], self._readAry(self.readLong))

    def readAryUlong(self):
        'int64[]'
        return cast(list[int], self._readAry(self.readUlong))

    def readAryFloat(self):
        return cast(list[float], self._readAry(self.readFloat))

    def readAryDouble(self):
        return cast(list[float], self._readAry(self.readDouble))

    def readAryBool(self):
        return cast(list[bool], self._readAry(self.readBool))

    def readAryStr(self):
        return cast(list[str], self._readAry(self.readStr))
