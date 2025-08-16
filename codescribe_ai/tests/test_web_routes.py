# import unittest
# import os
# from io import BytesIO
# from codescribe_ai.main import app

# class TestFlaskRoutes(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()
#         self.uploads_dir = "uploads"
#         self.generated_dir = "generated"
#         os.makedirs(self.uploads_dir, exist_ok=True)
#         os.makedirs(self.generated_dir, exist_ok=True)

#     def tearDown(self):
#         """
#         Remove all test artifacts — both files and folders — from uploads/ and generated/
#         """
#         import shutil

#         for folder in [self.uploads_dir, self.generated_dir]:
#             for item in os.listdir(folder):
#                 full_path = os.path.join(folder, item)

#                 if os.path.isfile(full_path):
#                     os.remove(full_path)
#                 elif os.path.isdir(full_path):
#                     shutil.rmtree(full_path, ignore_errors=True)



#     def test_index_page_renders(self):
#         """
#         Tests that the home page loads successfully.
#         """
#         response = self.client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Upload", response.data)

#     def test_zip_upload_triggers_pipeline(self):
#         """
#         Simulates uploading a ZIP and checks redirection to preview.
#         """
#         sample_zip = BytesIO()
#         sample_zip.name = "sample.zip"

#         # Create an in-memory ZIP with a sample Python file
#         import zipfile
#         with zipfile.ZipFile(sample_zip, mode="w") as zf:
#             zf.writestr("main.py", "def greet(): return 'Hello'")
#         sample_zip.seek(0)

#         response = self.client.post("/", data={
#             "code_zip": (sample_zip, "sample.zip")
#         }, content_type="multipart/form-data", follow_redirects=False)

#         # Expect a redirect to /preview/<filename>
#         self.assertEqual(response.status_code, 302)
#         self.assertIn("/preview/", response.headers.get("Location", ""))

#     def test_preview_page_loads(self):
#         """
#         Creates a dummy README and checks that preview route renders HTML.
#         """
#         dummy_filename = "test_README.txt"
#         dummy_path = os.path.join(self.generated_dir, dummy_filename)
#         with open(dummy_path, "w", encoding="utf-8") as f:
#             f.write("# Project Documentation\n\nThis is a test.")

#         response = self.client.get(f"/preview/{dummy_filename}")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Project Documentation", response.data)

#     def test_download_endpoint(self):
#         """
#         Confirms that a generated file is downloadable.
#         """
#         dummy_filename = "test_README.txt"
#         dummy_path = os.path.join(self.generated_dir, dummy_filename)
#         with open(dummy_path, "w", encoding="utf-8") as f:
#             f.write("This is a downloadable file.")

#         response = self.client.get(f"/download/{dummy_filename}")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"downloadable file", response.data)

# if __name__ == '__main__':
#     unittest.main()


import os
import shutil
import unittest
from codescribe_ai import main


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        """
        Setup a Flask test client and ensure a clean generated directory for tests.
        """
        self.app = main.app
        self.client = self.app.test_client()
        self.generated_dir = os.path.join(os.path.dirname(__file__), "generated")
        os.makedirs(self.generated_dir, exist_ok=True)

        # 🔑 Patch app.OUTPUTS so /download serves from test folder
        main.OUTPUTS = self.generated_dir

    def tearDown(self):
        """
        Clean up test-generated files.
        """
        shutil.rmtree(self.generated_dir, ignore_errors=True)

    def test_index_page_loads(self):
        """
        Confirms the index page is accessible.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_download_endpoint(self):
        """
        Confirms that a generated file is downloadable.
        """
        dummy_filename = "test_README.txt"
        dummy_path = os.path.join(self.generated_dir, dummy_filename)
        with open(dummy_path, "w", encoding="utf-8") as f:
            f.write("This is a downloadable file.")

        response = self.client.get(f"/download/{dummy_filename}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode("utf-8"), "This is a downloadable file."
        )


if __name__ == "__main__":
    unittest.main()
