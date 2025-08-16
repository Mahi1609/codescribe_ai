import unittest
import tempfile
import os
import json
from codescribe_ai.core.dependency_parser import extract_all_dependencies

class TestDependencyParser(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        # Create requirements.txt
        with open(os.path.join(self.test_dir, "requirements.txt"), "w") as f:
            f.write("flask\nrequests>=2.0\n")

        # Create package.json
        package_data = {
            "dependencies": {
                "react": "^18.0.0"
            },
            "devDependencies": {
                "jest": "^29.0.0"
            }
        }
        with open(os.path.join(self.test_dir, "package.json"), "w") as f:
            json.dump(package_data, f)

    def test_extract_all_dependencies(self):
        deps = extract_all_dependencies(self.test_dir)

        self.assertIn("flask", deps["python"])
        self.assertIn("requests>=2.0", deps["python"])
        self.assertIn("react", deps["node"])
        self.assertIn("jest", deps["node"])

if __name__ == "__main__":
    unittest.main()
