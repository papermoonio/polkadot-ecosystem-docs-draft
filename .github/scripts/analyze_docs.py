import os
from pathlib import Path
import re

def analyze_docs(root_dir='docs'):
    root = Path(root_dir)
    
    for item in root.rglob('*'):
        # Skip 'images' and '.snippets' folders and their contents
        if any(part in ['images', '.snippets'] for part in item.parts):
            continue

        if item.is_file():
            check_file_rules(item)
        elif item.is_dir():
            check_folder_rules(item)

def check_file_rules(file_path):
    if file_path.name == 'index.md':
        check_index_md_description(file_path)
    elif file_path.suffix == '.md':
        check_external_links(file_path)
        check_list_items(file_path)
        check_specific_words(file_path)

def check_index_md_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the description from the front matter
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        front_matter = match.group(1)
        description_match = re.search(r'description:\s*(.*)', front_matter)
        if description_match:
            description = description_match.group(1).strip()
            char_count = len(description)
            if char_count < 120 or char_count > 160:
                print(f"Warning: {file_path} - Description length is {char_count} characters. It should be between 120 and 160 characters.")
        else:
            print(f"Warning: {file_path} - Missing description in front matter.")
    else:
        print(f"Warning: {file_path} - Invalid or missing front matter.")

def check_external_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to find Markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)({[^}]*})?'
    
    for match in re.finditer(link_pattern, content):
        link_text, url, attributes = match.groups()
        
        # Check if the link is external (starts with http:// or https://)
        if url.startswith(('http://', 'https://')):
            if not attributes or ('target=_blank' not in attributes and 'target=\_blank' not in attributes):
                print(f"Warning: {file_path} - External link missing {{target=_blank}} or {{target=\\_blank}}: [{link_text}]({url})")

def check_list_items(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match list items
    list_item_pattern = r'^\s*[-*+]\s+(.+)$'
    list_item_pattern = r'^\s*(?:[-*+]|\d+\.)\s+(.+)$'
    
    for line_number, line in enumerate(content.split('\n'), 1):
        match = re.match(list_item_pattern, line)
        if match:
            item_content = match.group(1)
            if item_content.strip().endswith('.'):
                print(f"Warning: {file_path}:{line_number} - List item should not end with a period: {item_content}")

def check_specific_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    specific_words = ['he', 'she', 'his', 'her', 'we', 'us', 'our']
    
    for word in specific_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        
        for match in matches:
            line_number = content.count('\n', 0, match.start()) + 1
            print(f"Warning: {file_path}:{line_number} - Found specific word '{word}': {match.group()}")

def check_folder_rules(folder_path):
    # TODO: It should not be necessary to skip these folders here because they are already being skipped in the 'analyze_docs' function.
    # Skip 'images' and '.snippets' folders
    if folder_path.name in ['images', '.snippets']:
        print(f"Skipping {folder_path}")
        return

    index_file = folder_path / 'index.md'
    pages_file = folder_path / '.pages'

    if not index_file.exists():
        print(f"Warning: {folder_path} is missing an index.md file")

    if not pages_file.exists():
        print(f"Warning: {folder_path} is missing a .pages file")

def main():
    analyze_docs()

if __name__ == "__main__":
    main()