import base64
import os
from typing import Any, Dict, List

import yaml
from github import Auth, Github
from github.ContentFile import ContentFile
from github.Repository import Repository

from figh.base import VERSION_LATEST, ConfigStorage
from figh.config_file_format import ConfigFileFormat
from figh.util import nested_set


class GithubConfigStorage(ConfigStorage):
    github: Github
    repo: Repository
    base_branch: str
    file_format: ConfigFileFormat

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        repo_name: str,
        token: str,
        base_branch: str = "main",
        file_format: ConfigFileFormat = ConfigFileFormat.YAML,
    ):
        self.repo_name = repo_name
        self.github = Github(auth=Auth.Token(token))
        self.repo = self.github.get_repo(repo_name)
        self.base_branch = base_branch
        self.file_format = file_format

    def _get_repo_contents(self, ref, root_path: str = "/") -> Dict[str, Any]:
        files = self.repo.get_contents(root_path, ref=ref)
        all_files_data = {}
        while files:
            file_content = files.pop(0)
            if file_content.type == "dir":
                files.extend(self.repo.get_contents(file_content.path))
            else:
                content_string = base64.b64decode(file_content.content).decode("utf-8")
                if self.file_format.matched(file_content.path):
                    all_files_data[file_content.path] = content_string
        return all_files_data

    def _merge_configs(
        self, root_path: str, config_files: Dict[str, ContentFile]
    ) -> Dict[str, Any]:
        merged_config = {}
        if self.file_format == ConfigFileFormat.YAML:
            for path, content in config_files.items():
                config_keys = self._file_config_keys(root_path, path)
                config_data = yaml.safe_load(content)
                nested_set(merged_config, config_keys, config_data)
            return merged_config
        else:
            raise ValueError(f"unsupported config file format: {self.file_format}")

    @staticmethod
    def _file_config_keys(root_path: str, file_path: str) -> List[str]:
        root_path = root_path.strip("/")
        file_path = file_path.lstrip("/")
        if file_path.startswith(root_path):
            file_path = file_path[len(root_path) :].lstrip("/")
            file_path = os.path.splitext(file_path)[0]
            items = file_path.split("/")
            items = [item for item in items if item]
            return items
        else:
            return []

    def get(self, version: str = VERSION_LATEST, root_path: str = "/") -> Dict[str, Any]:
        if version is VERSION_LATEST:
            config_files = self._get_repo_contents(ref=self.base_branch, root_path=root_path)
        else:
            tag_ref = self.repo.get_git_ref(f"tags/{version}")
            tag_sha = tag_ref.object.sha
            config_files = self._get_repo_contents(ref=tag_sha, root_path=root_path)
        return self._merge_configs(root_path=root_path, config_files=config_files)
