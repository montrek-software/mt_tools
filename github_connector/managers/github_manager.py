import markdown
from django.conf import settings
from mt_tools.github_connector.managers.github_request_manager import (
    GitHubRequestManager,
)


class GitHubManager:
    request_manager_class = GitHubRequestManager

    def __init__(self):
        self.request_manager = self.request_manager_class(
            {"token": settings.MONTREK_GITHUB_TOKEN}
        )

    def get_milestone_description(
        self, owner: str, repository: str, milestone_nr: int
    ) -> str:
        milestone_data = self.request_manager.get_milestone(
            owner, repository, milestone_nr
        )
        if milestone_data:
            description = milestone_data[0].get("description", "")
        else:
            description = ""
        html = markdown.markdown(description)
        return html
