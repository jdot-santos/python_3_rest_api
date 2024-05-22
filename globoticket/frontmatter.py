"""
frontmatter.py
Responsible for getting the YAML files that builds the product info
for events and categories
"""
import re
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_DIRECTORY = Path(__file__).parent.parent / "product_info"


def get_frontmatter(product_code: str) -> dict[str, Any]:
    """Read the frontmatter for event with given product_code,
    and return the properties as a dict."""
    frontmatter = find_frontmatter_file(product_code, FRONTMATTER_DIRECTORY).read_text()
    return parse_frontmatter(frontmatter)


def find_frontmatter_file(product_code: str, frontmatter_dir: Path) -> Path:
    if not product_code.strip():
        raise ValueError(
            "An empty string was passed in. Please provide a valid product_code value."
        )

    for file_path in frontmatter_dir.rglob(f"{product_code}.yml"):
        return file_path  # return the first

    raise FileNotFoundError(f"File {product_code}.yml was not found")


class InvalidFrontmatterError(Exception):
    pass


FRONTMATTER_REGEX = re.compile(
    # The ? in the regex makes it non-greedy, which matches everything
    #   up to the three dashes
    # the re.DOTALL option makes the star wildcard also match a new
    #   line character
    r"(---\n(?P<yaml>.*?)---\n)(?P<content>.*)",
    re.DOTALL,
)


def parse_frontmatter(frontmatter: str) -> dict[str, Any]:
    """Return the contents of frontmatter as a dict.

    Raises an InvalidFrontmatterError if anything is wrong."""

    match = re.match(FRONTMATTER_REGEX, frontmatter)
    if not match:
        raise InvalidFrontmatterError("Invalid file structure")

    try:
        data = yaml.load(match.group("yaml"), Loader=yaml.FullLoader)
        data["content"] = match.group("content") or ""
    except (yaml.YAMLError, TypeError) as e:
        raise InvalidFrontmatterError("Invalid YAML (should be a dict)") from e

    return data
