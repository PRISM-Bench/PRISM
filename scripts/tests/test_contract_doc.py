import re
import unittest
from pathlib import Path

from scripts.validate_submission import CHECKS, REPO_ROOT

CONTRACT = REPO_ROOT / "submissions" / "CONTRACT.md"

# Every enforced rule in CONTRACT.md opens with: **[checked] `check_name`**
CHECKED_MARKER = re.compile(r"\*\*\[checked\] `([a-z_]+)`\*\*")


class ContractDocTests(unittest.TestCase):
    def test_contract_exists(self):
        self.assertTrue(CONTRACT.is_file(), f"{CONTRACT} is missing")

    def test_checked_tags_match_the_validator_registry(self):
        documented = set(CHECKED_MARKER.findall(CONTRACT.read_text(encoding="utf-8")))
        registered = {name for name, _ in CHECKS}
        self.assertEqual(
            documented,
            registered,
            "CONTRACT.md's [checked] rules and the validator's checks have diverged",
        )

    def test_every_honour_system_rule_says_why_it_cannot_be_checked(self):
        text = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("[honour system]", text)
        self.assertNotIn("[checked]  ", text)


if __name__ == "__main__":
    unittest.main()
