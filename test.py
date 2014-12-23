import unittest
from process_contacts import (
    get_first_value, combine_dictionary_values, combine_set_values)
from upload_contacts import get_keys


class TestFunctions(unittest.TestCase):
    def test_get_first_value(self):
        self.assertEqual(get_first_value([], 'foo'), None)
        self.assertEqual(
            get_first_value([{'foo': 'bar'}, {'bar': 'foo'}], 'foo'), 'bar')
        self.assertEqual(
            get_first_value([{'bar': 'foo'}, {'foo': 'bar'}], 'foo'), 'bar')
        self.assertEqual(
            get_first_value([{'bar': 'foo'}, {'notfoo': 'bar'}], 'foo'), None)

    def test_combine_dictionary_values(self):
        self.assertEqual(combine_dictionary_values([], 'foo'), {})
        self.assertEqual(
            combine_dictionary_values(
                [{'foo': {'bar': 'baz'}}, {'bar': 'foo'}], 'foo'),
            {'bar': 'baz'})
        self.assertEqual(
            combine_dictionary_values(
                [{'foo': {'bar': 'baz'}}, {'foo': {'baz': 'bar'}}], 'foo'),
            {'bar': 'baz', 'baz': 'bar'})
        self.assertEqual(
            combine_dictionary_values(
                [{'foo': {'bar': 'baz'}}, {'foo': {'bar': 'qux'}}], 'foo'),
            {'bar': 'qux'})

    def test_combine_set_values(self):
        self.assertEqual(combine_set_values([], 'foo'), [])
        self.assertEqual(
            combine_set_values([{'foo': ['bar']}, {'bar': ['foo']}], 'foo'),
            ['bar'])
        self.assertEqual(
            combine_set_values([{'foo': ['bar', 'baz']}, {'foo': ['baz']}],
                               'foo'),
            ['bar', 'baz'])

    def test_get_keys(self):
        self.assertEqual(get_keys([]), [])
        self.assertEqual(get_keys([{'key': '1'}, {'key': '2'}]), ['1', '2'])
        self.assertEqual(
            get_keys([{'key': '1'}, {'key': '2', 'foo': '3'}]), ['1', '2'])

if __name__ == '__main__':
    unittest.main()
