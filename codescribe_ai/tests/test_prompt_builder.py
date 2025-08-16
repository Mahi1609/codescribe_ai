import unittest
from codescribe_ai.core import prompt_builder

class TestPromptBuilder(unittest.TestCase):
    def test_build_prompt_with_file(self):
        code = "def add(a, b):\n    return a + b"
        file_path = "utils/math.py"
        prompt = prompt_builder.build_prompt(code, file_path)

        self.assertIn("add", prompt)
        self.assertIn("utils/math.py", prompt)
        self.assertIn("```python", prompt)

    def test_build_prompt_without_file(self):
        code = "print('Hello World')"
        prompt = prompt_builder.build_prompt(code)

        self.assertIn("Hello World", prompt)
        self.assertNotIn("File:", prompt)

if __name__ == '__main__':
    unittest.main()