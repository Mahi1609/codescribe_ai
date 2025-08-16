import unittest
import tempfile
import os
from core.env_var_parser import extract_env_variables

class TestEnvVarParser(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        # .env file
        with open(os.path.join(self.test_dir, ".env"), "w") as f:
            f.write("DEBUG=True\nSECRET_KEY='abc123'\n")

        # settings.py
        settings_path = os.path.join(self.test_dir, "settings.py")
        with open(settings_path, "w") as f:
            f.write("ALLOWED_HOSTS = '*'\nPORT = 8000\n")

    def test_extract_env_variables(self):
        result = extract_env_variables(self.test_dir)

        self.assertEqual(result["DEBUG"], "True")
        self.assertEqual(result["SECRET_KEY"], "abc123")
        self.assertEqual(result["ALLOWED_HOSTS"], "*")
        self.assertEqual(result["PORT"], "8000")

if __name__ == "__main__":
    unittest.main()
