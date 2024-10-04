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
