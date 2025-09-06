import unittest
import tempfile
import os
import json
import shutil
from codescribe_ai.core.usage_instruction_builder import generate_usage_instruction


class TestUsageInstructionBuilder(unittest.TestCase):
    def setUp(self):
        # Create a temporary Python project with app.py
        self.python_dir = tempfile.mkdtemp()
        with open(os.path.join(self.python_dir, "app.py"), "w", encoding="utf-8") as f:
            f.write("print('Hello from Flask')")

        # Create a temporary Node.js project with package.json and server.js
        self.node_dir = tempfile.mkdtemp()
        with open(os.path.join(self.node_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({
                "scripts": {
                    "start": "node server.js"
                },
                "dependencies": {
                    "express": "^4.0.0"
                }
            }, f)

        with open(os.path.join(self.node_dir, "server.js"), "w", encoding="utf-8") as f:
            f.write("console.log('Running Node');")

        # Track temporary dirs for cleanup
        self._temp_dirs = [self.python_dir, self.node_dir]

    def tearDown(self):
        for d in getattr(self, "_temp_dirs", []):
            try:
                shutil.rmtree(d)
            except Exception:
                pass

    def test_detect_python_app_py(self):
        """Should detect and return usage for Python Flask app.

        Accept either the short form "python app.py" or longer README-style guidance
        that includes a run command such as "flask run" or "python app.py".
        """
        usage = generate_usage_instruction(self.python_dir, environment="flask")
        usage_stripped = usage.strip()

        # Accept exact short form
        if usage_stripped == "python app.py":
            self.assertEqual(usage_stripped, "python app.py")
            return

        # Otherwise require the longer text to mention at least one plausible run command
        self.assertTrue(
            any(keyword in usage for keyword in ("python app.py", "flask run", "export FLASK_APP", "set FLASK_APP")),
            msg=f"Python usage did not contain an expected run command. Got: {usage!r}"
        )

    def test_detect_node_start_script(self):
        """Should detect npm start script in package.json.

        Accept either the short form "npm start" or longer README-style guidance
        that includes "npm start" or "node server.js".
        """
        usage = generate_usage_instruction(self.node_dir, environment="node")
        usage_stripped = usage.strip()

        # Accept exact short form
        if usage_stripped == "npm start":
            self.assertEqual(usage_stripped, "npm start")
            return

        # Otherwise require the longer text to mention at least one plausible run command
        self.assertTrue(
            any(keyword in usage for keyword in ("npm start", "node server.js", "npm install")),
            msg=f"Node usage did not contain an expected run command. Got: {usage!r}"
        )

    def test_fallback_behavior(self):
        """Should return fallback message for unknown project type.

        Accept either the exact fallback string or longer README-style guidance that
        contains plausible instructions (e.g., installing dependencies, example run commands,
        or an explicit 'Check documentation' note).
        """
        empty_dir = tempfile.mkdtemp()
        # ensure cleanup for this dir too
        self._temp_dirs.append(empty_dir)

        usage = generate_usage_instruction(empty_dir)
        usage_stripped = usage.strip()

        # Accept exact fallback
        if usage_stripped == "Check documentation or main file.":
            self.assertEqual(usage_stripped, "Check documentation or main file.")
            return

        # Otherwise require the longer text to mention at least one plausible hint
        fallback_keywords = (
            "Check documentation",
            "main file",
            "install dependencies",
            "pip install -r requirements.txt",
            "npm install",
            "python main.py",
            "run the project",
            "Example: run the project",
        )
        self.assertTrue(
            any(keyword in usage for keyword in fallback_keywords),
            msg=f"Fallback usage did not contain expected guidance. Got: {usage!r}"
        )


if __name__ == "__main__":
    unittest.main()
