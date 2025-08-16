import unittest
from core import tokenizer

class TestTokenizer(unittest.TestCase):
    def test_chunking_respects_token_limit(self):
        # Simulate a long code string of ~5000 characters (approx. 1250 tokens)
        long_code = "\n".join([f"def func{i}(): pass" for i in range(1000)])
        max_tokens = 200

        chunks = tokenizer.chunk_code(long_code, max_tokens=max_tokens)  # Calls chunk_code from tokenizer.py

        for chunk in chunks:
            est_tokens = tokenizer.estimate_tokens(chunk)  # Calls estimate_tokens to check size
            self.assertLessEqual(est_tokens, max_tokens+50)

if __name__ == '__main__':
    unittest.main()
