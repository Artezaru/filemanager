import unittest
import os
from filemanager import extract_file_components

class TestExtractFileComponents(unittest.TestCase):
    def test_extract_file_components(self):
        print("#---------------------------------------------")
        print("extract_file_components")
        filepath = os.path.join(os.getcwd(), "test_extract_file_components.py")
        path, name, ext = extract_file_components(filepath)
        self.assertIsInstance(path, str)
        self.assertIsInstance(name, str)
        self.assertIsInstance(ext, str)
        print(f"{filepath} components are : \n\t-> {path=}\n\t-> {name=}\n\t-> {ext=}")


if __name__ == '__main__':
    unittest.main()