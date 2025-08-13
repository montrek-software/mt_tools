from requesting.managers.request_manager import RequestJsonManager
from requesting.managers.authenticator_managers import (
    RequestBearerAuthenticator,
)


class GitHubRequestManager(RequestJsonManager):
    base_url = "https://api.github.com"
    authenticator_class = RequestBearerAuthenticator

    def get_milestone_path(self, owner: str, repository: str, milestone_nr: int) -> str:
        return f"/repos/{owner}/{repository}/milestones"

    def get_milestone(self, owner: str, repository: str, milestone_nr: int) -> dict:
        milestone_path = self.get_milestone_path(owner, repository, milestone_nr)
        return self.get_response(milestone_path)
