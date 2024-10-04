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
