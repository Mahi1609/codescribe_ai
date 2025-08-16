import unittest
from codescribe_ai.core.token_manager import TokenManager

def mock_token_estimator(text):  # Fake estimator: 1 token = 4 chars
    return len(text) // 4

class TestTokenManager(unittest.TestCase):

    def setUp(self):
        self.tm = TokenManager(max_tokens_global=1000)  # Simulate a 1000-token budget
        self.tm.set_token_estimator(mock_token_estimator)  # Use mock token estimator

    def test_add_usage_and_limit(self):
        # Add 2 chunks under the limit
        self.tm.add_usage("file1.py", "a" * 400)  # ~100 tokens
        self.tm.add_usage("file2.py", "b" * 800)  # ~200 tokens

        self.assertEqual(self.tm.get_total_used(), 300)
        self.assertEqual(self.tm.get_log()["file1.py"], 100)
        self.assertTrue(self.tm.can_process(600))  # 1000 - 300 = 700 available
        self.assertFalse(self.tm.can_process(800))  # Would exceed

    def test_reject_if_exceeds_limit(self):
        with self.assertRaises(RuntimeError):
            self.tm.add_usage("file3.py", "x" * 5000)  # ~1250 tokens > limit

    def test_get_remaining_tokens(self):
        self.tm.add_usage("file4.py", "y" * 1000)  # ~250 tokens
        self.assertEqual(self.tm.get_remaining(), 750)

if __name__ == '__main__':
    unittest.main()
