import unittest
import json
from app.test.context import relative_resource
from app.src import aggregation


class TestObject(object):
    id = ''
    content = ''

    def __init__(self, id, content):
        self.id = id
        self.content = content


class AggregationTest(unittest.TestCase):
    def test_group_by_field(self):
        albums = json.load(open(relative_resource('albums.json')))
        result = aggregation.group_by_field(albums, 'userId')
        self.assertEqual(10, len(result))
        for i in range(1, 11):
            self.assertIn(str(i), result)

    def test_group_by_attribute(self):
        objs = [TestObject(1, "abc"), TestObject(2, "abc"), TestObject(3, "cba")]
        result = aggregation.group_by_attribute(objs, 'content')
        self.assertEqual(2, len(result))
        self.assertEqual(2, len(result["abc"]))
        self.assertEqual(1, len(result["cba"]))

if __name__ == '__main__':
    unittest.main()
