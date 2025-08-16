import unittest
from unittest.mock import patch
from codescribe_ai.core import summarizer

class TestGroqSummarizer(unittest.TestCase):

    @patch("core.summarizer.requests.post")
    def test_summarize_code_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [
                {"message": {"content": "This function adds two numbers."}}
            ]
        }

        code = "def add(a, b): return a + b"
        summary = summarizer.summarize_code(code, file_path="utils/math.py")

        self.assertIsInstance(summary, str)
        self.assertIn("adds two numbers", summary)

    @patch("core.summarizer.requests.post")
    def test_summarize_code_api_failure(self, mock_post):
        mock_post.return_value.status_code = 401
        mock_post.return_value.text = "Unauthorized"

        with self.assertRaises(RuntimeError):
            summarizer.summarize_code("print('Hi')")

if __name__ == "__main__":
    unittest.main()



# import unittest
# from unittest.mock import patch
# from core import summarizer_openai

# class TestOpenAISummarizer(unittest.TestCase):

#     @patch("core.summarizer_openai.openai.ChatCompletion.create")
#     def test_summarize_code_success(self, mock_create):
#         mock_create.return_value = {
#             "choices": [
#                 {"message": {"content": "Prints Hello World."}}
#             ]
#         }

#         code = "print('Hello World')"
#         summary = summarizer_openai.summarize_code(code)

#         self.assertIsInstance(summary, str)
#         self.assertIn("Hello World", summary)

# if __name__ == "__main__":
#     unittest.main()
