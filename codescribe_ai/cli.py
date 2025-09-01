# import argparse
# import os
# import tempfile
# import shutil
# from codescribe_ai.scripts.run_pipeline import run_codescribe_pipeline
# from codescribe_ai.core.repo_downloader import download_and_extract_repo

# def main():
#     parser = argparse.ArgumentParser(description="AI-powered README generator")
#     parser.add_argument(
#         "source",
#         help="Path to local project folder or GitHub repo URL"
#     )
#     parser.add_argument(
#         "-o", "--output",
#         default="README.md",
#         help="Output README file path"
#     )
#     args = parser.parse_args()

#     # Check if source is GitHub URL
#     if args.source.startswith("http://") or args.source.startswith("https://"):
#         with tempfile.TemporaryDirectory() as tmpdir:
#             print(f"Downloading repository {args.source}...")
#             repo_path = download_and_extract_repo(args.source, tmpdir)
#             run_codescribe_pipeline(repo_path, args.output)
#     else:
#         # Local folder
#         src_path = os.path.abspath(args.source)
#         if not os.path.exists(src_path):
#             print(f"❌ Path does not exist: {src_path}")
#             return
#         run_codescribe_pipeline(src_path, args.output)

#     print(f"✅ README generated at: {args.output}")

# if __name__ == "__main__":
#     main()





import argparse
import os
import tempfile
import requests
from codescribe_ai.scripts.run_pipeline import run_codescribe_pipeline
from codescribe_ai.core.repo_downloader import download_and_extract_repo


def call_flask_api(source, output):
    """
    Fallback: call hosted Flask API when GROQ_API_KEY is not set.
    """
    flask_url = os.getenv("CODESCRIBE_API_URL", "https://codescribe-ai.onrender.com/generate")

    try:
        if source.startswith("http://") or source.startswith("https://"):
            # GitHub repo URL
            resp = requests.post(flask_url, data={"repo_url": source}, timeout=300)
        else:
            # Local folder → compress into zip and send
            import shutil, tempfile
            tmp_zip = tempfile.mktemp(suffix=".zip")
            shutil.make_archive(tmp_zip.replace(".zip", ""), "zip", source)
            with open(tmp_zip, "rb") as f:
                resp = requests.post(flask_url, files={"file": f}, timeout=300)

        if resp.status_code == 200:
            with open(output, "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"✅ README generated via Flask API at: {output}")
        else:
            print(f"❌ Flask API error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"❌ Failed to call Flask API: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI-powered README generator")
    parser.add_argument("source", help="Path to local project folder or GitHub repo URL")
    parser.add_argument("-o", "--output", default="README.md", help="Output README file path")
    args = parser.parse_args()

    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key:
        # 🔑 Run locally with Groq key
        if args.source.startswith("http://") or args.source.startswith("https://"):
            with tempfile.TemporaryDirectory() as tmpdir:
                print(f"Downloading repository {args.source}...")
                repo_path = download_and_extract_repo(args.source, tmpdir)
                run_codescribe_pipeline(repo_path, args.output)
        else:
            # Local folder
            src_path = os.path.abspath(args.source)
            if not os.path.exists(src_path):
                print(f"❌ Path does not exist: {src_path}")
                return
            run_codescribe_pipeline(src_path, args.output)

        print(f"✅ README generated locally at: {args.output}")
    else:
        # ⚠️ No key → use hosted API
        print("⚠️ No GROQ_API_KEY found → using Flask API fallback...")
        call_flask_api(args.source, args.output)


if __name__ == "__main__":
    main()