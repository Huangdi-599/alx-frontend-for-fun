#!/usr/bin/python3
"""
Markdown to HTML Converter
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    """
    Convert Markdown content to HTML and write to output file
    """
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the input file
    with open(input_file, 'r') as file:
        markdown_content = file.read()

    # Convert Markdown headings to HTML headings
    html_content = re.sub(r'^#\s(.+)$', r'<h1>\1</h1>', markdown_content, flags=re.MULTILINE)
    html_content = re.sub(r'^##\s(.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^###\s(.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^####\s(.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#####\s(.+)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^######\s(.+)$', r'<h6>\1</h6>', html_content, flags=re.MULTILINE)

    # Convert Markdown unordered lists to HTML lists
    html_content = re.sub(r'^-\s(.+)$', r'<ul>\n<li>\1</li>\n</ul>', html_content, flags=re.MULTILINE)

    # Convert Markdown ordered lists to HTML lists
    html_content = re.sub(r'^\*\s(.+)$', r'<ol>\n<li>\1</li>\n</ol>', html_content, flags=re.MULTILINE)

    # Convert Markdown paragraphs to HTML paragraphs
    html_content = re.sub(r'^([^\-*#].*)$', r'<p>\n\1\n</p>', html_content, flags=re.MULTILINE)

    # Convert Markdown bold syntax to HTML bold tags
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_content)
    html_content = re.sub(r'__(.*?)__', r'<em>\1</em>', html_content)

    # Convert custom syntax: [[content]] to MD5 hash (lowercase)
    html_content = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), html_content)

    # Convert custom syntax: ((content)) to remove all occurrences of 'c' (case insensitive)
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
