import importlib.util
import tempfile
import unittest
from pathlib import Path
from typing import Optional


def load_module():
    script = Path(__file__).resolve().parents[1] / "refresh_claude_code_projects.py"
    spec = importlib.util.spec_from_file_location("refresh_claude_code_projects", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_git_repo(path: Path, remote: Optional[str] = None, branch: str = "main"):
    path.mkdir(parents=True)
    (path / ".git").mkdir()
    (path / ".git" / "HEAD").write_text(f"ref: refs/heads/{branch}\n")
    if remote:
        (path / ".git" / "config").write_text(
            f'[remote "origin"]\n\turl = {remote}\n'
        )


class RefreshClaudeCodeProjectsTests(unittest.TestCase):
    def test_refresh_creates_symlinks_and_projects_markdown(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            projects_root = tmp_path / "projects"
            hub_root = tmp_path / "hub"
            make_git_repo(projects_root / "alpha", "git@github.com:kevin/alpha.git", "feature")
            make_git_repo(projects_root / "beta")

            result = module.refresh(projects_root, hub_root)

            self.assertEqual(result, {"added": 2, "removed": 0, "projects": 2})
            self.assertTrue((hub_root / "alpha").is_symlink())
            self.assertEqual((hub_root / "alpha").resolve(), (projects_root / "alpha").resolve())
            self.assertTrue((hub_root / "beta").is_symlink())
            markdown = (hub_root / "PROJECTS.md").read_text()
            self.assertIn("[alpha](./alpha)", markdown)
            self.assertIn("`feature`", markdown)
            self.assertIn("git@github.com:kevin/alpha.git", markdown)
            self.assertIn("[beta](./beta)", markdown)
            self.assertIn("(no origin)", markdown)

    def test_refresh_removes_stale_hub_symlink_without_touching_real_files(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            projects_root = tmp_path / "projects"
            hub_root = tmp_path / "hub"
            make_git_repo(projects_root / "current")
            stale_target = tmp_path / "missing"
            hub_root.mkdir()
            (hub_root / "stale").symlink_to(stale_target)
            (hub_root / "KEEP.md").write_text("do not remove")

            result = module.refresh(projects_root, hub_root)

            self.assertEqual(result["removed"], 1)
            self.assertFalse((hub_root / "stale").exists())
            self.assertEqual((hub_root / "KEEP.md").read_text(), "do not remove")
            self.assertTrue((hub_root / "current").is_symlink())

    def test_scan_projects_ignores_non_git_directories(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            projects_root = tmp_path / "projects"
            make_git_repo(projects_root / "repo")
            (projects_root / "notes").mkdir(parents=True)

            projects = module.scan_projects(projects_root)

            self.assertEqual([project.name for project in projects], ["repo"])


if __name__ == "__main__":
    unittest.main()
