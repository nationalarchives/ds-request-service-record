import re
import unittest

from app.constants import ExternalLinks
from app.lib.content import load_content


class TestMarkdownLinksInContent(unittest.TestCase):
    # Markdown links in content.yaml are written as [text](TARGET).
    # We only care about the TARGET part here, because that should map to an
    # ExternalLinks constant.
    LINK_PATTERN = re.compile(r"\[([^]]+)\]\(([^)]+)\)")

    def _iter_strings(self, node):
        # content.yaml is nested dictionaries and lists, so we recursively walk
        # the structure and yield every string value we find.
        if isinstance(node, dict):
            for value in node.values():
                yield from self._iter_strings(value)
        elif isinstance(node, list):
            for item in node:
                yield from self._iter_strings(item)
        elif isinstance(node, str):
            yield node

    def test_all_markdown_link_targets_are_external_links_constants(self):
        # Load the rendered content tree and inspect every string for markdown
        # links. Each target should match a name on ExternalLinks.
        content = load_content()
        for text in self._iter_strings(content):
            for match in self.LINK_PATTERN.finditer(text):
                target = match.group(2).strip()
                with self.subTest(target=target, text=text):
                    self.assertTrue(
                        hasattr(ExternalLinks, target),
                        f"Markdown link target '{target}' is not defined in ExternalLinks",
                    )


if __name__ == "__main__":
    unittest.main()
