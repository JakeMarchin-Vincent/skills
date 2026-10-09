"""Hermes package checks; answer quality requires separate live evaluation."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "aus-business-finder-mv"
SKILL = PACKAGE / "SKILL.md"


class AustralianBusinessFinderPackageTest(unittest.TestCase):
    def test_skill_has_hermes_entrypoint(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        parts = text.split("\n---\n", 1)
        self.assertEqual(len(parts), 2)
        frontmatter, body = parts
        self.assertRegex(frontmatter, r"(?m)^name: aus-business-finder-mv$")
        self.assertRegex(frontmatter, r"(?m)^description: \S.+$")
        match = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(match)
        assert match is not None
        description = match.group(1)
        self.assertLessEqual(len(description), 60)
        self.assertIn("Australian business", description)
        self.assertRegex(frontmatter, r"(?m)^version: \d+\.\d+\.\d+$")
        self.assertTrue(body.strip())
        self.assertNotIn("/home/dusk/", text)

    def test_every_package_reference_resolves_inside_package(self):
        files = [SKILL, *PACKAGE.glob("references/*.md")]
        self.assertGreaterEqual(len(files), 3)
        for source in files:
            text = source.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                resolved = (source.parent / target).resolve()
                with self.subTest(source=source.name, target=target):
                    self.assertTrue(resolved.is_relative_to(PACKAGE.resolve()))
                    self.assertTrue(resolved.is_file())
        self.assertIn("references/claim-checking.md", SKILL.read_text(encoding="utf-8"))

    def test_mit_notice_and_public_evaluation_are_present(self):
        notice = (PACKAGE / "references" / "LICENSE.md").read_text(encoding="utf-8")
        self.assertIn("MIT License", notice)
        self.assertIn("Jake Marchin-Vincent", notice)
        evaluation = ROOT / "docs" / "aus-business-finder" / "EVALUATION.md"
        self.assertTrue(evaluation.is_file())


if __name__ == "__main__":
    unittest.main()
