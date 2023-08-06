from typing import List

from git import Repo


class PruneRemote:
    EXCLUDED_BRANCHES = ['HEAD', 'main', 'master', 'develop', 'release']

    def __init__(self, repository_path: str, remote_name: str, current_branch: str):
        self.remote_name = remote_name
        self._repo = Repo.init(repository_path)
        self._repo.git.checkout(current_branch)

    def __is_excluded(self, branch: str) -> bool:
        excludes = [f'{self.remote_name}/{b}' for b in self.EXCLUDED_BRANCHES]
        return any([branch.startswith(e) for e in excludes])

    def get_remote_merged_branches(self) -> List[str]:
        branches = self._repo.git.branch(['-r', '--merged']).splitlines()
        return [b.lstrip() for b in branches if not self.__is_excluded(b.lstrip())]

    def remove_branches(self, branches: List[str]):
        for ref in self._repo.remote(self.remote_name).refs:
            for branch in branches:
                if ref.name.endswith(branch):
                    ref.delete(self._repo, ref)
