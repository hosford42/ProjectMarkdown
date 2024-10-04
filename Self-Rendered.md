# Directory Structure for '.'

```plaintext
├── LICENSE.md
├── README.md
├── project_markdown.py
└── test_project_markdown.py
```

## File: LICENSE.md

```markdown
Copyright 2024 Aaron Hosford

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without 
restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom 
the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.

```

## File: project_markdown.py

````python
import argparse
import os

import pyperclip


FILE_TYPES = {
    '.py': 'python',
    '.md': 'markdown',
    '.txt': 'plaintext'
}


def read_gitignore(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    ignore_patterns = set()

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.add(line)

    return ignore_patterns


def should_ignore(item, ignore_patterns):
    for pattern in ignore_patterns:
        if item == pattern or item.startswith(pattern.rstrip('/')):
            return True
    return False


def generate_markdown(directory):
    ignore_patterns = read_gitignore(directory)
    markdown = f"# Directory Structure for '{directory}'\n\n"
    markdown += "```plaintext\n"
    markdown += generate_structure(directory, ignore_patterns)
    markdown += "```\n\n"
    markdown += generate_file_contents(directory, ignore_patterns)
    return markdown


def generate_structure(directory, ignore_patterns, indent=0):
    structure = ""
    items = os.listdir(directory)
    items.sort()

    items = [item for item in items if not should_ignore(item, ignore_patterns)]

    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last_item = index == len(items) - 1
        prefix = "    " if is_last_item else "│   "
        connector = "└── " if is_last_item else "├── "

        structure += f"{connector}{item}\n"

        if os.path.isdir(path):
            sub_structure = generate_structure(path, ignore_patterns, indent + 1)
            sub_structure = (sub_structure
                             .replace("│", prefix)
                             .replace("├──", prefix + "├──")
                             .replace("└──", prefix + "└──"))
            structure += sub_structure

    return structure


def generate_file_contents(directory, ignore_patterns):
    contents = ""
    for item in os.listdir(directory):
        if should_ignore(item, ignore_patterns):
            continue
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            contents += f"## File: {item}\n\n"
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                file_contents = file.read()
                max_backticks = 0
                current_backticks = 0

                for char in file_contents:
                    if char == '`':
                        current_backticks += 1
                    else:
                        max_backticks = max(max_backticks, current_backticks)
                        current_backticks = 0

                max_backticks = max(max_backticks, current_backticks)
                delimiter = '`' * max(3, max_backticks + 1)
                syntax_signifier = FILE_TYPES.get(os.path.splitext(path)[-1], '')
                contents += f"{delimiter}{syntax_signifier}\n{file_contents}\n{delimiter}\n\n"
        elif os.path.isdir(path):
            contents += generate_file_contents(path, ignore_patterns)
    return contents


def copy_to_clipboard(text):
    # Use pyperclip to copy text to clipboard
    pyperclip.copy(text)


def main():
    parser = argparse.ArgumentParser(description='Generate a Markdown representation of a directory structure.')
    parser.add_argument('directory', type=str, help='The directory path to examine.')
    parser.add_argument('-o', '--output', type=str, help='Output file to save the report.')
    parser.add_argument('-p', '--print', action='store_true', help='Print the report to stdout.')

    args = parser.parse_args()

    report = generate_markdown(args.directory)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(report)
    elif args.print:
        print(report)
    else:
        copy_to_clipboard(report)


if __name__ == "__main__":
    main()

````

## File: README.md

````markdown
# Project Markdown

Project Markdown is a script designed to make it easy to
copy and paste a whole project in a form that makes it 
easy for an LLM to view the code in its entirety. Simply
put, it scans the entire project folder, builds a Markdown
representation of the contents, and copies that content
to the clipboard for you. It even respects your .gitignore,
so you don't end up with unwanted content listed.

## Features

- Recursively examines directories and subdirectories.
- Generates a Markdown-formatted directory structure.
- Outputs the contents of Python files in Markdown code blocks.
- Easy to use and integrate into other projects.

## Installation

To use the `project_markdown` module, you need Python 3.x 
installed on your system. You can clone the repository or 
download the module directly.

```bash
git clone https://github.com/hosford42/ProjectMarkdown.git
cd ProjectMarkdown
```

## Usage

1. **Run the Module**: You can run the module directly from the 
   command line.

   ```bash
   python project_markdown.py <project-path>
   ```

2. **Output**: The module will copy a Markdown representation
   of the directory structure and file contents to the
   clipboard.

### Example

The directory structure will be formatted like this:

```
example_directory/
├── src/
│   ├── parser.py
│   ├── stack.py
│   ├── vectorization.py
│   ├── summarization.py
│   └── output_generator.py
└── tests/
    ├── test_parser.py
    ├── test_stack.py
    ├── test_vectorization.py
    ├── test_summarization.py
    └── test_output_generator.py
```

After the directory structure, the file contents will be
included, each with its own heading and its own code block,
properly formatted for Markdown rendering.

If you'd like to see the actual content produced, take a
look at how Project Markdown [renders itself](Self-Rendered.md).

## Running Tests

To ensure the module works as expected, you can run the 
provided unit tests. Make sure you have `unittest` available 
(it is included with Python).

```bash
python -m unittest discover -s tests
```

## Contributing

Contributions are welcome! If you have suggestions for 
improvements or new features, feel free to open an issue or 
submit a pull request.

## License

This project is licensed under the MIT License. See the 
[LICENSE](LICENSE.md) file for details.

````

## File: test_project_markdown.py

`````python
import os
import shutil
import tempfile
import unittest

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

        expected_structure = (
            "├── file1.py\n"
            "├── file_with_backticks.py\n"
            "└── subdir1\n"
            "    └── file3.py\n"
        )

        self.assertEqual(structure, expected_structure,
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
        expected_structure = (
            "```plaintext\n"
            "├── file1.py\n"
            "├── file_with_backticks.py\n"
            "└── subdir1\n"
            "    └── file3.py\n"
            "```\n\n"
        )
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

`````

