import unittest
import os
from filemanager import search_files

class TestSearchFiles(unittest.TestCase):
    def test_search_files(self):
        print("#---------------------------------------------")
        print("search_files")
        filepaths = search_files(include_directory = os.path.dirname(os.getcwd()),
                                 include_extension = [".py", ".txt"],
                                 exclude_start = "test")
        self.assertIsInstance(filepaths, list)
        print(f"{len(filepaths)} files found :\n\t->{"\n\t->".join(filepaths)}")


if __name__ == '__main__':
    unittest.main()