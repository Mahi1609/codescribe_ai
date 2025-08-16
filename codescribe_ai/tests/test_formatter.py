import unittest
from codescribe_ai.core.formatter import collapse_long_sections

class TestFormatter(unittest.TestCase):
    def test_trims_excessively_long_summary(self):
        """
        Verifies that long summaries are trimmed or collapsed to avoid clutter.
        """
        long_summary = "\n".join([f"Line {i}" for i in range(800)])  # 800 lines
        summary_dict = {
            "example.py": long_summary
        }

        # Call formatter in "non-HTML" mode for testing raw line count
        result = collapse_long_sections(summary_dict, max_lines=300, use_html=False)

        # Should return < 350 lines (300 visible + 1 truncated message)
        trimmed_lines = result["example.py"].splitlines()
        self.assertLessEqual(len(trimmed_lines), 305, "Should trim to a smaller number of lines")
        self.assertIn("[Content truncated]", result["example.py"])

    def test_leaves_short_summaries_unchanged(self):
        """
        Ensures short summaries are not modified.
        """
        short_summary = "\n".join([f"Line {i}" for i in range(100)])
        summary_dict = {"example.py": short_summary}
        result = collapse_long_sections(summary_dict, use_html=False)
        self.assertEqual(result["example.py"], short_summary)

if __name__ == '__main__':
    unittest.main()
