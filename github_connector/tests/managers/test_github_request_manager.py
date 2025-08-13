from django.test import TestCase
from mt_tools.github_connector.managers.github_request_manager import (
    GitHubRequestManager,
)
from unittest.mock import patch, Mock
import requests


class TestGitHubRequestManager(TestCase):
    def test_get_milestone_path(self):
        manager = GitHubRequestManager({"token": "ABCDEF"})
        owner = "owner"
        repository = "repository"
        milestone_nr = 1
        path = manager.get_milestone_path(owner, repository, milestone_nr)
        self.assertEqual(path, f"/repos/{owner}/{repository}/milestones")

    def test_get_milestone_mocks_requests_and_returns_parsed_json(self):
        mgr = GitHubRequestManager({"token": "ABCDEF"})
        owner = "owner"
        repo = "repository"
        milestone_nr = 1

        expected_path = "/repos/owner/repository/milestones"
        expected_url = "https://api.github.test/repos/owner/repository/milestones"
        expected_headers = {"Authorization": "Bearer ABCDEF"}
        expected_json = {"id": 123, "title": "v1.0"}

        with (
            patch.object(mgr, "get_endpoint_url", return_value=expected_url) as ep_url,
            patch.object(mgr, "get_headers", return_value=expected_headers) as get_hdrs,
            patch("requests.get") as mock_get,
        ):
            fake_resp = Mock(spec=requests.Response)
            fake_resp.status_code = 200
            fake_resp.json.return_value = expected_json
            mock_get.return_value = fake_resp

            result = mgr.get_milestone(owner, repo, milestone_nr)

        # Wiring checks
        ep_url.assert_called_once_with(expected_path)
        get_hdrs.assert_called_once()
        mock_get.assert_called_once_with(
            expected_url,
            mgr.request_kwargs,
            headers=expected_headers,
            timeout=30,
        )
        # Behavior checks
        fake_resp.json.assert_called_once()
        self.assertEqual(result, expected_json)
