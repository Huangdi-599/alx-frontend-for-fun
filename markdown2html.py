#!/usr/bin/python3

"""
markdown2html.py

Converts Markdown file to HTML file with additional parsing.

Usage: ./markdown2html.py <input_file> <output_file>
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    """
    Converts Markdown file to HTML file with additional parsing.

    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the input file
    with open(input_file, 'r') as file:
        markdown_content = file.read()

    # Convert Markdown headings to HTML headings
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown_content)
    html_content = re.sub(r'__(.*?)__', r'<em>\1</em>', html_content)
    html_content = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), html_content)
    html_content = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', ''), html_content, flags=re.IGNORECASE)

    # Write the HTML content to the output file
    with open(output_file, 'w') as file:
        file.write(html_content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
