import unittest
from src.DLMS_SPODES.hdlc.snrm import SNRM


class TestType(unittest.TestCase):

    def test_SNRM(self):
        value = SNRM()
        self.assertEqual(SNRM().content, b'', "empty info")
        self.assertEqual(SNRM(max_info_receive=200).content, b'\x81\x80\x03\x06\x01\xc8', "receive")
        self.assertEqual(SNRM(200, 259).content, b'\x81\x80\x07\x05\x01\xc8\x06\x02\x01\x03', "recv200_tr259")
