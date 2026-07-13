import json
import tempfile
import unittest
from pathlib import Path

from survey_lottery.safety import find_forbidden_content


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "Survey_Lottery_Automation.ipynb"


class PortfolioSafetyTests(unittest.TestCase):
    def test_notebook_is_a_valid_walkthrough_using_the_package(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))

        self.assertGreaterEqual(len(notebook["cells"]), 4)
        code = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertIn("survey_lottery", code)

    def test_notebook_can_bootstrap_the_public_repository_in_colab(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        code = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )

        self.assertIn("git', 'clone", code)
        self.assertIn(
            "https://github.com/Hunter20041004/survey-lottery-automation.git",
            code,
        )

    def test_secret_scanner_flags_an_unsafe_file(self):
        with tempfile.TemporaryDirectory() as directory:
            unsafe_path = Path(directory) / "config.py"
            unsafe_path.write_text(
                "sender_"
                + "password = \""
                + "abcd"
                + " "
                + "efgh"
                + " "
                + "ijkl"
                + " "
                + "mnop\"",
                encoding="utf-8",
            )

            findings = find_forbidden_content((unsafe_path,))

        self.assertEqual((unsafe_path,), findings)

    def test_portfolio_text_files_contain_no_forbidden_content(self):
        text_suffixes = {".csv", ".ipynb", ".md", ".py", ".svg", ".toml"}
        portfolio_files = tuple(
            path
            for path in PROJECT_ROOT.rglob("*")
            if path.is_file()
            and path.suffix in text_suffixes
            and ".git" not in path.parts
            and ".worktrees" not in path.parts
        )

        self.assertEqual((), find_forbidden_content(portfolio_files))


if __name__ == "__main__":
    unittest.main()
