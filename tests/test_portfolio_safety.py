import json
import re
import tempfile
import unittest
from pathlib import Path

from survey_lottery.safety import find_forbidden_content


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "Survey_Lottery_Automation.ipynb"
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"

CHECKOUT_PIN = "34e114876b0b11c390a56381ad16ebd13914f8d5"
SETUP_PYTHON_PIN = "a26af69be951a213d495a4c3e4e4022e16d87065"


def assert_ci_workflow_contract(workflow: str) -> None:
    required = (
        "permissions:\n  contents: read",
        "timeout-minutes: 10",
        (
            "concurrency:\n"
            "  group: ci-${{ github.workflow }}-${{ github.ref }}\n"
            "  cancel-in-progress: true"
        ),
        'python-version: ["3.11", "3.12"]',
        f"actions/checkout@{CHECKOUT_PIN}",
        "persist-credentials: false",
        f"actions/setup-python@{SETUP_PYTHON_PIN}",
        "python3 -m pip install --upgrade pip setuptools",
        "python3 -m pip install -e . pip-audit",
        "python3 -m pip check",
        "python3 -m pip_audit",
        "PYTHONPATH=src python3 -m unittest discover -s tests -v",
    )
    for snippet in required:
        if snippet not in workflow:
            raise AssertionError(f"CI workflow is missing required contract: {snippet}")

    if workflow.count("\non:\n") != 1 or workflow.count("\npermissions:") != 1:
        raise AssertionError("CI workflow must declare one explicit trigger block")
    trigger_block = workflow.split("\non:\n", 1)[1].split("\npermissions:", 1)[0]
    if trigger_block.splitlines() != [
        "  push:",
        "  pull_request:",
        "  workflow_dispatch:",
    ]:
        raise AssertionError(
            "CI workflow must run only on push, pull_request, and workflow_dispatch"
        )

    if workflow.count("permissions:") != 1 or "contents: write" in workflow:
        raise AssertionError("CI workflow permissions must remain read-only")

    forbidden = (
        "gmail",
        "google",
        "smtp",
        "env:",
        "services:",
        "continue-on-error",
        "|| true",
        "curl ",
        "wget ",
    )
    lowered = workflow.lower()
    if re.search(r"\bsecrets\s*(?:\.|\[)", lowered):
        raise AssertionError("CI workflow must not reference GitHub secrets")
    for snippet in forbidden:
        if snippet in lowered:
            raise AssertionError(f"CI workflow contains forbidden behavior: {snippet}")

    expected_actions = {
        "actions/checkout": CHECKOUT_PIN,
        "actions/setup-python": SETUP_PYTHON_PIN,
    }
    action_refs = re.findall(r"uses:\s*([^@\s]+)@([^\s#]+)", workflow)
    if len(action_refs) != len(expected_actions):
        raise AssertionError("CI workflow must use exactly the approved official actions")
    for action, ref in action_refs:
        if expected_actions.get(action) != ref or not re.fullmatch(r"[0-9a-f]{40}", ref):
            raise AssertionError(f"CI action must use its approved immutable SHA: {action}")


class PortfolioSafetyTests(unittest.TestCase):
    def test_ci_is_least_privilege_and_runs_real_boundary_suite(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        assert_ci_workflow_contract(workflow)

        hostile_variants = (
            workflow.replace(CHECKOUT_PIN, "v4", 1),
            workflow.replace(CHECKOUT_PIN, "v4.3.1", 1),
            workflow.replace(SETUP_PYTHON_PIN, "v5", 1),
            workflow.replace(CHECKOUT_PIN, "0" * 40, 1),
            workflow.replace("cancel-in-progress: true", "cancel-in-progress: false", 1),
            workflow.replace(
                "group: ci-${{ github.workflow }}-${{ github.ref }}",
                "group:",
                1,
            ),
            workflow.replace("  pull_request:\n", "  workflow_dispatch:\n", 1),
            workflow.replace(
                "  workflow_dispatch:\n",
                "  workflow_dispatch:\n  schedule:\n",
                1,
            ),
            workflow.replace("  push:\n", "", 1),
            workflow.replace("  pull_request:\n", "", 1),
            workflow.replace(
                "      - name: Run boundary suite\n",
                "      - name: Read a secret\n"
                "        run: echo \"${{ secrets['CHECKOUT_TOKEN'] }}\"\n"
                "      - name: Run boundary suite\n",
                1,
            ),
        )
        for hostile_workflow in hostile_variants:
            with self.subTest(hostile_workflow=hostile_workflow):
                with self.assertRaises(AssertionError):
                    assert_ci_workflow_contract(hostile_workflow)

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
