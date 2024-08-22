import os
from pathlib import Path
import re
from typing import List, Tuple
from collections import namedtuple

Warning = namedtuple("Warning", ["file", "line", "message"])


class DocAnalyzer:
    def __init__(self, root_dir: str = "docs"):
        self.root_dir = Path(root_dir)
        self.warnings: List[Warning] = []
        self.specific_words = {"he", "she", "his", "her", "we", "us"}

    def analyze(self) -> List[Warning]:
        for item in self.root_dir.rglob("*"):
            if any(part in {"images", ".snippets"} for part in item.parts):
                continue

            if item.is_file():
                self.check_file_rules(item)
            elif item.is_dir():
                self.check_folder_rules(item)

        return self.warnings

    def check_folder_rules(self, folder_path: Path):
        if not (folder_path / "index.md").exists():
            self.warnings.append(Warning(folder_path, 0, "Missing an index.md file"))
        if not (folder_path / ".pages").exists():
            self.warnings.append(Warning(folder_path, 0, "Missing a .pages file"))

    def check_file_rules(self, file_path: Path):
        if file_path.name == "index.md":
            self.check_index_md_description(file_path)
        elif file_path.suffix == ".md":
            content = file_path.read_text(encoding="utf-8")
            self.check_external_links(file_path, content)
            self.check_list_items(file_path, content)
            self.check_specific_words(file_path, content)

    def check_index_md_description(self, file_path: Path):
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            self.warnings.append(
                Warning(file_path, 0, "Invalid or missing front matter.")
            )
            return

        front_matter = match.group(1)
        description_match = re.search(r"description:\s*(.*)", front_matter)
        if not description_match:
            self.warnings.append(
                Warning(file_path, 0, "Missing description in front matter.")
            )
            return

        description = description_match.group(1).strip()
        char_count = len(description)
        if char_count < 120 or char_count > 160:
            self.warnings.append(
                Warning(
                    file_path,
                    0,
                    f"Description length is {char_count} characters. It should be between 120 and 160 characters.",
                )
            )

    def check_external_links(self, file_path: Path, content: str):
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)({[^}]*})?"
        for match in re.finditer(link_pattern, content):
            link_text, url, attributes = match.groups()
            if url.startswith(("http://", "https://")) and not (
                attributes
                and ("target=_blank" in attributes or "target=\_blank" in attributes)
            ):
                self.warnings.append(
                    Warning(
                        file_path,
                        0,
                        f"External link missing {{target=_blank}} or {{target=\\_blank}}: [{link_text}]({url})",
                    )
                )

    def check_list_items(self, file_path: Path, content: str):
        list_item_pattern = r"^\s*(?:[-*+]|\d+\.)\s+(.+)$"
        for line_number, line in enumerate(content.splitlines(), 1):
            match = re.match(list_item_pattern, line)
            if match and match.group(1).strip().endswith("."):
                self.warnings.append(
                    Warning(
                        file_path,
                        line_number,
                        f"List item should not end with a period: {match.group(1)}",
                    )
                )

    def check_specific_words(self, file_path: Path, content: str):
        for word in self.specific_words:
            pattern = rf"\b{re.escape(word)}\b"
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_number = content.count("\n", 0, match.start()) + 1
                self.warnings.append(
                    Warning(
                        file_path,
                        line_number,
                        f"Found specific word '{word}': {match.group()}",
                    )
                )


def main():
    analyzer = DocAnalyzer()
    warnings = analyzer.analyze()

    if warnings:
        print(f"\nTotal warnings: {len(warnings)}")

        for warning in warnings:
            print(f"Warning: {warning.file}:{warning.line} - {warning.message}")

        exit(1)
    else:
        print("No warnings found.")
        exit(0)


if __name__ == "__main__":
    main()
