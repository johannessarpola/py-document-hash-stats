import unittest
from app.test.context import path_to_resources
from app.src import input_output

class ModelTest(unittest.TestCase):
    def test_get_jsons_from_folder(self):
        files = input_output.get_jsons_from_folder(path_to_resources())
        names = input_output.get_filepaths_in_folder(path_to_resources())
        self.assertEqual(len(files), len(names))
        self.assertGreaterEqual(len(names), 1)
        self.assertGreaterEqual(len(files), 1)

if __name__ == '__main__':
    unittest.main()