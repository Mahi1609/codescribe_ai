import unittest
import tempfile
import os
import json
from codescribe_ai.core.usage_instruction_builder import generate_usage_instruction

class TestUsageInstructionBuilder(unittest.TestCase):

    def setUp(self):
        self.python_dir = tempfile.mkdtemp()
        with open(os.path.join(self.python_dir, "app.py"), "w") as f:
            f.write("print('Hello from Flask')")

        self.node_dir = tempfile.mkdtemp()
        with open(os.path.join(self.node_dir, "package.json"), "w") as f:
            json.dump({
                "scripts": {
                    "start": "node server.js"
                },
                "dependencies": {
                    "express": "^4.0.0"
                }
            }, f)

        with open(os.path.join(self.node_dir, "server.js"), "w") as f:
            f.write("console.log('Running Node');")

    def test_detect_python_app_py(self):
        usage = generate_usage_instruction(self.python_dir, environment="flask")
        self.assertEqual(usage, "python app.py")

    def test_detect_node_start_script(self):
        usage = generate_usage_instruction(self.node_dir, environment="node")
        self.assertEqual(usage, "npm start")

    def test_fallback_behavior(self):
        empty_dir = tempfile.mkdtemp()
        usage = generate_usage_instruction(empty_dir)
        self.assertEqual(usage, "Check documentation or main file.")

if __name__ == "__main__":
    unittest.main()
