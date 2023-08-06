import os
from typing import Optional

import pytest

from figh import DupKeyException, GithubConfigStorage

TEST_RESOURCES_PATH = "/tests/resources"


@pytest.fixture(scope="module")
def github_test_storage(setup_test_env) -> GithubConfigStorage:
    token = os.getenv("TEST_GITHUB_TOKEN")
    repo = "skspark/figh-py"
    return GithubConfigStorage(repo_name=repo, token=token)


def test_single_file(github_test_storage):
    expected = {"first": {"foo": {"bar": "first"}, "foo2": {"bar2": "second"}}}
    config = github_test_storage.get(root_path=f"{TEST_RESOURCES_PATH}/single-yaml")
    print(f"single-yaml file config: {config}")
    assert config is not None
    assert config == expected


def test_nested(github_test_storage):
    expected = {
        "first": {"foo": {"bar": "first"}},
        "second": {
            "base": {"foo": {"bar": "second"}},
            "fourth": {"base": {"foo": {"bar": "fourth"}}},
        },
        "third": {"base": {"foo": {"bar": "third"}}},
    }
    config = github_test_storage.get(root_path=f"{TEST_RESOURCES_PATH}/nested-yaml")
    print(f"nested-yaml file config: {config}")

    assert config is not None
    assert config == expected


def test_dup_key(github_test_storage):
    dupkey_error: Optional[Exception] = None
    try:
        config = github_test_storage.get(root_path=f"{TEST_RESOURCES_PATH}/duplicated-yaml")
    except DupKeyException as e:
        dupkey_error = e
    assert dupkey_error is not None
