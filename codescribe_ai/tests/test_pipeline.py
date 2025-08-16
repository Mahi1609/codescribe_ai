import unittest
import os
from scripts.run_pipeline import run_codescribe_pipeline

class TestPipelineOutputFormats(unittest.TestCase):
    def setUp(self):
        """
        Set up a minimal test project directory and output paths.
        """
        self.test_dir = "tests/sample_project"
        self.output_md = "tests/sample_output/README.md"
        self.output_txt = "tests/sample_output/README.txt"

        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.output_md), exist_ok=True)

        with open(os.path.join(self.test_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write(
                "import os\n"
                "def greet(name):\n"
                "    return f'Hello {name}'\n"
                "\n"
                "if __name__ == '__main__':\n"
                "    print(greet('world'))"
            )

    def tearDown(self):
        """
        Clean up after each test run.
        """
        for file in [self.output_md, self.output_txt]:
            if os.path.exists(file):
                os.remove(file)

        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

    def test_pipeline_generates_md_and_txt(self):
        """
        Verifies pipeline generates both Markdown and plain text documentation.
        """
        # Run once for Markdown
        run_codescribe_pipeline(self.test_dir, self.output_md)
        self.assertTrue(os.path.exists(self.output_md), "README.md not generated")

        # Run again for plain text
        run_codescribe_pipeline(self.test_dir, self.output_txt)
        self.assertTrue(os.path.exists(self.output_txt), "README.txt not generated")

        # Check content
        with open(self.output_md, "r", encoding="utf-8") as f_md:
            md_content = f_md.read()
        with open(self.output_txt, "r", encoding="utf-8") as f_txt:
            txt_content = f_txt.read()

        self.assertIn("Project Documentation", md_content)
        self.assertIn("main.py", md_content)
        self.assertIn("Project Documentation", txt_content)
        self.assertIn("main.py", txt_content)

if __name__ == '__main__':
    unittest.main()
