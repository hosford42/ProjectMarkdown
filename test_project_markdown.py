import os
import shutil
import tempfile
import unittest
from textwrap import dedent

from project_markdown import generate_markdown, read_gitignore, should_ignore, generate_structure, generate_file_contents


class TestDirectoryMarkdown(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.create_test_files()

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def create_test_files(self):
        # Create a sample directory structure
        os.makedirs(os.path.join(self.test_dir, 'subdir1'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'subdir2'), exist_ok=True)

        with open(os.path.join(self.test_dir, 'file1.py'), 'w') as f:
            f.write("print('Hello from file1')")

        with open(os.path.join(self.test_dir, 'file2.py'), 'w') as f:
            f.write("print('Hello from file2')")

        with open(os.path.join(self.test_dir, 'subdir1', 'file3.py'), 'w') as f:
            f.write("print('Hello from file3')")

        with open(os.path.join(self.test_dir, 'subdir2', 'file4.py'), 'w') as f:
            f.write("print('Hello from file4')")

        # Create a file with varying backticks
        with open(os.path.join(self.test_dir, 'file_with_backticks.py'), 'w') as f:
            f.write("def example():\n    return \"```\n    print('Hello')\n```\n\"")

        # Create a .gitignore file and exclude itself
        with open(os.path.join(self.test_dir, '.gitignore'), 'w') as f:
            f.write(".gitignore\nfile2.py\nsubdir2/\n")

    def test_read_gitignore(self):
        ignore_patterns = read_gitignore(self.test_dir)
        self.assertIn('file2.py', ignore_patterns, "Expected 'file2.py' to be in ignore patterns.")
        self.assertIn('subdir2/', ignore_patterns, "Expected 'subdir2/' to be in ignore patterns.")

    def test_should_ignore(self):
        ignore_patterns = read_gitignore(self.test_dir)
        self.assertTrue(should_ignore('file2.py', ignore_patterns), "Expected 'file2.py' to be ignored.")
        self.assertTrue(should_ignore('subdir2', ignore_patterns), "Expected 'subdir2' to be ignored.")
        self.assertFalse(should_ignore('file1.py', ignore_patterns), "Expected 'file1.py' to NOT be ignored.")
        self.assertFalse(should_ignore('subdir1', ignore_patterns), "Expected 'subdir1' to NOT be ignored.")

    def test_generate_structure(self):
        ignore_patterns = read_gitignore(self.test_dir)
        structure = generate_structure(self.test_dir, ignore_patterns)

        expected_structure = dedent("""
            ├── file1.py
            ├── file_with_backticks.py
            └── subdir1
                └── file3.py
        """)

        self.assertEqual(structure.strip(), expected_structure.strip(),
                         f"Expected structure:\n{expected_structure}\nGot:\n{structure}")

    def test_generate_file_contents(self):
        ignore_patterns = read_gitignore(self.test_dir)
        contents = generate_file_contents(self.test_dir, ignore_patterns)

        expected_contents = (
            "## File: file1.py\n\n"
            "```python\nprint('Hello from file1')\n```\n\n"
            "## File: file_with_backticks.py\n\n"
            "````python\ndef example():\n    return \"```\n    print('Hello')\n```\n\"\n````\n\n"
            "## File: file3.py\n\n"
            "```python\nprint('Hello from file3')\n```\n\n"
        )

        self.assertEqual(contents, expected_contents,
                         f"Expected contents:\n{expected_contents}\nGot:\n{contents}")

    def test_generate_markdown(self):
        report = generate_markdown(self.test_dir)
        expected_report_start = "# Directory Structure for"
        expected_structure = dedent("""
            ```plaintext
            ├── file1.py
            ├── file_with_backticks.py
            └── subdir1
                └── file3.py
            ```\n""")
        expected_contents = (
            "## File: file1.py\n\n"
            "```python\nprint('Hello from file1')\n```\n\n"
            "## File: file_with_backticks.py\n\n"
            "````python\ndef example():\n    return \"```\n    print('Hello')\n```\n\"\n````\n\n"
            "## File: file3.py\n\n"
            "```python\nprint('Hello from file3')\n```\n\n"
        )

        self.assertTrue(report.startswith(expected_report_start),
                        "Report should start with the expected header.")
        self.assertIn(expected_structure, report,
                      f"Expected structure:\n{expected_structure}\nNot found in report:\n{report}")
        self.assertIn(expected_contents, report,
                      f"Expected contents:\n{expected_contents}\nNot found in report:\n{report}")


if __name__ == "__main__":
    unittest.main()
