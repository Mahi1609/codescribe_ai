import unittest
from codescribe_ai.core import parser
import tempfile
import os

class TestParser(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with nested code files for testing
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        with open(os.path.join(self.test_dir, "main.py"), "w") as f:
            f.write("def foo(): pass")
        with open(os.path.join(self.test_dir, "subdir", "utils.py"), "w") as f:
            f.write("class Bar: pass")

    def test_parse_structure(self):
        # Tests whether parse_repo_structure correctly finds and lists .py files
        result = parser.parse_repo_structure(self.test_dir)  # Calls function from core/parser.py
        self.assertIn("main.py", result)
        self.assertIn("subdir/utils.py", result)

    def tearDown(self):
        # Clean up the temporary test directory
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
