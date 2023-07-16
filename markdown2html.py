#!/usr/bin/python3

"""
Markdown to HTML Converter
"""

import sys
import os
import re
import hashlib

def convert_heading(match):
    """
    Converts Markdown headings to HTML headings
    """
    level = len(match.group(1))
    return f'<h{level}>{match.group(2)}</h{level}>'

def convert_unordered_list(match):
    """
    Converts Markdown unordered lists to HTML unordered lists
    """
    items = match.group(1).split('\n')
    list_items = ''.join([f'<li>{item.strip()}</li>' for item in items])
    return f'<ul>{list_items}</ul>'

def convert_ordered_list(match):
    """
    Converts Markdown ordered lists to HTML ordered lists
    """
    items = match.group(1).split('\n')
    list_items = ''.join([f'<li>{item.strip()}</li>' for item in items])
    return f'<ol>{list_items}</ol>'

def convert_paragraph(match):
    """
    Converts Markdown paragraphs to HTML paragraphs
    """
    lines = match.group(1).split('\n')
    content = '<br/>\n'.join([line.strip() for line in lines])
    return f'<p>{content}</p>'

def convert_bold(match):
    """
    Converts Markdown bold syntax to HTML bold tags
    """
    return f'<b>{match.group(1)}</b>'

def convert_emphasis(match):
    """
    Converts Markdown emphasis syntax to HTML emphasis tags
    """
    return f'<em>{match.group(1)}</em>'

def convert_custom_syntax(match):
    """
    Converts custom syntax [[content]] to MD5 hash (lowercase)
    """
    content = match.group(1)
    md5_hash = hashlib.md5(content.encode()).hexdigest()
    return md5_hash

def convert_custom_syntax_remove_c(match):
    """
    Converts custom syntax ((content)) to remove all 'c' occurrences (case insensitive)
    """
    content = match.group(1)
    return content.replace('c', '', flags=re.IGNORECASE)

def markdown_to_html(markdown_content):
    """
    Converts Markdown content to HTML
    """
    # Convert Markdown headings to HTML headings
    markdown_content = re.sub(r'^(#{1,6})\s*(.*?)$', convert_heading, markdown_content, flags=re.MULTILINE)

    # Convert Markdown unordered lists to HTML unordered lists
    markdown_content = re.sub(r'^\s*-\s+(.*)$', convert_unordered_list, markdown_content, flags=re.MULTILINE)

    # Convert Markdown ordered lists to HTML ordered lists
    markdown_content = re.sub(r'^\s*\*\s+(.*)$', convert_ordered_list, markdown_content, flags=re.MULTILINE)

    # Convert Markdown paragraphs to HTML paragraphs
    markdown_content = re.sub(r'^\s*(.*)$', convert_paragraph, markdown_content, flags=re.MULTILINE)

    # Convert Markdown bold syntax to HTML bold tags
    markdown_content = re.sub(r'\*\*(.*?)\*\*', convert_bold, markdown_content)

    # Convert Markdown emphasis syntax to HTML emphasis tags
    markdown_content = re.sub(r'__(.*?)__', convert_emphasis, markdown_content)

    # Convert custom syntax [[content]] to MD5 hash (lowercase)
    markdown_content = re.sub(r'\[\[(.*?)\]\]', convert_custom_syntax, markdown_content)

    # Convert custom syntax ((content)) to remove all 'c' occurrences (case insensitive)
    markdown_content = re.sub(r'\(\((.*?)\)\)', convert_custom_syntax_remove_c, markdown_content, flags=re.IGNORECASE)

    return markdown_content

def main():
    """
    Main function
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the input file
    with open(input_file, 'r') as file:
        markdown_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown_to_html(markdown_content)

    # Write the HTML content to the output file
    with open(output_file, 'w') as file:
        file.write(html_content)

    sys.exit(0)

if __name__ == "__main__":
    main()
