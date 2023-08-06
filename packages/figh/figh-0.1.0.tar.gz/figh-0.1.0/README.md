# figh-py
github as config storage, in python

## Usage
```python
from figh import GithubConfigStorage, ConfigFileFormat

# for github
s = GithubConfigStorage(repo_name="<github_repo>",
                        token="<github-token>",
                        file_format=ConfigFileFormat.YAML)
latest_configs = s.get(root_path="/tests/resources/single-yaml")
tag_configs = s.get(root_path="/tests/resources/single-yaml", version="0.1.0")
```

## Development Flow
for development flow, please refer to this [guide](.github/DEVELOPMENT_FLOW.md)
