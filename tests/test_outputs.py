from cartesi_nexus.outputs import Voucher, Base, output
from unittest import TestCase, main
from cartesi_nexus.helpers import hex2str, str2hex

import unittest
from cartesi_nexus.helpers import str2hex
import json


class TestVoucher(unittest.TestCase):
    def test_voucher_initialization(self):
        v1 = Voucher(data={'destination': '0x1234', 'payload': 'data'})
        self.assertEqual(v1.destination, '0x1234')
        self.assertEqual(v1.payload, 'data')
        self.assertIsNone(v1.destination_to)

        v2 = Voucher(data={'destination': '0x1234', 'destination_to': '0x5678', 'payload': 'data'})
        self.assertEqual(v2.destination, '0x1234')
        self.assertEqual(v2.destination_to, '0x5678')
        self.assertEqual(v2.payload, 'data')

    def test_voucher_setters(self):
        v = Voucher(data={'destination': '0x1234', 'payload': 'data'})
        v.destination = '0x5678'
        v.destination_to = '0x9ABC'
        v.payload = 'new_data'
        self.assertEqual(v.destination, '0x5678')
        self.assertEqual(v.destination_to, '0x9ABC')
        self.assertEqual(v.payload, 'new_data')


class TestBase(unittest.TestCase):
    def test_base_initialization(self):
        b1 = Base(payload='test_data')
        self.assertEqual(b1.python_payload, 'test_data')
        self.assertEqual(b1.payload, str2hex(json.dumps('test_data')))

        b2 = Base('direct_data')
        self.assertEqual(b2.python_payload, 'direct_data')
        self.assertEqual(b2.payload, str2hex(json.dumps('direct_data')))

    def test_base_payload_setter(self):
        b = Base('data')
        b.payload = 'new_payload'
        self.assertEqual(b.payload, 'new_payload')

    def test_base_invalid_init(self):
        with self.assertRaises(ValueError):
            Base()


class TestOutput(unittest.TestCase):
    def test_output_voucher(self):
        v = output('voucher', data={'destination': '0x1234', 'payload': 'data'})
        self.assertIsInstance(v, Voucher)
        self.assertEqual(v.destination, '0x1234')
        self.assertEqual(v.payload, 'data')

    def test_output_notice(self):
        n = output('notice', payload='notice_data')
        self.assertIsInstance(n, Base)
        self.assertEqual(n.python_payload, 'notice_data')

    def test_output_log(self):
        l = output('log', 'log_data')
        self.assertIsInstance(l, Base)
        self.assertEqual(l.python_payload, 'log_data')

    def test_output_error(self):
        e = output('error', payload='error_data')
        self.assertIsInstance(e, Base)
        self.assertEqual(e.python_payload, 'error_data')

    def test_output_invalid_type(self):
        with self.assertRaises(ValueError):
            output('invalid_type', payload='data')


if __name__ == '__main__':
    main()
