from github import Github
import os


class GithubRestClient(Github):
    def __init__(self, token: str):
        super().__init__(token)

    def get_releases(self, repo_name: str):
        """
        Get all releases from a repository.
        """
        repo = super().get_repo(repo_name)
        releases = [e for e in repo.get_releases()]
        return releases

    def get_tag(self, repo_name: str, tag_name: str):
        """
        Get a tag from a repository.
        """
        repo = super().get_repo(repo_name)
        tags = repo.get_tags()

        for tag in tags:
            if str(tag.name) == tag_name:
                return tag
        return None

    def list_contents(self, repo_name: str, folder_path: str):
        """
        List the contents of a folder from a repository.
        """
        repo = super().get_repo(repo_name)
        return repo.get_contents(folder_path)

    def get_contents(self, repo_name: str, file_path: str):
        """
        Get the contents of a file from a repository.
        """
        repo = super().get_repo(repo_name)
        contents = repo.get_contents(file_path)
        return contents
    
    def create_file(self, repo_name: str, file_path: str, content: str):
        """
        Create a file in a repository.
        """
        repo = super().get_repo(repo_name)
        commit_msg = 'Create file'
        repo.create_file(
            path=file_path, 
            message=commit_msg, 
            content=content
        )

    def get_commits(self, repo_name: str, number_of_commits: int = 1):
        """
        Get all commits from the repository.
        """
        repo = super().get_repo(repo_name)
        commits = [e for e in repo.get_commits()[:number_of_commits]]
        return commits

    def get_commit(self, repo_name: str, commit_sha: str):
        repo = super().get_repo(repo_name)
        commit = repo.get_commit(commit_sha)
        return commit

    def compare_commits(
        self, 
        repo_name: str,
        base_sha: str, 
        head_sha: str
    ):
        """
        Compare two commits and return the diff.
        """
        repo = super().get_repo(repo_name)
        diff = repo.compare(base_sha, head_sha)
        return diff
    
    def create_release(
        self,
        repo_name: str,
        version: str,
        tag_message: str,
        release_message: str,
        target_commitish: str,
        release_type: str = "commit"
    ):
        """
        Create a release and tag in a repository.
        """
        repo = super().get_repo(repo_name)
        release = repo.create_git_tag_and_release(
            tag=version,
            tag_message=tag_message,
            release_name=version,
            release_message=release_message,
            object=target_commitish,
            type=release_type
        )
        return release


