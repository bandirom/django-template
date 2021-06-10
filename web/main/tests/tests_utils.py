from django.test import TestCase

from main import utils


class UtilsTestCase(TestCase):

    def test_find_by_key(self):
        data = {
            'tes': 't',
            'dev': 'elop',
            'dict': {
                'AWS': {'founder': 'Jeffrey Preston', 'date': 2006},
                'Tesla': {'founder': 'Elon Musk', 'date': 2003}
            },
        }
        self.assertEqual(utils.find_by_key(data, 'tes'), 't')
        self.assertEqual(utils.find_by_key(data, 'AWS'), data['dict']['AWS'])
        self.assertEqual(utils.find_by_key(data, 'founder'), data['dict']['AWS']['founder'])
        data = {
            'list_dict': [
                {'clouds': ['AWS', 'GCP', 'Azure', 'Digital Ocean']},
                {'brands': ['Samsung', 'Tesla', 'Renault']},
            ],
        }
        self.assertEqual(utils.find_by_key(data, 'clouds'), data['list_dict'][0]['clouds'])

    def test_parse_str_with_space(self):
        str1 = "We are the champions"
        self.assertEqual(utils.parse_str_with_space(str1), str1)
        str2 = " You are looking great   "
        self.assertEqual(utils.parse_str_with_space(str2), 'You are looking great')
        str3 = " This    double  life you    lead is   eating you   up from  within    "
        self.assertEqual(utils.parse_str_with_space(str3), 'This double life you lead is eating you up from within')
