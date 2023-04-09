from django.test import TestCase, override_settings
from django.test.client import RequestFactory

from main import utils


class UtilsTestCase(TestCase):
    def test_parse_str_with_space(self):
        str1 = 'We are the champions'
        self.assertEqual(utils.parse_str_with_space(str1), str1)
        str2 = ' You are looking great   '
        self.assertEqual(utils.parse_str_with_space(str2), 'You are looking great')
        str3 = ' This    double  life you    lead is   eating you   up from  within    '
        self.assertEqual(utils.parse_str_with_space(str3), 'This double life you lead is eating you up from within')

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

    @override_settings(
        LANGUAGES=(
            ('en', 'English'),
            ('fr', 'French'),
            ('uk', 'Ukrainian'),
        )
    )
    def test_supported_languages(self):
        factory = RequestFactory()
        request = factory.get('/')
        self.assertEqual(utils.get_supported_user_language(request), None)
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'uk'
        self.assertEqual(utils.get_supported_user_language(request), 'uk')
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6'
        self.assertEqual(utils.get_supported_user_language(request), 'en')
