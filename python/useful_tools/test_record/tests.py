import unittest

import search_data


def match_test_result(val):
    return search_data.TEST_RESULT_PATTERN.match(val) is not None


class AllTestCase(unittest.TestCase):

    def test_result_match(self):
        self.assertTrue(match_test_result('P'))
        self.assertTrue(match_test_result('P,F'))
        self.assertFalse(match_test_result('P,F,'))
        self.assertTrue(match_test_result('P,F,S'))
        self.assertTrue(match_test_result('P,F,S,G'))

    def test_check_date(self):
        self.assertFalse(search_data.check_date_string(''))
        self.assertTrue(search_data.check_date_string('2020-01-23'))
        self.assertTrue(search_data.check_date_string('3033-01-23'))
        self.assertFalse(search_data.check_date_string('2020-01-63'))
        self.assertFalse(search_data.check_date_string('xxxxx'))
        # self.assertFalse(search_data._check_date(None))

    def test_common_param(self):
        """
            print(_deal_with_common_param('PCBST'))
            print(_deal_with_common_param(','))
            print(_deal_with_common_param(''))
            print(_deal_with_common_param([]))
            print(_deal_with_common_param(['', ',']))
            print(_deal_with_common_param(['', '', '']))
            print(_deal_with_common_param('PCBST, PCB2C'))
            print(_deal_with_common_param('PCB%'))
            print(_deal_with_common_param('PCB%, ASSY'))
            print(_deal_with_common_param(['PCBST', 'PCBFT']))
            print(_deal_with_common_param(['PCBST', 'PCBFT, PCB%']))
            print(_deal_with_common_param(['PCBST', 'PCBFT, PCBFT']))
            print(_deal_with_common_param(['PCBST', 'PCBFT, PCBFT']))
            # print(_deal_with_common_param([['PCBST', 'PCBFT, PCBFT'], []]))
        """
        self.assertEqual(search_data._deal_with_common_param(''), [])
        self.assertEqual(search_data._deal_with_common_param('%%%%%, ___,__'), [])
        self.assertEqual(search_data._deal_with_common_param('%%%%%, _____'), [])
        self.assertEqual(search_data._deal_with_common_param(','), [])
        self.assertEqual(search_data._deal_with_common_param(',,'), [])
        self.assertEqual(search_data._deal_with_common_param('PCBST,,'), [('PCBST', False)])
        self.assertEqual(search_data._deal_with_common_param(' PCBST  ,'), [('PCBST', False)])
        self.assertEqual(search_data._deal_with_common_param(' PCB%  ,'), [('PCB%', True)])
        self.assertEqual(search_data._deal_with_common_param(' PCB%  ,ASSY'), [('PCB%', True), ('ASSY', False)])
        self.assertEqual(search_data._deal_with_common_param(' PCB%  ,ASSY,%%%%%%,'), [('PCB%', True), ('ASSY', False)])

        # self.assertEqual(search_data._deal_with_common_param(None), [])


if __name__ == '__main__':
    unittest.main()
