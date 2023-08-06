"""Tests for Pulp download policies."""
import pytest

from pulp_smash.pulp3.bindings import delete_orphans
from pulp_smash.pulp3.utils import (
    get_added_content_summary,
    get_content_summary,
)
from pulp_deb.tests.functional.constants import DEB_FIXTURE_PACKAGE_COUNT, DEB_FIXTURE_SUMMARY


@pytest.mark.parametrize("policy", ["on_demand", "streamed"])
def test_download_policy(
    apt_package_api,
    deb_get_repository_by_href,
    deb_publication_factory,
    deb_remote_factory,
    deb_repository_factory,
    deb_sync_repository,
    orphans_cleanup_api_client,
    policy,
):
    """Test whether lazy synced content can be accessed with different download policies."""
    orphans_cleanup_api_client.cleanup({"orphan_protection_time": 0})
    # Create repository and remote and verify latest `repository_version` is 0
    repo = deb_repository_factory()
    remote = deb_remote_factory(policy=policy)
    assert repo.latest_version_href.endswith("/0/")

    # Sync and verify latest `repository_version` is 1
    deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)
    assert repo.latest_version_href.endswith("/1/")

    # Verify the correct amount of content units are available
    assert DEB_FIXTURE_SUMMARY == get_content_summary(repo.to_dict())
    assert DEB_FIXTURE_SUMMARY == get_added_content_summary(repo.to_dict())

    # Sync again and verify the same amount of content units are available
    latest_version_href = repo.latest_version_href
    deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)
    assert repo.latest_version_href == latest_version_href
    assert DEB_FIXTURE_SUMMARY == get_content_summary(repo.to_dict())

    # Create a publication and verify the `repository_version` is not empty
    publication = deb_publication_factory(repo, simple=True)
    assert publication.repository_version is not None

    # Verify the correct amount of packages are available
    content = apt_package_api.list()
    assert content.count == DEB_FIXTURE_PACKAGE_COUNT


# TODO: Should think of a better approach to test this case.
@pytest.mark.skip(reason="Currently breaking the CI")
@pytest.mark.parametrize("policy", ["on_demand", "streamed"])
def test_lazy_sync_immediate_download_test(
    artifacts_api_client,
    deb_get_remote_by_href,
    deb_get_repository_by_href,
    deb_patch_remote,
    deb_remote_factory,
    deb_repository_factory,
    deb_sync_repository,
    policy,
):
    """Test whether a immediate sync after a lazy one has all artifacts available."""
    # Cleanup artifacts
    NON_LAZY_ARTIFACT_COUNT = 17
    delete_orphans()

    # Create repository and remote and sync them
    repo = deb_repository_factory()
    remote = deb_remote_factory(policy=policy)
    deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)

    # Verify amount of artifacts are equal to NON_LAZY_ARTIFACT_COUNT
    artifacts = artifacts_api_client.list()
    assert artifacts.count == NON_LAZY_ARTIFACT_COUNT

    # Update remote policy to immediate and verify it is set
    deb_patch_remote(remote, {"policy": "immediate"})
    remote = deb_get_remote_by_href(remote.pulp_href)
    assert remote.policy == "immediate"

    # Sync with updated remote and verify the correct amount artifacts
    deb_sync_repository(remote, repo)
    repo = deb_get_repository_by_href(repo.pulp_href)
    artifacts = artifacts_api_client.list()
    assert artifacts.count == NON_LAZY_ARTIFACT_COUNT + DEB_FIXTURE_PACKAGE_COUNT
