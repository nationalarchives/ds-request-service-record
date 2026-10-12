import re
import unittest

from flask import url_for

from app import create_app
from app.constants import ExternalLinks, MultiPageFormRoutes
from app.lib.content import load_content


class TestMarkdownLinksInContent(unittest.TestCase):
    # Markdown links in content.yaml are written as [text](TARGET).
    # TARGET must now be explicit so content is self-describing:
    # - external:EXTERNAL_LINK_NAME
    # - route:ROUTE_NAME
    LINK_PATTERN = re.compile(r"\[([^]]+)]\(([^)]+)\)")

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.Test")

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

    def test_all_markdown_link_targets_use_supported_explicit_prefixes(self):
        # Load the rendered content tree and inspect every string for markdown
        # links. Each target must declare whether it is an external link or an
        # internal route, and then resolve against the matching source of truth.
        content = load_content()
        with self.app.test_request_context():
            for text in self._iter_strings(content):
                for match in self.LINK_PATTERN.finditer(text):
                    target = match.group(2).strip()
                    with self.subTest(target=target, text=text):
                        if target.startswith("external:"):
                            external_key = target.removeprefix("external:").strip()
                            self.assertTrue(
                                external_key,
                                "External markdown links must name an ExternalLinks constant after 'external:'",
                            )
                            self.assertTrue(
                                hasattr(ExternalLinks, external_key),
                                f"Markdown link target '{target}' is not defined in ExternalLinks",
                            )
                            continue

                        if target.startswith("route:"):
                            route_name = target.removeprefix("route:").strip()
                            self.assertTrue(
                                route_name,
                                "Route markdown links must name a MultiPageFormRoutes member after 'route:'",
                            )
                            self.assertTrue(
                                hasattr(MultiPageFormRoutes, route_name),
                                f"Markdown link target '{target}' is not defined in MultiPageFormRoutes",
                            )
                            endpoint = getattr(MultiPageFormRoutes, route_name).value
                            self.assertTrue(
                                url_for(endpoint),
                                f"Markdown link target '{target}' could not be resolved to a URL",
                            )
                            continue

                        self.fail(
                            f"Markdown link target '{target}' must use external:EXTERNAL_LINK_NAME or route:ROUTE_NAME"
                        )


if __name__ == "__main__":
    unittest.main()
