import os
import requests

class AITOSGithubClient:
    """
    A simplified GitHub API client for AITOS Dev Agent.
    """
    def __init__(self, token=None, repo=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo = repo or os.getenv('GITHUB_REPO')
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_branch(self, branch_name, base_branch="main"):
        # Get base branch SHA
        resp = requests.get(f"{self.base_url}/git/ref/heads/{base_branch}", headers=self.headers)
        sha = resp.json()['object']['sha']
        
        # Create new branch
        payload = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        return requests.post(f"{self.base_url}/git/refs", headers=self.headers, json=payload)

    def create_pull_request(self, title, body, head, base="main"):
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        return requests.post(f"{self.base_url}/pulls", headers=self.headers, json=payload)

    def update_file(self, path, message, content, sha, branch):
        import base64
        encoded_content = base64.b64encode(content.encode()).decode()
        payload = {
            "message": message,
            "content": encoded_content,
            "sha": sha,
            "branch": branch
        }
        return requests.put(f"{self.base_url}/contents/{path}", headers=self.headers, json=payload)
