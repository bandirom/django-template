from django.test import TestCase

from main import utils


class UtilsTestCase(TestCase):
    def test_find_by_key(self):
        data = {
            'tes': 't',
            'dev': 'elop',
            'dict': {
                'AWS': {'founder': 'Jeffrey Preston', 'date': 2006},
                'Tesla': {'founder': 'Elon Musk', 'date': 2003},
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
        str1 = 'We are the champions'
        self.assertEqual(utils.parse_str_with_space(str1), str1)
        str2 = ' You are looking great   '
        self.assertEqual(utils.parse_str_with_space(str2), 'You are looking great')
        str3 = ' This    double  life you    lead is   eating you   up from  within    '
        self.assertEqual(
            utils.parse_str_with_space(str3), 'This double life you lead is eating you up from within'
        )

    def test_find_dict_in_list(self):
        list_1 = [
            {
                'key1': 'Test1',
                'key2': 'test2',
            },
            {
                'key1': 'Value2',
                'key2': 'Valey3',
            },
            {
                'key1': 1,
                'key2': False,
            },
            {
                'key1': 100500,
                'key2': ['test1'],
            },
        ]
        result = utils.find_dict_in_list(target=list_1, dict_key='key1', lookup_value='Test1')
        self.assertEqual(result, list_1[0])
        result = utils.find_dict_in_list(target=list_1, dict_key='key2', lookup_value='test2')
        self.assertEqual(result, list_1[0])
        result = utils.find_dict_in_list(target=list_1, dict_key='key1', lookup_value=100500)
        self.assertEqual(result, list_1[3])
        result = utils.find_dict_in_list(target=list_1, dict_key='key2', lookup_value=['test1'])
        self.assertEqual(result, list_1[3])
        result = utils.find_dict_in_list(target=list_1, dict_key='key2', lookup_value=False)
        self.assertEqual(result, list_1[2])
