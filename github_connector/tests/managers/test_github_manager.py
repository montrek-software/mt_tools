from django.test import TestCase
from mt_tools.github_connector.managers.github_manager import GitHubManager


class MockGitHubRequestManager:
    def __init__(self, session_data) -> None:
        pass

    def get_milestone(self, owner: str, repository: str, milestone_nr: int):
        if owner == "owner" and repository == "repository" and milestone_nr == 1:
            return [{"description": "Test Milestone"}]


class MockGitHubManager(GitHubManager):
    request_manager_class = MockGitHubRequestManager


class TestGitHubManager(TestCase):
    def test_get_milestone_description(self):
        manager = MockGitHubManager()
        description = manager.get_milestone_description("owner", "repository", 1)
        self.assertEqual(description, "<p>Test Milestone</p>")

    def test_get_milestone_description__no_description(self):
        manager = MockGitHubManager()
        description = manager.get_milestone_description("not_an_owner", "repository", 1)
        self.assertEqual(description, "")
