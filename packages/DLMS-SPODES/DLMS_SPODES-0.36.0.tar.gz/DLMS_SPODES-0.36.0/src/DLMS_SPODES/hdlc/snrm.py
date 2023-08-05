from dataclasses import dataclass
from functools import cached_property
from ..hdlc.frame import Info
from struct import pack_into

MAX_INFO_DEFAULT = 128
WINDOW_DEFAULT = 1


@dataclass
class SNRM(Info):
    max_info_transmit: int = MAX_INFO_DEFAULT
    max_info_receive: int = MAX_INFO_DEFAULT
    window_transmit: int = WINDOW_DEFAULT
    window_receive: int = WINDOW_DEFAULT

    @cached_property
    def content(self) -> bytes:
        value = bytearray(17)  # max length of SNRM
        pack_into("BB", value, 0, 0x81, 0x80)
        offset: int = 3
        if self.max_info_transmit != MAX_INFO_DEFAULT:
            pack_into("B", value, offset, 5)  # tag max_value_transmit
            offset += 1
            if self.max_info_transmit <= 255:
                pack_into("BB", value, offset, 1, self.max_info_transmit)
                offset += 2
            else:
                pack_into(">BH", value, offset, 2, self.max_info_transmit)
                offset += 3
        if self.max_info_receive != MAX_INFO_DEFAULT:
            pack_into("B", value, offset, 6)  # tag max_value_receive
            offset += 1
            if self.max_info_receive <= 255:
                pack_into("BB", value, offset, 1, self.max_info_receive)
                offset += 2
            else:
                pack_into(">BH", value, offset, 2, self.max_info_receive)
                offset += 3
        if self.window_transmit != WINDOW_DEFAULT:
            pack_into("BBB", value, offset, 7, 1, self.window_transmit)
            offset += 3
        if self.window_receive != WINDOW_DEFAULT:
            pack_into("BBB", value, offset, 8, 1, self.window_receive)
            offset += 3
        if offset == 3:  # not info
            return bytes()
        else:
            pack_into("B", value, 2, offset-3)  # set length
            return bytes(value[:offset])

    def info(self) -> bytes:
        return self.content

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return F"max tr/rec: {self.max_info_transmit}/{self.max_info_receive}, wind tr/rec: {self.window_transmit}/{self.window_receive}"
