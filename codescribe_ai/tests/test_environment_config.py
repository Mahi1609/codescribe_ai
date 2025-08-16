# import unittest
# import os
# from core.environment_config import detect_environment

# class TestEnvironmentDetection(unittest.TestCase):
#     def setUp(self):
#         """
#         Set up different test directories for different environments.
#         """
#         self.test_base = "tests/env_samples"
#         os.makedirs(self.test_base, exist_ok=True)

#     def tearDown(self):
#         """
#         Clean up all test folders and files.
#         """
#         import shutil
#         if os.path.exists(self.test_base):
#             shutil.rmtree(self.test_base)

#     def _create_sample_project(self, folder_name, files: dict):
#         """
#         Utility to create a mock environment with specified files.
#         """
#         path = os.path.join(self.test_base, folder_name)
#         os.makedirs(path, exist_ok=True)
#         for filename, content in files.items():
#             with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
#                 f.write(content)
#         return path

#     def test_detect_react(self):
#         """
#         Should detect React project with .jsx file and react in package.json
#         """
#         files = {
#             "App.jsx": "function App() { return <div>Hello</div>; }",
#             "package.json": '{"dependencies": {"react": "^18.0.0"}}'
#         }
#         project = self._create_sample_project("react_project", files)
#         self.assertEqual(detect_environment(project), "react")

#     def test_detect_django(self):
#         """
#         Should detect Django project via manage.py and settings.py
#         """
#         files = {
#             "manage.py": "# Django entry point",
#             "settings.py": "INSTALLED_APPS = []"
#         }
#         project = self._create_sample_project("django_project", files)
#         self.assertEqual(detect_environment(project), "django")

#     def test_detect_node(self):
#         """
#         Should detect Node project via package.json and .js files
#         """
#         files = {
#             "server.js": "const express = require('express');",
#             "package.json": '{"dependencies": {"express": "^4.0.0"}}'
#         }
#         project = self._create_sample_project("node_project", files)
#         self.assertEqual(detect_environment(project), "node")

#     def test_detect_generic(self):
#         """
#         Should fall back to generic for unknown projects
#         """
#         files = {
#             "main.py": "print('Hello')",
#             "README.md": "# Just a Python script"
#         }
#         project = self._create_sample_project("generic_project", files)
#         self.assertEqual(detect_environment(project), "generic")


# if __name__ == '__main__':
#     unittest.main()


from codescribe_ai.core.environment_config import detect_environment
import os

def detect_environment(project_path: str) -> str:
    """
    Detects the environment type of a project based on common indicators.
    Returns: "python", "node", "react", etc. or "generic" if unknown.
    """

    for root, _, files in os.walk(project_path):
        # --- Python detection ---
        if any(f.endswith(".py") for f in files):
            return "python"

        # --- Node.js detection ---
        if "package.json" in files:
            return "node"

        # --- React detection (looks for .jsx or react keyword) ---
        if any(f.endswith(".jsx") or f.endswith(".tsx") for f in files):
            return "react"

    # Default fallback
    return "generic"
