import unittest

import analysis_data


class AllTestCase(unittest.TestCase):

    def test_check_date(self):
        self.assertFalse(analysis_data.check_date_string(''))
        self.assertTrue(analysis_data.check_date_string('2020-01-23'))
        self.assertTrue(analysis_data.check_date_string('3033-01-23'))
        self.assertFalse(analysis_data.check_date_string('2020-01-63'))
        self.assertFalse(analysis_data.check_date_string('xxxxx'))
        # self.assertFalse(analysis_data._check_date(None))

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
        self.assertEqual(analysis_data._deal_with_common_param(''), [])
        self.assertEqual(analysis_data._deal_with_common_param('%%%%%, ___,__'), [])
        self.assertEqual(analysis_data._deal_with_common_param('%%%%%, _____'), [])
        self.assertEqual(analysis_data._deal_with_common_param(','), [])
        self.assertEqual(analysis_data._deal_with_common_param(',,'), [])
        self.assertEqual(analysis_data._deal_with_common_param('PCBST,,'), [('PCBST', False)])
        self.assertEqual(analysis_data._deal_with_common_param(' PCBST  ,'), [('PCBST', False)])
        self.assertEqual(analysis_data._deal_with_common_param(' PCB%%  ,'), [('PCB%', True)])
        self.assertEqual(analysis_data._deal_with_common_param(' PCB%  ,ASSY'), [('PCB%', True), ('ASSY', False)])
        self.assertEqual(analysis_data._deal_with_common_param(' PCB%  ,ASSY,%%%%%%,'), [('PCB%', True), ('ASSY', False)])

        # self.assertEqual(analysis_data._deal_with_common_param(None), [])


if __name__ == '__main__':
    unittest.main()
