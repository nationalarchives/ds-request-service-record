import unittest
from pathlib import Path
import re
from app.lib.content import load_content


class TestForUnusedContent(unittest.TestCase):
    TEMPLATES_DIR = Path("app/templates")
    FORMS_DIR = Path("app/main/forms")
    SKIP_PATTERNS = [
        re.compile(r"\.rows"),
        re.compile(r"\.table_rows"),
        re.compile(r"\.fields"),
    ]

    @classmethod
    def setUpClass(cls):
        cls._template_texts = cls._read_all_html_templates()
        cls._form_texts = cls._read_all_form_files()

    @staticmethod
    def _read_all_html_templates():
        if not TestForUnusedContent.TEMPLATES_DIR.exists():
            return []
        texts = []
        for f in TestForUnusedContent.TEMPLATES_DIR.rglob("*.html"):
            try:
                texts.append(f.read_text(encoding="utf-8"))
            except Exception:
                pass
        return texts

    @staticmethod
    def _read_all_form_files():
        if not TestForUnusedContent.FORMS_DIR.exists():
            return []
        texts = []
        for f in TestForUnusedContent.FORMS_DIR.rglob("*.py"):
            try:
                texts.append(f.read_text(encoding="utf-8"))
            except Exception:
                pass
        return texts

    def _flatten(self, node, prefix=""):
        if isinstance(node, dict):
            for k, v in node.items():
                full = f"{prefix}.{k}" if prefix else k
                yield full
                yield from self._flatten(v, full)
        elif isinstance(node, list):
            for item in node:
                yield from self._flatten(item, prefix)

    def _field_base_name(self, key):
        # forms.fields.<field_name>.<rest>
        if key.startswith("forms.fields."):
            parts = key.split(".")
            if len(parts) >= 3:
                return parts[2]
        return None

    # This test checks that all content keys we have in the YAML are actually used in templates.
    # The intention here is to ensure we don't end up with unused content entries that
    # could confuse content designers or developers who may be reviewing the content.yaml file
    # to identify what content is in use.
    def test_content_used_in_templates(self):
        content = load_content()
        for key in self._flatten(content):
            if any(p.search(key) for p in self.SKIP_PATTERNS):
                continue
            with self.subTest(key=key):
                found = any(key in tpl for tpl in self._template_texts)
                self.assertTrue(found, f"Content key '{key}' not found in any template")

    # This test checks that all form field content keys we have in the YAML are used in forms.
    # We need a slightly different approach here because forms use the get_field_content() method
    # rather than directly referencing the content key.
    def test_for_fields_passed_to_get_field_content(self):
        content = load_content()
        for key in self._flatten(content):
            if not key.startswith("forms.fields."):
                continue
            field_name = self._field_base_name(key)
            if not field_name:
                continue
            with self.subTest(key=key):
                # Note: This regex is set to match the signature of get_field_content calls in forms.
                #       The test is therefore a little brittle, but it'll be immediately apparent if
                #       the test breaks due to changes in get_field_content.
                pattern = re.compile(
                    rf"get_field_content\(content,\s?['\"]{field_name}['\"],\s?['\"][a-z|_]+['\"]\)"
                )
                found = any(pattern.search(txt) for txt in self._form_texts)
                self.assertTrue(
                    found, f"Form field content key '{field_name}' not used in any form"
                )


if __name__ == "__main__":
    unittest.main()
