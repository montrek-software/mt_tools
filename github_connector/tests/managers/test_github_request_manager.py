from django.test import TestCase
from mt_tools.github_connector.managers.github_request_manager import (
    GitHubRequestManager,
)


class TestGitHubRequestManager(TestCase):
    def test_get_milestone_path(self):
        manager = GitHubRequestManager({"token": "ABCDEF"})
        owner = "owner"
        repository = "repository"
        milestone_nr = 1
        path = manager.get_milestone_path(owner, repository, milestone_nr)
        self.assertEqual(path, f"/repos/{owner}/{repository}/milestones")
